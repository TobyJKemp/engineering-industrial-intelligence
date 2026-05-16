# SOP Drafting Copilot: End-to-End Workflow

This guide explains exactly how this starter application works from input to output.

## 1) What This Application Does

The application builds a draft SOP prompt using:
- structured YAML input,
- Markdown process context,
- Markdown business knowledge,
- YAML guardrail policies.

Then it:
1. validates inputs,
2. assembles a final prompt,
3. generates a placeholder SOP output,˚c
4. validates the output with guardrails,
5. writes artifacts and a run manifest.

Current behavior note:
- The harness currently writes a placeholder SOP output (not a live model call yet).
- The structure is ready for replacing placeholder output with real LLM inference.

## 2) Project Files and Their Roles

Core runtime files:
- [config/app.yaml](config/app.yaml): Global app settings and relative file paths used by the harness.
- [harness/run.py](harness/run.py): Main orchestrator script. Loads files, validates, assembles prompt, validates output, writes artifacts.
- [requirements.txt](requirements.txt): Python dependencies.

Input knowledge and prompt files:
- [inputs/sample_input.yaml](inputs/sample_input.yaml): Structured request fields for SOP generation.
- [content/sample_content.md](content/sample_content.md): Process-specific context to ground the SOP.
- [knowledge/business_knowledge.md](knowledge/business_knowledge.md): Domain rules and drafting conventions.
- [prompts/task_prompt.md](prompts/task_prompt.md): Prompt template containing placeholders.
- [guardrails/policies.yaml](guardrails/policies.yaml): Input required fields + output section and forbidden-term checks.

Output artifacts:
- [outputs/runs](outputs/runs): Assembled prompt and model output markdown files.
- [outputs/logs](outputs/logs): Run manifest JSON with run metadata and artifact pointers.

## 3) How to Run

From this folder:
- [Starter_Applications/01_sop_drafting_copilot](.)

Step 1. Install dependencies
- pip install -r requirements.txt

Step 2. Execute harness
- python harness/run.py

If your workspace uses a virtual environment Python path, run with that interpreter instead.

Expected terminal output includes:
- Run complete: <timestamp run id>
- Assembled prompt: outputs/runs/<run id>_assembled_prompt.md
- Model output: outputs/runs/<run id>_model_output.md
- Manifest: outputs/logs/<run id>_manifest.json

## 4) What You Input

You directly edit these files before a run:

1. [inputs/sample_input.yaml](inputs/sample_input.yaml)
Used for high-level generation intent.
Fields currently used:
- facility_type
- procedure_title
- objective
- user_request
- response_format

2. [content/sample_content.md](content/sample_content.md)
Used for process situation details, observed issues, and controls.

3. [knowledge/business_knowledge.md](knowledge/business_knowledge.md)
Used for organizational rules, SOP conventions, compliance language.

4. [guardrails/policies.yaml](guardrails/policies.yaml)
Used to enforce:
- required input fields,
- forbidden output terms,
- mandatory output sections.

## 5) End-to-End Runtime Sequence

This is the exact order used by [harness/run.py](harness/run.py):

1. Load config
- Reads [config/app.yaml](config/app.yaml).
- Resolves relative paths for all downstream files.

2. Load source files
- Reads [inputs/sample_input.yaml](inputs/sample_input.yaml).
- Reads [content/sample_content.md](content/sample_content.md).
- Reads [knowledge/business_knowledge.md](knowledge/business_knowledge.md).
- Reads [prompts/task_prompt.md](prompts/task_prompt.md).
- Reads [guardrails/policies.yaml](guardrails/policies.yaml).

3. Validate input guardrails
- Checks required fields from guardrails.input.required_fields.
- Stops with error if any required field is missing or empty.

4. Assemble prompt
- Merges YAML input fields with:
  - content_context from content markdown,
  - business_knowledge from knowledge markdown.
- Replaces placeholders in [prompts/task_prompt.md](prompts/task_prompt.md).

5. Persist assembled prompt
- Writes outputs/runs/<run id>_assembled_prompt.md.

6. Generate output
- Currently creates a built-in placeholder SOP output in the harness code.

7. Validate output guardrails
- Ensures forbidden terms do not appear.
- Ensures all required sections exist (Summary, Scope, Prerequisites, Procedure Steps, Safety and Quality Checks, Escalation).
- Stops with error if checks fail.

8. Persist model output
- Writes outputs/runs/<run id>_model_output.md.

9. Persist manifest
- Writes outputs/logs/<run id>_manifest.json with:
  - run_id,
  - timestamp_utc,
  - app name,
  - model name,
  - artifact file locations,
  - status.

## 6) How Prompt Placeholders Map to Inputs

Template placeholders in [prompts/task_prompt.md](prompts/task_prompt.md) are filled from:

- {{facility_type}} -> inputs YAML
- {{procedure_title}} -> inputs YAML
- {{objective}} -> inputs YAML
- {{user_request}} -> inputs YAML
- {{response_format}} -> inputs YAML
- {{content_context}} -> content markdown file text
- {{business_knowledge}} -> knowledge markdown file text

If a placeholder exists in template but no value is provided, it will remain unreplaced text.

## 7) Typical Edit-Run-Inspect Loop

1. Edit request in [inputs/sample_input.yaml](inputs/sample_input.yaml).
2. Update process details in [content/sample_content.md](content/sample_content.md).
3. Update domain policy in [knowledge/business_knowledge.md](knowledge/business_knowledge.md) if needed.
4. Adjust guardrails in [guardrails/policies.yaml](guardrails/policies.yaml) for stricter or looser checks.
5. Run harness.
6. Inspect assembled prompt in outputs/runs.
7. Inspect output and manifest.
8. Repeat until prompt and policy behavior matches your target workflow.

## 8) Failure Modes and How to Understand Them

Input validation failure:
- Cause: Missing required field in input YAML.
- Fix: Add or populate required fields listed in guardrails.input.required_fields.

Output validation failure:
- Cause: Missing mandatory section heading or forbidden terms present.
- Fix: Adjust generated content logic or policy definitions.

Dependency failure:
- Cause: pyyaml not installed.
- Fix: pip install -r requirements.txt.

## 9) How to Move to a Real LLM Call

Replace the placeholder output block in [harness/run.py](harness/run.py) with a model API call:

1. Keep prompt assembly exactly as is.
2. Send assembled_prompt to your model client.
3. Receive text response as model_output.
4. Keep existing post-generation guardrail checks before writing output.
5. Keep manifest logging for traceability.

This preserves the same end-to-end workflow while switching from placeholder generation to real inference.

## 10) Minimal Operational Checklist

Before running:
- Inputs updated.
- Context updated.
- Guardrails match your expected SOP structure.

After running:
- Assembled prompt exists in outputs/runs.
- Output markdown exists in outputs/runs.
- Manifest exists in outputs/logs.
- Output passes required section and forbidden-term checks.
