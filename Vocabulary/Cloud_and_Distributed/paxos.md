# Paxos

## At a Glance
| | |
|---|---|
| **Category** | Algorithm |
| **Complexity** | Advanced |
| **Time to Learn** | 6-10 hours |
| **Prerequisites** | Distributed systems, consensus, failure models |

## One-Sentence Summary
Paxos is a family of algorithms for achieving consensus among distributed nodes, even in the presence of failures.

## Why This Matters to You
Paxos is foundational for building reliable distributed systems. It ensures consistency and coordination without a single point of failure. Understanding Paxos helps you reason about correctness and liveness in distributed databases and control planes.

## The Core Idea
### What It Is
Paxos works by having nodes propose values and reach agreement through a series of message exchanges. It guarantees safety (no two nodes decide differently) and liveness (progress is eventually made). While powerful, Paxos is considered difficult to understand and implement, leading to alternatives like Raft.

### What It Isn't
It is not a simple voting protocol. It is not always the best choice for performance or ease of implementation.

## How It Works
1. Proposer suggests a value to acceptors.
2. Acceptors respond according to protocol rules.
3. Once a quorum is reached, the value is chosen and committed.

## Think of It Like This
A group of people trying to agree on a meeting time via email: proposals are sent, responses collected, and consensus is reached even if some people don’t reply.

## The "So What?" Factor
**If you use this:**
- Strong consistency under failure.
- Predictable coordination for critical state.
- Reduced split-brain risk.

**If you don't:**
- Higher chance of inconsistent writes.
- Difficult recovery from coordination faults.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Do you truly need strong consistency here?
- [ ] Is quorum sizing aligned with failure tolerance goals?
- [ ] Are leader election and timeout parameters tested under packet loss?

## Watch Out For
⚠️ Misconfigured timeouts can cause leader churn.
⚠️ Consensus in high-latency regions can degrade throughput.

## Connections
**Builds On:** [distributed_consensus.md](distributed_consensus.md), [replication.md](replication.md)
**Works With:** [raft_protocol.md](raft_protocol.md), [strong_consistency.md](strong_consistency.md)
**Leads To:** Advanced consensus protocols

## Quick Decision Guide
**Use this when you need to:** coordinate critical writes with strict correctness.
**Skip this when:** eventual consistency is acceptable and throughput is dominant.

## Further Exploration
- 📖 https://lamport.azurewebsites.net/pubs/paxos-simple.pdf
- 🎯 https://raft.github.io/
- 💡 https://jepsen.io/consistency

---
*Added: May 22, 2026 | Updated: May 22, 2026 | Confidence: High*

