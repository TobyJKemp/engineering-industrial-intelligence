# Tool Discovery

## At a Glance
| | |
|---|---|
| **Category** | Capability Management |
| **Complexity** | Beginner |
| **Time to Learn** | 30-60 minutes |
| **Prerequisites** | Basic understanding of tool metadata and registration |

## One-Sentence Summary
Tool discovery is the process of finding available tools and understanding what each tool can do before invocation.

## Why This Matters to You
You cannot orchestrate effectively if you do not know your capability surface. Discovery helps agents and humans choose the right tool faster and avoid duplicate implementations. It also reduces misuse by clarifying constraints and expected inputs. In large systems, discovery is the entry point for safe extensibility.

## The Core Idea
### What It Is
Tool discovery exposes searchable information about tools, such as names, descriptions, schemas, permissions, and status. Discovery can be static (registry files) or dynamic (runtime capability queries).

Quality discovery includes enough metadata to decide suitability without trial-and-error calls. This lowers latency and error rates in orchestration.

### What It Isn't
Tool discovery is not tool execution. It should describe capability, not trigger side effects.

It is also not useful if metadata is stale or inconsistent.

## How It Works
1. Register tools with metadata and schemas in a discoverable catalog.
2. Query the catalog by intent, capability, or constraints.
3. Select tools based on fit, permissions, and compatibility.

## Think of It Like This
Think of checking a yard equipment catalog before dispatching crews, so the right equipment is selected the first time.

## The "So What?" Factor
**If you use this:**
- You reduce time spent guessing which tool to call.
- You improve reliability by selecting tools with known contracts.
- You enable scalable extension ecosystems.

**If you don't:**
- Teams duplicate tools because existing ones are hard to find.
- Wrong-tool errors increase and slow delivery.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Does each tool have complete and searchable metadata?
- [ ] Are capability descriptions updated when behavior changes?
- [ ] Can discovery results be filtered by permission scope?

## Watch Out For
⚠️ Discovery catalogs that list tools but omit critical constraints.
⚠️ Runtime-only tools missing from documentation and registry views.

## Connections
**Builds On:** [tool_registration.md](tool_registration.md), [tool_metadata.md](tool_metadata.md)
**Works With:** [tool_schema.md](tool_schema.md), [tool_marketplace.md](tool_marketplace.md)
**Leads To:** [tool_invocation.md](tool_invocation.md), [tool_composition.md](tool_composition.md)

## Quick Decision Guide
**Use this when you need to:** Choose the right tool quickly in a growing capability set.
**Skip this when:** The workflow has one fixed tool with no alternatives.

## Further Exploration
- [Service discovery patterns](https://martinfowler.com/articles/microservices.html)
- [API catalog best practices](https://swagger.io/resources/articles/best-practices-in-api-design/)
- [Capability registries in plugin ecosystems](https://code.visualstudio.com/api)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
