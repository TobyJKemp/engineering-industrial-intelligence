# color_change_04

Completely YAML-driven browser app generation using an LLM.

This project treats YAML as the source of truth for:
- UI structure
- Behavior/event graph
- Guardrails/policies
- Required output files and tests
- Validation rules and auto-repair inputs

## Folder Layout
- `app_spec.yaml`: main declarative architecture spec
- `schema/app_schema.yaml`: schema for validating `app_spec.yaml`
- `policies/school_policies.md`: markdown guardrails with fenced YAML policy block
- `prompts/task_prompt.md`: generation contract sent to the LLM
- `harness/run.py`: deterministic compile/validate/repair loop
- `tests/`: schema and validator tests
- `generated/`: generated app artifacts
- `outputs/`: assembled prompts, model outputs, and logs

## Run
1. Install dependencies:
   python -m pip install -r requirements.txt
2. Create a `.env` file in this folder with your API key:
   OPENAI_API_KEY="<your_key>"
3. Load `.env` before running (or export manually):
   set -a && source .env && set +a
   (Alternative: export OPENAI_API_KEY="<your_key>")
4. Generate files with LLM:
   python harness/run.py
5. Open generated/index.html

Important: the required variable name is `OPENAI_API_KEY` (not `OPEN_API_KEY`).

## Notes
- The harness validates spec + policy + generated output.
- If validation fails, the harness performs an auto-repair loop using structured feedback.
- No files outside this project folder are modified.
