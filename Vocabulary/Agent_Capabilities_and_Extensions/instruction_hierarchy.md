# Instruction Hierarchy

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Control / Orchestration |
| **Complexity** | Intermediate |
| **Time to Learn** | 1 hour for basics |
| **Prerequisites** | Understanding of agent instructions, configuration, and orchestration |

## One-Sentence Summary
Instruction hierarchy is the structured organization of agent instructions into levels of authority or specificity, enabling clear precedence and conflict resolution in complex systems.

## Why This Matters to You
If you want agents to behave predictably, resolve conflicting directives, or support layered customization, instruction hierarchy is essential. It brings order and clarity to agent control.

## The Core Idea
### What It Is
Instruction hierarchy means:
- Organizing instructions from general (global) to specific (local)
- Defining which instructions override or inherit from others
- Supporting multi-level customization (system, user, session, task)

### What It Isn't
It is not just a flat list or unordered set. True hierarchy is structured, with clear relationships and precedence.

## How It Works
1. **Define Levels**: Specify instruction layers (e.g., global, project, user, session).
2. **Set Precedence**: Establish rules for which instructions take priority.
3. **Resolve Conflicts**: Use the hierarchy to determine final agent behavior.

## Think of It Like This
Like a chain of command in an organization—orders flow from the top, but can be refined or overridden at lower levels.

## The "So What?" Factor
**If you use this:**
- Predictable, manageable agent behavior
- Easier customization and troubleshooting
- Fewer conflicts and surprises

**If you don't:**
- Conflicting or unpredictable agent actions
- Harder to scale or maintain systems

## Practical Checklist
- [ ] Are instruction levels clearly defined?
- [ ] Is precedence documented and enforced?
- [ ] Are conflicts resolved systematically?

## Watch Out For
⚠️ Ambiguous or circular hierarchies
⚠️ Unclear override rules

## Connections
**Builds On:** [custom_instructions.md](custom_instructions.md), [configuration_inheritance.md](configuration_inheritance.md)
**Works With:** [instruction_precedence.md](instruction_precedence.md), [instructions_file.md](instructions_file.md)
**Leads To:** [agent_orchestration.md](agent_orchestration.md), [multi-agent_system.md](../Agent_and_Orchestration/multi-agent_system.md)

## Quick Decision Guide
**Use this when you need to:** Layer, override, or organize agent instructions
**Skip this when:** All instructions are flat or static

## Further Exploration
- 📖 [Microsoft: Policy and Hierarchy Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/policy)
- 🛠️ [YAML Inheritance Techniques](https://yaml.org/spec/1.2/spec.html)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
