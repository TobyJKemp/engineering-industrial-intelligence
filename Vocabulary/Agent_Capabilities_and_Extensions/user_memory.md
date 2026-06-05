# User Memory

## At a Glance
| | |
|---|---|
| **Category** | Memory Pattern |
| **Complexity** | Beginner |
| **Time to Learn** | 30-60 minutes |
| **Prerequisites** | Context management and personalization basics |

## One-Sentence Summary
User memory is persistent information about a person's preferences and patterns that helps an assistant provide more consistent, personalized support over time.

## Why This Matters to You
Without memory, every session starts from zero. User memory reduces repetition and improves continuity in recurring workflows. It helps assistants adapt to preferred formats, priorities, and constraints. In long-running engineering work, this saves time and reduces frustration.

## The Core Idea
### What It Is
User memory stores stable, cross-session facts such as preferred response style, recurring project practices, and common constraints. It is typically separate from temporary session state and repository-specific notes.

Effective user memory is concise, relevant, and updated as preferences change. It should improve outcomes without creating privacy or overfitting problems.

### What It Isn't
User memory is not a complete transcript archive. It should capture distilled, reusable signals.

It is also not a license to store sensitive secrets. Security and privacy boundaries still apply.

## How It Works
1. Capture stable preference signals from repeated interactions.
2. Store them in persistent user-scoped memory.
3. Retrieve and apply them contextually in future sessions.

## Think of It Like This
Think of a seasoned dispatcher who remembers a team's preferred reporting format and applies it every shift.

## The "So What?" Factor
**If you use this:**
- You reduce repetitive instructions across sessions.
- You improve personalization without reconfiguration each time.
- You increase consistency in communication and outputs.

**If you don't:**
- Users repeatedly restate the same preferences.
- Session quality varies and onboarding takes longer.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Is the memory item stable and broadly reusable?
- [ ] Does it avoid sensitive or unnecessary personal data?
- [ ] Is there a clear way to update or remove outdated memory?

## Watch Out For
⚠️ Storing ephemeral details that quickly become misleading.
⚠️ Retaining memory that should be deleted for privacy reasons.

## Connections
**Builds On:** [memory_persistence.md](memory_persistence.md), [memory_scope.md](memory_scope.md)
**Works With:** [repository_memory.md](repository_memory.md), [session_memory.md](session_memory.md)
**Leads To:** [memory_retrieval.md](memory_retrieval.md), [stateful_conversation.md](stateful_conversation.md)

## Quick Decision Guide
**Use this when you need to:** Preserve stable user preferences across conversations.
**Skip this when:** Information is task-specific and temporary.

## Further Exploration
- [Human-centered AI personalization](https://pair.withgoogle.com/)
- [Privacy by design principles](https://www.ipc.on.ca/wp-content/uploads/resources/7foundationalprinciples.pdf)
- [Context management in assistant systems](https://arxiv.org/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: Medium*
