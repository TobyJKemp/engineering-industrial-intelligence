# color_change_04 Workflow Explanation

This document explains exactly how the app is generated and how runtime behavior is constrained.

## 1) Source of Truth

The project is YAML-first. The primary specification is in:
- `app_spec.yaml`

It declares:
- UI structure (control IDs, labels, classes)
- Behavior/event graph (load/change/click actions)
- Guardrails and policy source
- Required generated files
- Validation and auto-repair settings
- Prompting contract for model output

## 2) Inputs and Their Roles

### A) Architecture Spec
- File: `app_spec.yaml`
- Role: declarative architecture contract.
- Key sections:
  - `ui.structure.controls`
  - `behavior.events`
  - `guardrails.*`
  - `required_files`
  - `validation.rules`
  - `validation.auto_repair`
  - `prompting.output_contract`

### B) Schema
- File: `schema/app_schema.yaml`
- Role: validates `app_spec.yaml` shape before any LLM call.
- Enforces required sections and expected types.
- Prevents generation from running on malformed specs.

### C) Policies / Guardrails
- File: `policies/school_policies.md`
- Role: policy source embedded in markdown as fenced YAML.
- The harness extracts and parses the fenced `yaml` block.
- Includes approved policy IDs and allowed colors.

### D) Prompt Template
- File: `prompts/task_prompt.md`
- Role: generation instructions and strict output contract.
- Requires model output to be one JSON object mapping file paths to file contents.

## 3) Harness Pipeline (Deterministic Orchestration)

Entry point:
- `harness/run.py`

Pipeline order:
1. Load spec from `app_spec.yaml`.
2. Load schema from `schema/app_schema.yaml`.
3. Validate spec with JSON Schema (`jsonschema.validate`).
4. Read policy markdown and parse fenced YAML block.
5. Verify required policy IDs from `guardrails.required_policy_ids`.
6. Read prompt template from `prompting.task_prompt_path`.
7. Assemble final prompt payload (spec + policy markdown).
8. Call the LLM API.
9. Parse model response as a JSON object (`{ path: content }`).
10. Validate generated output against rules from spec.
11. If valid, write generated files and run artifacts.
12. If invalid and auto-repair is enabled, retry with structured feedback until `max_attempts`.

The harness is deterministic around the model call: all pre/post checks are rule-driven and repeatable.

## 4) How Harness, Policies, and Schema Interact

### Schema -> Harness
- The harness uses the schema as a gate.
- If the spec misses required keys or has wrong types, generation stops immediately.
- Effect: no prompt is sent to LLM until the architecture contract is valid.

### Policies -> Harness
- The harness parses policy markdown and turns it into structured policy objects.
- It checks required policy IDs exist (for example, `michigan` and `stanford`).
- It computes allowed color values from policies.
- During output validation, generated JS is scanned for hex colors and compared against allowed policy colors.

### Spec Validation Rules -> Harness
- `validation.rules` define what must be true in generated output.
- Implemented checks include:
  - required generated files are present
  - required DOM IDs appear in generated HTML
  - required policy IDs appear in generated JS
  - generated JS color literals stay within policy-approved colors

### Auto-Repair Loop
- Controlled by `validation.auto_repair`:
  - `enabled`
  - `max_attempts`
  - `include_previous_output`
  - `feedback_fields`
- On failure, harness sends structured feedback to the model:
  - `errors`
  - `failed_rules`
  - `missing_files`
- Optionally includes previous model output for iterative correction.

## 5) Output Contract and Materialization

The model must return exactly one JSON object:
- Keys: required file paths (for example, `generated/index.html`)
- Values: file contents as strings

The harness then:
- Writes files inside project root only (path safety check)
- Refuses writes outside the folder
- Writes run artifacts to `outputs/`:
  - `outputs/runs/*_assembled_prompt.md`
  - `outputs/runs/*_model_output.md`
  - `outputs/logs/*_manifest.json`

## 6) Runtime Behavior of Generated App

After generation, browser runtime works as follows:
1. On page load, initialize DOM refs and policies.
2. Render school options from policy map.
3. Render available colors for selected school.
4. Apply first allowed color by default.
5. On school change, refresh color options/buttons and re-apply first allowed color.
6. On color dropdown change, apply selected color only if allowed.
7. On color button click, apply clicked color only if allowed.

This keeps UI actions constrained by policy guardrails.

## 7) Failure Modes and Stops

The harness stops with explicit errors when:
- `OPENAI_API_KEY` is missing.
- Spec fails schema validation.
- Policy markdown is missing a fenced YAML block.
- Required policy IDs are not present.
- Model output is not parseable as required JSON object.
- Output fails validation after max repair attempts.

## 8) Why This Is YAML-Driven

This project is YAML-driven because architecture, behavior graph, validation rules, and repair policy are all declared in YAML and consumed by the harness before/after generation.

The LLM is used as a constrained code synthesis engine, while schema + guardrails + validators keep generation within the declared architecture.
