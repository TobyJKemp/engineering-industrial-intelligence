# Cache Invalidation

## At a Glance
| | |
|---|---|
| **Category** | Technique / Data Management |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for patterns, days to weeks to master edge cases |
| **Prerequisites** | Caching concepts, data consistency basics, distributed systems fundamentals |

## One-Sentence Summary
Cache invalidation is the process of removing or updating stale cached data so that future reads return fresh, correct values—one of the hardest problems in distributed systems engineering.

## Why This Matters to You
Caches make AI systems fast, but they create a dangerous risk: serving outdated data. If an AI agent reads a cached prompt configuration that was updated 10 minutes ago, it may operate on the wrong instructions. If a recommendation system serves cached embeddings for a user profile that has since changed, it produces irrelevant results. Knowing when and how to invalidate caches correctly is what separates reliable systems from ones that serve subtly wrong answers silently and indefinitely.

## The Core Idea
### What It Is
Cache invalidation is the mechanism by which a cache is told that data it holds is no longer valid. "Invalid" means either:
- **Stale:** The source-of-truth data has changed and the cache still holds the old version.
- **Expired:** A time-to-live (TTL) has elapsed, making the cached value suspect regardless of whether underlying data changed.

There are three dominant invalidation strategies:
1. **Time-To-Live (TTL):** Each cache entry expires after a fixed duration. Simple and predictable, but imprecise—stale data may be served until TTL elapses, and valid data may be evicted too soon.
2. **Event-driven invalidation:** When source data changes, an event is published (via a message queue or pub/sub system) and cache entries are invalidated immediately. More precise, more complex.
3. **Write-through / Write-around invalidation:** When a write occurs to the source, the cache is updated or cleared in the same transaction. Keeps cache consistent at the cost of higher write latency.

### What It Isn't
Cache invalidation is not cache eviction. Eviction is capacity management—removing old entries when the cache is full (e.g., LRU eviction policy). Invalidation is correctness management—removing entries because the data they represent is no longer accurate. These can happen independently.

## How It Works
1. **Data changes at the source:** A database record is updated, a configuration file is rewritten, or a model artifact is replaced.
2. **Invalidation is triggered:** Either automatically via TTL expiration, via a change event published to a queue, or via explicit cache key deletion in a write path.
3. **Cache removes or marks the entry:** The entry is deleted or flagged as stale.
4. **Next read causes a cache miss:** The application fetches fresh data from the source, which populates the cache again.
5. **Cache serves fresh data:** Subsequent reads hit the refreshed cache entry until the next invalidation cycle.

## Think of It Like This
A whiteboard in a control room has train schedules written on it for quick reference. When a train's departure time changes, someone must erase the old time and write the new one—otherwise operators will keep referencing the wrong schedule. TTL is like erasing everything every hour "just in case." Event-driven invalidation is like having the scheduling system send a direct notification to the whiteboard operator the moment a change is made.

## The "So What?" Factor
**If you use this:**
- Systems serve accurate, up-to-date data even when caching aggressively for performance
- Bugs from stale data are detected and handled at the architecture level rather than appearing as mysterious intermittent errors
- AI agents and retrieval systems operate on correct context rather than silently outdated information

**If you don't:**
- Caches serve stale data silently—users and agents receive outdated information with no error signal
- Debugging becomes very difficult because incorrect behavior only manifests hours or days after a source change
- Trust in AI outputs erodes when results are inconsistent with reality

## Practical Checklist
Before implementing a caching layer, ask yourself:
- [ ] How often does the underlying data change? (Determines appropriate TTL or event frequency)
- [ ] What is the acceptable staleness window? (5 seconds? 5 minutes? 5 hours?)
- [ ] Can I detect source data changes to drive event-based invalidation?
- [ ] Do I have a cache key strategy that targets precise entries rather than full cache flushes?
- [ ] Have I handled the thundering herd problem—many simultaneous cache misses after invalidation?
- [ ] What happens if the invalidation event is lost? (Design for eventual correctness)

## Watch Out For
⚠️ **The thundering herd:** Invalidating a popular cache entry causes all requests to simultaneously miss and hammer the source. Use jittered TTLs or probabilistic early recomputation (e.g., cache warming).
⚠️ **Over-invalidation:** Clearing entire caches on any change is safe but defeats the purpose of caching—performance collapses under load.
⚠️ **Distributed cache inconsistency:** In multi-node caches, invalidation events may not propagate to all nodes simultaneously, causing a window where different nodes serve different data.
⚠️ **Ignoring invalidation in AI pipelines:** Cached embeddings, prompt templates, or retrieved context that doesn't invalidate on source document changes leads to agents reasoning on stale knowledge.

## Connections
**Builds On:** [Caching Strategy](caching_strategy.md), [Eventual Consistency](../Cloud_and_Distributed/eventual_consistency.md)
**Works With:** [Distributed System](../Cloud_and_Distributed/distributed_system.md), [Strong Consistency](../Cloud_and_Distributed/strong_consistency.md), [Throughput](throughput.md), [Latency](latency.md)
**Leads To:** [Performance Tuning](performance_tuning.md), [Bottleneck](bottleneck.md)

## Quick Decision Guide
**Use this when you need to:** Ensure a cache does not serve stale data after the underlying source has changed.
**Skip this when:** Your data is immutable (cache-forever is safe) or your TTL window is acceptable and simplicity is preferred over precision.

## Further Exploration
- 📖 [Caching Strategies and How to Choose the Right One (AWS)](https://aws.amazon.com/caching/best-practices/)
- 🎯 [Redis cache invalidation patterns](https://redis.io/docs/manual/keyspace-notifications/)
- 💡 [Designing Data-Intensive Applications, Chapter 5 – Replication (Martin Kleppmann)](https://dataintensive.net/)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
