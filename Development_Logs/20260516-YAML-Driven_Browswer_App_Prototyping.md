# 2026-05-16 - YAML-Driven Browser App Prototyping with Harness Generation and Markdown Guardrails

## 1) Session Intent
- Theme: Build small browser apps from structured instructions, then shift to policy-driven generation.
- Why today: Practice turning YAML and Markdown into working applications through a harness workflow.
- Time box (planned vs actual): Planned 60-90 min, actual ~2.5-3 hours.

## 2) Inputs
- Tutorial/source links: Existing project patterns from prior folder scaffolds and generated app workflows.
- Prompt(s) used: Requests to create app structures, wire YAML as source-of-truth, add guardrails, and validate runtime behavior.
- Starting assumptions: YAML files alone would directly control browser behavior without additional orchestration.

## 3) What I Tried
- Experiment 1:
	- Setup: Single-button color-change browser app with YAML + HTML/CSS/JS.
	- Change made: Added YAML config and initial static web files.
	- Expected result: Editing YAML would change app behavior.
	- Actual result: App worked, but YAML was only descriptive until a generator/harness consumed it.
- Experiment 2:
	- Setup: Added generator harness to read YAML and produce browser files, then expanded to multi-control and policy modes.
	- Change made: Generated output files into a dedicated subfolder and introduced Markdown guardrails with two school policy alternatives.
	- Expected result: Behavior constrained by declared policies and reproducible from config.
	- Actual result: Successful generation and policy-constrained runtime behavior for selected school color sets.

## 4) Outcomes
- What worked: YAML-driven generation via [harness](../YAML_Instructions/template/knowledge/business_knowledge.md#L12), generated output organization, and Markdown [guardrail](../YAML_Instructions/template/knowledge/business_knowledge.md#L13) parsing.
- What failed: Early runs from incorrect working directory/interpreter; environment key confusion.
- What was confusing: Difference between "YAML as notes/spec" vs "YAML as executable source through a [harness](../YAML_Instructions/template/knowledge/business_knowledge.md#L12)."
- Surprises: How quickly reliability improved after standardizing file structure and generation flow.

## 5) Learning Capture
- New concept(s): Source-of-truth config, generation harness, policy guardrails from Markdown, and output artifact segregation.
- Rule of thumb: Config does nothing by itself; it only matters when a deterministic runtime step reads and enforces it.
- Common pitfall to avoid: Assuming terminal/session env vars persist or that running from any folder will work.
- "I can explain this now" (2-3 sentences): YAML and Markdown are inputs, not execution engines. A harness is the bridge that parses those inputs, validates them against rules, and generates runnable app artifacts. Browser behavior then comes from generated HTML/CSS/JS, which should be regenerated whenever policy/config changes.

## 6) Reuse Artifacts
- Snippets worth keeping: YAML schema pattern for app config, generator validation pattern, and policy parsing from fenced YAML in Markdown.
- Reusable prompt pattern: "Create a YAML-first browser app with generated outputs, validate config keys, and place artifacts in a generated subfolder."
- Reusable workflow/harness step: Edit config/policy -> run generator -> open generated app -> verify against acceptance criteria.
- Tags (5-8): yaml-first, harness, browser-app, guardrails, markdown-policy, generated-artifacts, config-validation, iterative-prototyping

## 7) Retrieval Test (2-minute check)
- Question I should be able to answer tomorrow: "How do I make YAML actually control app behavior instead of just documenting it?"
- Where in my notes is the answer: In today's sections "What I Tried," "Outcomes," and "Learning Capture."
- Could I find it in under 2 minutes? (Yes/No): Yes
- If No, what should be retagged/renamed: N/A

## 8) Confidence + Next Step
- Confidence (1-5): 4
- Next tiny test (15-30 min): Add one more policy source with a third brand palette and enforce a stricter validation rule (for example, required contrast-safe fallback color).
- Stop/continue decision: Continue with one focused extension, then stop and capture diffs in notes.
