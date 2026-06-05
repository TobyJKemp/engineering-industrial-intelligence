# Instruction Precedence

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Control / Orchestration |
| **Complexity** | Intermediate |
| **Time to Learn** | 1 hour for basics |
| **Prerequisites** | Understanding of agent instructions, configuration, and orchestration |

## One-Sentence Summary
Instruction precedence is the rule or logic that determines which instruction takes priority when multiple directives apply to an agent or system.

## Why This Matters to You
If you want agents to behave predictably, resolve conflicts, or support layered customization, instruction precedence is essential. It ensures clarity and control in complex systems.

## The Core Idea
### What It Is
Instruction precedence means:
- Defining which instruction overrides others in case of conflict
- Supporting multi-level customization (system, user, session, task)
- Enabling clear, predictable agent behavior

### What It Isn't
It is not just a random or ad hoc process. True precedence is systematic, documented, and enforced by code or configuration.

## How It Works
1. **Define Precedence Rules**: Specify which instructions take priority (e.g., local over global).
2. **Apply Systematically**: Use rules to resolve conflicts at runtime.
3. **Document and Test**: Ensure precedence is clear and reliable.

## Think of It Like This
Like traffic rules at an intersection—clear right-of-way prevents accidents and confusion.

## The "So What?" Factor
**If you use this:**
- Predictable, manageable agent behavior
- Easier customization and troubleshooting
- Fewer conflicts and surprises

**If you don't:**
- Conflicting or unpredictable agent actions
- Harder to scale or maintain systems

## Practical Checklist
- [ ] Are precedence rules clearly defined and documented?
- [ ] Are conflicts resolved systematically?
- [ ] Is precedence enforced by code or configuration?

## Watch Out For
⚠️ Ambiguous or undocumented precedence
⚠️ Inconsistent enforcement

## Connections
**Builds On:** [instruction_hierarchy.md](instruction_hierarchy.md), [custom_instructions.md](custom_instructions.md)
**Works With:** [instructions_file.md](instructions_file.md), [configuration_inheritance.md](configuration_inheritance.md)
**Leads To:** [agent_orchestration.md](agent_orchestration.md), [multi-agent_system.md](../Agent_and_Orchestration/multi-agent_system.md)

## Quick Decision Guide
**Use this when you need to:** Resolve conflicts or layer agent instructions
**Skip this when:** All instructions are flat or static

## Further Exploration
- 📖 [Microsoft: Policy and Precedence Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/policy)
- 🛠️ [YAML Inheritance Techniques](https://yaml.org/spec/1.2/spec.html)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
