# Eventual Consistency

## At a Glance
| | |
|---|---|
| **Category** | Technique |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours |
| **Prerequisites** | Replication, distributed data models, CAP trade-offs |

## One-Sentence Summary
Eventual consistency allows replicas to converge over time instead of requiring every read to immediately reflect the latest write.

## Why This Matters to You
Strict consistency can be expensive or slow at scale, especially across regions. Eventual consistency lets systems remain available and fast during partitions or latency spikes. The trade-off is handling stale reads and reconciliation logic. Choosing this model deliberately prevents correctness surprises.

## The Core Idea
### What It Is
Writes propagate asynchronously to replicas. During propagation windows, clients can observe different versions depending on replica and timing. Convergence happens when updates have been applied everywhere.

Many large-scale data stores use this model for high throughput and geographic distribution.

### What It Isn't
It is not "random inconsistency forever." It is also not appropriate when immediate global correctness is mandatory.

## How It Works
1. Accept write locally or at a preferred replica.
2. Replicate updates asynchronously.
3. Resolve conflicts and converge state.

## Think of It Like This
Timetables posted across stations update at slightly different moments, but all boards eventually show the same official schedule.

## The "So What?" Factor
**If you use this:**
- Better availability and write throughput.
- Lower latency in geographically distributed setups.
- Graceful behavior under partitions.

**If you don't:**
- Strong consistency costs may limit scale.
- Availability may drop under network stress.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Can the business tolerate temporary stale reads?
- [ ] What conflict resolution strategy is required?
- [ ] Which user flows need read-after-write guarantees?

## Watch Out For
⚠️ Subtle bugs when clients assume immediate global truth.
⚠️ Poorly designed merge policies can lose intent.

## Connections
**Builds On:** [replication.md](replication.md), [cap_theorem.md](cap_theorem.md)
**Works With:** [multi_region.md](multi_region.md), [cloud_computing.md](cloud_computing.md)
**Leads To:** [strong_consistency.md](strong_consistency.md) trade-off analysis

## Quick Decision Guide
**Use this when you need to:** maximize availability and scale with acceptable temporary divergence.
**Skip this when:** every read must immediately reflect committed writes globally.

## Further Exploration
- 📖 https://jepsen.io/consistency
- 🎯 https://www.allthingsdistributed.com/2008/12/eventually_consistent.html
- 💡 https://dataintensive.net/

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*

