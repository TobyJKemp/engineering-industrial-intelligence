# Multi Root Workspace

## At a Glance
| | |
|---|---|
| **Category** | Workspace Pattern |
| **Complexity** | Beginner |
| **Time to Learn** | 30-45 minutes |
| **Prerequisites** | Basic IDE and repository structure knowledge |

## One-Sentence Summary
A multi root workspace is an editor setup that opens and manages multiple repositories or folders as one working context.

## Why This Matters to You
Real AI and software systems are rarely contained in one folder. A multi root workspace helps you operate across service repos, docs repos, and infrastructure files without constant context switching. This reduces navigation friction and makes cross-repo changes easier to reason about. For agent workflows, it gives tools a broader but still structured view of related assets.

## The Core Idea
### What It Is
In a multi root workspace, your editor treats several folder roots as one logical workspace. You can search across all roots, run tasks per root, and keep related work visible in one session.

This pattern is common in platform teams where code, runbooks, and configuration are split across repositories. It enables coordinated updates while preserving repository boundaries.

### What It Isn't
A multi root workspace is not a monorepo. Repositories stay independent, with their own histories and lifecycles.

It is also not automatic shared context for every tool. Tooling must still handle root scope and path resolution correctly.

## How It Works
1. Add multiple folders to one workspace definition.
2. Configure per-root tasks, settings, and search filters.
3. Execute and review changes while tracking which root each action affects.

## Think of It Like This
Think of a dispatcher overseeing several connected rail yards from one control panel instead of walking between separate control rooms.

## The "So What?" Factor
**If you use this:**
- You reduce friction for cross-repo feature and incident work.
- You improve visibility of dependencies between code and documentation.
- You speed up onboarding for complex, distributed systems.

**If you don't:**
- Teams lose time switching windows and missing cross-repo impacts.
- Coordination errors increase when related changes are split across sessions.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Which repositories should be grouped for real workflows?
- [ ] Are search and task scopes clear enough to avoid wrong-root edits?
- [ ] Do contributors understand root-specific ownership and branching?

## Watch Out For
⚠️ Running commands in the wrong root when folder names are similar.
⚠️ Assuming workspace-wide settings apply safely to every repository.

## Connections
**Builds On:** [workspace_scope.md](workspace_scope.md), [workspace_state.md](workspace_state.md)
**Works With:** [workspace_awareness.md](workspace_awareness.md), [repository_context.md](repository_context.md)
**Leads To:** [codebase_understanding.md](codebase_understanding.md), [parallel_tool_execution.md](parallel_tool_execution.md)

## Quick Decision Guide
**Use this when you need to:** Work across multiple related repositories in one coordinated workflow.
**Skip this when:** A single repository contains everything needed for your task.

## Further Exploration
- [VS Code multi-root workspace docs](https://code.visualstudio.com/docs/editor/multi-root-workspaces)
- [Monorepo vs multirepo tradeoffs](https://martinfowler.com/articles/monorepos.html)
- [Repository architecture patterns](https://docs.github.com/en/repositories)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
