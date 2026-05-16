# SOP Drafting Copilot: End-to-End Workflow

This document explains exactly how this application runs in:
- [YAML_Instructions/01_sop_drafting_copilot](.)

## 1) What the App Does

The harness builds an SOP draft workflow from:
- YAML configuration,
- YAML structured request fields,
- YAML instruction blocks,
- Markdown process context,
- Markdown business knowledge,
- YAML guardrail policy.

Then it:
1. validates required inputs,
2. assembles the full prompt,
3. calls the model API with the assembled prompt,
4. validates output structure and policy,
5. validates step count against max_steps,
6. writes run artifacts and manifest.

## 2) Files Used and When

Runtime control:
- [config/app.yaml](config/app.yaml): App metadata and file path wiring.
- [harness/run.py](harness/run.py): Orchestration script and validators.

Prompt inputs:
- [inputs/sample_input.yaml](inputs/sample_input.yaml): SOP request plus YAML instructions.
- [content/sample_content.md](content/sample_content.md): Process context text.
- [knowledge/business_knowledge.md](knowledge/business_knowledge.md): Domain conventions.
- [prompts/task_prompt.md](prompts/task_prompt.md): Prompt template with placeholders.
- [guardrails/policies.yaml](guardrails/policies.yaml): Input and output policy checks.

Artifacts:
- [outputs/runs](outputs/runs): Assembled prompt + model output.
- [outputs/logs](outputs/logs): Run manifest JSON.

## 3) How to Run

From this folder:
- [YAML_Instructions/01_sop_drafting_copilot](.)

Install dependencies:
- pip install -r requirements.txt

Set API key:
- cp .env.example .env
- set OPENAI_API_KEY in .env

Run harness:
- python harness/run.py

Expected output lines:
- Run complete: <run_id>
- Assembled prompt: outputs/runs/<run_id>_assembled_prompt.md
- Model output: outputs/runs/<run_id>_model_output.md
- Manifest: outputs/logs/<run_id>_manifest.json

## 4) YAML Inputs You Edit

Edit [inputs/sample_input.yaml](inputs/sample_input.yaml) before each run.

Core request fields:
- facility_type
- procedure_title
- objective
- user_request
- response_format

YAML instruction fields:
- role_instructions
- style_instructions
- output_constraints
- do_not_do

How instruction fields are used:
- They are injected directly into the prompt template.
- They are required by input guardrails.
- output_constraints.max_steps drives the step counter guardrail.

## 5) Full Runtime Sequence

Execution order in [harness/run.py](harness/run.py):

1. Read [config/app.yaml](config/app.yaml)
- Resolve all runtime file paths.

2. Load source content
- [inputs/sample_input.yaml](inputs/sample_input.yaml)
- [content/sample_content.md](content/sample_content.md)
- [knowledge/business_knowledge.md](knowledge/business_knowledge.md)
- [prompts/task_prompt.md](prompts/task_prompt.md)
- [guardrails/policies.yaml](guardrails/policies.yaml)

3. Input validation
- Check guardrails.input.required_fields.
- Fail if any required field is missing/empty.

4. Prompt assembly
- Merge YAML input + markdown sources.
- Render placeholders in prompt template.
- YAML lists/dicts are rendered as readable YAML text.

5. Save assembled prompt
- Write outputs/runs/<run_id>_assembled_prompt.md.

6. Generate output
- The harness calls the OpenAI Responses API using the configured model name.
- It loads environment values from .env before reading OPENAI_API_KEY.
- The returned text is used as model_output.

7. Output guardrails
- Forbidden terms check.
- Required sections check.

8. Step counter guardrail
- Read output_constraints.max_steps.
- Count numbered steps in generated markdown.
- Fail if step_count > max_steps.

9. Save output + manifest
- outputs/runs/<run_id>_model_output.md
- outputs/logs/<run_id>_manifest.json

## 6) Placeholder Mapping

In [prompts/task_prompt.md](prompts/task_prompt.md), placeholders map as:
- {{facility_type}} <- input YAML
- {{procedure_title}} <- input YAML
- {{objective}} <- input YAML
- {{user_request}} <- input YAML
- {{role_instructions}} <- input YAML
- {{style_instructions}} <- input YAML
- {{output_constraints}} <- input YAML
- {{do_not_do}} <- input YAML
- {{response_format}} <- input YAML
- {{content_context}} <- content markdown
- {{business_knowledge}} <- knowledge markdown

## 7) Failures and Fixes

Input required field failure:
- Cause: Missing required key in input YAML.
- Fix: Add missing keys listed in guardrails.input.required_fields.

Section policy failure:
- Cause: Missing required heading.
- Fix: Ensure generated output includes each required section.

Forbidden term failure:
- Cause: Output includes blocked text.
- Fix: Remove or rephrase blocked terms.

Step counter failure:
- Cause: Numbered step count exceeds output_constraints.max_steps.
- Fix: Reduce numbered steps or raise max_steps in input YAML.

## 8) Typical Edit-Run-Inspect Loop

1. Update [inputs/sample_input.yaml](inputs/sample_input.yaml).
2. Update [content/sample_content.md](content/sample_content.md).
3. Update [knowledge/business_knowledge.md](knowledge/business_knowledge.md) as needed.
4. Adjust [guardrails/policies.yaml](guardrails/policies.yaml) if policy changes.
5. Run harness.
6. Inspect generated artifacts under outputs/runs and outputs/logs.

## 9) Moving to Real Model Calls

This project already uses real model calls.
If you change providers later:
1. Keep prompt assembly and validations unchanged.
2. Swap only the call_model implementation in [harness/run.py](harness/run.py).
3. Keep output guardrails and step counter before artifact write.
4. Keep manifest logging for traceability.
