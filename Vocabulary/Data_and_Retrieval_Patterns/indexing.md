# Indexing

## At a Glance
| | |
|---|---|
| **Category** | Data Structure / Search Optimization |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 3-6 hours for fundamentals, weeks for optimization mastery |
| **Prerequisites** | Understanding of [vector_database](vector_database.md), [embeddings](../Foundational_AI & ML/embeddings.md), [semantic_search](semantic_search.md), [similarity_score](similarity_score.md) |

## One-Sentence Summary
Indexing is the process of organizing high-dimensional vector embeddings into specialized data structures (like HNSW or IVF) that enable sub-second similarity searches across millions of vectors—transforming RAG systems from "compare query to every document" (taking minutes) to "traverse optimized graph to nearest neighbors" (taking milliseconds), making production-scale semantic search actually feasible.

## Why This Matters to You
When you build RAG systems in 2026, indexing is what makes them fast enough for production. Without indexing, searching 1 million document chunks means computing similarity between your query vector and all 1 million stored vectors—taking 30+ seconds per query, completely unusable. With proper indexing (HNSW, IVF-PQ, or similar), that same search takes 10-50 milliseconds, a 1000x speedup. But indexing isn't magic—it's a carefully tuned trade-off between search speed, accuracy (recall), and memory usage. An HNSW index with `ef_construction=400` finds 98% of true nearest neighbors in 15ms but uses 3GB RAM per million vectors; an IVF-PQ index with 4096 clusters finds 85% of nearest neighbors in 5ms but uses only 500MB. Choosing wrong index parameters means either unacceptable latency (users wait seconds for answers), poor retrieval quality (missing 30% of relevant chunks), or memory exhaustion (OOM crashes). Understanding index types (exact vs approximate, graph-based vs clustering-based), tuning parameters (ef_construction, nprobe, M), and measuring trade-offs (recall@k vs latency vs memory) determines whether your RAG system scales to production workloads. At enterprise scale with 10+ million chunks, indexing strategy can mean the difference between a $500/month vector database bill and $50,000/month (wrong index = need 10x more machines for acceptable latency). In 2026, with vector databases powering everything from customer support to code completion, indexing expertise is essential infrastructure knowledge—the difference between RAG systems that feel instant and reliable versus those abandoned for being too slow or inaccurate.

## The Core Idea
### What It Is
Indexing in the context of vector databases is the process of organizing high-dimensional vectors into specialized data structures that enable fast approximate nearest neighbor (ANN) search. Instead of exhaustive comparison (brute force), indexes use clever data structures—graphs, trees, hash tables, or clusters—to narrow the search space dramatically, achieving sub-linear query times while maintaining high accuracy.

**The Fundamental Challenge:**

Given:
- **Query vector**: Your 384-dimensional or 1536-dimensional embedding
- **Database**: 1 million to 100+ million stored vectors
- **Goal**: Find k=10 most similar vectors (nearest neighbors)

**Brute Force Approach (No Index):**
```python
import numpy as np
import time

def brute_force_search(query_vector, database_vectors, k=10):
    """
    Exhaustive search - compare query to every vector.
    
    Complexity: O(n * d) where n = number of vectors, d = dimension
    """
    # Compute similarity to every vector
    similarities = []
    for i, db_vector in enumerate(database_vectors):
        # Cosine similarity
        similarity = np.dot(query_vector, db_vector) / (
            np.linalg.norm(query_vector) * np.linalg.norm(db_vector)
        )
        similarities.append((similarity, i))
    
    # Sort and return top k
    similarities.sort(reverse=True)
    return similarities[:k]

# Simulate 1 million 384-dim vectors
num_vectors = 1_000_000
dimensions = 384

database = np.random.randn(num_vectors, dimensions).astype('float32')
query = np.random.randn(dimensions).astype('float32')

# Normalize for cosine similarity
database = database / np.linalg.norm(database, axis=1, keepdims=True)
query = query / np.linalg.norm(query)

start = time.time()
results = brute_force_search(query, database, k=10)
elapsed = time.time() - start

print(f"Brute force search of {num_vectors:,} vectors:")
print(f"Time: {elapsed:.3f} seconds")
print(f"Top result similarity: {results[0][0]:.4f}")

# Output: ~30-60 seconds (unusable for production)
```

**With Indexing - 1000x Faster:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, HnswConfigDiff
import uuid

# Initialize Qdrant with HNSW index
client = QdrantClient(":memory:")

client.create_collection(
    collection_name="fast_search",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    ),
    hnsw_config=HnswConfigDiff(
        m=16,  # Number of connections per layer
        ef_construction=200  # Search breadth during construction
    )
)

# Index vectors (one-time cost)
print("Indexing 1 million vectors...")
index_start = time.time()

# Batch upload
batch_size = 1000
for i in range(0, num_vectors, batch_size):
    batch_end = min(i + batch_size, num_vectors)
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=database[j].tolist(),
            payload={"index": j}
        )
        for j in range(i, batch_end)
    ]
    client.upsert(collection_name="fast_search", points=points)
    
    if i % 10000 == 0:
        print(f"  Indexed {i:,} vectors...")

index_time = time.time() - index_start
print(f"Indexing complete: {index_time:.1f} seconds")

# Query with index (sub-second!)
search_start = time.time()
results = client.search(
    collection_name="fast_search",
    query_vector=query.tolist(),
    limit=10
)
search_time = time.time() - search_start

print(f"\nIndexed search of {num_vectors:,} vectors:")
print(f"Time: {search_time*1000:.1f} milliseconds")
print(f"Top result similarity: {results[0].score:.4f}")
print(f"Speedup: {elapsed/search_time:.0f}x faster")

# Output: ~10-50ms (1000x faster than brute force!)
```

**Why Indexing Works:**

Indexes exploit two key insights:

1. **Locality**: Similar vectors cluster together in high-dimensional space. You don't need to check vectors far from the query.

2. **Navigation**: By building structures (graphs, trees, clusters) during indexing, you can navigate directly to relevant regions, skipping vast portions of the database.

**Major Index Types:**

**1. HNSW (Hierarchical Navigable Small World)**
```python
"""
HNSW: Graph-based index with layered structure.

Structure:
- Multiple layers of graphs
- Each vertex = vector
- Edges connect similar vectors
- Top layers = sparse, long-range connections
- Bottom layer = dense, local connections

Search:
1. Start at top layer, greedy navigation
2. Descend to lower layers
3. Continue until finding k nearest neighbors

Pros:
- Excellent recall (>95% typical)
- Fast search (10-50ms for millions)
- Good for high-dim vectors

Cons:
- High memory usage (~2-4GB per million vectors)
- Slower indexing than alternatives
- Cannot add/remove efficiently (need rebuild)
"""

from qdrant_client.models import HnswConfigDiff

# Configure HNSW index
hnsw_config = HnswConfigDiff(
    m=16,                    # Edges per vertex (higher = better recall, more memory)
    ef_construction=200,     # Search width during build (higher = better quality, slower)
    full_scan_threshold=10000  # Switch to brute force below this size
)

client.create_collection(
    collection_name="hnsw_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    hnsw_config=hnsw_config
)

# Query-time parameters
results = client.search(
    collection_name="hnsw_collection",
    query_vector=query.tolist(),
    limit=10,
    search_params={
        "hnsw_ef": 128  # Search width at query time (higher = better recall, slower)
    }
)

# Tuning guide:
# - m: 16-64 (16 standard, 32-64 for higher recall)
# - ef_construction: 100-400 (200 balanced, 400 high quality)
# - hnsw_ef: 64-256 (128 balanced, 256 high recall)
```

**2. IVF (Inverted File Index)**
```python
"""
IVF: Clustering-based index using k-means.

Structure:
- Divide vectors into N clusters (centroids)
- Each cluster contains nearby vectors
- Store inverted lists (cluster -> vector IDs)

Search:
1. Find nprobe nearest cluster centroids to query
2. Search only vectors in those clusters
3. Return top k overall

Pros:
- Fast search with good recall
- Memory efficient
- Easy to add/remove vectors (dynamic)

Cons:
- Requires training on representative data
- Need to tune nprobe vs speed trade-off
- Cluster imbalance can hurt performance
"""

# Faiss example (popular for IVF)
import faiss

# Create IVF index
dimension = 384
nlist = 4096  # Number of clusters (sqrt(n) to n/30 typical)

# Train on sample vectors (need representative data)
train_vectors = database[:100000]  # Use 100k for training

# Create quantizer (finds nearest clusters)
quantizer = faiss.IndexFlatL2(dimension)

# Create IVF index
index = faiss.IndexIVFFlat(
    quantizer,
    dimension,
    nlist,
    faiss.METRIC_L2
)

# Train index on sample data
print("Training IVF index...")
index.train(train_vectors)
print(f"Trained with {nlist} clusters")

# Add all vectors
print("Adding vectors to index...")
index.add(database)
print(f"Indexed {index.ntotal:,} vectors")

# Search with nprobe parameter
nprobe = 64  # Search this many clusters (higher = better recall, slower)
index.nprobe = nprobe

start = time.time()
distances, indices = index.search(query.reshape(1, -1), k=10)
elapsed = time.time() - start

print(f"IVF search: {elapsed*1000:.1f}ms")
print(f"Top 10 indices: {indices[0]}")

# Tuning guide:
# - nlist: sqrt(n) to n/30 (4096 for ~1M vectors)
# - nprobe: 1-256 (64 balanced, 128-256 high recall)
# - Trade-off: nprobe=1 fastest, nprobe=nlist = brute force
```

**3. IVF-PQ (Product Quantization)**
```python
"""
IVF-PQ: Memory-efficient variant using compression.

Structure:
- IVF clustering (same as above)
- + Product Quantization compression
- Splits vectors into sub-vectors
- Quantizes each sub-vector separately

Memory savings:
- Original: 384 float32 = 1536 bytes
- PQ compressed: 384/8 sub-vectors × 1 byte = 48 bytes
- 32x compression!

Pros:
- Extremely memory efficient
- Scales to 100M+ vectors on single machine
- Still fast search

Cons:
- Lower recall than HNSW/IVF-Flat
- Lossy compression (approximate)
- Requires careful tuning
"""

# Create IVF-PQ index
m = 48  # Number of sub-vectors (dimension must be divisible)
nbits = 8  # Bits per sub-vector code (8 = 256 centroids per sub-vector)

index_pq = faiss.IndexIVFPQ(
    quantizer,
    dimension,
    nlist,
    m,
    nbits
)

# Train and add
index_pq.train(train_vectors)
index_pq.add(database)

# Search
index_pq.nprobe = 64
start = time.time()
distances, indices = index_pq.search(query.reshape(1, -1), k=10)
elapsed = time.time() - start

print(f"IVF-PQ search: {elapsed*1000:.1f}ms")
print(f"Memory per vector: ~{(m * nbits) / 8:.0f} bytes (vs {dimension*4} bytes uncompressed)")

# Tuning guide:
# - m: 8-96 (48 balanced, higher = better quality)
# - nbits: 8 typical (16 for higher quality but more memory)
# - nprobe: same as IVF
```

**Index Comparison:**

| Index Type | Recall | Speed | Memory | Use Case |
|------------|--------|-------|---------|----------|
| Brute Force | 100% | Slow (30s) | Low | < 10k vectors, perfect recall needed |
| HNSW | 95-99% | Fast (15ms) | High | < 10M vectors, need best recall |
| IVF-Flat | 90-95% | Fast (10ms) | Medium | 100k-10M vectors, balanced |
| IVF-PQ | 80-90% | Fastest (5ms) | Low | 10M+ vectors, memory constrained |
| LSH | 70-85% | Fastest (3ms) | Very Low | 100M+ vectors, speed critical |

**Measuring Index Quality:**

```python
class IndexBenchmark:
    """
    Benchmark index performance: recall, latency, memory.
    """
    
    def __init__(self, database_vectors, ground_truth_func):
        """
        Args:
            database_vectors: All vectors in database
            ground_truth_func: Function returning true k-NN
        """
        self.database = database_vectors
        self.ground_truth_func = ground_truth_func
    
    def measure_recall_at_k(
        self,
        index,
        query_vectors,
        k=10
    ) -> dict:
        """
        Measure recall@k: % of true nearest neighbors found.
        
        Recall@10 = 0.95 means index finds 9.5 out of 10 true neighbors on average
        """
        recalls = []
        latencies = []
        
        for query in query_vectors:
            # Get ground truth (brute force)
            true_neighbors = set(self.ground_truth_func(query, k))
            
            # Get index results
            start = time.time()
            index_results = index.search(query, k)
            latency = time.time() - start
            
            index_neighbors = set([r.payload["index"] for r in index_results])
            
            # Calculate recall
            overlap = len(true_neighbors & index_neighbors)
            recall = overlap / k
            recalls.append(recall)
            latencies.append(latency)
        
        return {
            "recall@k": np.mean(recalls),
            "avg_latency_ms": np.mean(latencies) * 1000,
            "p95_latency_ms": np.percentile(latencies, 95) * 1000,
            "p99_latency_ms": np.percentile(latencies, 99) * 1000
        }
    
    def measure_memory(self, index) -> dict:
        """
        Estimate index memory usage.
        """
        import sys
        
        # Rough estimation (platform-specific)
        if hasattr(index, 'ntotal'):
            # Faiss index
            memory_bytes = index.ntotal * index.d * 4  # float32
            if hasattr(index, 'nlist'):
                # Add IVF overhead
                memory_bytes += index.nlist * index.d * 4
        else:
            # Generic estimation
            memory_bytes = sys.getsizeof(index)
        
        return {
            "memory_mb": memory_bytes / (1024 * 1024),
            "memory_per_vector_bytes": memory_bytes / len(self.database) if len(self.database) > 0 else 0
        }
    
    def compare_indexes(
        self,
        indexes: dict[str, object],
        query_vectors,
        k=10
    ):
        """
        Compare multiple indexes.
        
        Args:
            indexes: {"HNSW": hnsw_index, "IVF": ivf_index, ...}
        """
        results = {}
        
        for name, index in indexes.items():
            print(f"\nBenchmarking {name}...")
            
            # Measure recall and latency
            recall_metrics = self.measure_recall_at_k(index, query_vectors, k)
            
            # Measure memory
            memory_metrics = self.measure_memory(index)
            
            results[name] = {
                **recall_metrics,
                **memory_metrics,
                "score": recall_metrics["recall@k"] * 0.4 + (1 - recall_metrics["avg_latency_ms"]/1000) * 0.3 + (1 - memory_metrics["memory_mb"]/10000) * 0.3
            }
            
            print(f"  Recall@{k}: {recall_metrics['recall@k']:.3f}")
            print(f"  Latency (avg): {recall_metrics['avg_latency_ms']:.1f}ms")
            print(f"  Latency (p95): {recall_metrics['p95_latency_ms']:.1f}ms")
            print(f"  Memory: {memory_metrics['memory_mb']:.0f} MB")
        
        # Print comparison
        print("\n=== Index Comparison ===")
        print(f"{'Index':<15} {'Recall@10':<12} {'Latency':<12} {'Memory':<12} {'Score':<8}")
        print("-" * 65)
        
        for name, metrics in sorted(results.items(), key=lambda x: x[1]['score'], reverse=True):
            print(f"{name:<15} {metrics['recall@k']:<12.3f} {metrics['avg_latency_ms']:<12.1f} {metrics['memory_mb']:<12.0f} {metrics['score']:<8.3f}")
        
        return results

# Usage
# benchmark = IndexBenchmark(database, brute_force_search)
# test_queries = database[:100]  # Sample queries
# results = benchmark.compare_indexes(
#     {
#         "HNSW-16": hnsw_index_16,
#         "HNSW-32": hnsw_index_32,
#         "IVF-4096": ivf_index,
#         "IVF-PQ": ivf_pq_index
#     },
#     test_queries,
#     k=10
# )
```

### What It Isn't
Indexing is not **perfect search**. Approximate nearest neighbor (ANN) indexes trade accuracy for speed—they find ~90-99% of true nearest neighbors, not 100%. If you need perfect recall, use brute force (but accept slow queries).

It's not **free**. Indexing has costs: one-time indexing time (minutes to hours for millions of vectors), ongoing memory usage (GB to tens of GB), and maintenance overhead (rebuilding indexes when data changes significantly).

Indexing is not **one-size-fits-all**. HNSW works great for 1-10M vectors with high recall needs; IVF-PQ works for 100M+ vectors with memory constraints. Wrong choice means either unusable latency or poor recall.

It's not **query-agnostic**. Index parameters tuned for k=10 nearest neighbors may not work well for k=100. Similarly, indexes optimized for single-query latency differ from those optimized for batch throughput.

Indexing is not **automatic optimization**. Vector databases provide defaults, but production systems need tuning based on your specific data distribution, query patterns, and latency/recall requirements.

Finally, indexing is not **static**. As your dataset grows or changes, index performance degrades. Indexes need periodic rebuilding or online optimization to maintain quality.

## How It Works

### Building Production Indexes

**Step 1: Choose Index Type Based on Scale**
```python
def recommend_index_type(
    num_vectors: int,
    dimension: int,
    recall_requirement: float,  # e.g., 0.95
    latency_requirement_ms: float,  # e.g., 50ms
    memory_budget_gb: float  # e.g., 16GB
) -> dict:
    """
    Recommend index configuration based on requirements.
    """
    # Estimate memory per vector for different indexes
    memory_per_vector = {
        "hnsw": dimension * 4 + 64,  # float32 + graph overhead
        "ivf_flat": dimension * 4 + 16,  # float32 + cluster pointers
        "ivf_pq": (dimension // 8) + 16,  # compressed + pointers
    }
    
    recommendations = []
    
    # Check each index type
    for index_type, bytes_per_vec in memory_per_vector.items():
        total_memory_gb = (num_vectors * bytes_per_vec) / (1024**3)
        
        if total_memory_gb > memory_budget_gb:
            continue  # Doesn't fit in memory
        
        # Estimate performance
        if index_type == "hnsw":
            expected_recall = 0.98
            expected_latency = 15
        elif index_type == "ivf_flat":
            expected_recall = 0.93
            expected_latency = 10
        elif index_type == "ivf_pq":
            expected_recall = 0.85
            expected_latency = 5
        
        # Check if meets requirements
        meets_recall = expected_recall >= recall_requirement
        meets_latency = expected_latency <= latency_requirement_ms
        
        if meets_recall and meets_latency:
            recommendations.append({
                "index_type": index_type,
                "expected_recall": expected_recall,
                "expected_latency_ms": expected_latency,
                "memory_gb": total_memory_gb,
                "fits_requirements": True
            })
    
    if not recommendations:
        # No perfect match - show why
        recommendations.append({
            "index_type": "None suitable",
            "message": "No index meets all requirements. Consider: reducing recall requirement, increasing latency tolerance, or adding more memory."
        })
    
    return {
        "num_vectors": num_vectors,
        "requirements": {
            "recall": recall_requirement,
            "latency_ms": latency_requirement_ms,
            "memory_gb": memory_budget_gb
        },
        "recommendations": recommendations
    }

# Example usage
rec = recommend_index_type(
    num_vectors=5_000_000,
    dimension=384,
    recall_requirement=0.95,
    latency_requirement_ms=20,
    memory_budget_gb=16
)

print(f"For {rec['num_vectors']:,} vectors:")
for r in rec['recommendations']:
    if r.get('fits_requirements'):
        print(f"\n{r['index_type'].upper()}:")
        print(f"  Recall: {r['expected_recall']:.2%}")
        print(f"  Latency: {r['expected_latency_ms']}ms")
        print(f"  Memory: {r['memory_gb']:.1f} GB")
```

**Step 2: Tune Index Parameters**
```python
def tune_hnsw_parameters(
    sample_vectors,
    target_recall=0.95,
    max_latency_ms=50
):
    """
    Find optimal HNSW parameters through grid search.
    """
    # Parameter ranges to test
    m_values = [8, 16, 24, 32]
    ef_construction_values = [100, 200, 300, 400]
    ef_search_values = [64, 128, 192, 256]
    
    best_config = None
    best_score = 0
    
    for m in m_values:
        for ef_construction in ef_construction_values:
            # Build index
            index = build_hnsw_index(
                sample_vectors,
                m=m,
                ef_construction=ef_construction
            )
            
            for ef_search in ef_search_values:
                # Test index
                metrics = benchmark_index(
                    index,
                    sample_vectors[:100],  # Test queries
                    ef_search=ef_search
                )
                
                # Check if meets requirements
                if (metrics['recall'] >= target_recall and 
                    metrics['latency_ms'] <= max_latency_ms):
                    
                    # Score = recall (higher better) - latency penalty
                    score = metrics['recall'] - (metrics['latency_ms'] / max_latency_ms * 0.1)
                    
                    if score > best_score:
                        best_score = score
                        best_config = {
                            "m": m,
                            "ef_construction": ef_construction,
                            "ef_search": ef_search,
                            "recall": metrics['recall'],
                            "latency_ms": metrics['latency_ms']
                        }
    
    return best_config

# Usage
# best = tune_hnsw_parameters(database[:10000], target_recall=0.95, max_latency_ms=20)
# print(f"Optimal HNSW config: m={best['m']}, ef_construction={best['ef_construction']}, ef_search={best['ef_search']}")
```

## Think of It Like This
Imagine you're organizing a massive library with 1 million books and need to help people find similar books quickly.

**Without indexing** (brute force), when someone asks "Find books similar to this mystery novel," you examine every single book in the library, reading descriptions and comparing. This takes hours.

**With a bad indexing system** (Dewey Decimal only), you organize books into 100 broad categories. When someone wants similar books, you search only the "Mystery" section—faster than checking everything, but still slow (thousands of books to compare), and you miss mysteries mis-categorized elsewhere.

**With a good indexing system** (HNSW-like), you create a sophisticated network: books are organized by similarity, with short-distance connections to very similar books and long-distance connections creating a navigable map. When someone asks for similar books, you start at any book, follow similarity connections to get closer and closer to the target region, then examine just the neighborhood—finding great matches in seconds, not hours. You might miss the absolute perfect match hiding in a distant section, but you find 95% of the best matches with 1% of the effort.

Indexing is that sophisticated organization system—trading perfect exhaustive search for practical, fast, good-enough search that makes production systems actually usable.

## The "So What?" Factor
**If you implement proper indexing:**
- Query latency drops 100-1000x (30 seconds → 30 milliseconds)
- Systems scale to millions/billions of vectors on reasonable hardware
- Production RAG systems deliver sub-second response times
- Users experience instant search (no noticeable delay)
- Cost optimization possible (right index = fewer machines needed)
- Throughput increases (handle 1000s of queries per second)
- Memory usage optimized (IVF-PQ fits 10x more vectors)
- Can measure and guarantee performance (recall, latency, memory)
- AB testing different index configurations to optimize
- Production-ready search that users actually want to use

**If you ignore indexing (brute force):**
- Queries take seconds to minutes (unusable UX)
- Cannot scale beyond 10k-100k vectors
- Users abandon system due to latency
- Need massive compute (100x more machines for acceptable speed)
- Cannot handle production query volumes
- Memory exhausted quickly
- No way to trade accuracy for speed
- Fixed cost regardless of actual needs
- Cannot optimize for your specific use case
- RAG systems remain research demos, never reach production

## Practical Checklist
Before deploying indexed vector search, ask yourself:
- [ ] Have I benchmarked index types on my actual data and queries?
- [ ] Do I understand the recall/latency/memory trade-offs for my use case?
- [ ] Have I measured baseline performance (brute force) for comparison?
- [ ] Have I tuned index parameters based on my requirements?
- [ ] Am I monitoring index performance in production (latency, recall)?
- [ ] Do I have a strategy for rebuilding indexes as data changes?
- [ ] Have I tested index performance at expected scale (not just samples)?
- [ ] Am I using appropriate distance metric (cosine, L2, dot product)?
- [ ] Have I validated recall meets quality requirements for RAG?
- [ ] Do I have alerting for index performance degradation?
- [ ] Have I documented index configuration and tuning rationale?
- [ ] Do I understand when to rebuild vs incrementally update indexes?

## Watch Out For
⚠️ **Recall degradation with scale**: Index recall measured on 100k vectors may not hold at 10M vectors. Test at production scale.

⚠️ **Parameter tuning is dataset-specific**: HNSW m=16 works great for one dataset, terrible for another. Always benchmark on YOUR data.

⚠️ **Memory estimation errors**: Indexes use more RAM than naive calculations suggest (graph overhead, metadata, etc.). Test with actual memory profiling.

⚠️ **Index staleness**: As data changes significantly, index quality degrades. Need periodic rebuilds or online updates.

⚠️ **Distance metric mismatches**: If embeddings are normalized for cosine similarity, using L2 distance produces wrong results. Match metric to embedding model.

⚠️ **Query-time parameter tuning**: HNSW `ef_search` or IVF `nprobe` critically impact latency/recall. Default values often suboptimal.

⚠️ **Batch vs single-query optimization**: Index tuned for single low-latency queries may not be optimal for batch processing. Different use cases need different configs.

⚠️ **Cold start issues**: First queries after index load may be slower (cache warming). Monitor p99 latency, not just average.

⚠️ **Dimensionality curse**: As vector dimension increases (384 → 1536 → 3072), index performance degrades. Some indexes work better for high-dim vectors.

⚠️ **Training data representativeness**: IVF indexes trained on non-representative data create poor clusters, hurting recall. Training data must match production query distribution.

## Connections
**Builds On:**
- [vector_database](vector_database.md) - Infrastructure providing indexing
- [embeddings](../Foundational_AI & ML/embeddings.md) - Vectors being indexed
- [similarity_score](similarity_score.md) - Metric for nearest neighbor search
- Data structures (graphs, trees, hash tables)

**Works With:**
- [semantic_search](semantic_search.md) - Indexing enables fast semantic search
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - RAG depends on indexed retrieval
- [reranking](reranking.md) - Fast index retrieval + accurate reranking pipeline
- [document_chunking](document_chunking.md) - Chunks are what gets indexed
- [data_pipeline](data_pipeline.md) - Pipeline includes indexing stage

**Leads To:**
- Hybrid indexes (combining multiple strategies)
- GPU-accelerated indexing
- Distributed indexes across multiple machines
- Online learning indexes (adapt to query patterns)
- Multi-modal indexes (text + images + code)

**Related Patterns:**
- [caching](caching.md) - Caching search results complements indexing
- Database indexing (B-trees, hash indexes)
- Approximate algorithms and trade-offs
- [scalability](../System_Architecture/scalability.md) - Indexing enables scale
- Performance optimization

## Quick Decision Guide
**Use HNSW when:**
- Dataset: < 10M vectors
- Need: High recall (95-99%)
- Have: Sufficient memory (~3GB per million vectors)
- Priority: Best retrieval quality
- Acceptable: Slower index building

**Use IVF-Flat when:**
- Dataset: 100k - 10M vectors
- Need: Balanced recall/speed (90-95%)
- Have: Moderate memory (~1.5GB per million vectors)
- Priority: Fast search with good quality
- Need: Dynamic updates (add/remove vectors)

**Use IVF-PQ when:**
- Dataset: 10M+ vectors
- Need: Acceptable recall (80-90%)
- Have: Limited memory (~500MB per million vectors)
- Priority: Maximum scale, minimum cost
- Acceptable: Lower recall for cost savings

**Use brute force when:**
- Dataset: < 10k vectors
- Need: Perfect recall (100%)
- Use case: Critical applications (legal, medical) where missing documents unacceptable
- Have: Time (queries < 100ms even with brute force)

**Parameter starting points:**
- **HNSW**: m=16, ef_construction=200, ef_search=128 (balanced)
- **IVF**: nlist=sqrt(N), nprobe=64 (N = num vectors)
- **IVF-PQ**: m=48, nbits=8, nprobe=64

## Further Exploration
- 📖 "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality" - Original ANN research
- 🎯 Faiss documentation - Facebook's vector index library
- 💡 "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" (HNSW paper)
- 📖 Qdrant documentation - Modern vector database with HNSW
- 🎯 "Product Quantization for Nearest Neighbor Search" - PQ compression technique
- 💡 Pinecone indexing guides - Production index optimization
- 📖 "A Survey on Learning to Hash" - LSH and learning-based indexing
- 🎯 Weaviate indexing architecture - Implementation details
- 💡 "Billion-scale similarity search with GPUs" - GPU-accelerated indexing
- 📖 ANN Benchmarks - Comprehensive index comparisons

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
