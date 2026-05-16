# 01_sop_drafting_copilot

Minimal SOP Drafting Copilot scaffold using YAML inputs, Markdown context, a harness, and guardrails.

## Run

1. Install dependencies:
   pip install -r requirements.txt
2. Execute harness:
   python harness/run.py

## What it does

- Loads configuration from YAML.
- Loads SOP request parameters from YAML.
- Loads process context and business knowledge from Markdown.
- Renders an SOP drafting prompt template.
- Applies input and output guardrail checks for SOP structure.
- Writes run artifacts to outputs/runs and outputs/logs.
