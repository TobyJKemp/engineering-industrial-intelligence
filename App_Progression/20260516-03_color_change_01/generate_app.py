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


def js_string_list(items: list[str]) -> str:
    escaped = [item.replace("\\", "\\\\").replace('"', '\\"') for item in items]
    return ", ".join(f'"{item}"' for item in escaped)


def build_html(title: str, button_id: str, button_text: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <main class=\"app\">
    <button id=\"{button_id}\" type=\"button\">{button_text}</button>
  </main>
  <script src=\"script.js\"></script>
</body>
</html>
"""


def build_css(button_id: str) -> str:
    return f""":root {{
  --bg: #ffffff;
  --button-bg: #1f2937;
  --button-text: #ffffff;
}}

* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--bg);
  font-family: \"Segoe UI\", Tahoma, Geneva, Verdana, sans-serif;
  transition: background-color 220ms ease;
}}

#{button_id} {{
  border: 0;
  border-radius: 10px;
  padding: 0.85rem 1.1rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--button-bg);
  color: var(--button-text);
}}

#{button_id}:focus-visible {{
  outline: 3px solid #111827;
  outline-offset: 3px;
}}
"""


def build_js(button_id: str, colors: list[str]) -> str:
    if not colors:
        raise SystemExit("behavior.on_button_click.color_list must contain at least one color.")

    return f"""const colors = [{js_string_list(colors)}];

const button = document.getElementById(\"{button_id}\");

if (!button) {{
  throw new Error(\"Missing button element: {button_id}\");
}}

function pickRandomColor() {{
  const index = Math.floor(Math.random() * colors.length);
  return colors[index];
}}

button.addEventListener(\"click\", () => {{
  document.body.style.backgroundColor = pickRandomColor();
}});
"""


def main() -> None:
    config = load_config(CONFIG_PATH)

    title = require(config, "ui.title")
    button_id = require(config, "ui.button.id")
    button_text = require(config, "ui.button.text")
    colors = require(config, "behavior.on_button_click.color_list")

    if not isinstance(colors, list) or any(not isinstance(c, str) for c in colors):
        raise SystemExit("behavior.on_button_click.color_list must be a list of strings.")

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

    html_path.write_text(build_html(title, button_id, button_text), encoding="utf-8")
    css_path.write_text(build_css(button_id), encoding="utf-8")
    js_path.write_text(build_js(button_id, colors), encoding="utf-8")

    print("Generated files:")
    print(f"- {html_path.relative_to(ROOT)}")
    print(f"- {css_path.relative_to(ROOT)}")
    print(f"- {js_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
