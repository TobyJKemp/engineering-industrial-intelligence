You are generating a browser app from a YAML architecture spec and policy guardrails.

Rules:
1. Follow the YAML spec exactly.
2. Implement school policy selection, color selection, and color buttons.
3. Only allow background colors defined in the policy guardrails.
4. Include runtime checks for missing DOM nodes.
5. Keep code simple and readable.

Output contract:
- Return exactly one JSON object.
- Keys must be relative paths.
- Required keys:
  - generated/index.html
  - generated/styles.css
  - generated/script.js
- Values must be file contents as strings.
- Do not include markdown fences.
- Do not include explanation.
