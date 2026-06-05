# Circuit Breaker

## At a Glance
| | |
|---|---|
| **Category** | Reliability Pattern / Fault Tolerance |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-4 hours for concept, days to implement robustly |
| **Prerequisites** | Error handling, retry logic, distributed systems basics |

## One-Sentence Summary
A Circuit Breaker is a design pattern that prevents a system from repeatedly attempting operations likely to fail—such as calling an unavailable service—by "opening the circuit" after a threshold of failures, temporarily blocking further attempts and allowing the system to recover, thus transforming cascading failures and resource exhaustion into controlled, self-healing behavior.

## Why This Matters to You
In distributed AI agent systems, dependencies (APIs, databases, external services) can become slow or unavailable. Without a circuit breaker, your agent keeps retrying failed operations, overwhelming the dependency and your own system—leading to retry storms, increased latency, and system-wide outages. With a circuit breaker, after a set number of failures, the system stops making requests for a cooldown period, giving the dependency time to recover and preventing further damage. This pattern is essential for building resilient, production-grade agent systems that can withstand partial failures and recover gracefully.

## The Core Idea
### What It Is
A circuit breaker monitors the success and failure rates of operations. When failures exceed a threshold, it "opens" the circuit, blocking further attempts for a set period. After the cooldown, it enters a "half-open" state, allowing a limited number of test requests. If these succeed, the circuit "closes" and normal operation resumes; if not, it reopens. This prevents repeated failures from overwhelming systems and enables self-healing.

**States:**
- **Closed:** Normal operation; all requests pass through.
- **Open:** Requests are blocked immediately; system returns error or fallback.
- **Half-Open:** Limited requests allowed to test if dependency has recovered.

**Key Parameters:**
- Failure threshold (number or percentage of failures before opening)
- Cooldown period (how long to stay open)
- Success threshold (number of successful requests to close circuit)

**Implementation:**
- Track recent operation outcomes (success/failure)
- On threshold breach, open circuit and start cooldown timer
- After cooldown, allow test requests (half-open)
- If test requests succeed, close circuit; if not, reopen

**Example:**
If an LLM API fails 5 times in a row, the circuit breaker opens for 60 seconds. During this time, all requests fail fast (no API call). After 60 seconds, one request is allowed through. If it succeeds, the circuit closes; if not, it reopens for another cooldown.

## Analogy
Think of a household circuit breaker: if too much current flows (overload), the breaker trips, cutting power to prevent fire. After cooling down, you can reset it. Similarly, a software circuit breaker "trips" on repeated failures, blocking requests to prevent system overload, and resets after a cooldown.

## Checklist
- [x] Monitor operation outcomes (success/failure)
- [x] Define failure and success thresholds
- [x] Implement open, closed, and half-open states
- [x] Block requests when open; allow limited requests when half-open
- [x] Log state transitions and failures
- [x] Integrate with retry and fallback logic

## Common Pitfalls
- Setting thresholds too low (circuit opens on minor blips)
- Setting cooldown too short (dependency not recovered)
- Not logging state transitions (hard to debug)
- Not integrating with fallback (users see errors instead of degraded service)
- Forgetting to reset after recovery

## Watch Out For

⚠️ **Thresholds set too low:** Circuit opens on minor fluctuations.
⚠️ **Cooldown period too short:** Dependency doesn't have time to recover.
⚠️ **Not logging state transitions:** Hard to debug when circuit opened unexpectedly.
⚠️ **No integration with fallback:** Users see errors instead of degraded service.
⚠️ **Stuck in open state:** Circuit never resets after dependency recovers.

## Practical Checklist

Before implementing circuit breaker:
- [ ] Have you defined failure threshold (count or percentage)?
- [ ] Is cooldown period appropriate for your dependencies?
- [ ] Are open, closed, and half-open states implemented?
- [ ] Do blocked requests fail fast without retrying?
- [ ] Are limited test requests allowed in half-open state?
- [ ] Is there fallback behavior when circuit is open?
- [ ] Are state transitions logged?
- [ ] Can you monitor circuit state and transitions?
- [ ] Is circuit breaker integrated with retry logic?
- [ ] Can you manually reset circuit if needed?
- [ ] Are thresholds tuned based on actual failure patterns?
- [ ] Have you tested recovery scenarios?

## Connections
- [Retry Logic](retry_logic.md)
- [Fallback Strategy](fallback_strategy.md)
- [Error Handling](error_handling.md)
- [Monitoring](monitoring.md)
- [Observability](observability.md)

## Further Exploration

- 📖 **"Release It!" by Michael Nygard** — production-ready design patterns
- 📖 **"Designing Data-Intensive Applications" by Martin Kleppmann** — resilience patterns
- 🎯 **Circuit Breaker Configuration Tuning Guide** — threshold and cooldown settings
- 💡 **Case Study: Graceful Degradation** — circuit breaker prevented cascade
- 💡 **Case Study: Broken Circuit** — circuit breaker misconfigured or stuck

---
*Added: June 2, 2026 | Updated: June 2, 2026 | Confidence: High*
