# Rolling Deployment

## At a Glance
| | |
|---|---|
| **Category** | Deployment Strategy / DevOps |
| **Complexity** | Intermediate |
| **Time to Learn** | 1 hour |
| **Prerequisites** | CI/CD, Kubernetes or orchestration basics |

## One-Sentence Summary
A rolling deployment is a strategy for updating applications by incrementally replacing old versions with new ones, ensuring zero or minimal downtime and continuous service availability.

## Why This Matters to You
Rolling deployments are essential for modern, always-on systems. They enable safe, gradual updates, reduce risk, and allow for quick rollback if issues arise. In 2026, rolling deployments are a best practice for cloud-native and microservices architectures.

## The Core Idea
### What It Is
A rolling deployment updates a subset of instances (pods, VMs, containers) at a time, monitoring health before proceeding. This allows users to continue accessing the service while the update progresses.

### What It Isn't
Rolling deployments are not all-or-nothing (like blue/green). They don’t guarantee zero downtime if health checks or rollback are misconfigured. Not a replacement for canary or feature flag strategies.

## How It Works
1. Start with all instances running the old version.
2. Incrementally replace instances with the new version.
3. Monitor health and pause/rollback if issues are detected.

## Think of It Like This
A rolling deployment is like changing tires on a moving car—one at a time, so the car keeps going.

## The "So What?" Factor
**If you use this:**
- You minimize downtime and user disruption
- You can quickly detect and roll back issues
- You enable continuous delivery and rapid iteration

**If you don't:**
- Updates are riskier and more disruptive
- Harder to recover from failed deployments
- Slower release cycles and innovation

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are health checks and monitoring in place?
- [ ] Is rollback automated and tested?
- [ ] Are deployment increments tuned for your workload?

## Watch Out For
⚠️ Misconfigured health checks—can cause unnoticed failures
⚠️ Too large increments—can cause service disruption

## Connections
**Builds On:** CI/CD, orchestration, monitoring
**Works With:** Kubernetes, cloud platforms, blue/green and canary deployments
**Leads To:** Safer, faster releases, continuous delivery

## Quick Decision Guide
**Use this when you need to:** Update applications with minimal downtime and risk
**Skip this when:** You need instant cutover or complex testing (use blue/green or canary)

## Further Exploration
- 📖 [Kubernetes Rolling Updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
- 🎯 [Deployment Strategies](https://learn.microsoft.com/en-us/azure/architecture/framework/devops/deployment-strategies)

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*
