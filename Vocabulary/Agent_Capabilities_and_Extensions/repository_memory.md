# Repository Memory

## At a Glance
| | |
|---|---|
| **Category** | Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 45-90 minutes |
| **Prerequisites** | Context management, project conventions, and knowledge capture basics |

## One-Sentence Summary
Repository memory is persistent, workspace-scoped knowledge that helps agents and contributors retain project-specific facts across sessions.

## Why This Matters to You
Without a memory layer, teams repeatedly rediscover the same rules and pitfalls. Repository memory captures proven facts close to where they are used, reducing cognitive load and rework. It also helps AI assistants provide more consistent outputs over time. In operational terms, it becomes a shared memory rail that keeps knowledge flowing between sessions.

## The Core Idea
### What It Is
Repository memory stores stable, high-value knowledge tied to a specific codebase or knowledge repository. Typical content includes build commands, naming conventions, architectural boundaries, and lessons learned from recurring failures.

Unlike global user preferences, repository memory is local to one workspace. This scoping prevents cross-project contamination and keeps recommendations relevant.

### What It Isn't
Repository memory is not a dumping ground for temporary notes. Short-lived task state belongs in session memory.

It is also not a substitute for source-of-truth documentation. Memory should reference and reinforce canonical docs, not compete with them.

## How It Works
1. Capture concise, reusable facts discovered during real work.
2. Store them in repository-scoped memory files with clear organization.
3. Retrieve and update memory as the repository evolves.

## Think of It Like This
Think of repository memory as the route knowledge held by experienced dispatchers, written down so every shift can operate with the same hard-earned insight.

## The "So What?" Factor
**If you use this:**
- You reduce repeated mistakes and duplicated investigation effort.
- You improve assistant continuity across separate sessions.
- You accelerate onboarding with practical, project-specific guidance.

**If you don't:**
- Institutional knowledge stays fragile and person-dependent.
- The same context gaps keep resurfacing in reviews and incidents.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Is this fact stable enough to be useful across future sessions?
- [ ] Is the note concise and linked to the relevant source artifact?
- [ ] Does repository scope prevent accidental leakage to other projects?

## Watch Out For
⚠️ Storing outdated memory entries that silently mislead future work.
⚠️ Writing long narrative notes instead of short, actionable facts.

## Connections
**Builds On:** [memory_scope.md](memory_scope.md), [memory_organization.md](memory_organization.md)
**Works With:** [memory_retrieval.md](memory_retrieval.md), [memory_persistence.md](memory_persistence.md)
**Leads To:** [session_memory.md](session_memory.md), [user_memory.md](user_memory.md)

## Quick Decision Guide
**Use this when you need to:** Preserve repository-specific lessons and conventions across sessions.
**Skip this when:** Information is temporary or already captured in canonical docs without reuse value.

## Further Exploration
- [Knowledge management systems thinking](https://www.atlassian.com/work-management/knowledge-sharing)
- [Post-incident learning practices](https://sre.google/sre-book/postmortem-culture/)
- [Operational runbook documentation patterns](https://www.pagerduty.com/resources/learn/what-is-a-runbook/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: Medium*
