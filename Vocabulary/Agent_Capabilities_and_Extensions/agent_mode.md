# Agent Mode

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Configuration |
| **Complexity** | Beginner |
| **Time to Learn** | 30 minutes to understand; 1–2 hours to design your own modes |
| **Prerequisites** | Basic familiarity with AI agents; helpful to understand agent_customization |

## One-Sentence Summary
An agent mode is a named, pre-packaged behavioral profile that switches an AI agent into a specific configuration — changing its persona, available tools, constraints, and response style — in a single step.

## Why This Matters to You
Every task you do with an AI agent has a different character: sometimes you need it to freely read and edit files across your entire repository; other times you want it to answer a question without touching anything. Without modes, you either configure the agent from scratch each time (slow) or use a one-size-fits-all default that's wrong for most situations (frustrating). Agent modes give you a library of purpose-fit configurations you can switch instantly, the same way you'd switch a power tool's setting before starting a job. If you're building or working with AI systems in this repository, understanding modes lets you design agents that behave predictably in each context rather than agents that drift based on what was last asked of them.

## The Core Idea

### What It Is
An agent mode is a bundle of settings that collectively define how an agent should behave in a given context. Think of it as a saved state for the agent's identity and capabilities. When you activate a mode, you simultaneously change the agent's instructions, the tools it has access to, the permissions it operates under, the tone it uses, and the level of autonomy it assumes — all without having to re-specify any of it.

The most concrete example is VS Code's GitHub Copilot, which ships with three distinct modes. **Ask mode** keeps the agent conversational: it reads your code and answers questions but never writes to files. **Edit mode** makes targeted changes to files you explicitly select, with the agent acting more like a precise editor than an advisor. **Agent mode** grants the broadest autonomy — the agent can run terminal commands, read and write files across the workspace, call external tools, and take multi-step actions to complete a goal. Same underlying model; completely different behavior based on the active mode.

Modes exist at multiple scales. A single tool like Copilot has built-in modes. But you can also define custom modes: a "code review" mode that enforces strict style standards and suppresses speculative suggestions; a "brainstorm" mode that encourages creative output and formats responses as exploratory lists; a "database documentation" mode that follows this repository's documentation templates and restricts the agent to read-only operations.

### What It Isn't
A mode is not a separate AI model or a fine-tuned variant. The underlying language model doesn't change when you switch modes — the model's weights, knowledge, and capabilities remain constant. What changes is the context the model operates in: the system prompt, the tools made available, and the constraints applied. A mode is configuration, not retraining.

A mode is also not the same as a single instruction or prompt. A prompt is a one-time input for a one-time response. A mode is a persistent configuration that shapes every response for the duration of a session or task. You prompt the agent; you operate in a mode.

## How It Works

1. **Mode definition** — A mode is specified as a named configuration block, typically in a settings file, instruction file, or YAML definition. It declares the system prompt or instruction set, the allowed/denied tools, any output format constraints, and the persona to adopt.

2. **Activation** — The user selects a mode (via a UI dropdown, a slash command, a config flag, or a programmatic call). The agent loads that mode's configuration and applies it to the session.

3. **Constraint enforcement** — During the session, the mode's rules are enforced. Tool calls that aren't in the allowed list are rejected. Instructions that conflict with the mode's constraints are overridden. The agent's responses are shaped by the mode's persona and format requirements.

4. **Isolation and scope** — Mode settings typically apply for the duration of a task or session. Switching modes resets the configuration cleanly. Some systems allow modes to inherit from a base mode, so you only specify the delta rather than rewriting everything.

5. **Deactivation / switching** — When the task changes, the user switches to a different mode. The new mode's configuration replaces the previous one. Session history (conversation context) may or may not carry over depending on the platform.

## Think of It Like This
Think of a Swiss Army knife. Every tool is in the same device — the same steel, the same manufacturer, the same basic construction. But when you unfold the blade, the knife behaves like a knife. When you unfold the scissors, it behaves like scissors. When you unfold the bottle opener, it behaves like a bottle opener. You don't buy a new knife for each task; you switch the active configuration.

Agent modes work exactly this way. The agent is the knife. Modes are the foldable tools. Agent mode is fully extended — all capabilities deployed. Ask mode is the blade alone — precise and focused, no extras. A custom "documentation" mode is a specialty attachment you designed yourself. The underlying object is identical; what changes is which capabilities are exposed and active.

## The "So What?" Factor

**If you use modes:**
- Agents behave predictably across task types — reviewers trust that "edit mode" won't autonomously delete files, and "agent mode" is expected to take initiative.
- Onboarding new team members is faster — "use ask mode for questions, agent mode for implementation tasks" is a single rule that encodes hours of tribal knowledge.
- Mistakes are bounded — a mode configured for read-only operations can't accidentally modify production data even if the agent misunderstands the request.
- Workflows become composable — you can chain mode switches as part of a repeatable process (research in ask mode → draft in agent mode → review in edit mode).

**If you don't:**
- The agent's behavior becomes context-dependent and hard to predict — one session it's conservative, the next it's aggressively autonomous, and the difference is subtle prompt wording.
- Every new user has to learn the agent's "personality" through trial and error rather than through a named, documented configuration.
- Audit trails are harder — "the agent was in agent mode" is a meaningful statement; "the agent was doing something" is not.

## Practical Checklist
Before designing or selecting a mode, ask yourself:
- [ ] What is the task scope — read-only, targeted edits, or full autonomy?
- [ ] Which tools should be available, and which must be explicitly excluded?
- [ ] What persona and tone matches this task (advisor, executor, reviewer)?
- [ ] Does this mode need guardrails for sensitive operations (production systems, external APIs)?
- [ ] How will users know which mode to use, and how will they switch?
- [ ] Should this mode inherit from a base mode, or be fully standalone?

## Watch Out For

⚠️ **Mode sprawl** — It's tempting to create a new mode for every slight variation in workflow. Resist this. Too many modes are as confusing as none. Keep modes to meaningfully distinct behavioral profiles; use instructions or prompts to handle minor variations within a mode.

⚠️ **False security from restrictive modes** — A mode that says "read-only" doesn't enforce this at the model level; it works by not loading write tools. If the mode definition is wrong, or if a tool has side effects that aren't obvious, the restriction doesn't hold. Verify mode definitions against actual tool inventories, not assumed ones.

⚠️ **Context bleed between modes** — Some platforms carry conversation history across mode switches. If the agent learned something in agent mode that conflicts with read-only mode's intent, the residual context can override the mode's constraints. Be explicit when switching: "You are now in ask mode. Do not edit any files."

⚠️ **Hardcoded vs. configurable modes** — Platform-defined modes (like Copilot's Ask/Edit/Agent) are fixed and can't be modified. Custom modes you define are flexible but require maintenance. Know which kind you're working with before assuming you can change the behavior.

## Connections
**Builds On:**
- `agent_customization` — Modes are a specific implementation pattern within the broader customization framework
- `system_prompt` — Mode instructions are typically delivered as or alongside the system prompt
- `agent_configuration` — Modes are a layer on top of base agent configuration

**Works With:**
- `tool_permission` — Modes often define which tool permissions are active
- `access_boundary` — Mode scope determines what the agent can see and touch
- `adaptive_behavior` — Modes enable controlled adaptation across contexts
- `agent_delegation` — A parent agent might activate a child agent in a specific mode
- `guardrails` — Modes and guardrails work together to enforce safe behavior

**Leads To:**
- `agent_loop` — Once in a mode, the agent runs its action-observation loop within that mode's constraints
- `workspace_awareness` — Agent mode (full autonomy) typically enables maximum workspace awareness
- `context_management` — Switching modes requires careful management of what context carries over

## Quick Decision Guide
**Use a defined mode when you need to:** Reliably reproduce a specific agent behavior across sessions, users, or time — especially when the stakes of getting the behavior wrong are non-trivial.

**Skip modes (use ad-hoc prompts) when:** The task is truly one-off, the behavioral variation is minor, or you're still exploring what the right configuration even is.

## Further Exploration
- 📖 [GitHub Copilot Agent Mode documentation](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-in-the-command-line) — concrete example of a production mode system
- 🎯 Try switching between Ask, Edit, and Agent mode in VS Code Copilot on the same task to feel the behavioral difference firsthand
- 💡 Review `agent_customization.md` in this vocabulary for the complete framework that modes fit within

---
*Added: 2026-05-21 | Updated: 2026-05-21 | Confidence: High*
