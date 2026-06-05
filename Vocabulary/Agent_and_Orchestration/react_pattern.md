# ReAct Pattern

## At a Glance
| | |
|---|---|
| **Category** | Reasoning Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Prompt engineering and agent loop basics |

## One-Sentence Summary
The ReAct pattern is an agent reasoning loop that alternates between reasoning (thought) and acting (tool use) to solve complex tasks step by step.

## Why This Matters to You
ReAct is a proven pattern for improving agent reliability and transparency. It makes reasoning explicit, supports self-correction, and enables more robust multi-step workflows. Many state-of-the-art agent frameworks use ReAct as a foundation.

## The Core Idea
### What It Is
ReAct stands for Reason + Act. The agent alternates between thinking (generating intermediate thoughts or plans) and acting (invoking tools or taking steps). Each action is informed by the latest reasoning, and each reasoning step incorporates new observations.

This pattern supports error recovery, context updates, and transparent traceability.

### What It Isn't
ReAct is not a black box; it is designed for interpretability and stepwise control.

It is also not limited to LLMs—any agent with reasoning and action capabilities can use this pattern.

## How It Works
1. Perceive input or environment.
2. Generate reasoning step (thought, plan, or hypothesis).
3. Take action (tool call, query, or output).
4. Observe result and repeat until goal or stop condition.

## Think of It Like This
Think of a train crew alternating between planning the next move and executing it, adjusting as new information arrives.

## The "So What?" Factor
**If you use this:**
- You improve agent transparency and debuggability.
- You enable stepwise error recovery and adaptation.
- You support more complex, multi-step workflows.

**If you don't:**
- Agents become opaque and harder to debug.
- Multi-step tasks are more brittle and error-prone.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are reasoning and action steps clearly separated and logged?
- [ ] Is there a mechanism for error recovery and self-correction?
- [ ] Can the pattern be adapted to your agent’s domain and tools?

## Watch Out For
⚠️ Overly verbose reasoning that slows down workflows.
⚠️ Skipping observation or feedback steps between actions.

## Connections
**Builds On:** [agent_loop.md](agent_loop.md), [self_correction.md](../Agent_Capabilities_and_Extensions/self_correction.md)
**Works With:** [reflection.md](reflection.md), [tool_composition.md](../Agent_Capabilities_and_Extensions/tool_composition.md)
**Leads To:** [autonomous_operation.md](../Agent_Capabilities_and_Extensions/autonomous_operation.md), [planning.md](planning.md)

## Quick Decision Guide
**Use this when you need to:** Improve agent reliability and transparency in multi-step tasks.
**Skip this when:** The workflow is atomic or fully scripted.

## Further Exploration
- [ReAct pattern paper](https://arxiv.org/abs/2210.03629)
- [Chain-of-thought prompting](https://arxiv.org/abs/2201.11903)
- [Stepwise agent debugging](https://arxiv.org/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
