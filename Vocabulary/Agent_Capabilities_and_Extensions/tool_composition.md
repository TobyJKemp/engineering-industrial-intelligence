# Tool Composition

## At a Glance
| | |
|---|---|
| **Category** | Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Tool invocation basics and workflow design |

## One-Sentence Summary
Tool composition is combining multiple tools into a coordinated sequence so their outputs create a higher-value end result.

## Why This Matters to You
Most meaningful tasks require more than one tool call. Composition helps you move from isolated actions to reliable workflows that produce complete outcomes. It reduces manual glue work and makes automation reusable. In agent systems, strong composition is what turns capability into practical productivity.

## The Core Idea
### What It Is
Tool composition organizes tools as a pipeline or graph where each step has a clear role. One tool gathers data, another transforms it, and another validates or persists results.

Good composition explicitly handles dependencies, error branches, and output formats between steps. This prevents fragile workflows that break when one tool changes behavior.

### What It Isn't
Tool composition is not calling many tools randomly. Ordering, contracts, and control flow matter.

It is also not a replacement for tool quality. Poorly designed tools still produce poor composed workflows.

## How It Works
1. Decompose the task into sub-operations and map each to an appropriate tool.
2. Define input-output contracts and ordering constraints between steps.
3. Execute, validate intermediate results, and handle errors before continuing.

## Think of It Like This
Think of assembling a train movement plan where signaling, dispatch, and crew scheduling each contribute one necessary piece.

## The "So What?" Factor
**If you use this:**
- You can automate complex tasks with predictable outcomes.
- You reduce handoff failures between tool steps.
- You create reusable operational patterns.

**If you don't:**
- Work stays manual and repetitive.
- Multi-tool workflows fail unpredictably at integration points.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Is each tool step necessary and clearly scoped?
- [ ] Are intermediate outputs validated before the next step?
- [ ] Is there an explicit fallback path for failed steps?

## Watch Out For
⚠️ Hidden dependencies where one tool silently assumes another tool's format.
⚠️ Overly long chains that become hard to debug and maintain.

## Connections
**Builds On:** [tool_invocation.md](tool_invocation.md), [tool_schema.md](tool_schema.md)
**Works With:** [tool_dependency.md](tool_dependency.md), [tool_result_handling.md](tool_result_handling.md)
**Leads To:** [parallel_tool_execution.md](parallel_tool_execution.md), [subagent_spawning.md](subagent_spawning.md)

## Quick Decision Guide
**Use this when you need to:** Turn multiple discrete tool capabilities into one end-to-end workflow.
**Skip this when:** A single tool can complete the task with no downstream integration.

## Further Exploration
- [Workflow orchestration patterns](https://martinfowler.com/articles/patterns-of-distributed-systems/)
- [Data pipeline design fundamentals](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/)
- [State machine patterns for orchestration](https://statecharts.dev/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
