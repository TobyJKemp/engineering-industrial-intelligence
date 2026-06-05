# Latency

## At a Glance
| | |
|---|---|
| **Category** | Concept / Performance Engineering |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for concepts, ongoing for measurement and optimization |
| **Prerequisites** | Basic understanding of how requests travel through a system |

## One-Sentence Summary
Latency is the time elapsed between initiating a request and receiving its response—the delay that users and downstream systems experience while waiting for an operation to complete.

## Why This Matters to You
In AI systems, latency is often the primary user-facing performance metric. An LLM that produces a brilliant response in 30 seconds may still feel unusable compared to one that produces a good response in 2 seconds. Streaming, caching, batching, and model selection decisions all fundamentally come down to latency management. If you're building or evaluating AI-powered products, understanding latency at each stage of your pipeline is essential to delivering good user and agent experiences.

## The Core Idea
### What It Is
Latency measures delay, not speed or capacity. It answers the question: "How long does this take?"

Key latency concepts in AI systems:

**Time to First Token (TTFT):** For generative AI systems, how long until the model starts producing output. Critical for streaming interfaces where users see tokens appear progressively.

**Time to Last Token (TTLT):** Total end-to-end time from request to complete response. Relevant for synchronous, non-streaming use cases.

**P50 / P95 / P99 Latency:** Percentile-based measurements that characterize the distribution:
- P50 (median): 50% of requests complete faster than this
- P95: 95% complete faster—the typical "tail latency"
- P99: 99% complete faster—the worst-case experience most users encounter

Always measure P95 and P99, not just average. The average hides the tail, and the tail is where user complaints come from.

**Latency components in an AI pipeline:**
- Network round-trip time
- Queue wait time (if request is queued before processing)
- Model loading time (on cold starts)
- Model inference time (dominant for large models)
- Post-processing and serialization time

### What It Isn't
Latency is not throughput. High throughput doesn't mean low latency, and vice versa. A system can process millions of requests per day (high throughput) while each individual request waits minutes (high latency). They measure different things. See [Throughput](throughput.md) for the complementary concept.

## How It Works
1. **Measure baseline:** Add timing instrumentation at the entry and exit points of each significant stage. Use distributed tracing (OpenTelemetry) for multi-service systems.
2. **Characterize distribution:** Compute P50, P95, P99 across a representative traffic sample—not averages.
3. **Identify dominant contributors:** Break down end-to-end latency into components. Usually, one stage dominates (model inference, a slow DB query, network hop).
4. **Optimize the critical path:** Focus on the highest-latency stage. Options include caching, model quantization, hardware acceleration, connection pooling, or architectural redesign.
5. **Set SLOs:** Define latency Service Level Objectives (e.g., P95 < 2s) to create a measurable target and detect regressions.
6. **Monitor continuously:** Latency regressions often occur after deployments. Continuous monitoring catches them before users file complaints.

## Think of It Like This
Think of ordering food at a restaurant. Latency is the time between placing your order and receiving your meal. It doesn't matter how many other tables are being served (throughput)—your experience is determined entirely by your wait time. A restaurant that serves 200 tables per night but makes each table wait 90 minutes has a throughput advantage and a latency problem.

## The "So What?" Factor
**If you use this:**
- AI systems are tuned to meet response time expectations for their use case (real-time chat vs. batch analysis vs. background processing)
- Latency budgets are allocated across pipeline stages, preventing any one component from degrading the full experience
- Regressions are caught early through continuous latency monitoring

**If you don't:**
- Slow responses degrade user experience without clear signal on where the delay is occurring
- Debugging performance problems is reactive and slow
- AI agents that chain multiple operations accumulate latency unpredictably

## Practical Checklist
Before deploying an AI service, ask yourself:
- [ ] What is the user's acceptable wait time for this use case?
- [ ] Have I measured latency at P50, P95, and P99—not just average?
- [ ] Which stage of the pipeline contributes the most to end-to-end latency?
- [ ] For generative AI: have I measured Time to First Token separately from total response time?
- [ ] Have I set an SLO that will alert on latency regression?
- [ ] Have I tested latency under realistic concurrent load, not just sequential single requests?

## Watch Out For
⚠️ **Averaging latency:** Averages mask tail latency. The user at P99 has the worst experience and is the most likely to churn. Always track percentiles.
⚠️ **Ignoring queue latency:** Under load, requests often wait in a queue before processing begins. Queue wait time can dominate total latency at high concurrency.
⚠️ **Cold starts in serverless and container workloads:** A cold start (loading model weights, initializing containers) can add seconds of latency for the first request on a new instance. Design for warm instances on critical paths.
⚠️ **Latency budget erosion in multi-hop systems:** An AI agent that calls 5 services, each with 200ms P95 latency, has a 1000ms aggregate P95—before any of those services have a bad day.

## Connections
**Builds On:** [Throughput](throughput.md)
**Works With:** [Bottleneck](bottleneck.md), [Caching Strategy](caching_strategy.md), [Performance Tuning](performance_tuning.md), [Profiling](profiling.md)
**Leads To:** [Auto Scaling](auto_scaling.md), [Capacity Planning](capacity_planning.md), [Token Economics](token_economics.md)

## Quick Decision Guide
**Use this when you need to:** Understand user-facing delay, design SLOs, identify performance bottlenecks, or compare architectural options for time-sensitive workloads.
**Skip this when:** The workload is pure batch processing with no user-facing time constraint—in that case, throughput and cost are the primary metrics.

## Further Exploration
- 📖 [Latency Numbers Every Programmer Should Know (Jeff Dean)](https://colin-scott.github.io/personal_website/research/interactive_latency.html)
- 🎯 [OpenTelemetry tracing quickstart](https://opentelemetry.io/docs/getting-started/)
- 💡 [The USE and RED methods for latency analysis (Brendan Gregg)](https://www.brendangregg.com/usemethod.html)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
