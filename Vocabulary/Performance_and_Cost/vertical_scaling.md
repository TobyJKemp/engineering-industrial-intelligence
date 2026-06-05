# Vertical Scaling

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Infrastructure |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Cloud computing basics, understanding of instance types and resource allocation |

## One-Sentence Summary
Vertical scaling (scaling up) means increasing the compute resources—CPU, memory, GPU VRAM—of a single instance to handle more load, rather than adding more instances.

## Why This Matters to You
Many AI workloads don't scale horizontally without significant architectural effort—a single large language model may require all its weights in one GPU's VRAM, a stateful process may require a specific memory footprint, or a database primary needs more power before read replicas can help. Vertical scaling is often the fastest and simplest path to immediate capacity relief. Understanding when it works well and when it hits a wall is essential for efficient infrastructure decision-making.

## The Core Idea
### What It Is
Vertical scaling increases the size of an individual resource:
- **CPU:** Moving from a 4-core to 16-core instance
- **Memory (RAM):** Moving from 16GB to 64GB RAM for a memory-intensive workload
- **GPU VRAM:** Moving from a V100 (16GB) to an A100 (80GB) to fit a larger model in memory
- **Storage IOPS:** Upgrading disk tier for I/O-bound database workloads
- **Network bandwidth:** Moving to a higher-bandwidth instance type for data-intensive transfers

In cloud environments, vertical scaling is typically implemented by:
1. Stopping the instance
2. Changing its instance type to a larger one
3. Restarting

Some cloud services support live vertical scaling (e.g., adjusting ECS task CPU/memory, Kubernetes vertical pod autoscaling) without full restarts.

**When vertical scaling is preferred:**
- **Stateful workloads:** Databases, caches, and stateful processes often can't run as multiple equal instances without complex partitioning
- **Model fitting:** A model that requires 40GB VRAM must run on a single GPU with at least that capacity—no amount of horizontal scaling solves an insufficient VRAM problem
- **Simplicity:** Vertical scaling requires no application changes and is easier to reason about than distributed systems
- **Low traffic, high compute:** Small-scale high-compute jobs (training runs, batch inference on one machine) are often better suited to a single large instance than a distributed setup

### What It Isn't
Vertical scaling is not infinitely elastic. Every cloud provider has a maximum instance size. Beyond that ceiling, only horizontal scaling (or specialized multi-GPU distributed systems) can provide more capacity. Vertical scaling also doesn't improve availability—a larger single instance fails just as completely as a smaller one; it's just less likely to be overloaded.

## How It Works
1. **Identify the resource constraint:** Profiling reveals whether CPU, memory, VRAM, or I/O is the limiting factor.
2. **Choose the next tier:** Select the instance type that adds the needed resource while minimizing waste on unused dimensions.
3. **Estimate performance improvement:** Verify that the bottleneck is the resource you're scaling, not another factor (e.g., scaling CPU on a memory-bound workload won't help).
4. **Execute the resize:** Stop the workload, resize the instance, restart, and validate.
5. **Monitor post-resize:** Confirm the bottleneck has been resolved and utilization is now at a healthy level on the new instance size.
6. **Set a ceiling:** Know the maximum vertical scale available and plan horizontal scaling architecture before you hit it.

## Think of It Like This
Upgrading vertical scaling is like moving from a studio apartment to a 3-bedroom—you're giving a single person (process) more space to work in. That same person can do more now because they aren't cramped. But no matter how big the apartment gets, eventually there's a maximum size in the building (instance type ceiling). If you need to accommodate a whole team, you eventually need multiple apartments (horizontal scaling) rather than a single ever-larger one.

## The "So What?" Factor
**If you use this:**
- Immediate capacity relief is available without application code changes for stateful or hard-to-distribute workloads
- Model serving becomes possible as models grow larger—VRAM scaling is often the only solution for large models
- Simple workloads remain simple rather than incurring distributed systems complexity prematurely

**If you don't:**
- Hitting resource limits (OOM, CPU saturation) causes crashes and degraded performance without an obvious remedy
- Large model inference is impossible without adequate VRAM, making model selection constrained by hardware
- Performance problems that are actually resource exhaustion get misdiagnosed as application bugs

## Practical Checklist
Before vertically scaling, ask yourself:
- [ ] Have I profiled to confirm which specific resource is the constraint?
- [ ] Is the bottleneck the resource I'm planning to scale (not something else)?
- [ ] What is the maximum instance size available for this workload? (Know the ceiling)
- [ ] Will vertical scaling require downtime? If so, can it be scheduled?
- [ ] Is the cost of the larger instance justified by the performance or capability gain?
- [ ] Is this a temporary measure, or do I need to plan horizontal scaling architecture for the long term?

## Watch Out For
⚠️ **Hitting the ceiling:** Every cloud instance type has a maximum size. When you reach it, vertical scaling is exhausted—plan horizontal scaling architecture before you're forced to.
⚠️ **Scaling the wrong resource:** Adding RAM when the bottleneck is CPU (or vice versa) wastes money and produces no improvement. Profile first.
⚠️ **Downtime during resize:** Most vertical scaling operations require an instance restart. Plan for maintenance windows and drain traffic gracefully.
⚠️ **Over-scaling:** Jumping from a $100/month instance to a $1000/month instance for marginal gains wastes budget that could fund horizontal scale or other optimizations. Size incrementally.

## Connections
**Builds On:** [Cloud Computing](../Cloud_and_Distributed/cloud_computing.md), [Bottleneck](bottleneck.md)
**Works With:** [Horizontal Scaling](horizontal_scaling.md), [Auto Scaling](auto_scaling.md), [Right Sizing](right_sizing.md), [Capacity Planning](capacity_planning.md)
**Leads To:** [Horizontal Scaling](horizontal_scaling.md), [Cost Optimization](cost_optimization.md)

## Quick Decision Guide
**Use this when you need to:** Provide more resources to a stateful workload, fit a larger model in VRAM, or resolve resource exhaustion quickly without application refactoring.
**Skip this when:** The workload is stateless and can be distributed horizontally, or you've already reached the maximum instance size for the cloud service.

## Further Exploration
- 📖 [AWS EC2 instance types and sizing guide](https://aws.amazon.com/ec2/instance-types/)
- 🎯 [Kubernetes Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)
- 💡 [GPU instance selection for LLM inference (NVIDIA)](https://developer.nvidia.com/blog/selecting-the-right-nvidia-gpu-for-large-language-model-inference/)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
