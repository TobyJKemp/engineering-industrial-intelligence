# Color Change 03: Workflow Explanation

This app is similar to color_change_02, but policy guardrails come from markdown.

## 1) Source Files

- [color_change.yaml](color_change.yaml)
  - App config and output paths.
- [school_policies.md](school_policies.md)
  - Guardrails source. Includes policy data in a fenced yaml block.
- [generate_app.py](generate_app.py)
  - Harness that reads YAML config + markdown policy guardrails and generates browser files.

## 2) Guardrail Policies

The markdown guardrails define exactly two valid alternatives:
- University of Michigan brand colors
- Stanford University brand colors

The generated app only allows these policies and these color values.

## 3) Build Flow

1. Run [generate_app.py](generate_app.py).
2. Harness loads [color_change.yaml](color_change.yaml).
3. Harness extracts policy yaml block from [school_policies.md](school_policies.md).
4. Harness validates policy structure.
5. Harness writes:
   - [generated/index.html](generated/index.html)
   - [generated/styles.css](generated/styles.css)
   - [generated/script.js](generated/script.js)

## 4) Runtime Flow

1. Open [generated/index.html](generated/index.html).
2. Select a school from dropdown.
3. Click a color button or choose from color dropdown.
4. Background changes only to colors allowed by selected school policy.
