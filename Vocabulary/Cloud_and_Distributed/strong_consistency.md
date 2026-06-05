# Strong Consistency

## Summary
**Strong consistency** is a consistency model in distributed systems where all clients always see the most recent write for a given piece of data. After a write completes, any subsequent read (by any client, anywhere) will return that value or a more recent one.

## Motivation
⚠️ Ensure correctness in distributed databases and storage systems.
⚠️ Prevent anomalies due to stale or out-of-order reads.
⚠️ Required for applications with strict data integrity needs (e.g., banking, inventory).

## Explanation
In a strongly consistent system, operations appear to occur in a single, globally agreed-upon order. This is often achieved using consensus protocols (e.g., Paxos, Raft) or by centralizing updates. Strong consistency simplifies application logic but can reduce performance and availability, especially across geographically distributed nodes.

## Analogy
Strong consistency is like a single, up-to-date scoreboard at a sports event: everyone sees the same score at the same time, no matter where they are in the stadium.

## Practical Checklist
- [x] All reads reflect the latest completed write
- [x] No stale or out-of-order data
- [x] Often requires coordination/consensus
- [x] May impact latency and availability
- [ ] Is strong consistency a business requirement?
- [ ] Have you measured latency impact?
- [ ] Is your system tested for partition scenarios?
- [ ] Are transaction guarantees documented?
- [ ] Have you monitored availability impact?
- [ ] Is failover behavior tested?

## Watch Out For
⚠️ Can introduce high latency, especially in multi-region deployments.
⚠️ May reduce system availability (see CAP theorem).
⚠️ Not always necessary—overuse can waste resources.



## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

## Connections
- [eventual_consistency.md](eventual_consistency.md)
- [cap_theorem.md](cap_theorem.md)
- [paxos.md](paxos.md)
- [raft_protocol.md](raft_protocol.md)

## References
- [Consistency models (Jepsen)](https://jepsen.io/consistency)
- [Wikipedia: Consistency model](https://en.wikipedia.org/wiki/Consistency_model)

## Metadata
⚠️ Created: 2024-06-08
⚠️ Updated: 2024-06-08
⚠️ Author: GitHub Copilot


