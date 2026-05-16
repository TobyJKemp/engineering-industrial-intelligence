# Color Change 02: Workflow Explanation

This app uses YAML as the source of truth and a harness to generate browser files.

## 1) Files

- [color_change.yaml](color_change.yaml)
  - Defines UI title, six buttons, dropdown options, and output paths.
- [generate_app.py](generate_app.py)
  - Reads YAML and generates browser files.
- [generated/index.html](generated/index.html)
  - Generated page structure.
- [generated/styles.css](generated/styles.css)
  - Generated styles.
- [generated/script.js](generated/script.js)
  - Generated interaction logic.

## 2) Build Flow

1. Run [generate_app.py](generate_app.py).
2. Harness loads [color_change.yaml](color_change.yaml).
3. Harness validates:
   - exactly six buttons
   - required dropdown fields
   - output file paths
4. Harness writes generated files under generated/.

## 3) Runtime Flow

1. Open [generated/index.html](generated/index.html).
2. Click a button to set that button color as background.
3. Change dropdown value to set selected color as background.

## 4) How to Run

1. Install dependency:
   python -m pip install -r requirements.txt
2. Generate app:
   python generate_app.py
3. Open in browser:
   open generated/index.html

## 5) Customization

Edit [color_change.yaml](color_change.yaml), then rerun [generate_app.py](generate_app.py).

Most useful fields:
- ui.buttons
- ui.dropdown.options
- ui.title
- output_files
