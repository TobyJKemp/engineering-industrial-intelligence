# Skill Context

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Data Structure |
| **Complexity** | Intermediate |
| **Time to Learn** | 1–2 hours for basics; more for advanced use |
| **Prerequisites** | Understanding of skills, agent frameworks, and context management |

## One-Sentence Summary
Skill context is the set of information and state provided to a skill at invocation time, enabling it to operate effectively within the current environment, user session, or workflow.

## Why This Matters to You
Skill context is what makes your skills smart, adaptable, and relevant. By providing each skill with the right context—such as user preferences, session data, or environmental variables—you ensure that it can make informed decisions, personalize its behavior, and interact smoothly with other components. Without proper context, skills become rigid, error-prone, or unable to handle real-world complexity. Mastering skill context is essential for building agents that are truly intelligent and user-centric.

## The Core Idea

### What It Is
Skill context is a data structure or object that encapsulates all relevant information a skill needs to perform its function. This can include user input, session memory, environmental variables, authentication tokens, and more. When an agent invokes a skill, it passes the current context, allowing the skill to access everything it needs to operate correctly and consistently.

Skill context enables skills to be stateless (relying only on provided context) or stateful (updating the context as they run), supporting modularity and reusability.

### What It Isn't
Skill context is not hard-coded configuration or global state. It is not a catch-all for unrelated data, nor is it a replacement for persistent storage or long-term memory. Context should be relevant, scoped, and managed carefully to avoid confusion or security risks.

## How It Works
1. **Assemble Context**: The agent gathers all relevant information for the current invocation.
2. **Pass to Skill**: The context is provided as an argument or object when calling the skill.
3. **Skill Uses Context**: The skill reads from (and may update) the context to perform its task.

## Think of It Like This
Skill context is like a briefing folder handed to a consultant before a meeting: it contains all the background, goals, and constraints needed to do the job well.

## The "So What?" Factor
**If you use this:**
- Skills can personalize responses and adapt to changing situations
- Agents become more modular and easier to test
- Complex workflows are easier to manage and debug

**If you don't:**
- Skills may behave unpredictably or lack necessary information
- Code becomes tangled with global variables or hard-coded values
- Adapting to new requirements becomes much harder

## Practical Checklist
Before implementing, ask yourself:
- [ ] What information does each skill need to operate correctly?
- [ ] Is the context structure clear, documented, and secure?
- [ ] Can context be extended or updated as requirements evolve?

## Watch Out For
⚠️ Overloading context with unnecessary data can cause confusion or security issues  
⚠️ Inconsistent context structures make skills hard to reuse or maintain

## Connections
**Builds On:** context management, state management, [session_memory.md]  
**Works With:** [skill.md], [skill_composition.md], [tool_invocation.md], [trace_logging.md]  
**Leads To:** [stateful_conversation.md], [self_correction.md], [specialized_agent.md]

## Quick Decision Guide
**Use this when you need to:** Provide skills with the information they need to act intelligently and contextually  
**Skip this when:** Skills are trivial, stateless, or require no external information

## Further Exploration
- 📖 [Context Objects in Software Design](https://martinfowler.com/bliki/ContextObject.html)
- 🎯 [Microsoft Semantic Kernel: Context Management](https://learn.microsoft.com/en-us/semantic-kernel/agents/context/)
- 💡 [Best Practices for Context Passing in AI Systems](https://rasa.com/docs/rasa/core/context/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
