# Change Data Capture (CDC)

## At a Glance
| | |
|---|---|
| **Category** | Data Integration Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Database concepts, event streaming basics |

## One-Sentence Summary
Change Data Capture (CDC) is a technique for identifying and capturing changes made to data in a source system so they can be replicated or processed elsewhere.

## Why This Matters to You
CDC enables real-time data integration, replication, and analytics. It reduces the need for full data reloads and supports event-driven architectures. Mastering CDC is essential for building scalable, low-latency data pipelines and keeping systems in sync.

## The Core Idea
### What It Is
CDC monitors inserts, updates, and deletes in a database or data source. It captures these changes as events, which can be streamed to downstream systems for processing, analytics, or replication.

CDC can be implemented using database logs, triggers, or polling mechanisms, and is often used in modern data lakes and streaming architectures.

### What It Isn't
CDC is not a full data dump or batch ETL; it only processes changes.

It is also not always trivial to implement—schema changes and out-of-order events can add complexity.

## How It Works
1. Monitor the source system for data changes.
2. Capture change events and serialize them (often as logs or messages).
3. Deliver events to consumers (e.g., data warehouse, analytics, microservices).

## Think of It Like This
Think of a security camera that only records when there is movement, rather than recording the entire day.

## The "So What?" Factor
**If you use this:**
- You enable near-real-time data synchronization.
- You reduce bandwidth and processing costs.
- You support event-driven and microservices architectures.

**If you don't:**
- Data may become stale or inconsistent between systems.
- Full reloads become expensive and slow.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Does your source system support CDC natively?
- [ ] Are downstream consumers able to process change events?
- [ ] How will you handle schema evolution and error recovery?

## Watch Out For
⚠️ Missed or duplicate events due to system failures.
⚠️ Complexity in handling schema changes and ordering.

## Connections
**Builds On:** [event_stream.md](event_stream.md), [etl_process.md](etl_process.md)
**Works With:** [data_lakehouse.md](data_lakehouse.md), [stream_processing.md](stream_processing.md)
**Leads To:** [data_lineage.md](data_lineage.md), [data_quality.md](data_quality.md)

## Quick Decision Guide
**Use this when you need to:** Keep systems in sync or enable real-time analytics.
**Skip this when:** Only full data loads are needed or latency is not a concern.

## Further Exploration
- [CDC overview](https://en.wikipedia.org/wiki/Change_data_capture)
- [Debezium documentation](https://debezium.io/)
- [CDC in cloud data platforms](https://docs.microsoft.com/azure/architecture/patterns/change-data-capture)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
