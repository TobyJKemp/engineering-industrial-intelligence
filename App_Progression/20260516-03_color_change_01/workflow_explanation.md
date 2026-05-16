# Color Change App: Workflow Explanation

This document explains how the YAML-driven browser app in this folder works end-to-end.

## 1) What the App Does

The app shows one button on a web page.
When you click the button, the page background changes to a random color.

In this version, YAML is the source of truth and a harness generates the app files.

## 2) Files in This Folder

- [color_change.yaml](color_change.yaml)
  - Source-of-truth configuration file.
  - Defines title, button id/text, behavior, and color list.

- [generate_app.py](generate_app.py)
  - Harness/generator script.
  - Reads color_change.yaml and writes generated/index.html, generated/styles.css, and generated/script.js.

- [requirements.txt](requirements.txt)
  - Python dependency for YAML parsing.

- [generated/index.html](generated/index.html)
  - Generated output file.
  - Defines page structure and button element.

- [generated/styles.css](generated/styles.css)
  - Generated output file.
  - Styles page and button.

- [generated/script.js](generated/script.js)
  - Generated output file.
  - Contains color list from YAML and click handler logic.

- [README.md](README.md)
  - Quick run instructions and project summary.

## 3) Build Flow (YAML to App Files)

1. Run [generate_app.py](generate_app.py).
2. Harness loads [color_change.yaml](color_change.yaml).
3. Harness validates required YAML fields.
4. Harness generates:
  - [generated/index.html](generated/index.html)
  - [generated/styles.css](generated/styles.css)
  - [generated/script.js](generated/script.js)

## 4) Runtime Flow (What Happens When You Open generated/index.html)

1. Browser loads [generated/index.html](generated/index.html).
2. Browser loads [generated/styles.css](generated/styles.css) and applies layout/colors.
3. Browser loads [generated/script.js](generated/script.js).
4. JavaScript attaches a click handler to the button id defined in YAML (ui.button.id).
5. User clicks button.
6. Script chooses a random color from the colors array.
7. Script updates page background color.

## 5) How to Run

1. Install dependency:
  - python -m pip install -r requirements.txt
2. Generate app from YAML:
  - python generate_app.py
3. Open [generated/index.html](generated/index.html) in a browser.

Terminal shortcut on macOS:
- open generated/index.html

## 6) How to Customize

Change app behavior by editing [color_change.yaml](color_change.yaml), then run [generate_app.py](generate_app.py).

Most useful fields:
- ui.title
- ui.button.id
- ui.button.text
- behavior.on_button_click.color_list
- output_files

After YAML changes, regenerate app files.

## 7) What YAML Is Doing Here

[color_change.yaml](color_change.yaml) is actively used by the harness.
It controls what gets written into HTML/CSS/JS output files.

The browser still executes HTML/CSS/JS, but those files now come from YAML through the generator.
