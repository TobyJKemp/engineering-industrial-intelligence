# Retry Logic

## At a Glance
| | |
|---|---|
| **Category** | Technique |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 2-3 hours to understand, practice to implement well |
| **Prerequisites** | Basic error handling, understanding of transient vs. permanent failures |

## One-Sentence Summary
Retry Logic is the practice of automatically re-attempting failed operations—with strategic delays and limits—to handle transient failures (temporary network issues, rate limits, brief service outages) without burdening users or overwhelming systems, transforming intermittent hiccups into successful operations while recognizing when persistence becomes pointless and escalation is needed.

## Why This Matters to You
Networks fail. APIs timeout. Services get overloaded. Rate limits trigger. These failures aren't bugs in your code—they're facts of distributed computing. Without retry logic, your AI agent fails the instant any dependency hiccups: "API unavailable, request failed" even though retrying one second later would succeed. Users face errors for problems that are genuinely temporary. With retry logic, your agent absorbs these transient failures: automatically re-attempts after brief delays, succeeds on the second or third try, and users never know anything went wrong. The alternative—manual retry by users—is frustrating: they must recognize transient failures, wait an appropriate amount, and click "try again." Good retry logic handles this automatically. But naive retry logic creates new problems: infinite loops hammering broken services, wasted API costs on unrecoverable errors, cascading failures when many agents retry simultaneously. Smart retry logic knows when to try again, when to wait longer, when to give up, and when to escalate to humans—transforming distributed system fragility into resilient agent operations.

## The Core Idea
### What It Is
Retry Logic is the systematic approach to automatically re-attempting failed operations based on failure type, attempt count, and timing strategy. The practice distinguishes between transient failures (temporary issues that may resolve—network blips, rate limits, service overload) and permanent failures (fundamental problems that won't resolve—invalid credentials, missing resources, syntax errors). For transient failures, retry logic implements automatic re-attempts with increasingly longer delays. For permanent failures, it fails immediately without wasting effort. The goal is resilience: absorbing temporary problems without manual intervention while avoiding infinite loops and cascading failures.

The practice operates through several key decisions. Failure classification determines whether to retry: transient errors (HTTP 503, timeout, rate limit) trigger retries; permanent errors (HTTP 400, authentication failure, not found) don't. Retry count limits prevent infinite loops: typically 3-5 attempts maximum before giving up. Backoff strategy controls delay between attempts: exponential backoff (1s, 2s, 4s, 8s) prevents overwhelming recovering services. Jitter adds randomness to delays, preventing thundering herd problems where many agents retry simultaneously. These elements combine to create resilient-but-bounded retry behavior.

Retry logic also considers idempotency—whether operations can be safely re-executed without side effects. Idempotent operations (GET requests, setting values to specific states) can retry freely. Non-idempotent operations (POST requests creating resources, incrementing counters) risk duplication if retried naively. For non-idempotent operations, retry logic must use idempotency keys or check whether previous attempts succeeded before retrying.

Modern retry logic implements circuit breaker patterns: if many consecutive failures occur, "open the circuit"—stop retrying temporarily and fail fast, giving broken services time to recover. After cooldown, try one request ("half-open"). If successful, "close the circuit" and resume normal retry behavior. If failures persist, reopen the circuit. This prevents cascading failures and reduces unnecessary load on struggling systems.

### What It Isn't
Retry Logic is not a substitute for fixing root causes. If operations consistently require retries, something is broken. Retry logic masks symptoms temporarily while you investigate and fix underlying problems—it's not a permanent solution to systemic issues.

It's also not appropriate for all failures. Permanent errors (invalid input, authorization failures, resource not found) won't resolve with retries. Retrying these wastes resources and delays user feedback. Retry logic must distinguish transient from permanent failures and only retry the former.

Finally, retry logic isn't "keep trying forever." Unbounded retries create infinite loops, waste resources, and delay necessary escalation. Always implement maximum retry counts and absolute timeout limits. If five retries failed, the sixth probably will too—give up and report the error.

## How It Works
Implementing effective retry logic combines several strategies:

1. **Exponential Backoff** - Increase delay between retry attempts exponentially: first retry after 1 second, second after 2 seconds, third after 4 seconds, fourth after 8 seconds, capping at reasonable maximum (typically 60-120 seconds). This gives transient issues time to resolve without overwhelming services. The exponential growth ensures longer failures get longer pauses, appropriate to severity.

2. **Jitter Addition** - Add random variation to backoff delays: instead of exactly 2 seconds, wait 1.5-2.5 seconds (randomized). This prevents thundering herd problems—when 1000 agents all fail simultaneously and retry at identical times, creating synchronized load spikes. Jitter spreads retries across time, smoothing load.

3. **Maximum Retry Limits** - Set hard limits on retry attempts: typically 3-5 retries maximum. Track attempt count and fail permanently after exceeding limit. This prevents infinite loops and ensures timely failure reporting. Balance persistence (more retries = higher success rate) against cost and latency (fewer retries = faster failure, lower cost).

4. **Failure Type Classification** - Classify errors before deciding to retry. Retryable: network errors, timeouts, HTTP 503 (service unavailable), 429 (rate limit), 502/504 (gateway errors). Non-retryable: HTTP 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), validation errors. Use error codes and exception types to classify accurately.

5. **Idempotency Handling** - For idempotent operations (GET, PUT with same values, DELETE), retry freely. For non-idempotent operations (POST, increment), use idempotency keys—unique identifiers ensuring retries don't duplicate effects. Server recognizes idempotency key and returns previous result instead of creating duplicates.

6. **Circuit Breaker Integration** - Track failure rates for each dependency. If failure rate exceeds threshold (e.g., 50% over 10 requests), open circuit—stop retrying, fail fast immediately. After cooldown period (e.g., 60 seconds), enter half-open state—try one request. If successful, close circuit and resume retries. If failed, reopen circuit. This protects struggling services and prevents cascading failures.

7. **Retry Budget Management** - Implement organization-wide retry budgets preventing retry storms. Track total retry rate across all agents. If exceeding budget, throttle new retries. This prevents situations where retries themselves become the load problem, overwhelming systems that are trying to recover.

8. **Logging and Observability** - Log all retry attempts with context: operation attempted, failure reason, attempt number, delay used, success/failure outcome. This enables debugging ("why did this take 15 seconds?" → "3 retries with backoff"), monitoring retry rates (high rates indicate dependency problems), and tuning retry policies (are we retrying too much or too little?).

9. **User Communication** - For user-facing operations, communicate retry status: "API temporarily unavailable, retrying..." or progress indicators during retries. Don't leave users wondering whether the system is working. For quick retries (under 5 seconds), hide retries from users. For longer retries, show progress and offer cancel options.

10. **Graceful Degradation After Exhaustion** - When retries exhaust, don't just fail—provide useful information and alternatives. "Service unavailable after 5 attempts. Try again in 5 minutes or contact support." If possible, fall back to cached data, alternative services, or reduced functionality rather than complete failure.

## Think of It Like This
Imagine calling a friend whose phone is busy. You don't immediately conclude they're unreachable forever—you wait a minute and try again. If still busy, you wait a bit longer and try once more. Maybe you try a third time after a few more minutes. But you don't call every 10 seconds for an hour (that's harassment, not persistence). And if they explicitly reject your call (send to voicemail), you don't keep calling—that's a permanent signal, not a temporary issue. You also don't all simultaneously call at exactly 2:00 PM (thundering herd)—that would overwhelm them. That's retry logic: smart persistence that distinguishes temporary busy signals from permanent unavailability, waits appropriately between attempts, knows when to stop, and avoids overwhelming the very thing you're trying to reach.

## The "So What?" Factor
**If you implement retry logic:**
- Agents absorb transient failures without bothering users
- Network blips, brief rate limits, temporary outages become invisible
- Success rates increase significantly (70-80% of transient failures resolve with retry)
- User experience improves—operations complete despite intermittent issues
- System load is managed through backoff and jitter
- Cascading failures are prevented through circuit breakers
- Cost optimization occurs by recognizing permanent failures quickly
- Debugging is easier with retry logs showing what happened and why

**If you don't:**
- Every transient failure becomes a user-visible error
- Users must manually retry operations, creating frustration
- Success rates are artificially low due to unhandled temporary issues
- No protection against overwhelming recovering services
- Cascading failures when multiple dependencies struggle simultaneously
- Higher operational burden as humans manually retry failed operations
- Poor user experience from brittleness in face of normal distributed system behavior
- Difficult debugging without understanding which failures are recurring vs. transient

## Practical Checklist
Before deploying retry logic:
- [ ] Have you classified which errors are transient vs. permanent?
- [ ] Is exponential backoff implemented with appropriate initial delay and cap?
- [ ] Is jitter added to backoff delays to prevent thundering herd?
- [ ] Are maximum retry counts enforced (typically 3-5 attempts)?
- [ ] Do you handle idempotency for non-idempotent operations?
- [ ] Are circuit breakers protecting frequently-failing dependencies?
- [ ] Is retry status communicated to users for long operations?
- [ ] Are retries logged with sufficient context for debugging?
- [ ] Do you have absolute timeout limits beyond retry logic?
- [ ] Are retry rates monitored and alerted on when abnormally high?
- [ ] Does exhausted retry logic provide useful next steps to users?
- [ ] Have you tested retry behavior under various failure scenarios?
- [ ] Are you tracking success rate by attempt number (1st, 2nd, 3rd)?

## Watch Out For
⚠️ **Retry Storms** - When many agents fail simultaneously and retry in synchronization, creating load spikes that prevent recovery. Mitigate with jitter and circuit breakers. Synchronized retries can make problems worse, not better.

⚠️ **Retrying Permanent Failures** - Wasting retries on errors that won't resolve (bad input, authorization failures) delays user feedback and costs money. Classify errors accurately—only retry transient failures. Log classification mistakes and refine over time.

⚠️ **No Maximum Limits** - Retrying indefinitely creates infinite loops, wastes resources, and delays necessary escalation. Always implement maximum retry counts and absolute timeouts. Persistence becomes stubbornness without limits.

⚠️ **Immediate Retry Without Backoff** - Retrying instantly after failure doesn't give systems time to recover and can overwhelm struggling services. Always use backoff—even 1 second is better than immediate. Fast retries often waste all attempts before transient issues resolve.

⚠️ **Ignoring Idempotency** - Retrying non-idempotent operations without idempotency keys creates duplicates: double charges, duplicate records, repeated actions. Use idempotency keys or check previous attempt results before retrying non-idempotent operations.

⚠️ **Silent Retries on Non-Transient Issues** - If retries consistently succeed only after multiple attempts, you're masking a systemic problem. Monitor retry patterns—frequent retries indicate underlying issues requiring investigation and fixing.

## Connections
**Builds On:** 
- [Error Handling](error_handling.md) - Retry logic is a specific error handling strategy
- [Deterministic Controls](deterministic_controls.md) - Retry limits act as deterministic bounds

**Works With:** 
- [Fallback Strategy](fallback_strategy.md) - Fallbacks activate when retries exhaust
- [Circuit Breakers](../../Software_Engineering/) - Circuit breakers determine when to stop retrying
- [Rate Limiting](../../Performance_and_Cost/) - Rate limits often trigger retry logic
- [Observability](../../MLOps/) - Monitoring retry patterns reveals system health

**Leads To:** 
- [Resilience Engineering](../../Infrastructure_and_DevOps/) - Retry logic is one resilience pattern among many
- [Chaos Engineering](../../Testing_and_Evaluation/) - Testing retry behavior through fault injection
- [Service Reliability](../../Cloud_and_Distributed/) - Retries contribute to overall service reliability
- [Cost Optimization](../../Performance_and_Cost/) - Smart retry policies reduce unnecessary API costs

## Quick Decision Guide
**Implement retry logic when:** Calling external APIs or services, accessing databases over networks, performing operations prone to transient failures (network I/O, distributed systems), or building production systems where user experience matters and manual retry is unacceptable.

**Skip retry logic when:** Operations are guaranteed idempotent and fast (local function calls, in-memory operations), failures are always permanent (input validation, authentication), or you're prototyping and complexity isn't yet justified.

## Further Exploration
- 📖 **"Release It!" by Michael Nygard** - Comprehensive coverage of retry patterns, circuit breakers, and stability patterns
- 🎯 **Implement Exponential Backoff** - Add retry logic to an API call. Measure: success rate by attempt, average completion time, retry percentage. Tune backoff parameters based on data
- 💡 **Tenacity Library (Python)** - Study production-ready retry library: backoff strategies, stop conditions, retry predicates, before/after hooks
- 📖 **AWS SDK Retry Strategy** - Examine AWS's adaptive retry mode: automatically adjusts retry behavior based on service health and request types
- 🎯 **Test Failure Scenarios** - Use chaos engineering to inject failures: network latency, timeouts, rate limits. Verify retry logic handles gracefully and succeeds when possible
- 💡 **Polly Library (.NET)** - Study retry policies, circuit breakers, bulkhead isolation. See how established libraries structure retry logic
- 📖 **"Designing Data-Intensive Applications" by Martin Kleppmann** - Sections on handling failures in distributed systems, idempotency, and retry safety

---
*Added: May 15, 2026 | Updated: May 15, 2026 | Confidence: High*
