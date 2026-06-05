# Caching Strategy

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Performance Engineering |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-4 hours for patterns, ongoing practice for production tuning |
| **Prerequisites** | Basic understanding of latency, data storage, read/write patterns |

## One-Sentence Summary
A caching strategy is the deliberate plan for what data to cache, where to cache it, how long to keep it, and how to invalidate it—balancing speed against correctness and cost.

## Why This Matters to You
AI systems are expensive to run. Every inference call, every embedding computation, every database lookup has a cost in time and money. Caching strategies let you serve repeated or similar requests from fast, cheap memory instead of recomputing expensive results. Conversely, a poorly chosen strategy silently corrupts your system with stale data. Knowing the patterns lets you choose the right one and avoid the traps.

## The Core Idea
### What It Is
Caching is storing a copy of data in a location that can be read faster or cheaper than the origin source. The strategy defines the rules governing this behavior. The major patterns are:

**Read-Through:** The application always reads from the cache. On a cache miss, the cache automatically fetches from the source, stores the result, and returns it. The application never talks directly to the source.

**Write-Through:** Every write goes simultaneously to both the cache and the source. Cache and source stay synchronized at all times. High write latency, but very consistent reads.

**Write-Behind (Write-Back):** Writes go to the cache immediately and are asynchronously flushed to the source later. Very fast writes, but risk of data loss if the cache fails before flushing.

**Cache-Aside (Lazy Loading):** The application manages the cache explicitly. On a miss, the application fetches from the source, writes to the cache, and returns the data. Simple and flexible—most common in practice.

**Refresh-Ahead:** Cache entries are proactively refreshed before they expire, so reads never encounter a miss on hot data. Reduces latency spikes at TTL expiration.

### What It Isn't
A caching strategy is not a database. It is not the source of truth. It is an optimization layer. If the cache is lost, the system must still function correctly by falling back to the source. A caching strategy also doesn't replace data consistency design—it requires a companion invalidation strategy.

## How It Works
1. **Identify hot data:** Profile your system to find what data is read frequently and changes infrequently. These are strong candidates for caching.
2. **Choose a pattern:** Match the read/write ratio and consistency requirements to one of the patterns above.
3. **Define cache keys:** Keys must uniquely identify the data. Poor key design causes misses on equivalent requests or collisions between different data.
4. **Set TTL:** Define how long entries live based on acceptable staleness and data change frequency.
5. **Plan for invalidation:** Decide how stale entries are removed when source data changes.
6. **Monitor hit/miss ratios:** Cache effectiveness is measured by hit rate. Below ~80%, the cache is not covering its cost.

## Think of It Like This
A reference desk librarian keeps the 20 most-requested books on a shelf right next to them instead of making patrons wait while they retrieve books from deep in the stacks. When a patron requests a book that's on the shelf, they get it instantly. When the book isn't there (cache miss), the librarian walks to retrieve it and may add it to the shelf. The strategy determines which books belong on that shelf and when to return them.

## The "So What?" Factor
**If you use this:**
- Read latency drops dramatically for repeated or popular queries—often from hundreds of milliseconds to under a millisecond
- Expensive compute (embeddings, inference, DB queries) is amortized across many requests
- System throughput scales significantly without additional backend capacity

**If you don't:**
- Every request pays full cost, even for identical repeated queries
- Systems become expensive to scale because adding users linearly adds backend load
- Latency is high and variable, degrading user and agent experience

## Practical Checklist
Before implementing a cache, ask yourself:
- [ ] What is the read-to-write ratio? (High read-to-write strongly favors caching)
- [ ] How often does this data change? (Infrequent changes mean longer TTL is safe)
- [ ] What is the acceptable staleness window for correctness?
- [ ] How will you handle cache invalidation when source data changes?
- [ ] What happens when the cache is cold (empty) at startup?
- [ ] Have you chosen a key structure that uniquely maps requests to cache entries?

## Watch Out For
⚠️ **Cache stampede:** When a popular entry expires simultaneously, all requests miss and pile up on the source. Mitigate with jittered TTLs or probabilistic early refresh.
⚠️ **Incorrect cache keys:** Caching a response that varies by user and returning it to a different user is a serious data leakage bug.
⚠️ **Caching errors:** Caching a failed response (e.g., a 500 error) means all users get the error until TTL expires. Cache successes only, or use very short TTLs for errors.
⚠️ **Treating the cache as a database:** Never make the cache the only place important data exists. It can evict entries under memory pressure.

## Connections
**Builds On:** [Latency](latency.md), [Throughput](throughput.md), [Content Delivery Network](../Cloud_and_Distributed/content_delivery_network.md)
**Works With:** [Cache Invalidation](cache_invalidation.md), [Performance Tuning](performance_tuning.md), [Bottleneck](bottleneck.md)
**Leads To:** [Cost Optimization](cost_optimization.md), [Capacity Planning](capacity_planning.md)

## Quick Decision Guide
**Use this when you need to:** Reduce latency and backend load for frequently-read, rarely-changed data.
**Skip this when:** Data changes on every request, correctness is critical and invalidation is complex, or the data set is too large and varied to benefit from a bounded cache.

## Further Exploration
- 📖 [AWS Caching Best Practices](https://aws.amazon.com/caching/best-practices/)
- 🎯 [Redis as a cache: patterns and anti-patterns](https://redis.io/docs/manual/patterns/)
- 💡 [Designing Data-Intensive Applications, Chapter 11 – Caching (Martin Kleppmann)](https://dataintensive.net/)

---
*Added: May 26, 2026 | Updated: May 26, 2026 | Confidence: High*
