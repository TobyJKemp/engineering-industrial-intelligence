# Agent Delegation

## At a Glance
| | |
|---|---|
| **Category** | Orchestration Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Task decomposition and permission models |

## One-Sentence Summary
Agent delegation is assigning responsibility for a subtask or decision to another agent, often with explicit boundaries and expectations.

## Why This Matters to You
Delegation enables specialization and parallelism. It lets complex workflows scale by breaking them into manageable parts. In agent systems, delegation is a key mechanism for distributing work, managing risk, and improving throughput.

## The Core Idea
### What It Is
Delegation involves a parent or coordinator agent identifying a subtask, selecting a suitable agent, and transferring authority for that task. The delegating agent may specify constraints, expected outputs, and escalation paths.

Effective delegation includes monitoring, feedback, and the ability to revoke or reassign tasks as needed.

### What It Isn't
Delegation is not abdication. The delegator remains responsible for overall outcomes.

It is also not always static; dynamic delegation adapts to changing context and agent capabilities.

## How It Works
1. Identify subtask and select agent with required skills or context.
2. Transfer authority with clear boundaries and expectations.
3. Monitor progress, provide feedback, and integrate results.

## Think of It Like This
Think of a dispatcher assigning a specific train movement to a local operator while retaining overall network responsibility.

## The "So What?" Factor
**If you use this:**
- You increase throughput and specialization.
- You reduce bottlenecks and single points of failure.
- You improve adaptability to changing workloads.

**If you don't:**
- One agent becomes overloaded or stuck on tasks outside its expertise.
- System resilience and efficiency suffer.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are delegation boundaries and escalation paths clear?
- [ ] Is there feedback and monitoring between delegator and delegate?
- [ ] Can tasks be reassigned if conditions change?

## Watch Out For
⚠️ Over-delegation without accountability or feedback.
⚠️ Delegation loops or deadlocks in complex workflows.

## Connections
**Builds On:** [task_decomposition.md](task_decomposition.md), [permission_delegation.md](../Agent_Capabilities_and_Extensions/permission_delegation.md)
**Works With:** [subagent_spawning.md](../Agent_Capabilities_and_Extensions/subagent_spawning.md), [agent_collaboration.md](agent_collaboration.md)
**Leads To:** [autonomous_operation.md](../Agent_Capabilities_and_Extensions/autonomous_operation.md), [planning.md](planning.md)

## Quick Decision Guide
**Use this when you need to:** Distribute work across agents for efficiency and specialization.
**Skip this when:** The task is atomic or requires single-agent context.

## Further Exploration
- [Delegation in multi-agent systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Task assignment strategies](https://arxiv.org/)
- [Orchestration patterns in AI](https://martinfowler.com/articles/patterns-of-distributed-systems/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
