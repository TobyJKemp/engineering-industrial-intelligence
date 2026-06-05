# Liveness Probe

## At a Glance
| | |
|---|---|
| **Category** | Kubernetes Health Check |
| **Complexity** | Beginner |
| **Time to Learn** | 30 minutes |
| **Prerequisites** | Kubernetes basics, container health |

## One-Sentence Summary
A liveness probe is a Kubernetes mechanism that checks if a container is running as expected, enabling automatic restarts of unhealthy containers to maintain application reliability.

## Why This Matters to You
Liveness probes are critical for self-healing in Kubernetes. They detect when an application is stuck or unresponsive and trigger restarts, reducing downtime and manual intervention. In 2026, robust liveness probes are a best practice for all production workloads.

## The Core Idea
### What It Is
A liveness probe is a periodic check (HTTP, TCP, or command) defined in a Pod spec. If the probe fails, Kubernetes restarts the container. This ensures that transient or permanent failures don’t require human intervention.

### What It Isn't
Liveness probes are not for readiness (whether a service is ready to receive traffic)—that’s what readiness probes are for. They’re not a replacement for application-level monitoring or logging.

## How It Works
1. Define a liveness probe in your Pod spec (e.g., HTTP GET `/healthz`).
2. Kubernetes runs the probe at intervals.
3. If the probe fails repeatedly, the container is restarted automatically.

## Think of It Like This
A liveness probe is like a nurse checking a patient’s pulse—if there’s no response, action is taken to revive the patient.

## The "So What?" Factor
**If you use this:**
- Your apps recover from hangs and deadlocks automatically
- You reduce downtime and manual restarts
- You improve reliability and user experience

**If you don't:**
- Stuck containers can cause outages and degraded service
- Manual intervention is needed to restore service
- You risk longer recovery times and customer impact

## Practical Checklist
Before implementing, ask yourself:
- [ ] Does my app have a reliable health endpoint or check?
- [ ] Are probe intervals and thresholds tuned for my workload?
- [ ] Are failures logged and monitored?

## Watch Out For
⚠️ Misconfigured probes—can cause unnecessary restarts
⚠️ Using liveness for readiness—can disrupt rolling updates

## Connections
**Builds On:** Kubernetes, containers, health checks
**Works With:** Readiness probes, monitoring, alerting
**Leads To:** Self-healing systems, automated recovery

## Quick Decision Guide
**Use this when you need to:** Ensure containers are running and recover from failures automatically
**Skip this when:** Your workload is short-lived or managed outside Kubernetes

## Further Exploration
- 📖 [Kubernetes Liveness and Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- 🎯 [Best Practices for Probes](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-pod-health/)

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*
