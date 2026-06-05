# Error Handling

## At a Glance
| | |
|---|---|
| **Category** | Technique |
| **Complexity** | Intermediate |
| **Time to Learn** | 4-6 hours to understand patterns, weeks to master edge cases |
| **Prerequisites** | Software error handling basics, API interactions, asynchronous operations |

## One-Sentence Summary
Error Handling is the practice of anticipating, detecting, and recovering from failures in AI agent operations—transforming inevitable breakdowns (API timeouts, malformed outputs, tool failures) into manageable situations that preserve system stability and provide useful feedback rather than catastrophic crashes.

## Why This Matters to You
AI agents fail in more creative ways than traditional software. An API times out—that's familiar. But an agent hallucinates a tool name that doesn't exist, generates syntactically valid but semantically nonsensical SQL, exceeds its context window mid-operation, or enters an infinite retry loop because it doesn't understand the error message. Traditional try-catch blocks aren't enough. Without thoughtful error handling, your agent crashes on edge cases, wastes tokens retrying unrecoverable failures, provides cryptic error messages that users can't act on, or worse—silently produces wrong results. With good error handling, failures become learning opportunities: the agent recognizes recoverable vs. terminal errors, retries with exponential backoff, degrades gracefully when full functionality isn't available, logs rich context for debugging, and escalates to humans when automated recovery isn't possible. Error handling is the difference between a fragile prototype that works in demos and a robust system that survives production.

## The Core Idea
### What It Is
Error Handling in AI agent systems is the comprehensive approach to managing failures across multiple dimensions: external dependencies (APIs, databases, tools), agent behavior (malformed outputs, hallucinations, infinite loops), resource constraints (context window limits, token budgets, rate limits), and system-level issues (network failures, service outages, timeout errors). Unlike traditional error handling which focuses on code exceptions, AI error handling must address the probabilistic nature of agent decision-making—errors aren't just bugs to fix but expected outcomes to manage.

The practice operates at several levels. Immediate error detection identifies when something has gone wrong: an API returns 500, a generated JSON is unparsable, a tool execution raises an exception, a validation check fails. Classification determines error type and recoverability: Is this temporary (network blip) or permanent (invalid credentials)? Transient (rate limit) or persistent (bad configuration)? Recoverable through retry or requiring human intervention? Recovery strategies implement appropriate responses: retry with exponential backoff for transient failures, fallback to alternative approaches when primary methods fail, graceful degradation when full functionality is impossible, state rollback to known-good configurations.

AI agents introduce unique error categories. Output format errors occur when the agent generates responses that don't match expected schemas—JSON with missing fields, API calls with incorrect parameter types, SQL with syntax errors. Semantic errors happen when output is syntactically valid but meaningfully wrong—a correct JSON structure requesting deletion of the wrong records. Context window errors emerge when conversation history plus retrieved documents exceed model limits. Tool hallucination occurs when agents reference tools that don't exist or misuse tools that do. Token budget exhaustion stops operations mid-task. Each requires specialized handling approaches.

Effective error handling provides multiple layers of protection. Preventive measures like input validation and deterministic controls reduce error likelihood. Detection mechanisms like output validation and monitoring identify errors quickly. Recovery strategies like retry logic and fallback behaviors handle errors that occur. Escalation paths ensure humans intervene when automated recovery fails. Observability through comprehensive logging enables debugging and continuous improvement. Together, these create resilient systems that degrade gracefully rather than failing catastrophically.

### What It Isn't
Error Handling is not error prevention. While good design reduces errors, no system eliminates them entirely. Errors will occur; handling means managing them gracefully, not pretending they won't happen.

It's also not just logging errors. Logging is crucial for debugging, but error handling requires action: retry, fallback, escalate, rollback. Simply recording that an error occurred without responding doesn't constitute handling.

Finally, error handling isn't hiding failures from users. Transparent error communication—explaining what went wrong and what's being done about it—builds trust. Silently swallowing errors or providing generic "something went wrong" messages frustrates users and prevents them from taking corrective action.

## How It Works
Comprehensive error handling combines multiple strategies:

1. **Error Classification and Routing** - When errors occur, classify them immediately: transient (temporary network issues, rate limits) vs. persistent (invalid credentials, missing resources), recoverable (can retry or use alternatives) vs. terminal (fundamental failures requiring human intervention). Classification determines handling strategy. Transient errors trigger retry logic; terminal errors escalate immediately.

2. **Exponential Backoff Retry** - For transient failures, retry with increasing delays: first attempt immediate, second after 1 second, third after 2 seconds, fourth after 4 seconds, capping at reasonable maximum (60 seconds). This prevents overwhelming struggling services while giving transient issues time to resolve. Include jitter (random variation in delay) to prevent thundering herd problems when many agents retry simultaneously.

3. **Circuit Breaker Pattern** - Track failure rates for external dependencies. If failures exceed threshold (e.g., 50% failure rate over 10 requests), "open the circuit"—stop attempting requests temporarily, return errors immediately. After cooldown period, try one request ("half-open"). If successful, resume normal operation ("close circuit"). If failure persists, reopen circuit. This prevents cascading failures and gives broken services time to recover.

4. **Fallback Strategies** - Define alternative approaches when primary methods fail. If primary API is unavailable, use cached data or alternative API. If agent can't generate valid JSON, use structured output parser with error correction. If context window is exceeded, summarize history or use smaller context. Fallbacks maintain partial functionality rather than total failure.

5. **Output Validation and Correction** - Before executing agent outputs, validate: schema compliance, semantic correctness, safety constraints. If validation fails, attempt automatic correction: parsing errors might be fixed by removing extraneous characters, missing fields might use defaults, type mismatches might coerce to correct types. If correction succeeds, proceed; if it fails, request agent regeneration with error context.

6. **Graceful Degradation** - When full functionality is impossible, provide reduced capability rather than nothing. If document retrieval fails, answer from conversation history only. If code execution times out, return partial results with timeout notice. If token budget is exhausted, complete current subtask and pause rather than abrupt halt. Users prefer limited functionality to total failure.

7. **Idempotency and Safe Retries** - Design operations to be safely retryable. Use idempotency keys for API calls—retrying the same operation doesn't duplicate effects. Check state before actions: if the file already exists from a previous attempt, skip creation rather than error. Read-check-write patterns ensure retries don't corrupt state.

8. **Human Escalation Paths** - Define clear thresholds for human intervention: repeated failures despite retries, errors requiring judgment (ambiguous user intent, conflicting constraints), terminal errors blocking progress. Escalation includes: descriptive error context, state at failure time, recovery attempts made, suggested next actions. This enables humans to resolve issues efficiently.

9. **Context-Rich Logging** - Log not just that an error occurred, but full context: agent state, conversation history, inputs, outputs, recovery attempts, timestamps. Structured logging (JSON) enables queries: "show all context window errors in the last week." Rich logs make debugging possible—without context, errors are mysteries; with context, they're solvable problems.

10. **Error Budgets and Thresholds** - Set acceptable error rates: if agent has >10% failure rate, investigate; if >50%, take offline. Error budgets balance reliability against innovation—some errors are acceptable during learning, but sustained high rates indicate problems requiring attention.

## Think of It Like This
Imagine an experienced restaurant server. When something goes wrong—kitchen is out of an ingredient, dishwasher broke a plate, order got lost—they don't panic or give up. They assess the situation: Is this fixable? Can we substitute another ingredient? Should I comp the meal? Do I need to get the manager? They provide alternatives, communicate clearly with customers ("I apologize, we're out of salmon, but the halibut is excellent tonight—may I bring you that instead?"), and escalate when needed. They don't hide problems, but they also don't make customers deal with every kitchen issue. That's error handling: graceful recovery, clear communication, appropriate escalation, maintaining service even when things go wrong.

## The "So What?" Factor
**If you implement good error handling:**
- Agents survive production edge cases that would crash naive implementations
- Transient failures (network blips, temporary rate limits) recover automatically
- Users receive actionable error messages instead of cryptic stack traces
- Debugging becomes possible through rich logging with full context
- System reliability improves as errors are managed rather than causing cascades
- Partial functionality remains available even when components fail
- Human intervention is triggered appropriately—not too early, not too late
- Error patterns reveal improvement opportunities through systematic logging

**If you don't:**
- Agents crash on recoverable failures, requiring manual restarts
- Transient issues become permanent failures without retry logic
- Cascading failures occur as one error triggers others downstream
- Users face cryptic errors they can't understand or act on
- Debugging is painful without context about what went wrong and why
- Systems are fragile—any unexpected condition causes total failure
- Human operators are overwhelmed by trivial errors that should self-recover
- Error insights are lost—no systematic data to drive reliability improvements

## Practical Checklist
Before deploying an agent with error handling:
- [ ] Have you identified all external dependencies and their failure modes?
- [ ] Are errors classified by type (transient/persistent, recoverable/terminal)?
- [ ] Is retry logic implemented with exponential backoff and maximum attempts?
- [ ] Do you have circuit breakers protecting external service calls?
- [ ] Are there fallback strategies when primary approaches fail?
- [ ] Does output validation catch common agent mistakes before execution?
- [ ] Can the system degrade gracefully when full functionality isn't available?
- [ ] Are operations idempotent and safe to retry?
- [ ] Do users receive clear, actionable error messages?
- [ ] Are human escalation paths defined with appropriate thresholds?
- [ ] Does logging capture sufficient context for debugging?
- [ ] Have you tested error handling paths, not just happy paths?
- [ ] Are error rates monitored with alerts on threshold violations?

## Watch Out For
⚠️ **Retry Without Backoff** - Immediately retrying failed operations overwhelms struggling services, worsens problems, and wastes resources. Always use exponential backoff. If the service is already failing, hammering it with rapid retries makes recovery harder.

⚠️ **Catching Everything** - Broad catch-all error handlers hide specific issues, making debugging impossible and potentially masking serious problems. Catch specific error types, handle them appropriately, and let unexpected errors surface for investigation.

⚠️ **Infinite Retry Loops** - Retrying non-transient errors forever wastes resources and delays necessary escalation. Set maximum retry counts and timeout limits. If five retries failed, the sixth probably will too—escalate instead.

⚠️ **Silent Failures** - Swallowing errors without logging or notification creates invisible problems. Systems appear to work but produce wrong results. All errors should be logged, and significant errors should trigger alerts or user notifications.

⚠️ **Poor Error Messages** - Generic messages like "Error occurred" or technical stack traces don't help users. Good error messages explain: what went wrong, why it might have happened, what the user can do about it. "API rate limit exceeded. Retrying in 60 seconds." is actionable; "Error 429" is not.

⚠️ **Not Testing Error Paths** - Testing only happy paths leaves error handling unvalidated. Use chaos engineering: inject faults, simulate API failures, cause timeouts. Verify error handling works before encountering real failures in production.

## Connections
**Builds On:** 
- [Agent State](agent_state.md) - Error recovery requires understanding and potentially rolling back state
- [Deterministic Controls](deterministic_controls.md) - Controls prevent many errors from occurring

**Works With:** 
- [Context Management](context_management.md) - Managing context window errors
- [Observability](../../Cloud_and_Distributed/) - Monitoring and logging for error detection
- [Exception Handling](../../Dispatching/Exception_Handling/) - System-level exception management patterns
- [Circuit Breakers](../../Software_Engineering/) - Preventing cascading failures
- [Resilience Patterns](../../Software_Engineering/) - Broader reliability strategies

**Leads To:** 
- [Chaos Engineering](../../Testing_and_Evaluation/) - Proactive error injection testing
- [Incident Response](../../Yard_Operations/) - Managing when error handling isn't sufficient
- [Reliability Engineering](../../Infrastructure_and_DevOps/) - System-wide reliability practices
- [Agent Monitoring](../../MLOps/) - Continuous observation of agent health

## Quick Decision Guide
**Invest heavily in error handling when:** Deploying agents to production, agents interact with multiple external services, operations have real-world consequences (data modification, user-facing actions), reliability is critical for user trust, agents run autonomously without immediate human supervision.

**Use simpler approaches when:** Early prototyping where rapid iteration matters more than reliability, fully sandboxed environments where failures are harmless, educational contexts where seeing raw errors aids learning, or systems with constant human supervision that can intervene immediately.

## Further Exploration
- 📖 **"Site Reliability Engineering" by Google** - Chapters on error budgets, handling failures, building reliable systems applicable to AI agents
- 🎯 **Implement Circuit Breaker** - Add circuit breaker pattern to an external API call. Measure: How often does it open? Does it prevent cascading failures? What's the recovery time?
- 💡 **Tenacity Library (Python)** - Study this retry/backoff library. It demonstrates best practices: exponential backoff, maximum attempts, configurable wait strategies
- 📖 **"Release It!" by Michael Nygard** - Patterns for building resilient systems: timeouts, circuit breakers, bulkheads, all applicable to agent error handling
- 🎯 **Error Injection Testing** - Deliberately break components your agent depends on. Does it recover gracefully? Are error messages clear? Does logging provide sufficient context?
- 💡 **LangChain Error Handling** - Examine how LangChain handles LLM errors, parsing failures, tool exceptions. Learn from established patterns
- 📖 **AWS Error Retry and Exponential Backoff** - Study AWS SDK retry policies. They've refined these patterns across millions of applications

---
*Added: May 15, 2026 | Updated: May 15, 2026 | Confidence: High*
