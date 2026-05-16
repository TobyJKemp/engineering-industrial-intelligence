# simple_application_01

Minimal scaffold for YAML + Markdown driven prompt experiments with a harness and guardrails.

## Run

1. Install dependencies:
   pip install -r requirements.txt
2. Execute harness:
   python harness/run.py

## What it does

- Loads configuration from YAML.
- Loads content and business knowledge from Markdown.
- Renders a prompt template.
- Runs basic input/output guardrail checks.
- Writes run artifacts to outputs/runs and outputs/logs.
