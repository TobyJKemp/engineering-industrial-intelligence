# color_change_02

YAML-driven browser app with six color buttons and a color dropdown.

## Files
- color_change.yaml
- generate_app.py
- requirements.txt
- generated/index.html
- generated/styles.css
- generated/script.js

## Run
1. Install dependency:
   python -m pip install -r requirements.txt
2. Generate app files from YAML:
   python generate_app.py
3. Open generated/index.html in your browser.

## Behavior
- Six buttons each set a specific background color.
- Blue button sets background to blue.
- Red button sets background to red.
- Dropdown selection sets background to selected color.
