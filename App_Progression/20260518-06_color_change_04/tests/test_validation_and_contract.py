from __future__ import annotations

from pathlib import Path

import yaml

from harness.run import parse_policy_markdown, validate_generated_map

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    assert isinstance(data, dict)
    return data


def test_policy_markdown_has_required_ids() -> None:
    spec = load_yaml(ROOT / "app_spec.yaml")
    policies = parse_policy_markdown(ROOT / spec["guardrails"]["policy_source"]["path"])
    ids = {p["id"] for p in policies}
    for required in spec["guardrails"]["required_policy_ids"]:
        assert required in ids


def test_validator_catches_missing_files() -> None:
    spec = load_yaml(ROOT / "app_spec.yaml")
    policies = parse_policy_markdown(ROOT / spec["guardrails"]["policy_source"]["path"])
    incomplete = {
        "generated/index.html": "<html><body></body></html>",
        "generated/styles.css": "body { background: #fff; }",
    }

    result = validate_generated_map(incomplete, spec, policies)
    assert result.missing_files
    assert "required-files-present" in result.failed_rules


def test_validator_accepts_policy_colors_only() -> None:
    spec = load_yaml(ROOT / "app_spec.yaml")
    policies = parse_policy_markdown(ROOT / spec["guardrails"]["policy_source"]["path"])
    generated = {
        "generated/index.html": """
<!doctype html>
<html><body>
<select id=\"schoolSelect\"></select>
<div id=\"colorButtons\"></div>
<select id=\"colorSelect\"></select>
</body></html>
""",
        "generated/styles.css": "body { margin: 0; }",
        "generated/script.js": """
const map = { michigan: ['#00274C'], stanford: ['#8C1515'] };
""",
    }

    result = validate_generated_map(generated, spec, policies)
    assert "allowed-colors-only" not in result.failed_rules
