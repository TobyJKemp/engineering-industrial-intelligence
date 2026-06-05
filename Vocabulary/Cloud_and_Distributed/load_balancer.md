# Load Balancer

## At a Glance
| | |
|---|---|
| **Category** | Technique |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Networking, distributed systems |

## One-Sentence Summary
A load balancer distributes network or application traffic across multiple servers to optimize resource use and maximize uptime.

## Why This Matters to You
Load balancers prevent overload on any single server, improve reliability, and enable seamless failover and maintenance. They are essential for scaling web applications and microservices.

## The Core Idea
### What It Is
Load balancers use algorithms (round-robin, least connections, etc.) to route requests. They can operate at different layers (L4, L7) and support health checks, SSL termination, and session persistence. Common in cloud, web, and microservices architectures.

### What It Isn't
It is not a replacement for application-level error handling or redundancy. It is not a security device, though it can help absorb some attacks.

## How It Works
1. Accept incoming requests.
2. Select a healthy backend server.
3. Forward the request and return the response.

## Think of It Like This
A traffic cop directing cars to different lanes to avoid congestion and keep traffic flowing smoothly.

## The "So What?" Factor
**If you use this:**
- Higher reliability and scalability.
- Easier maintenance and upgrades.
- Better user experience under load.

**If you don't:**
- Single server overload and downtime.
- Harder to scale and maintain services.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are all backend servers healthy and monitored?
- [ ] Is session persistence required?
- [ ] Are health checks and failover configured?

## Watch Out For
⚠️ Misconfigured health checks can cause downtime.
⚠️ Single point of failure if not redundant.

## Connections
**Builds On:** [autoscaling.md](autoscaling.md), [cloud_computing.md](cloud_computing.md)
**Works With:** [high_availability.md](high_availability.md), [fault_tolerance.md](fault_tolerance.md)
**Leads To:** Global load balancing and SRE practices

## Quick Decision Guide
**Use this when you need to:** distribute load and improve uptime.
**Skip this when:** a single server is sufficient for the workload.

## Further Exploration
- 📖 https://en.wikipedia.org/wiki/Load_balancing_(computing)
- 🎯 https://learn.microsoft.com/azure/load-balancer/load-balancer-overview
- 💡 https://aws.amazon.com/elasticloadbalancing/

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*

