from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "app_spec.yaml"
SCHEMA_PATH = ROOT / "schema" / "app_schema.yaml"


@dataclass
class ValidationResult:
    errors: list[str]
    failed_rules: list[str]
    missing_files: list[str]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{path.name} must contain a top-level mapping.")
    return data


def parse_policy_markdown(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```yaml\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        raise SystemExit("Policy markdown must include a fenced ```yaml ... ``` block.")

    block = yaml.safe_load(match.group(1).strip()) or {}
    if not isinstance(block, dict) or "policies" not in block:
        raise SystemExit("Policy yaml block must include top-level key: policies")

    policies = block["policies"]
    if not isinstance(policies, list) or not policies:
        raise SystemExit("policies must be a non-empty list")

    for policy in policies:
        if not isinstance(policy, dict):
            raise SystemExit("Each policy must be a mapping")
        for key in ("id", "school", "allowed_colors"):
            if key not in policy:
                raise SystemExit(f"Each policy must include key: {key}")
        if not isinstance(policy["allowed_colors"], list) or not policy["allowed_colors"]:
            raise SystemExit("allowed_colors must be a non-empty list")
        for color in policy["allowed_colors"]:
            if not isinstance(color, dict) or "name" not in color or "value" not in color:
                raise SystemExit("Each allowed_colors entry must include name and value")

    return policies


def validate_spec(spec: dict[str, Any], schema: dict[str, Any]) -> None:
    jsonschema.validate(instance=spec, schema=schema)


def ensure_required_policy_ids(policies: list[dict[str, Any]], required_ids: list[str]) -> None:
    existing = {str(p["id"]) for p in policies}
    missing = [pid for pid in required_ids if pid not in existing]
    if missing:
        raise SystemExit(f"Policy markdown missing required policy ids: {missing}")


def assemble_prompt(spec: dict[str, Any], prompt_template: str, policies_markdown: str) -> str:
    payload = {
        "spec": spec,
        "policy_markdown": policies_markdown,
    }
    return (
        f"{prompt_template.strip()}\n\n"
        "INPUT_PAYLOAD_JSON:\n"
        f"{json.dumps(payload, indent=2)}\n"
    )


def call_openai_chat(model: str, temperature: float, system_prompt: str, user_prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required.")

    body = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    req = urllib.request.Request(
        url="https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"LLM request failed: HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"LLM request failed: {exc}") from exc

    parsed = json.loads(raw)
    return parsed["choices"][0]["message"]["content"]


def extract_json_object(text: str) -> dict[str, str]:
    stripped = text.strip()

    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in parsed.items()):
            return parsed
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        parsed = json.loads(fenced.group(1))
        if isinstance(parsed, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in parsed.items()):
            return parsed

    raise SystemExit("Model output must be a JSON object mapping file paths to file contents.")


def allowed_color_set(policies: list[dict[str, Any]]) -> set[str]:
    values: set[str] = set()
    for policy in policies:
        for color in policy["allowed_colors"]:
            values.add(str(color["value"]).upper())
    return values


def get_control_id(spec: dict[str, Any], control_type: str, fallback: str) -> str:
    controls = spec["ui"]["structure"]["controls"]
    for control in controls:
        if control.get("id") == fallback:
            return str(control["id"])
    for control in controls:
        if control.get("type") == control_type:
            return str(control["id"])
    raise SystemExit(f"Could not infer control id for type={control_type}, fallback={fallback}")


def validate_generated_map(files: dict[str, str], spec: dict[str, Any], policies: list[dict[str, Any]]) -> ValidationResult:
    errors: list[str] = []
    failed_rules: list[str] = []

    required_files = [str(p) for p in spec["required_files"]]
    missing_files = [path for path in required_files if path not in files]
    if missing_files:
        failed_rules.append("required-files-present")
        errors.append(f"Missing required files: {missing_files}")

    html = files.get("generated/index.html", "")
    js = files.get("generated/script.js", "")

    school_id = get_control_id(spec, "select", "schoolSelect")
    color_id = get_control_id(spec, "select", "colorSelect")
    buttons_id = get_control_id(spec, "div", "colorButtons")

    for dom_id in (school_id, color_id, buttons_id):
        if f'id="{dom_id}"' not in html:
            if "required-selectors-present" not in failed_rules:
                failed_rules.append("required-selectors-present")
            errors.append(f"HTML missing required id: {dom_id}")

    required_policy_ids = [str(x) for x in spec["guardrails"]["required_policy_ids"]]
    for pid in required_policy_ids:
        if pid not in js:
            if "policy-ids-present" not in failed_rules:
                failed_rules.append("policy-ids-present")
            errors.append(f"JS missing required policy id: {pid}")

    allowed = allowed_color_set(policies)
    hex_values = re.findall(r"#[0-9A-Fa-f]{6}", js)
    bad_hex = sorted({value.upper() for value in hex_values if value.upper() not in allowed})
    if bad_hex and spec["guardrails"].get("enforce_only_allowed_colors", False):
        failed_rules.append("allowed-colors-only")
        errors.append(f"JS includes colors not allowed by policy: {bad_hex}")

    return ValidationResult(errors=errors, failed_rules=failed_rules, missing_files=missing_files)


def write_files(root: Path, files: dict[str, str]) -> None:
    for rel_path, content in files.items():
        target = (root / rel_path).resolve()
        if not str(target).startswith(str(root.resolve())):
            raise SystemExit(f"Refusing to write outside project root: {rel_path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def write_run_artifacts(root: Path, assembled_prompt: str, model_output: str, manifest: dict[str, Any]) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    runs = root / "outputs" / "runs"
    logs = root / "outputs" / "logs"
    runs.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    (runs / f"{stamp}_assembled_prompt.md").write_text(assembled_prompt, encoding="utf-8")
    (runs / f"{stamp}_model_output.md").write_text(model_output, encoding="utf-8")
    (logs / f"{stamp}_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    spec = load_yaml(SPEC_PATH)
    schema = load_yaml(SCHEMA_PATH)
    validate_spec(spec, schema)

    policy_rel = str(spec["guardrails"]["policy_source"]["path"])
    policy_path = ROOT / policy_rel
    policies_markdown = policy_path.read_text(encoding="utf-8")
    policies = parse_policy_markdown(policy_path)

    required_policy_ids = [str(x) for x in spec["guardrails"]["required_policy_ids"]]
    ensure_required_policy_ids(policies, required_policy_ids)

    prompt_template_path = ROOT / str(spec["prompting"]["task_prompt_path"])
    prompt_template = prompt_template_path.read_text(encoding="utf-8")

    model = str(spec["llm"]["model"])
    temperature = float(spec["llm"]["temperature"])

    max_attempts = int(spec["validation"]["auto_repair"]["max_attempts"])
    include_previous = bool(spec["validation"]["auto_repair"].get("include_previous_output", True))

    system_prompt = (
        "You are a strict code generator. Output only what the user asks. "
        "Return a JSON object when requested."
    )

    assembled_prompt = assemble_prompt(spec, prompt_template, policies_markdown)
    model_output = ""
    last_result = ValidationResult(errors=[], failed_rules=[], missing_files=[])

    previous_output = ""
    for attempt in range(1, max_attempts + 1):
        prompt = assembled_prompt
        if attempt > 1:
            feedback = {
                "attempt": attempt,
                "errors": last_result.errors,
                "failed_rules": last_result.failed_rules,
                "missing_files": last_result.missing_files,
            }
            prompt += "\nREPAIR_FEEDBACK_JSON:\n" + json.dumps(feedback, indent=2) + "\n"
            if include_previous and previous_output:
                prompt += "\nPREVIOUS_MODEL_OUTPUT:\n" + previous_output + "\n"

        model_output = call_openai_chat(model, temperature, system_prompt, prompt)
        previous_output = model_output
        generated_map = extract_json_object(model_output)

        last_result = validate_generated_map(generated_map, spec, policies)
        if not last_result.errors:
            write_files(ROOT, generated_map)
            manifest = {
                "status": "success",
                "attempt": attempt,
                "model": model,
                "required_files": spec["required_files"],
            }
            write_run_artifacts(ROOT, assembled_prompt, model_output, manifest)
            print("Generation succeeded.")
            for path in spec["required_files"]:
                print(f"- {path}")
            return

    manifest = {
        "status": "failed",
        "attempts": max_attempts,
        "model": model,
        "errors": last_result.errors,
        "failed_rules": last_result.failed_rules,
        "missing_files": last_result.missing_files,
    }
    write_run_artifacts(ROOT, assembled_prompt, model_output, manifest)
    raise SystemExit("Generation failed after max attempts. See outputs/logs for details.")


if __name__ == "__main__":
    main()
