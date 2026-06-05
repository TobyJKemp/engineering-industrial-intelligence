# Structured Tool Output

## At a Glance
| | |
|---|---|
| **Category** | Data Contract Pattern |
| **Complexity** | Beginner |
| **Time to Learn** | 30-60 minutes |
| **Prerequisites** | JSON/schema basics and tool integration experience |

## One-Sentence Summary
Structured tool output is returning tool results in a predictable schema so downstream systems can parse, validate, and act on them reliably.

## Why This Matters to You
Free-form tool responses are hard to automate safely. Structured output makes orchestration predictable and reduces parsing errors. It also improves debugging because expected fields and types are explicit. For agent systems, this is a key enabler of dependable multi-step automation.

## The Core Idea
### What It Is
Structured output uses a defined schema for tool responses, including required fields, types, status indicators, and error envelopes. Consumers can then validate inputs programmatically before proceeding.

This approach supports better composition: one tool's output can become another tool's input without fragile text parsing. It also improves observability and contract testing.

### What It Isn't
Structured output is not overengineering for every tiny script. The schema should match system complexity.

It is also not enough to define schema once and forget it. Versioning and backward compatibility still matter.

## How It Works
1. Define response schema including success and error structures.
2. Emit tool results that conform strictly to the schema.
3. Validate outputs before downstream consumption and log contract violations.

## Think of It Like This
Think of receiving standardized rail manifests instead of handwritten notes, so loading and routing can be automated safely.

## The "So What?" Factor
**If you use this:**
- You reduce brittle parsing and integration failures.
- You enable robust automation and tool chaining.
- You improve contract clarity for contributors and reviewers.

**If you don't:**
- Downstream steps break on wording changes.
- Incidents become harder to diagnose due to ambiguous outputs.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Does the schema include clear status and error details?
- [ ] Are required fields sufficient for downstream decisions?
- [ ] Is schema evolution versioned and tested?

## Watch Out For
⚠️ Returning mixed structured and free-form payloads that confuse consumers.
⚠️ Silent schema drift between producer and consumer services.

## Connections
**Builds On:** [tool_schema.md](tool_schema.md), [tool_validation.md](tool_validation.md)
**Works With:** [tool_result_handling.md](tool_result_handling.md), [tool_invocation.md](tool_invocation.md)
**Leads To:** [tool_composition.md](tool_composition.md), [parallel_tool_execution.md](parallel_tool_execution.md)

## Quick Decision Guide
**Use this when you need to:** Automate reliable handoffs between tools and orchestration layers.
**Skip this when:** Output is only for one-time human reading with no downstream automation.

## Further Exploration
- [JSON Schema specification](https://json-schema.org/)
- [API contract testing patterns](https://martinfowler.com/articles/microservice-testing/#contract-testing)
- [Reliable tool orchestration design](https://www.cncf.io/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
