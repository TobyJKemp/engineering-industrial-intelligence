# color_change_03

YAML-driven browser app with markdown-based guardrails for school brand colors.

## Files
- color_change.yaml
- school_policies.md
- generate_app.py
- requirements.txt
- generated/index.html
- generated/styles.css
- generated/script.js

## Run
1. Install dependency:
   python -m pip install -r requirements.txt
2. Generate app files:
   python generate_app.py
3. Open generated/index.html in your browser.

## What Is New
- Guardrails are in markdown, not YAML.
- Two allowed policy alternatives:
  - University of Michigan brand colors
  - Stanford University brand colors
- School dropdown and color controls are constrained to those policies.
