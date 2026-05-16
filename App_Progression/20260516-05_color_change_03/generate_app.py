from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "color_change.yaml"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{path.name} must contain a top-level mapping.")
    return data


def require(config: dict, dotted_key: str):
    value = config
    for part in dotted_key.split("."):
        if not isinstance(value, dict) or part not in value:
            raise SystemExit(f"Missing required config key: {dotted_key}")
        value = value[part]
    return value


def parse_policy_markdown(path: Path) -> list[dict]:
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

    ids = {p["id"] for p in policies}
    required_ids = {"michigan", "stanford"}
    if not required_ids.issubset(ids):
        raise SystemExit("Policies must include both ids: michigan and stanford")

    return policies


def esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_html(title: str, school_selector_id: str, color_selector_id: str, button_container_id: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{esc(title)}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <main class=\"app\">
    <h1>{esc(title)}</h1>

    <label for=\"{esc(school_selector_id)}\">School policy</label>
    <select id=\"{esc(school_selector_id)}\"></select>

    <div id=\"{esc(button_container_id)}\" class=\"button-grid\"></div>

    <label for=\"{esc(color_selector_id)}\">Choose color</label>
    <select id=\"{esc(color_selector_id)}\"></select>
  </main>
  <script src=\"script.js\"></script>
</body>
</html>
"""


def build_css() -> str:
    return """:root {
  --bg: #ffffff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--bg);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  transition: background-color 180ms ease;
}

.app {
  display: grid;
  gap: 0.8rem;
  width: min(92vw, 560px);
  padding: 1.1rem;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.86);
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
}

button,
select {
  border: 1px solid #9ca3af;
  border-radius: 8px;
  font-size: 0.96rem;
  padding: 0.6rem 0.72rem;
}

button {
  cursor: pointer;
  background: #111827;
  color: #ffffff;
}
"""


def policies_js_object(policies: list[dict]) -> str:
    rows = []
    for policy in policies:
        colors = ", ".join(
            f'{{ name: "{esc(c["name"])}", value: "{esc(c["value"])}" }}' for c in policy["allowed_colors"]
        )
        row = (
            f'"{esc(policy["id"])}": {{ '
            f'school: "{esc(policy["school"])}", '
            f'colors: [{colors}] '
            f'}}'
        )
        rows.append(row)
    return ",\n  ".join(rows)


def build_js(
    policies: list[dict],
    default_policy_id: str,
    school_selector_id: str,
    color_selector_id: str,
    button_container_id: str,
) -> str:
    policy_object = policies_js_object(policies)

    return f"""const policyMap = {{
  {policy_object}
}};

const schoolSelect = document.getElementById("{esc(school_selector_id)}");
const colorSelect = document.getElementById("{esc(color_selector_id)}");
const buttonContainer = document.getElementById("{esc(button_container_id)}");

if (!schoolSelect || !colorSelect || !buttonContainer) {{
  throw new Error("Missing one or more required UI elements.");
}}

function setBackground(color) {{
  document.body.style.backgroundColor = color;
}}

function renderSchools() {{
  const ids = Object.keys(policyMap);
  schoolSelect.innerHTML = ids
    .map((id) => `<option value="${{id}}">${{policyMap[id].school}}</option>`)
    .join("");

  const fallback = ids.includes("{esc(default_policy_id)}") ? "{esc(default_policy_id)}" : ids[0];
  schoolSelect.value = fallback;
}}

function renderColors(policyId) {{
  const policy = policyMap[policyId];
  if (!policy) {{
    return;
  }}

  colorSelect.innerHTML = policy.colors
    .map((item) => `<option value="${{item.value}}">${{item.name}}</option>`)
    .join("");

  buttonContainer.innerHTML = "";
  policy.colors.forEach((item) => {{
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = item.name;
    button.addEventListener("click", () => setBackground(item.value));
    buttonContainer.appendChild(button);
  }});

  if (policy.colors.length > 0) {{
    colorSelect.value = policy.colors[0].value;
    setBackground(policy.colors[0].value);
  }}
}}

schoolSelect.addEventListener("change", (event) => {{
  renderColors(event.target.value);
}});

colorSelect.addEventListener("change", (event) => {{
  const schoolId = schoolSelect.value;
  const policy = policyMap[schoolId];
  const isAllowed = policy && policy.colors.some((item) => item.value === event.target.value);
  if (isAllowed) {{
    setBackground(event.target.value);
  }}
}});

renderSchools();
renderColors(schoolSelect.value);
"""


def main() -> None:
    config = load_yaml(CONFIG_PATH)

    title = require(config, "ui.title")
    school_selector_id = require(config, "ui.school_selector_id")
    color_selector_id = require(config, "ui.color_selector_id")
    button_container_id = require(config, "ui.button_container_id")
    policy_markdown = require(config, "guardrails.policy_markdown")
    default_policy_id = require(config, "guardrails.default_policy_id")

    policies = parse_policy_markdown(ROOT / policy_markdown)

    output_files = config.get("output_files", ["generated/index.html", "generated/styles.css", "generated/script.js"])
    if not isinstance(output_files, list) or len(output_files) != 3:
        raise SystemExit(
            "output_files must be a list of exactly 3 file paths, for example: "
            "generated/index.html, generated/styles.css, generated/script.js"
        )

    html_path = ROOT / output_files[0]
    css_path = ROOT / output_files[1]
    js_path = ROOT / output_files[2]

    html_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.parent.mkdir(parents=True, exist_ok=True)

    html_path.write_text(
        build_html(title, school_selector_id, color_selector_id, button_container_id),
        encoding="utf-8",
    )
    css_path.write_text(build_css(), encoding="utf-8")
    js_path.write_text(
        build_js(policies, default_policy_id, school_selector_id, color_selector_id, button_container_id),
        encoding="utf-8",
    )

    print("Generated files:")
    print(f"- {html_path.relative_to(ROOT)}")
    print(f"- {css_path.relative_to(ROOT)}")
    print(f"- {js_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
