# Horizontal Scaling

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Infrastructure |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts, days to implement well |
| **Prerequisites** | Cloud computing basics, load balancing, statelessness concepts |

## One-Sentence Summary
Horizontal scaling (scaling out) means adding more instances of a service to distribute load across multiple nodes, rather than making a single node larger.

## Why This Matters to You
Most AI serving infrastructure—APIs, inference endpoints, embedding services—is designed to scale horizontally. When request volume grows, you add more instances of the service behind a load balancer. This is the dominant scaling model in modern cloud-native systems because it provides linear capacity growth, geographic distribution, and resilience through redundancy. Understanding when and how to scale horizontally vs. vertically is fundamental to building reliable AI systems.

## The Core Idea
### What It Is
Horizontal scaling adds more instances of the same service type to increase total capacity. If one inference server handles 100 requests/second, adding a second brings total capacity to 200 requests/second, a third to 300, and so on.

The key requirements for effective horizontal scaling:
- **Stateless services:** Each instance must be able to handle any request independently, without depending on local state from a previous request. State is stored externally (database, cache, object storage).
- **Load distribution:** A load balancer sits in front of the instances and routes incoming requests across them.
- **Health checking:** The load balancer must detect and route around unhealthy instances automatically.
- **Identical instances:** All instances run the same code and configuration, making them interchangeable.

Horizontal scaling is also the basis for high availability—running multiple instances means the system survives individual instance failures without downtime.

### What It Isn't
Horizontal scaling is not always the right answer. Services with hard state (e.g., a single database with a primary node) don't scale horizontally without architectural changes (sharding, read replicas). It's also not free—managing a fleet of instances adds operational complexity compared to a single large server. For some workloads, vertical scaling is simpler and equally effective.

## How It Works
1. **Stateless design:** Ensure the service stores no local state between requests. Session state, user data, and computation results go into shared storage.
2. **Containerize:** Package the service in a container (Docker) to make instances identical and deployable anywhere.
3. **Deploy multiple instances:** Use an orchestrator (Kubernetes, ECS) to run multiple replicas of the container.
4. **Load balance:** Route incoming traffic across all healthy instances using a load balancer.
5. **Auto scale:** Configure auto scaling policies to add or remove instances based on demand metrics.
6. **Monitor:** Track per-instance health, error rates, and utilization to detect anomalies.

## Think of It Like This
A coffee shop with one barista has a maximum throughput of one drink per 3 minutes. When the morning rush comes, hiring more baristas scales horizontally—the throughput doubles with each addition. The coffee shop doesn't need a single superhuman barista (vertical scaling); it needs a team of standard baristas working in parallel. The counter (load balancer) directs each customer to the next available barista.

## The "So What?" Factor
**If you use this:**
- Capacity grows linearly with instances—predictable and programmable scaling
- System survives instance failures without downtime (redundancy is inherent)
- Auto scaling can match capacity to demand in real time, controlling costs

**If you don't:**
- Stuck scaling vertically, which hits hardware limits and has diminishing returns
- Single points of failure cause full outages when individual servers crash
- Capacity changes require manual intervention or service restarts

## Practical Checklist
Before horizontally scaling a service, ask yourself:
- [ ] Is the service stateless? (Local state between requests breaks horizontal scaling)
- [ ] Where does session and user state live? (Must be in a shared store, not local memory)
- [ ] Is a load balancer in place to distribute traffic?
- [ ] Are health checks configured so unhealthy instances are automatically removed from rotation?
- [ ] Are all instances configured identically? (Config drift causes inconsistent behavior)
- [ ] How does the database handle increased concurrent connections from more instances?

## Watch Out For
⚠️ **Stateful services masquerading as stateless:** In-memory caches, local file writes, or sticky session assumptions break when multiple instances are deployed.
⚠️ **Database connection explosion:** 10 instances each opening 100 DB connections = 1000 connections. Use a connection pooler (PgBouncer, RDS Proxy) to prevent overwhelming the database.
⚠️ **Config drift:** If instance configurations diverge (different environment variables, different code versions), behavior becomes inconsistent and debugging becomes extremely difficult.
⚠️ **Not enough headroom:** Horizontal scaling has a spin-up delay. If you wait until 100% utilization before scaling, new instances won't be ready before requests start failing.

## Connections
**Builds On:** [Cloud Computing](../Cloud_and_Distributed/cloud_computing.md), [Load Balancer](../Cloud_and_Distributed/load_balancer.md), [Container](../Infrastructure_and_DevOps/container.md)
**Works With:** [Auto Scaling](auto_scaling.md), [Vertical Scaling](vertical_scaling.md), [Kubernetes](../Infrastructure_and_DevOps/kubernetes.md), [High Availability](../Cloud_and_Distributed/high_availability.md), [Service Mesh](../Infrastructure_and_DevOps/service_mesh.md)
**Leads To:** [Capacity Planning](capacity_planning.md), [Cost Optimization](cost_optimization.md)

## Quick Decision Guide
**Use this when you need to:** Increase capacity for stateless services, achieve geographic redundancy, or build resilience through redundant instances.
**Skip this when:** The service has hard stateful requirements that prevent multiple independent instances, or when a single larger instance is simpler and sufficient for the workload.

## Further Exploration
- 📖 [The Twelve-Factor App – Processes (stateless process model)](https://12factor.net/processes)
- 🎯 [Kubernetes Deployments and ReplicaSets walkthrough](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- 💡 [Designing Distributed Systems (Brendan Burns, O'Reilly)](https://www.oreilly.com/library/view/designing-distributed-systems/9781491983638/)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
