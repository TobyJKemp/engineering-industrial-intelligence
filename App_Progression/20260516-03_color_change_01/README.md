# color_change

YAML-driven browser app with one button that changes the page background color.

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
4. Click "Change Background Color".

## Notes
- No backend is required.
- Edit only color_change.yaml, then re-run generate_app.py.
- generated/index.html, generated/styles.css, and generated/script.js are generated output files.
