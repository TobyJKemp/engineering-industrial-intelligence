from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    from openai import OpenAI
    import yaml
except ImportError as exc:
    raise SystemExit("Missing dependency. Install with 'pip install -r requirements.txt'.") from exc


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_required_fields(input_data: dict, required_fields: list[str]) -> list[str]:
    missing = [field for field in required_fields if field not in input_data or input_data[field] in (None, "")]
    return missing


def format_prompt_value(value: object) -> str:
    if isinstance(value, (dict, list)):
        return yaml.safe_dump(value, sort_keys=False).strip()
    return str(value)


def render_template(template: str, values: dict) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", format_prompt_value(value))
    return rendered


def count_numbered_steps(markdown_text: str) -> int:
    return len(re.findall(r"^\s*\d+\.\s+", markdown_text, flags=re.MULTILINE))


def call_model(prompt: str, model_name: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model_name,
        input=prompt,
    )
    model_output = (response.output_text or "").strip()
    if not model_output:
        raise SystemExit("Model returned an empty response.")
    return model_output


def main() -> None:
    config = load_yaml(ROOT / "config/app.yaml")
    paths = config["paths"]

    input_data = load_yaml(ROOT / paths["input_yaml"])
    content_context = load_text(ROOT / paths["content_markdown"])
    business_knowledge = load_text(ROOT / paths["business_knowledge"])
    prompt_template = load_text(ROOT / paths["prompt_template"])
    guardrails = load_yaml(ROOT / paths["guardrails"])["guardrails"]

    missing = validate_required_fields(input_data, guardrails["input"]["required_fields"])
    if missing:
        raise SystemExit(f"Input validation failed. Missing required fields: {', '.join(missing)}")

    prompt_values = {
        **input_data,
        "content_context": content_context,
        "business_knowledge": business_knowledge,
    }
    assembled_prompt = render_template(prompt_template, prompt_values)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    runs_dir = ROOT / paths["output_runs_dir"]
    logs_dir = ROOT / paths["output_logs_dir"]
    runs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    prompt_file = runs_dir / f"{run_id}_assembled_prompt.md"
    prompt_file.write_text(assembled_prompt, encoding="utf-8")

    model_output = call_model(assembled_prompt, config["model"]["name"])

    forbidden_terms = set(guardrails["output"].get("forbidden_terms", []))
    blocked_terms = [term for term in forbidden_terms if term in model_output]
    if blocked_terms:
        raise SystemExit(f"Output validation failed due to forbidden terms: {', '.join(blocked_terms)}")

    required_sections = guardrails["output"].get("must_include_sections", [])
    missing_sections = [section for section in required_sections if f"# {section}" not in model_output]
    if missing_sections:
        raise SystemExit(f"Output validation failed. Missing sections: {', '.join(missing_sections)}")

    output_constraints = input_data.get("output_constraints", {})
    max_steps = output_constraints.get("max_steps") if isinstance(output_constraints, dict) else None
    if isinstance(max_steps, int) and max_steps > 0:
        step_count = count_numbered_steps(model_output)
        if step_count > max_steps:
            raise SystemExit(
                f"Output validation failed. Procedure step count {step_count} exceeds max_steps {max_steps}"
            )

    output_file = runs_dir / f"{run_id}_model_output.md"
    output_file.write_text(model_output, encoding="utf-8")

    manifest = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "app": config["app"]["name"],
        "model": config["model"]["name"],
        "prompt_file": str(prompt_file.relative_to(ROOT)),
        "output_file": str(output_file.relative_to(ROOT)),
        "status": "ok",
    }
    manifest_file = logs_dir / f"{run_id}_manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Run complete: {run_id}")
    print(f"Assembled prompt: {prompt_file.relative_to(ROOT)}")
    print(f"Model output: {output_file.relative_to(ROOT)}")
    print(f"Manifest: {manifest_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
