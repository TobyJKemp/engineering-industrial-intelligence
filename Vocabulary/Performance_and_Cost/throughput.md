# Throughput

## At a Glance
| | |
|---|---|
| **Category** | Concept / Performance Engineering |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for concepts, ongoing for measurement and optimization |
| **Prerequisites** | Basic understanding of system components and workload characteristics |

## One-Sentence Summary
Throughput is the amount of work a system completes per unit of time—measuring capacity and efficiency rather than individual request delay.

## Why This Matters to You
AI platforms are often evaluated in terms of throughput: how many inference requests per second can your API serve, how many tokens per second does your model generate, how many training examples per minute does your pipeline process. Throughput determines the economic viability of your system—a model that costs $0.10 per inference at 10 requests/second becomes $0.001 per inference at 1000 requests/second due to GPU amortization. Understanding throughput is fundamental to sizing infrastructure and pricing AI services.

## The Core Idea
### What It Is
Throughput measures the rate of successful work completion through a system. It is expressed in units appropriate to the workload:

- **Web services:** Requests per second (RPS) or queries per second (QPS)
- **LLM inference:** Tokens per second (output tokens generated)
- **Data pipelines:** Records per second, rows per minute
- **Training:** Samples per second, steps per minute
- **Storage:** Bytes per second (read/write bandwidth)

**Throughput vs. Latency:** These measure fundamentally different things and can be optimized independently:
- Latency asks: "How long does *my* request take?"
- Throughput asks: "How many requests can the system handle *in total* per second?"

A system can have high throughput (serving many requests/sec) while individual requests still have high latency. A single-threaded system might have low latency per request but terrible throughput because it can only serve one at a time.

**Little's Law** relates the two mathematically:

$$L = \lambda W$$

Where L is the average number of requests in the system, λ is throughput (arrival rate), and W is average latency. This means: at fixed latency, more throughput requires proportionally more concurrency.

**GPU batch efficiency:** In AI inference, GPU throughput is maximized by batching multiple requests together. A GPU processing a batch of 32 requests doesn't take 32x longer than a single request—it might take 2x longer. The per-request GPU cost drops dramatically with batching, which is why throughput optimization for inference often focuses on batching strategy.

### What It Isn't
Throughput is not the same as speed. A slow but parallel system may have high throughput while each individual unit of work takes a long time. It's also not a fixed property of a system—throughput changes with concurrency, load, and architecture. And it's not the only metric that matters: high throughput with unacceptable latency produces poor user experience.

## How It Works
1. **Measure baseline:** Run load tests that gradually increase concurrent requests to measure throughput at different concurrency levels.
2. **Find the saturation point:** Throughput increases with concurrency up to a point, then plateaus or declines (queuing theory: Little's Law at saturation). The saturation point is the system's effective maximum throughput.
3. **Identify the bottleneck:** At saturation, one component is the constraint. Profile to find it.
4. **Optimize:** Address the bottleneck. Common levers: batching (GPU), parallelism, caching, faster hardware, horizontal scaling.
5. **Re-measure:** Confirm improvement and find the new saturation point.

## Think of It Like This
A highway measures throughput in vehicles per hour. A single-lane road at 60mph might pass 1,200 vehicles per hour. A 4-lane highway at the same speed passes 4,800. Adding lanes is horizontal scaling—it multiplies throughput without changing per-vehicle travel time. A faster speed limit improves both. A bottleneck (an on-ramp merge, a toll booth) reduces the effective throughput regardless of road capacity elsewhere.

## The "So What?" Factor
**If you use this:**
- Infrastructure is sized to handle required traffic volumes with defined headroom
- Economic models for AI inference are grounded in real throughput numbers, not guesses
- Scaling decisions are data-driven: more throughput needed → scale the identified constraint

**If you don't:**
- Infrastructure is sized by feel, leading to over- or under-provisioning
- AI service pricing and unit economics are unknowable
- Capacity planning conversations have no quantitative foundation

## Practical Checklist
Before sizing or pricing an AI service, ask yourself:
- [ ] What is the measured throughput at representative concurrency and batch size?
- [ ] What is the saturation point (maximum throughput before latency degrades unacceptably)?
- [ ] Is GPU batching configured to maximize throughput for inference workloads?
- [ ] Does throughput scale linearly with additional instances (confirming stateless horizontal scalability)?
- [ ] Have I measured throughput under realistic mixed workload, not just identical synthetic requests?
- [ ] Is my SLO expressed in both throughput and latency terms?

## Watch Out For
⚠️ **Throughput cliffs:** Some systems perform well up to a threshold and degrade catastrophically beyond it (connection pool exhaustion, GC pause storms). Always load-test beyond expected peak.
⚠️ **Throughput vs. goodput:** Throughput counts all completed work, including error responses. Goodput counts only successful responses. A system under overload may have high error throughput and low goodput—measuring only throughput can mislead.
⚠️ **Ignoring tail latency at high throughput:** A system with great throughput but P99 latency of 10 seconds is unacceptable for interactive use cases even if the aggregate numbers look fine.
⚠️ **Single-threaded benchmarks:** Testing throughput with a single sequential client measures per-request latency, not throughput. Use concurrent clients in load tests.

## Connections
**Builds On:** [Latency](latency.md)
**Works With:** [Bottleneck](bottleneck.md), [Performance Tuning](performance_tuning.md), [Profiling](profiling.md), [Auto Scaling](auto_scaling.md), [Horizontal Scaling](horizontal_scaling.md)
**Leads To:** [Capacity Planning](capacity_planning.md), [Cost Optimization](cost_optimization.md), [Token Economics](token_economics.md)

## Quick Decision Guide
**Use this when you need to:** Size infrastructure, price AI services, validate that a system can handle required load, or identify where to optimize for capacity.
**Skip this when:** The workload is single-user or so infrequent that per-request latency is the only meaningful metric.

## Further Exploration
- 📖 [Little's Law and queuing theory primer (Wikipedia)](https://en.wikipedia.org/wiki/Little%27s_law)
- 🎯 [k6 load testing tool for measuring throughput](https://k6.io/docs/)
- 💡 [Continuous Batching for LLM inference throughput (Orca paper)](https://www.usenix.org/conference/osdi22/presentation/yu)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
