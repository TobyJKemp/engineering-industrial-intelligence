from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "color_change.yaml"


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise SystemExit("color_change.yaml must contain a top-level mapping.")
    return data


def require(config: dict, dotted_key: str):
    value = config
    for part in dotted_key.split("."):
        if not isinstance(value, dict) or part not in value:
            raise SystemExit(f"Missing required config key: {dotted_key}")
        value = value[part]
    return value


def js_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def validate_buttons(buttons: list[dict]) -> None:
    if not isinstance(buttons, list) or len(buttons) != 6:
        raise SystemExit("ui.buttons must be a list with exactly 6 entries.")

    for button in buttons:
        if not isinstance(button, dict):
            raise SystemExit("Each ui.buttons entry must be a mapping.")
        for key in ("id", "label", "color"):
            if key not in button or not isinstance(button[key], str) or not button[key].strip():
                raise SystemExit(f"Each button must include a non-empty string field: {key}")


def build_html(title: str, buttons: list[dict], dropdown_id: str, dropdown_label: str, options: list[dict]) -> str:
    buttons_html = "\n    ".join(
        f'<button type="button" id="{js_escape(btn["id"])}" data-color="{js_escape(btn["color"])}">{js_escape(btn["label"])}</button>'
        for btn in buttons
    )

    options_html = "\n          ".join(
        f'<option value="{js_escape(opt["value"])}">{js_escape(opt["name"])}</option>'
        for opt in options
    )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{js_escape(title)}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <main class=\"app\">
    <h1>{js_escape(title)}</h1>
    <div class=\"button-grid\">
    {buttons_html}
    </div>
    <label for=\"{js_escape(dropdown_id)}\">{js_escape(dropdown_label)}</label>
    <select id=\"{js_escape(dropdown_id)}\">
          {options_html}
    </select>
  </main>
  <script src=\"script.js\"></script>
</body>
</html>
"""


def build_css() -> str:
    return """:root {
  --bg: white;
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
  gap: 0.9rem;
  width: min(92vw, 540px);
  padding: 1.25rem;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.84);
}

h1 {
  margin: 0;
  font-size: 1.2rem;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.55rem;
}

button,
select {
  border: 1px solid #9ca3af;
  border-radius: 8px;
  font-size: 0.96rem;
  padding: 0.65rem 0.75rem;
}

button {
  cursor: pointer;
  background: #111827;
  color: #ffffff;
}

button:focus-visible,
select:focus-visible {
  outline: 3px solid #111827;
  outline-offset: 2px;
}
"""


def build_js(buttons: list[dict], dropdown_id: str) -> str:
    button_data = ",\n  ".join(
        f'{{ id: "{js_escape(btn["id"])}", color: "{js_escape(btn["color"])}" }}' for btn in buttons
    )

    return f"""const buttons = [
  {button_data}
];

const select = document.getElementById("{js_escape(dropdown_id)}");

if (!select) {{
  throw new Error("Missing dropdown element: {js_escape(dropdown_id)}");
}}

function setBackground(color) {{
  document.body.style.backgroundColor = color;
}}

buttons.forEach((buttonConfig) => {{
  const button = document.getElementById(buttonConfig.id);
  if (!button) {{
    throw new Error(`Missing button element: ${{buttonConfig.id}}`);
  }}

  button.addEventListener("click", () => {{
    setBackground(buttonConfig.color);
  }});
}});

select.addEventListener("change", (event) => {{
  setBackground(event.target.value);
}});
"""


def main() -> None:
    config = load_config(CONFIG_PATH)

    title = require(config, "ui.title")
    buttons = require(config, "ui.buttons")
    dropdown = require(config, "ui.dropdown")

    validate_buttons(buttons)

    if not isinstance(dropdown, dict):
        raise SystemExit("ui.dropdown must be a mapping.")

    for key in ("id", "label", "options"):
        if key not in dropdown:
            raise SystemExit(f"ui.dropdown must include key: {key}")

    dropdown_id = dropdown["id"]
    dropdown_label = dropdown["label"]
    options = dropdown["options"]

    if not isinstance(dropdown_id, str) or not dropdown_id.strip():
        raise SystemExit("ui.dropdown.id must be a non-empty string.")
    if not isinstance(dropdown_label, str) or not dropdown_label.strip():
        raise SystemExit("ui.dropdown.label must be a non-empty string.")
    if not isinstance(options, list) or not options:
        raise SystemExit("ui.dropdown.options must be a non-empty list.")

    for option in options:
        if not isinstance(option, dict) or "name" not in option or "value" not in option:
            raise SystemExit("Each ui.dropdown.options entry must have name and value.")

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

    html_path.write_text(build_html(title, buttons, dropdown_id, dropdown_label, options), encoding="utf-8")
    css_path.write_text(build_css(), encoding="utf-8")
    js_path.write_text(build_js(buttons, dropdown_id), encoding="utf-8")

    print("Generated files:")
    print(f"- {html_path.relative_to(ROOT)}")
    print(f"- {css_path.relative_to(ROOT)}")
    print(f"- {js_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
