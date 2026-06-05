# CAP Theorem

## Summary
The **CAP theorem** states that a distributed system can only guarantee two out of the following three properties at any given time: Consistency, Availability, and Partition Tolerance. It is a fundamental principle for designing distributed databases and services.

## Motivation
- Guide trade-offs in distributed system design.
- Understand limitations of consistency and availability during network partitions.
- Inform architecture choices for databases and cloud services.

## Explanation
- **Consistency:** Every read receives the most recent write or an error.
- **Availability:** Every request receives a (non-error) response, without guarantee that it contains the most recent write.
- **Partition Tolerance:** The system continues to operate despite arbitrary partitioning due to network failures.
During a partition, a system must choose between consistency and availability. No system can guarantee all three simultaneously.

## Analogy
Like a restaurant with three priorities: always serving hot food (consistency), never turning away customers (availability), and staying open even if the kitchen and dining room are separated (partition tolerance)—you can only pick two at a time.

## Practical Checklist
- [x] Consistency
- [x] Availability
- [x] Partition tolerance
- [x] Trade-off required during network failures
- [ ] Have you documented which two properties your system prioritizes?
- [ ] Is your team aware of CAP theorem implications?
- [ ] Have you tested behavior during network partitions?
- [ ] Are monitoring and alerting configured for partition scenarios?
- [ ] Have you communicated trade-offs to stakeholders?
- [ ] Is failover strategy documented and tested?

## Watch Out For
⚠️ Misunderstanding the theorem as "pick any two" at all times (it applies only during partitions).
⚠️ Overlooking the impact of network failures.
⚠️ Assuming all systems must sacrifice consistency or availability.
⚠️ Ignoring the cost of achieving partition tolerance.

## Connections
- [eventual_consistency.md](eventual_consistency.md)
- [strong_consistency.md](strong_consistency.md)
- [replication.md](replication.md)

## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

## References
- [Brewer's CAP Theorem](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)
- [Wikipedia: CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)

## Metadata
- Created: 2024-06-08
- Updated: 2024-06-08
- Author: GitHub Copilot

