# Auto Scaling

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Infrastructure |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-4 hours for concepts, days to weeks to tune well |
| **Prerequisites** | Cloud computing basics, containerization concepts, load balancing |

## One-Sentence Summary
Auto scaling automatically adjusts the number of running instances of a service up or down in real time based on demand, so your system handles traffic spikes without waste during quiet periods.

## Why This Matters to You
AI workloads are inherently bursty—inference requests can spike 10x during peak hours and drop to near zero overnight. Without auto scaling, you either overpay for idle compute or you cap out and drop requests during surges. If you're building or operating AI agents, pipelines, or APIs, auto scaling is the mechanism that keeps your system responsive and cost-efficient without constant manual intervention.

## The Core Idea
### What It Is
Auto scaling is a feedback control loop for compute capacity. You define scaling policies—rules that say "add 2 instances when CPU > 70% for 3 minutes" or "scale to zero after 10 minutes of no traffic"—and the platform continuously monitors metrics and executes scaling decisions automatically.

There are two primary axes:
- **Horizontal scaling (scale out/in):** Add or remove instances. This is the dominant model in cloud-native workloads.
- **Vertical scaling (scale up/down):** Increase or decrease resources (CPU, RAM) per instance. Less common in auto scaling because it often requires restarts.

Modern auto scaling also includes **predictive scaling**, which uses historical patterns to pre-warm capacity before expected spikes rather than reacting after the fact.

### What It Isn't
Auto scaling is not a substitute for good architecture. If your application has a bottleneck in a single database or a shared stateful component, adding more instances won't help—it may make things worse. Auto scaling also doesn't guarantee zero latency during scale-up events; there's always a brief lag between a trigger condition and new instances being ready.

## How It Works
1. **Monitoring:** A metrics system continuously collects signals—CPU utilization, memory, request queue depth, custom application metrics (e.g., tokens per second for an LLM API).
2. **Evaluation:** The auto scaler compares current metrics against scaling policy thresholds.
3. **Decision:** When thresholds are breached for a configured duration (to avoid flapping), the scaler decides to add or remove instances.
4. **Execution:** New instances are provisioned, initialized, and registered with the load balancer. Old instances are drained of active connections before termination.
5. **Stabilization:** A cooldown period prevents thrashing—rapid oscillation between scaling decisions.

## Think of It Like This
Imagine a restaurant that hires and releases servers based on how full the dining room is. A sensor counts tables occupied; when it exceeds 80%, a manager calls in two more servers from a standby pool. When occupancy drops below 30% for 20 minutes, two servers finish their shift and go home. The restaurant never overpays for an empty dining room and never fails to seat guests during a rush.

## The "So What?" Factor
**If you use this:**
- AI services remain responsive during unpredictable traffic surges without manual intervention
- Infrastructure costs track actual demand instead of worst-case peaks
- Engineers stop waking up at 3am to manually spin up instances during traffic events

**If you don't:**
- You pay for idle capacity 24/7, or you hard-cap capacity and drop requests at peak load
- Any traffic spike becomes an incident instead of a routine handled event
- Scaling becomes a manual, error-prone, reactive process

## Practical Checklist
Before implementing, ask yourself:
- [ ] What metric best represents load on this service? (CPU, request queue depth, custom metric?)
- [ ] What is the startup time of a new instance? (Determines how aggressively you must pre-scale)
- [ ] Are there stateful components that don't scale horizontally? (Databases, caches, shared queues)
- [ ] Have you set minimum and maximum instance bounds to prevent runaway costs or zero-capacity events?
- [ ] Have you configured cooldown periods to prevent scaling flap?
- [ ] Is there a health check in place so the load balancer doesn't route to unhealthy new instances?

## Watch Out For
⚠️ **Scale-in too fast:** Terminating instances before draining active connections causes dropped requests. Always configure connection draining.
⚠️ **Wrong metric:** Scaling on CPU while the real bottleneck is memory or I/O gives you more useless instances. Pick the metric that actually correlates with user-visible degradation.
⚠️ **Cold start latency:** For AI inference services, loading a model on a fresh instance can take 30-90 seconds. If you don't account for this, auto scaling won't save you from brief latency spikes.
⚠️ **Runaway scaling:** Always set a maximum instance cap. A bug that triggers infinite retries can otherwise cause infinite scale-out and catastrophic cost.

## Connections
**Builds On:** [Cloud Computing](../Cloud_and_Distributed/cloud_computing.md), [Load Balancer](../Cloud_and_Distributed/load_balancer.md), [Horizontal Scaling](horizontal_scaling.md)
**Works With:** [Capacity Planning](capacity_planning.md), [Bottleneck](bottleneck.md), [Health Check](../Infrastructure_and_DevOps/health_check.md), [Kubernetes](../Infrastructure_and_DevOps/kubernetes.md), [Node Pool](../Infrastructure_and_DevOps/node_pool.md)
**Leads To:** [Cost Optimization](cost_optimization.md), [Reserved Instance](reserved_instance.md), [Vertical Scaling](vertical_scaling.md)

## Quick Decision Guide
**Use this when you need to:** Handle variable or unpredictable traffic loads without paying for peak capacity 24/7.
**Skip this when:** Your workload is perfectly predictable and constant, or startup latency is so high that reactive scaling is useless (consider pre-provisioned reserved capacity instead).

## Further Exploration
- 📖 [AWS Auto Scaling concepts](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- 🎯 [Kubernetes Horizontal Pod Autoscaler walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)
- 💡 [KEDA: Kubernetes-based Event Driven Autoscaling for AI workloads](https://keda.sh/)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
