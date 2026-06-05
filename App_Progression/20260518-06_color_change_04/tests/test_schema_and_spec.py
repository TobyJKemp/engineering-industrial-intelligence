from __future__ import annotations

from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    assert isinstance(data, dict)
    return data


def test_spec_matches_schema() -> None:
    schema = load_yaml(ROOT / "schema" / "app_schema.yaml")
    spec = load_yaml(ROOT / "app_spec.yaml")
    jsonschema.validate(instance=spec, schema=schema)


def test_required_sections_present() -> None:
    spec = load_yaml(ROOT / "app_spec.yaml")
    assert "ui" in spec
    assert "behavior" in spec
    assert "guardrails" in spec
    assert "required_files" in spec
    assert "tests" in spec
    assert "validation" in spec
