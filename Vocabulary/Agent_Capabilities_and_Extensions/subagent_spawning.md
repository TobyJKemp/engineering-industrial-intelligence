# Subagent Spawning

## At a Glance
| | |
|---|---|
| **Category** | Orchestration Capability |
| **Complexity** | Advanced |
| **Time to Learn** | 2-4 hours |
| **Prerequisites** | Agent orchestration, task decomposition, and context management |

## One-Sentence Summary
Subagent spawning is launching specialized child agents to handle focused tasks and then returning their results to a coordinating parent agent.

## Why This Matters to You
No single agent is optimal at every task. Subagent spawning lets you delegate work to specialized capabilities without losing overall coordination. This improves throughput and can raise output quality for complex workflows. It also mirrors how high-performing teams distribute work while keeping shared goals aligned.

## The Core Idea
### What It Is
Subagent spawning creates temporary or scoped agents with a specific mission, context package, and expected return format. A parent agent delegates work, waits for results, and integrates outputs into the broader workflow.

This pattern supports parallelization and specialization, especially for tasks like repository exploration, data analysis, or targeted remediation.

### What It Isn't
Subagent spawning is not uncontrolled agent proliferation. Each child should have clear scope, lifecycle, and constraints.

It is also not a replacement for good planning. Poor decomposition can make distributed work slower and noisier.

## How It Works
1. Parent agent decomposes work and defines subagent tasks with boundaries.
2. Spawn subagents with required context, tools, and expected output schema.
3. Collect, validate, and merge results into final parent-level decisions.

## Think of It Like This
Think of a dispatch center assigning specialized crews to separate incidents, then consolidating their updates into one coordinated network plan.

## The "So What?" Factor
**If you use this:**
- You increase throughput on complex multi-part workflows.
- You improve quality by matching tasks to specialized capabilities.
- You keep parent orchestration focused on integration and risk control.

**If you don't:**
- One agent becomes a bottleneck for unrelated tasks.
- Complex assignments take longer and lose specialist depth.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are task boundaries explicit enough for independent execution?
- [ ] Is subagent output format strict enough for reliable merging?
- [ ] Are lifecycle, timeout, and failure rules defined?

## Watch Out For
⚠️ Sending too much context to subagents, increasing cost and confusion.
⚠️ Merging inconsistent outputs without normalization and validation.

## Connections
**Builds On:** [specialized_agent.md](specialized_agent.md), [agent_delegation.md](agent_delegation.md)
**Works With:** [parallel_tool_execution.md](parallel_tool_execution.md), [structured_tool_output.md](structured_tool_output.md)
**Leads To:** [autonomous_operation.md](autonomous_operation.md), [skill_orchestration.md](skill_orchestration.md)

## Quick Decision Guide
**Use this when you need to:** Split a complex objective into specialized, concurrent workstreams.
**Skip this when:** The task is simple and delegation overhead outweighs benefits.

## Further Exploration
- [Multi-agent systems overview](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Task decomposition in autonomous systems](https://arxiv.org/)
- [Workflow orchestration patterns](https://martinfowler.com/articles/patterns-of-distributed-systems/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: Medium*
