# Readiness Probe

## At a Glance
| | |
|---|---|
| **Category** | Kubernetes Health Check |
| **Complexity** | Beginner |
| **Time to Learn** | 30 minutes |
| **Prerequisites** | Kubernetes basics, container health |

## One-Sentence Summary
A readiness probe is a Kubernetes mechanism that checks if a container is ready to accept traffic, ensuring only healthy pods receive requests.

## Why This Matters to You
Readiness probes prevent traffic from being sent to pods that are not yet ready, reducing errors and improving user experience. In 2026, readiness probes are a best practice for all production workloads, especially those with startup delays or dependencies.

## The Core Idea
### What It Is
A readiness probe is a periodic check (HTTP, TCP, or command) defined in a Pod spec. If the probe fails, the pod is removed from service endpoints until it passes.

### What It Isn't
Readiness probes are not for liveness (whether a container is running)—that’s what liveness probes are for. They don’t replace application-level monitoring or alerting.

## How It Works
1. Define a readiness probe in your Pod spec (e.g., HTTP GET `/ready`).
2. Kubernetes runs the probe at intervals.
3. If the probe fails, the pod is marked as not ready and removed from load balancers.

## Think of It Like This
A readiness probe is like a restaurant’s “Open” sign—if it’s not lit, customers (traffic) are not allowed in.

## The "So What?" Factor
**If you use this:**
- You avoid sending traffic to unready or initializing pods
- You reduce user-facing errors during rollouts and restarts
- You improve reliability and deployment safety

**If you don't:**
- Users may hit unready pods, causing errors
- Deployments and scaling are riskier
- Harder to ensure smooth rollouts

## Practical Checklist
Before implementing, ask yourself:
- [ ] Does my app have a reliable readiness check?
- [ ] Are probe intervals and thresholds tuned for my workload?
- [ ] Are failures logged and monitored?

## Watch Out For
⚠️ Misconfigured probes—can cause traffic black holes
⚠️ Using readiness for liveness—can mask failures

## Connections
**Builds On:** Kubernetes, containers, health checks
**Works With:** Liveness probes, load balancers, monitoring
**Leads To:** Safer deployments, improved user experience

## Quick Decision Guide
**Use this when you need to:** Ensure only healthy pods receive traffic
**Skip this when:** Your workload is short-lived or managed outside Kubernetes

## Further Exploration
- 📖 [Kubernetes Liveness and Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- 🎯 [Best Practices for Probes](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-pod-health/)

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*
