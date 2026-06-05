# Reranking

## At a Glance
| | |
|---|---|
| **Category** | Retrieval Optimization Technique |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 2-3 hours for concepts, 1-2 days for implementation |
| **Prerequisites** | Understanding of [semantic_search](semantic_search.md), [similarity_score](similarity_score.md), [embeddings](../Foundational_AI & ML/embeddings.md) |

## One-Sentence Summary
Reranking refines initial search results by applying a more sophisticated but slower model to a smaller candidate set, dramatically improving relevance at the top of your results—so your RAG system retrieves the truly best 5 documents instead of the best 5 from an imperfect initial ranking.

## Why This Matters to You
When you build RAG systems in 2026, initial [semantic_search](semantic_search.md) often gets "close but not quite right." Your [vector_database](vector_database.md) retrieves 20 potentially relevant documents in milliseconds using fast bi-encoder embeddings, but when you look at the top 5, they're not actually the most relevant—maybe the best document is ranked 7th or 12th because bi-encoders only compare query and document embeddings independently, missing subtle relevance signals. Your agent then generates answers using suboptimal context, producing mediocre results. Reranking solves this by applying a more powerful cross-encoder model that can consider the query and each document together, capturing interaction and context that bi-encoders miss. The result: You retrieve 50 candidates quickly (fast bi-encoder), rerank them with sophisticated scoring (slower cross-encoder), and select the top 5 for your LLM—dramatically improving answer quality. Studies show reranking can improve relevance by 20-40% with minimal latency increase (50-100ms for 20 candidates). This two-stage approach (fast retrieval → accurate reranking) is now standard in production RAG systems, search engines, recommendation systems, and any agent that needs to find the truly best results, not just pretty good ones. Without reranking, you're leaving significant accuracy on the table; with it, your agents deliver noticeably better answers.

## The Core Idea
### What It Is
Reranking is a two-stage retrieval optimization where an initial fast retrieval model produces candidate results, then a more sophisticated but slower model rescores those candidates to improve ranking quality at the top positions.

**The Two-Stage Pipeline:**

**Stage 1: Fast Retrieval (Bi-Encoder)**
```python
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Initialize fast bi-encoder for retrieval
retrieval_model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, 384 dimensions
vector_db = QdrantClient(host="localhost", port=6333)

def initial_retrieval(query: str, top_k: int = 50) -> list[dict]:
    """
    Stage 1: Fast retrieval using bi-encoder embeddings.
    
    Bi-encoder:
    - Encodes query and documents independently
    - Fast: Can pre-compute document embeddings, compare via dot product
    - Trade-off: Misses query-document interaction signals
    
    Returns many candidates (top_k=50) to ensure relevant docs are in the set.
    """
    query_embedding = retrieval_model.encode(query)
    
    # Fast vector search (milliseconds)
    results = vector_db.search(
        collection_name="knowledge_base",
        query_vector=query_embedding,
        limit=top_k  # Over-retrieve: get 50 to ensure good docs are present
    )
    
    return [
        {
            "id": hit.id,
            "text": hit.payload["text"],
            "retrieval_score": hit.score
        }
        for hit in results
    ]

# Example: Retrieve 50 candidates
query = "How do I handle API rate limiting in production?"
candidates = initial_retrieval(query, top_k=50)

print(f"Retrieved {len(candidates)} candidates in ~5ms")
print(f"Top candidate score: {candidates[0]['retrieval_score']:.3f}")
```

**Stage 2: Reranking (Cross-Encoder)**
```python
from sentence_transformers import CrossEncoder
import numpy as np

# Initialize cross-encoder for reranking
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')  # Slow but accurate

def rerank_results(
    query: str,
    candidates: list[dict],
    top_k: int = 5
) -> list[dict]:
    """
    Stage 2: Rerank candidates using cross-encoder.
    
    Cross-encoder:
    - Encodes query + document together (concatenated)
    - Captures interaction: How well does this specific document answer this query?
    - Slow: Cannot pre-compute, must score each (query, doc) pair
    - Much more accurate for ranking
    
    Args:
        query: User's search query
        candidates: Results from initial retrieval
        top_k: How many top results to return after reranking
    
    Returns:
        Top-k documents after reranking
    """
    # Create (query, document) pairs
    pairs = [(query, candidate["text"]) for candidate in candidates]
    
    # Score all pairs with cross-encoder (50-100ms for 50 docs)
    rerank_scores = reranker.predict(pairs)
    
    # Add rerank scores to candidates
    for candidate, rerank_score in zip(candidates, rerank_scores):
        candidate["rerank_score"] = float(rerank_score)
    
    # Sort by rerank score (not original retrieval score)
    reranked = sorted(
        candidates,
        key=lambda x: x["rerank_score"],
        reverse=True
    )
    
    # Return top-k after reranking
    return reranked[:top_k]

# Rerank the 50 candidates to find best 5
final_results = rerank_results(query, candidates, top_k=5)

print(f"\nAfter reranking:")
for i, result in enumerate(final_results, 1):
    print(f"{i}. Score: {result['rerank_score']:.3f} (was rank {candidates.index(result)+1})")
    print(f"   {result['text'][:80]}...")

# Output shows reranking often promotes results from positions 7-15 to top 5
```

**Complete RAG Pipeline with Reranking:**
```python
from openai import OpenAI

openai_client = OpenAI()

def rag_with_reranking(question: str) -> dict:
    """
    Full RAG pipeline with two-stage retrieval optimization.
    
    Pipeline:
    1. Fast retrieval: Get 50 candidates (~5ms)
    2. Rerank: Score 50 candidates, select top 5 (~50ms)
    3. Generate: Use top 5 as context for LLM (~2000ms)
    
    Total: ~2055ms (reranking adds only 50ms, 2.4% overhead)
    """
    # Stage 1: Fast retrieval
    candidates = initial_retrieval(question, top_k=50)
    
    # Stage 2: Rerank to find truly best results
    top_docs = rerank_results(question, candidates, top_k=5)
    
    # Build context from reranked results
    context = "\n\n".join([
        f"[{i+1}] {doc['text']}"
        for i, doc in enumerate(top_docs)
    ])
    
    # Stage 3: Generate answer with best context
    prompt = f"""Answer the question using the provided context. Cite sources by number [1], [2], etc.

Context:
{context}

Question: {question}

Answer:"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": top_docs,
        "retrieval_count": len(candidates)
    }

# Example usage
result = rag_with_reranking("How do I handle API rate limiting in production?")

print(f"Answer: {result['answer']}")
print(f"\nRetrieved {result['retrieval_count']} candidates, reranked to best {len(result['sources'])}")
```

**Why Two Stages?**

**Bi-Encoder (Stage 1) - Fast but Approximate:**
```python
# Bi-encoder: Independent encoding
query_embedding = encode(query)              # [0.2, 0.8, 0.3, ...]
doc_embedding = encode(document)             # [0.3, 0.7, 0.4, ...]

# Similarity via dot product (pre-computable)
score = dot_product(query_embedding, doc_embedding)

# Problem: Query and document never "see" each other
# Misses: "This specific phrase in doc answers this specific question"
```

**Cross-Encoder (Stage 2) - Slow but Accurate:**
```python
# Cross-encoder: Joint encoding
combined = concatenate(query, document)      # "query [SEP] document"
score = encode_and_score(combined)           # Model sees both together

# Captures interaction: How well does THIS doc answer THIS query?
# But: Cannot pre-compute, must score every (query, doc) pair
```

**Why Not Just Use Cross-Encoder for Everything?**
- **Scaling problem**: 1M documents × 1 query = 1M cross-encoder calls
- Cross-encoder on 1M docs = ~30 minutes (impractical)
- Bi-encoder on 1M docs = ~50ms (via vector search)

**Solution: Hybrid Approach**
1. Bi-encoder retrieves 50 candidates from 1M docs in 50ms
2. Cross-encoder reranks 50 candidates in 50ms
3. Total: 100ms (1800× faster than pure cross-encoder)

### What It Isn't
Reranking is not **just sorting by similarity**. Initial retrieval already sorted by similarity—reranking applies a *different, more sophisticated scoring function* that captures signals the initial model missed.

It's not **a replacement for good initial retrieval**. Reranking can only improve what's in the candidate set. If relevant documents aren't in the top 50, reranking can't magically retrieve them. "Garbage in, garbage out" applies—you need quality candidates first.

Reranking is not **always beneficial**. If initial retrieval is already highly accurate (e.g., exact keyword match scenarios), reranking adds latency without improving results. Use when initial ranking has room for improvement.

It's not **free**. Every candidate requires a forward pass through the reranking model. 50 candidates × 50ms each = minimal overhead, but 500 candidates × 50ms = noticeable delay. Choose candidate count wisely.

Reranking is not **deterministic with model changes**. Switching reranking models changes scores and rankings. Track model versions and validate that changes improve metrics before deploying.

Finally, it's not **interpretable by default**. Cross-encoder scores are relative rankings, not absolute relevance measures. A score of 8.2 doesn't mean "82% relevant"—it just means more relevant than documents scoring 7.5. Use thresholds cautiously.

## How It Works

### Implementing Production Reranking

**Step 1: Choose Retrieval and Reranking Models**
```python
from sentence_transformers import SentenceTransformer, CrossEncoder

# 2026 popular model combinations:

# Option 1: General purpose (English)
retrieval_model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast retrieval
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')  # Accurate reranking

# Option 2: Higher quality (larger models)
retrieval_model = SentenceTransformer('all-mpnet-base-v2')  # Better retrieval
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')  # More accurate

# Option 3: Multilingual
retrieval_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
reranker = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')  # 100+ languages

# Option 4: Domain-specific (fine-tune on your data)
retrieval_model = SentenceTransformer('path/to/finetuned-retriever')
reranker = CrossEncoder('path/to/finetuned-reranker')

# Trade-offs:
# - Larger models = better accuracy, slower inference
# - Fine-tuned models = best accuracy for your domain, requires training data
# - Multilingual models = broader language support, slightly lower per-language accuracy
```

**Step 2: Determine Optimal Candidate Count**
```python
def evaluate_candidate_count(
    test_queries: list[dict],
    candidate_counts: list[int] = [10, 20, 50, 100, 200]
) -> dict:
    """
    Find optimal number of candidates for reranking.
    
    Goal: Maximize recall@k in candidate set while minimizing reranking cost.
    
    Metrics:
    - Recall@candidate_count: Are relevant docs in the candidates?
    - Precision@5 after reranking: Are top 5 actually relevant?
    - Latency: How long does reranking take?
    """
    results = {}
    
    for count in candidate_counts:
        recalls = []
        precisions = []
        latencies = []
        
        for test in test_queries:
            query = test["query"]
            relevant_doc_ids = set(test["relevant_docs"])
            
            # Measure retrieval + reranking time
            import time
            start = time.time()
            
            # Retrieve candidates
            candidates = initial_retrieval(query, top_k=count)
            candidate_ids = [c["id"] for c in candidates]
            
            # Rerank
            final_results = rerank_results(query, candidates, top_k=5)
            final_ids = [r["id"] for r in final_results]
            
            latencies.append(time.time() - start)
            
            # Recall: Are relevant docs in candidates?
            recall = len(set(candidate_ids) & relevant_doc_ids) / len(relevant_doc_ids)
            recalls.append(recall)
            
            # Precision: Are top 5 after reranking actually relevant?
            precision = len(set(final_ids) & relevant_doc_ids) / 5
            precisions.append(precision)
        
        results[count] = {
            "recall": np.mean(recalls),
            "precision@5": np.mean(precisions),
            "latency_ms": np.mean(latencies) * 1000
        }
    
    return results

# Find sweet spot
metrics = evaluate_candidate_count(test_suite)

for count, metrics_dict in metrics.items():
    print(f"Candidates: {count}")
    print(f"  Recall: {metrics_dict['recall']:.3f}")
    print(f"  Precision@5: {metrics_dict['precision@5']:.3f}")
    print(f"  Latency: {metrics_dict['latency_ms']:.1f}ms")

# Typical finding: 50 candidates offers best recall/latency trade-off
# 20 candidates = 95% recall, 45ms
# 50 candidates = 98% recall, 55ms  ← Sweet spot
# 100 candidates = 99% recall, 95ms (diminishing returns)
```

**Step 3: Implement Hybrid Scoring**
```python
def hybrid_reranking(
    query: str,
    candidates: list[dict],
    retrieval_weight: float = 0.3,
    rerank_weight: float = 0.7,
    top_k: int = 5
) -> list[dict]:
    """
    Combine retrieval and rerank scores for robust ranking.
    
    Why hybrid:
    - Retrieval score: Fast, captures semantic similarity
    - Rerank score: Slow, captures query-document fit
    - Combined: Balanced ranking less sensitive to model quirks
    
    Typical weights: 30% retrieval, 70% rerank (rerank more trusted)
    """
    # Normalize retrieval scores to [0, 1]
    retrieval_scores = [c["retrieval_score"] for c in candidates]
    max_retrieval = max(retrieval_scores)
    min_retrieval = min(retrieval_scores)
    
    for c in candidates:
        c["retrieval_norm"] = (c["retrieval_score"] - min_retrieval) / \
                              (max_retrieval - min_retrieval + 1e-9)
    
    # Get rerank scores
    pairs = [(query, c["text"]) for c in candidates]
    rerank_scores = reranker.predict(pairs)
    
    # Normalize rerank scores to [0, 1]
    max_rerank = max(rerank_scores)
    min_rerank = min(rerank_scores)
    
    for c, score in zip(candidates, rerank_scores):
        c["rerank_norm"] = (score - min_rerank) / (max_rerank - min_rerank + 1e-9)
        
        # Compute hybrid score
        c["hybrid_score"] = (
            retrieval_weight * c["retrieval_norm"] +
            rerank_weight * c["rerank_norm"]
        )
    
    # Sort by hybrid score
    ranked = sorted(candidates, key=lambda x: x["hybrid_score"], reverse=True)
    
    return ranked[:top_k]

# Use hybrid scoring for more robust rankings
results = hybrid_reranking(query, candidates, top_k=5)
```

**Step 4: Add Diversity to Prevent Redundancy**
```python
def diverse_reranking(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    diversity_threshold: float = 0.85
) -> list[dict]:
    """
    Rerank with diversity constraint: Avoid near-duplicate results.
    
    Strategy:
    1. Select highest-scoring document
    2. For each subsequent position, skip docs too similar to already-selected
    3. Continue until top_k unique results
    
    Args:
        diversity_threshold: Skip docs with similarity > threshold to selected docs
    """
    # Rerank all candidates
    pairs = [(query, c["text"]) for c in candidates]
    rerank_scores = reranker.predict(pairs)
    
    # Sort by rerank score
    for c, score in zip(candidates, rerank_scores):
        c["rerank_score"] = float(score)
    
    ranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    
    # Select diverse top-k
    selected = []
    
    for candidate in ranked:
        if len(selected) >= top_k:
            break
        
        # Check similarity to already-selected docs
        is_diverse = True
        for selected_doc in selected:
            similarity = compute_similarity(
                candidate["text"],
                selected_doc["text"]
            )
            
            if similarity > diversity_threshold:
                is_diverse = False
                break
        
        if is_diverse:
            selected.append(candidate)
    
    return selected

def compute_similarity(text1: str, text2: str) -> float:
    """Compute semantic similarity between two texts."""
    embeddings = retrieval_model.encode([text1, text2])
    return np.dot(embeddings[0], embeddings[1]) / \
           (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
```

**Step 5: Monitor Reranking Effectiveness**
```python
def monitor_reranking_impact(
    query: str,
    candidates: list[dict],
    ground_truth_relevant: set[int]
) -> dict:
    """
    Measure reranking effectiveness vs baseline.
    
    Metrics:
    - MRR (Mean Reciprocal Rank): Position of first relevant result
    - NDCG@5: Ranking quality for top 5
    - Precision@5: What fraction of top 5 are relevant?
    """
    # Baseline: Top 5 from initial retrieval (no reranking)
    baseline_top5 = candidates[:5]
    
    # Reranked: Top 5 after reranking
    reranked_top5 = rerank_results(query, candidates, top_k=5)
    
    def calculate_metrics(results):
        # MRR: Position of first relevant result
        for rank, doc in enumerate(results, 1):
            if doc["id"] in ground_truth_relevant:
                mrr = 1 / rank
                break
        else:
            mrr = 0
        
        # Precision@5
        relevant_in_top5 = sum(
            1 for doc in results
            if doc["id"] in ground_truth_relevant
        )
        precision = relevant_in_top5 / len(results)
        
        return {"mrr": mrr, "precision@5": precision}
    
    baseline_metrics = calculate_metrics(baseline_top5)
    reranked_metrics = calculate_metrics(reranked_top5)
    
    return {
        "baseline": baseline_metrics,
        "reranked": reranked_metrics,
        "improvement": {
            "mrr": reranked_metrics["mrr"] - baseline_metrics["mrr"],
            "precision@5": reranked_metrics["precision@5"] - baseline_metrics["precision@5"]
        }
    }

# Track improvement over time
impact = monitor_reranking_impact(query, candidates, relevant_doc_ids)

print(f"Baseline MRR: {impact['baseline']['mrr']:.3f}")
print(f"Reranked MRR: {impact['reranked']['mrr']:.3f}")
print(f"Improvement: +{impact['improvement']['mrr']:.3f}")
```

## Think of It Like This
Imagine you're hiring for a specialized role.

**Initial retrieval** is like screening 1,000 resumes based on keywords (fast but superficial). You filter to candidates with "Python," "machine learning," and "5+ years experience"—this gives you 50 qualified candidates in minutes. But keyword matching misses nuance: Is their ML experience relevant to your specific problem? Do their projects align with your needs?

**Reranking** is like conducting phone screens with those 50 candidates (slower but deeper). You ask specific questions about their experience, assess fit, and evaluate how well their background matches your actual requirements. After these conversations, you discover that candidate #12 from the resume screen is actually the best fit—their projects perfectly align even though their resume didn't emphasize the right keywords. You promote them to your top 5.

In AI systems, bi-encoders are the resume screen (fast, broad), cross-encoders are the phone screens (slow, precise), and reranking is the process of using both—screen broadly, then evaluate deeply—to find the truly best matches, not just keyword-similar ones.

## The "So What?" Factor
**If you implement reranking:**
- RAG systems retrieve genuinely relevant context, not just semantically similar
- Answer quality improves 20-40% as LLMs receive better source material
- Top results are more accurate—the best document is actually ranked first
- You can over-retrieve (50 candidates) for recall, then narrow to top 5 for precision
- Latency increase is minimal (~50ms for 50 candidates, 2-4% overhead)
- Search handles subtle relevance distinctions that embeddings miss
- Agents provide more precise, better-grounded answers
- You outperform systems relying on single-stage retrieval
- User satisfaction increases—queries return what users actually wanted
- You can tune retrieval/reranking balance for your quality/latency requirements

**If you skip reranking:**
- Initial retrieval rankings are final—mediocre rankings produce mediocre answers
- Relevant documents at positions 7-15 never surface to top 5
- RAG systems use suboptimal context, generating less accurate answers
- You leave 20-40% accuracy improvement on the table
- Agents can't distinguish "pretty good" from "actually best" matches
- Single-stage retrieval must be perfect (high bar, rarely achieved)
- Search quality plateaus at bi-encoder limitations
- Competitive disadvantage vs systems using reranking
- More user frustration—results are "close but not quite right"
- Harder to debug why retrieval misses—no second scoring pass to adjust

## Practical Checklist
Before implementing reranking, ask yourself:
- [ ] Have I measured baseline retrieval quality (precision@5, MRR, NDCG)?
- [ ] Is there room for improvement? (If P@5 > 95%, reranking may not help)
- [ ] Have I chosen appropriate retrieval and reranking models for my domain?
- [ ] Have I determined optimal candidate count (typically 20-50)?
- [ ] Am I over-retrieving enough to ensure relevant docs are in candidates?
- [ ] Have I tested reranking latency with my expected load?
- [ ] Do I have evaluation metrics to measure reranking effectiveness?
- [ ] Am I using hybrid scoring (combining retrieval + rerank scores)?
- [ ] Have I considered diversity constraints to avoid redundant results?
- [ ] Am I monitoring reranking impact in production (A/B testing)?
- [ ] Do I have fallback logic if reranking fails or times out?
- [ ] Have I documented which reranking model version is deployed?

## Watch Out For
⚠️ **Insufficient candidates**: If you only retrieve 10 candidates but relevant documents are at position 15-20, reranking can't help. Over-retrieve (50+ candidates) to ensure relevant docs are present.

⚠️ **Reranking latency at scale**: Reranking 50 docs = 50ms. Reranking 500 docs = 500ms. Choose candidate count based on acceptable latency. Batch reranking requests when possible.

⚠️ **Ignoring baseline quality**: If initial retrieval is terrible (relevant docs not in top 100), fix retrieval first. Reranking only helps if good candidates are present but poorly ranked.

⚠️ **Score interpretation**: Cross-encoder scores are relative, not absolute. Don't set hard thresholds like "only use docs scoring > 8.0"—thresholds vary by query. Use ranking order instead.

⚠️ **Model version drift**: Changing reranking models changes rankings. Test new models offline before deploying. Track model versions in production.

⚠️ **Overfitting to reranker**: Don't tune entire system around reranking model quirks. Maintain strong initial retrieval—reranking should enhance, not compensate for weak retrieval.

⚠️ **No diversity control**: Reranking may promote multiple near-identical documents to top 5 (e.g., different versions of same FAQ). Add diversity constraints to ensure variety.

⚠️ **Single-model dependency**: If reranking fails or times out, have fallback (use initial retrieval rankings). Don't make reranking a single point of failure.

⚠️ **Ignoring computational costs**: Cross-encoders are more expensive than bi-encoders. For high-volume applications, consider model optimization (quantization, distillation) or caching frequent query results.

⚠️ **Not measuring impact**: Deploy reranking with A/B testing. Measure if it actually improves user metrics (click-through rate, task completion, satisfaction), not just retrieval metrics.

## Connections
**Builds On:**
- [semantic_search](semantic_search.md) - Initial retrieval stage that reranking improves
- [similarity_score](similarity_score.md) - Understanding scoring and ranking
- [embeddings](../Foundational_AI & ML/embeddings.md) - Bi-encoders vs cross-encoders
- [vector_database](vector_database.md) - Fast initial retrieval infrastructure

**Works With:**
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - RAG systems using reranking for better context
- [document_chunking](document_chunking.md) - Chunking strategies affect reranking effectiveness
- [query_optimization](query_optimization.md) - Query reformulation before retrieval/reranking
- [context_window](context_window.md) - Selecting top-k reranked docs for LLM context
- [metadata](metadata.md) - Pre-filtering before reranking to reduce candidates
- Hybrid search - Combining semantic and keyword retrieval before reranking

**Leads To:**
- Multi-stage retrieval pipelines (retrieve → filter → rerank → select)
- Learned-to-rank (LTR) systems with multiple ranking signals
- Personalized reranking (user preferences influencing scores)
- Domain-specific reranker fine-tuning

**Related Patterns:**
- [evaluation_metrics](../Testing_and_Evaluation/evaluation_metrics.md) - Measuring reranking effectiveness (MRR, NDCG, P@k)
- [caching](caching.md) - Caching reranking results for frequent queries
- Reciprocal Rank Fusion (combining multiple retrieval sources before reranking)
- Result diversification (ensuring variety in top results)

## Quick Decision Guide
**Use reranking when:**
- Initial retrieval ranking is imperfect (relevant docs present but poorly ranked)
- Answer quality matters more than minimal latency
- You have 10-100 candidates to rerank (manageable scope)
- Building RAG systems where context quality is critical
- Users need the truly best results, not just pretty good ones
- You can afford 50-100ms latency overhead per query
- Precision at top positions (P@1, P@5) is key metric

**Skip reranking when:**
- Initial retrieval is already highly accurate (P@5 > 95%)
- Latency requirements are extremely strict (<10ms total)
- Candidate set is massive (>500 docs, reranking too slow)
- Simple keyword exact-match scenarios where reranking adds no value
- Computational budget is tight (reranking adds inference cost)
- Use simpler solutions first, add reranking if needed

**Consider alternatives:**
- Better initial retrieval models (upgrade embeddings)
- Hybrid search (semantic + keyword) may obviate reranking
- Query expansion or reformulation
- Metadata filtering to reduce candidate set

## Further Exploration
- 📖 "Contextualized Reranking with Cross-Encoders" - Understanding cross-encoder architectures
- 🎯 Sentence-Transformers reranking guide - Implementation patterns
- 💡 "In-Batch Negatives for Knowledge Retrieval" - Training better retrieval/reranking models
- 📖 "BEIR: A Heterogeneous Benchmark for Information Retrieval" - Evaluating reranking effectiveness
- 🎯 "Dense Passage Retrieval + Reranking" - Two-stage pipeline design
- 💡 LangChain reranking integrations - Production patterns
- 📖 "RankGPT: LLMs as Rerankers" - Using LLMs for reranking (2024+)
- 🎯 Cohere Rerank API - Commercial reranking service
- 💡 "From Retrieval to Generation: Optimizing RAG Pipelines" - End-to-end optimization
- 📖 "Learning to Rank for Information Retrieval" - Theoretical foundations

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
