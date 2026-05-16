# 01_sop_drafting_copilot

Minimal SOP Drafting Copilot scaffold using YAML inputs, Markdown context, a harness, and guardrails.

## Run

1. Install dependencies:
   pip install -r requirements.txt
2. Create local env file:
   cp .env.example .env
3. Set API key in .env:
   OPENAI_API_KEY="<your_api_key>"
4. Execute harness:
   python harness/run.py

## What it does

- Loads configuration from YAML.
- Loads SOP request parameters from YAML.
- Loads YAML instruction blocks (role, style, output constraints, prohibited patterns).
- Loads process context and business knowledge from Markdown.
- Renders an SOP drafting prompt template.
- Calls the configured model with the assembled prompt.
- Applies input and output guardrail checks for SOP structure.
- Applies a step counter guardrail using output_constraints.max_steps.
- Writes run artifacts to outputs/runs and outputs/logs.

## YAML Instructions

Instruction fields in inputs/sample_input.yaml are injected into the prompt template:
- role_instructions
- style_instructions
- output_constraints
- do_not_do

These are also validated as required input fields in guardrails/policies.yaml.

## Step Counter Guardrail

The harness enforces output_constraints.max_steps:
- It counts numbered list steps in the generated markdown.
- If the step count is greater than max_steps, the run fails with validation error.

## Model Call

The harness uses the OpenAI Responses API in harness/run.py:
- Model name is read from config/app.yaml.
- Prompt text is assembled from YAML + Markdown sources.
- API key is read from OPENAI_API_KEY (loaded from .env if present).
- .env is ignored by git via .gitignore, while .env.example is tracked.
- If OPENAI_API_KEY is missing, the run exits with a clear error.
