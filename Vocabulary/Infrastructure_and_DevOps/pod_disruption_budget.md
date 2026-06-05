
# Pod Disruption Budget (PDB)

## At a Glance
| | |
|---|---|
| **Category** | Kubernetes Availability / Reliability |
| **Complexity** | Intermediate |
| **Time to Learn** | 1 hour |
| **Prerequisites** | Kubernetes basics, deployments, scaling |

## One-Sentence Summary
A Pod Disruption Budget (PDB) in Kubernetes defines the minimum number or percentage of pods that must remain available during voluntary disruptions, ensuring application reliability during maintenance or upgrades.

## Why This Matters to You
PDBs protect your applications from excessive downtime during planned operations (like node upgrades or scaling). In 2026, PDBs are a best practice for all critical workloads, helping maintain service levels and user experience.

## The Core Idea
### What It Is
A PDB is a Kubernetes resource that specifies how many pods in a deployment, stateful set, or replica set must be available at all times. Kubernetes uses this to control the rate of voluntary disruptions (e.g., draining nodes, rolling updates).

### What It Isn't
PDBs do not prevent involuntary disruptions (e.g., node crashes). They don’t guarantee zero downtime—just a minimum level of availability during planned changes.

## How It Works
1. Define a PDB with minAvailable or maxUnavailable for a set of pods.
2. Kubernetes enforces the budget during voluntary disruptions.
3. If the budget would be violated, the disruption is blocked until enough pods are available.

## Think of It Like This
A PDB is like a rule that says, “At least 3 cashiers must be open at all times”—even during shift changes, the store keeps running.

## The "So What?" Factor
**If you use this:**
- You maintain application availability during maintenance
- You reduce risk of outages from planned operations
- You improve reliability and user trust

**If you don't:**
- Maintenance can cause unexpected downtime
- Users may experience service interruptions
- Harder to meet SLAs and reliability goals

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are critical workloads protected by PDBs?
- [ ] Are budgets tuned for scaling and maintenance needs?
- [ ] Are disruptions monitored and logged?

## Watch Out For
⚠️ Setting budgets too high—can block necessary maintenance
⚠️ Not updating PDBs as workloads scale

## Connections
**Builds On:** Kubernetes, deployments, scaling
**Works With:** Node draining, rolling updates, monitoring
**Leads To:** High availability, reliability engineering

## Quick Decision Guide
**Use this when you need to:** Maintain availability during planned disruptions
**Skip this when:** Workloads are non-critical or short-lived

## Further Exploration
- 📖 [Kubernetes Pod Disruption Budgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
- 🎯 [PDB Best Practices](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-pod-disruption/)

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*
