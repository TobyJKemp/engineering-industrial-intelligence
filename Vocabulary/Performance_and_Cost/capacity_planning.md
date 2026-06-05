# Capacity Planning

## At a Glance
| | |
|---|---|
| **Category** | Practice / Infrastructure Management |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 hours for concepts and frameworks, weeks to develop instincts |
| **Prerequisites** | Understanding of throughput, latency, scaling, and basic cloud cost models |

## One-Sentence Summary
Capacity planning is the discipline of forecasting future resource needs—compute, memory, storage, network—and ensuring those resources are available before demand exceeds supply.

## Why This Matters to You
AI workloads are uniquely challenging to capacity-plan: model inference is compute-intensive, training is GPU-hungry, and traffic can spike dramatically with product launches or viral events. Without capacity planning, you discover you've run out of GPU quota in the middle of a launch, or you're paying 3x more than needed because you provisioned for peak loads that occur 2% of the time. Getting this right saves significant money and prevents operational failures.

## The Core Idea
### What It Is
Capacity planning bridges the gap between current resource state and future demand. It answers three questions:
1. **What do I have?** Current inventory of resources and their utilization.
2. **What will I need?** Projected demand growth from user growth, feature expansion, or new workloads.
3. **When will I run out?** The point at which current capacity is exhausted, which is the deadline for procurement or scaling action.

The process draws on:
- **Utilization data:** Historical CPU, memory, GPU, and storage metrics to understand current headroom
- **Growth models:** Linear, exponential, or seasonal projections of traffic and usage
- **Load testing results:** Measured system behavior under specific traffic volumes
- **Business forecasts:** Planned marketing campaigns, feature launches, user acquisition targets

For AI systems, capacity planning must also account for model-specific resource profiles: a larger model may require 4x the GPU memory, a batch inference job may saturate a GPU for hours, and embedding generation at scale has very different compute profiles than autoregressive generation.

### What It Isn't
Capacity planning is not a one-time exercise. It's a recurring practice, typically revisited quarterly or when significant business events are planned. It's also not the same as auto scaling—auto scaling reacts to demand in real time, while capacity planning ensures the infrastructure ceiling is high enough that auto scaling has room to operate.

## How It Works
1. **Baseline:** Measure current resource utilization at representative load. Identify peak, average, and trough patterns.
2. **Model growth:** Estimate how demand will change over the planning horizon (3, 6, 12 months). Use historical growth rates, product roadmaps, and business plans.
3. **Project exhaustion:** Apply growth model to current capacity. Identify when utilization will exceed safe operating levels (typically 70-80% to leave headroom).
4. **Design for headroom:** Plan target utilization levels that allow for unexpected spikes without hitting hard limits.
5. **Procure or provision:** For cloud resources, request quota increases. For reserved or dedicated resources, purchase commitments with appropriate lead times.
6. **Review and iterate:** Revisit projections as actual growth deviates from forecasts.

## Think of It Like This
A city civil engineer planning water infrastructure doesn't wait for the city's population to exhaust the current reservoir before building a new one. They track current consumption, model population growth, calculate when the reservoir will run dry, and begin construction years in advance—because building a reservoir takes time. Capacity planning is the engineering practice of ensuring you're never caught without water.

## The "So What?" Factor
**If you use this:**
- Infrastructure is ready before demand hits, not scrambled into place after the fact
- Reserved instance or committed use discounts are captured, cutting costs significantly vs. on-demand pricing
- Teams can make confident product and launch commitments knowing infrastructure can support them

**If you don't:**
- Resource exhaustion causes production outages or throttling at the worst possible moment (a product launch)
- Reactive provisioning relies on expensive on-demand pricing with no time for optimization
- GPU quota requests that take days or weeks cause launch delays

## Practical Checklist
Before a product launch or planning cycle, ask yourself:
- [ ] What is current utilization at representative load?
- [ ] What is the expected growth rate over the planning horizon?
- [ ] At current growth, when will utilization exceed 70-80% of capacity?
- [ ] Are there any upcoming events (launches, marketing campaigns) that will cause step-change demand increases?
- [ ] What is the procurement lead time for additional capacity? (GPU reservations can have weeks of lead time)
- [ ] Have I accounted for peak-to-average ratios in my models?
- [ ] Is auto scaling enabled to handle intra-day variability within the planned capacity ceiling?

## Watch Out For
⚠️ **Planning for average, not peak:** Averages hide the spikes that cause outages. Always model peak utilization, not average utilization.
⚠️ **Ignoring AI-specific resource profiles:** LLM inference memory requirements grow non-linearly with model size and context length. Plan separately for GPU memory, not just compute.
⚠️ **Static planning in dynamic environments:** A plan made in January may be irrelevant by March if a product launch or viral event changes the growth curve. Revisit frequently.
⚠️ **Underpurchasing reserved capacity:** Reserving too little to avoid risk means paying on-demand prices for baseline workloads that run 24/7—the most expensive way to run predictable load.

## Connections
**Builds On:** [Throughput](throughput.md), [Latency](latency.md), [Bottleneck](bottleneck.md)
**Works With:** [Auto Scaling](auto_scaling.md), [Reserved Instance](reserved_instance.md), [Right Sizing](right_sizing.md), [Cost Optimization](cost_optimization.md), [Horizontal Scaling](horizontal_scaling.md), [Vertical Scaling](vertical_scaling.md)
**Leads To:** [Cost Optimization](cost_optimization.md), [Resource Tagging](resource_tagging.md)

## Quick Decision Guide
**Use this when you need to:** Prepare for a product launch, quarterly growth, or any event that may significantly increase resource demand.
**Skip this when:** You're early-stage with no meaningful traffic and auto scaling is sufficient to handle all variability without hitting quota limits.

## Further Exploration
- 📖 [Site Reliability Engineering, Chapter 23 – Managing Critical State (Google)](https://sre.google/sre-book/managing-critical-state/)
- 🎯 [AWS Compute Optimizer for right-sizing and capacity analysis](https://aws.amazon.com/compute-optimizer/)
- 💡 [Capacity Planning for Web Performance (O'Reilly)](https://www.oreilly.com/library/view/capacity-planning-for/9780596518578/)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
