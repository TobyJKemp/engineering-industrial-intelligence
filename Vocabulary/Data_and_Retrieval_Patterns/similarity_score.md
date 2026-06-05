# Similarity Score

## At a Glance
| | |
|---|---|
| **Category** | Measurement / Retrieval Metric |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for fundamentals, ongoing practice for threshold tuning |
| **Prerequisites** | Understanding of [embeddings](../Foundational_AI & ML/embeddings.md), [vector_database](vector_database.md), basic vector mathematics |

## One-Sentence Summary
A similarity score is a numerical measurement (typically 0-1 or -1 to 1) quantifying how similar two items are—like determining that "vehicle maintenance issues" (0.87 similarity) is much more related to "car problems" than "cooking recipes" (0.12 similarity) by comparing their vector embeddings.

## Why This Matters to You
When you build AI agent systems in 2026, nearly every retrieval operation depends on similarity scores. Your RAG agent searches a knowledge base for relevant context—how does it decide which documents are "relevant"? It computes similarity scores between the query embedding and document embeddings, retrieving items with scores above a threshold (e.g., > 0.7). Your recommendation system suggests similar products—similarity scores determine "similar." Your agent checks if a generated answer matches expected output—similarity score quantifies the match. Without understanding similarity scores, you can't interpret why your RAG system retrieves certain documents, debug poor retrieval quality, set appropriate thresholds, or optimize search relevance. A score of 0.95 might seem "highly relevant" but could be meaningless if your threshold is wrong. A score of 0.65 might be great for some use cases, poor for others. Similarity scores are the fundamental metric that powers [semantic_search](semantic_search.md), [vector_database](vector_database.md) queries, [reranking](reranking.md), and nearly every retrieval decision your agents make. Understanding what they measure, how they're calculated, and how to interpret them is essential for building effective retrieval systems.

## The Core Idea
### What It Is
A similarity score quantifies how alike two items are, typically represented as vectors (embeddings). The score is a single number derived from comparing vector representations, with higher scores indicating greater similarity (or lower distance, depending on the metric).

**Common Similarity Metrics:**

**1. Cosine Similarity**:
Measures the angle between two vectors. Range: -1 (opposite directions) to 1 (same direction).
```python
import numpy as np

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    Returns: -1 to 1 (1 = identical direction, 0 = orthogonal, -1 = opposite)
    """
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

# Example: Semantic similarity between sentences
query_embedding = embed("How do I reset my password?")
doc1_embedding = embed("Password reset instructions")
doc2_embedding = embed("Ice cream recipes")

score1 = cosine_similarity(query_embedding, doc1_embedding)  # 0.87 (high similarity)
score2 = cosine_similarity(query_embedding, doc2_embedding)  # 0.12 (low similarity)

# Most common in semantic search (2026 standard)
# Works well for embeddings because it's magnitude-invariant
```

**Why cosine is popular**: It measures direction similarity regardless of magnitude. Two vectors pointing the same direction have similarity 1.0 even if one is twice as long. Perfect for embeddings where magnitude is less meaningful than direction.

**2. Euclidean Distance (L2 Distance)**:
Straight-line distance between two points in vector space. Range: 0 (identical) to ∞ (further apart = less similar).
```python
def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute Euclidean distance between two vectors.
    Returns: 0 to infinity (0 = identical, larger = less similar)
    """
    return np.sqrt(np.sum((vec1 - vec2) ** 2))

# Convert to similarity score (0-1 range)
def euclidean_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Convert Euclidean distance to 0-1 similarity."""
    distance = euclidean_distance(vec1, vec2)
    return 1 / (1 + distance)  # Closer to 0 = higher similarity

distance = euclidean_distance(query_embedding, doc1_embedding)  # 2.3
similarity = euclidean_similarity(query_embedding, doc1_embedding)  # 0.30

# Less common for high-dimensional embeddings
# Suffers from "curse of dimensionality"
```

**3. Dot Product**:
Sum of element-wise multiplications. Range: -∞ to ∞ (for normalized vectors: -1 to 1).
```python
def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute dot product between two vectors.
    For unit-normalized vectors, equivalent to cosine similarity.
    """
    return np.dot(vec1, vec2)

# For normalized embeddings (unit length), dot product = cosine similarity
normalized_query = query_embedding / np.linalg.norm(query_embedding)
normalized_doc = doc1_embedding / np.linalg.norm(doc1_embedding)

score = dot_product(normalized_query, normalized_doc)  # 0.87 (same as cosine)

# Faster than cosine (no division) if vectors are pre-normalized
# Common optimization in vector databases
```

**4. Manhattan Distance (L1 Distance)**:
Sum of absolute differences along each dimension.
```python
def manhattan_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute Manhattan (city-block) distance.
    Returns: 0 to infinity (0 = identical)
    """
    return np.sum(np.abs(vec1 - vec2))

# Rarely used for embeddings
# More common for categorical features or sparse data
```

**5. Jaccard Similarity** (for sets, not vectors):
Measures overlap between sets. Range: 0 (no overlap) to 1 (identical sets).
```python
def jaccard_similarity(set1: set, set2: set) -> float:
    """
    Compute Jaccard similarity between two sets.
    Returns: 0 to 1 (1 = identical sets)
    """
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union

# For keyword overlap, tag similarity
query_keywords = {"password", "reset", "account"}
doc1_keywords = {"password", "reset", "instructions", "account"}
doc2_keywords = {"recipe", "cooking", "ingredients"}

score1 = jaccard_similarity(query_keywords, doc1_keywords)  # 0.75 (high overlap)
score2 = jaccard_similarity(query_keywords, doc2_keywords)  # 0.0 (no overlap)

# Used in hybrid search alongside vector similarity
```

**In 2026 AI Agent Systems:**

**RAG Retrieval with Similarity Scores**:
```python
def retrieve_relevant_documents(
    query: str,
    vector_db,
    top_k: int = 5,
    similarity_threshold: float = 0.7
) -> list[dict]:
    """
    Retrieve documents with similarity scores above threshold.
    
    Args:
        query: User question
        vector_db: Vector database client
        top_k: Maximum documents to retrieve
        similarity_threshold: Minimum similarity score (0-1)
    
    Returns:
        List of documents with similarity scores
    """
    # Generate query embedding
    query_embedding = embedding_model.embed(query)
    
    # Search vector database
    results = vector_db.search(
        vector=query_embedding,
        limit=top_k,
        score_threshold=similarity_threshold  # Only return docs with score >= 0.7
    )
    
    # Format results with scores
    documents = []
    for result in results:
        documents.append({
            "text": result.payload["text"],
            "score": result.score,  # Similarity score (0-1)
            "metadata": result.payload.get("metadata", {})
        })
    
    return documents

# Example usage
docs = retrieve_relevant_documents(
    query="How do I implement retry logic?",
    vector_db=client,
    top_k=3,
    similarity_threshold=0.75  # Only highly relevant docs
)

for doc in docs:
    print(f"Score: {doc['score']:.3f} - {doc['text'][:100]}")
# Output:
# Score: 0.891 - Retry logic with exponential backoff is essential...
# Score: 0.847 - Implement retries using decorators for clean code...
# Score: 0.782 - Error handling and retry strategies for APIs...
```

**Adaptive Threshold Based on Score Distribution**:
```python
def retrieve_with_adaptive_threshold(
    query: str,
    vector_db,
    min_docs: int = 3,
    max_docs: int = 10,
    base_threshold: float = 0.7
) -> list[dict]:
    """
    Retrieve documents with adaptive threshold based on score distribution.
    
    Strategy:
    - If top results have very high scores (>0.9), use high threshold
    - If top results are mediocre (<0.8), lower threshold to get enough docs
    - Always return at least min_docs, at most max_docs
    """
    query_embedding = embedding_model.embed(query)
    
    # Get more candidates than needed
    candidates = vector_db.search(
        vector=query_embedding,
        limit=max_docs * 2
    )
    
    if not candidates:
        return []
    
    # Analyze score distribution
    top_score = candidates[0].score
    
    # Adaptive threshold logic
    if top_score > 0.9:
        # Very relevant results - be selective
        threshold = 0.85
    elif top_score > 0.8:
        # Good results - use standard threshold
        threshold = base_threshold
    else:
        # Mediocre results - lower threshold to get enough docs
        threshold = max(0.5, top_score - 0.2)
    
    # Filter by threshold
    filtered = [c for c in candidates if c.score >= threshold]
    
    # Ensure min/max constraints
    if len(filtered) < min_docs:
        filtered = candidates[:min_docs]  # Return best available
    elif len(filtered) > max_docs:
        filtered = filtered[:max_docs]  # Cap at maximum
    
    return [
        {
            "text": r.payload["text"],
            "score": r.score,
            "metadata": r.payload.get("metadata", {})
        }
        for r in filtered
    ]
```

**Similarity Score for Answer Validation**:
```python
def validate_answer_similarity(
    generated_answer: str,
    expected_answer: str,
    threshold: float = 0.8
) -> dict:
    """
    Check if generated answer is semantically similar to expected answer.
    
    Used in:
    - Testing/evaluation
    - Quality assurance
    - Regression detection
    """
    # Generate embeddings
    generated_embedding = embedding_model.embed(generated_answer)
    expected_embedding = embedding_model.embed(expected_answer)
    
    # Compute similarity
    similarity = cosine_similarity(generated_embedding, expected_embedding)
    
    return {
        "similarity_score": similarity,
        "passes_threshold": similarity >= threshold,
        "generated": generated_answer,
        "expected": expected_answer
    }

# Example: Testing agent responses
result = validate_answer_similarity(
    generated_answer="To reset your password, go to Settings > Account > Reset Password",
    expected_answer="Navigate to Settings, then Account, and click Reset Password",
    threshold=0.8
)

print(f"Similarity: {result['similarity_score']:.3f}")  # 0.92
print(f"Passes: {result['passes_threshold']}")  # True
```

### What It Isn't
A similarity score is not **absolute truth**. A score of 0.85 doesn't mean "85% similar" in any universal sense. It's a relative measurement within your embedding space. Scores are meaningful for comparison (0.85 > 0.65 = first item more similar) but not as standalone percentages.

It's not **the same across metrics**. Cosine similarity of 0.7 is not comparable to Euclidean distance of 0.7. Different metrics have different ranges and interpretations. Always know which metric you're using and what its range represents.

Similarity scores are not **constant across embedding models**. The same two texts embedded with different models produce different similarity scores. GPT-4 embeddings might give 0.82, Sentence-BERT might give 0.74 for the same comparison. Scores are tied to the embedding space.

They're not **calibrated probabilities**. A similarity score of 0.9 doesn't mean "90% probability of relevance." Scores aren't probabilistic unless specifically calibrated. Use them for ranking and thresholding, not as probabilities.

Similarity scores are not **free from bias**. If your embedding model has biases (associating certain concepts incorrectly), similarity scores inherit those biases. High similarity might reflect embedding artifacts rather than true semantic relatedness.

Finally, they're not **the only relevance signal**. Similarity score is one factor in determining relevance. Combine with metadata (recency, source authority, user context), keyword matching (hybrid search), and [reranking](reranking.md) for better results.

## How It Works

### Computing Similarity Scores

**Basic Vector Comparison**:
```python
from openai import OpenAI

client = OpenAI()

def compute_similarity(text1: str, text2: str) -> float:
    """Compute similarity between two texts using embeddings."""
    # Generate embeddings
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text1, text2]
    )
    
    embedding1 = np.array(response.data[0].embedding)
    embedding2 = np.array(response.data[1].embedding)
    
    # Compute cosine similarity
    similarity = cosine_similarity(embedding1, embedding2)
    
    return similarity

# Example comparisons
score1 = compute_similarity(
    "The cat sat on the mat",
    "A feline rested on the rug"
)  # 0.89 - semantically similar

score2 = compute_similarity(
    "The cat sat on the mat",
    "Quantum computing is complex"
)  # 0.23 - semantically different
```

**Batch Similarity Computation**:
```python
def compute_similarity_matrix(texts: list[str]) -> np.ndarray:
    """
    Compute pairwise similarity between all texts.
    
    Returns:
        NxN matrix where entry [i,j] is similarity between texts[i] and texts[j]
    """
    # Generate all embeddings in one batch
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    
    # Extract embeddings
    embeddings = np.array([d.embedding for d in response.data])
    
    # Compute pairwise similarities
    # Normalize embeddings for dot product = cosine similarity
    normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    # Similarity matrix via matrix multiplication
    similarity_matrix = np.dot(normalized, normalized.T)
    
    return similarity_matrix

# Example: Find most similar pairs in a collection
texts = [
    "Machine learning algorithms",
    "AI and neural networks",
    "Cooking pasta recipes",
    "Deep learning models",
    "Baking bread at home"
]

sim_matrix = compute_similarity_matrix(texts)

# Print similarities
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        print(f"{texts[i][:20]:20} <-> {texts[j][:20]:20} : {sim_matrix[i,j]:.3f}")

# Output:
# Machine learning... <-> AI and neural net... : 0.892
# Machine learning... <-> Cooking pasta re... : 0.234
# Machine learning... <-> Deep learning mo... : 0.911
# Machine learning... <-> Baking bread at ... : 0.198
# AI and neural net... <-> Cooking pasta re... : 0.221
# ...
```

### Setting Thresholds

**Empirical Threshold Determination**:
```python
def find_optimal_threshold(
    queries: list[str],
    relevant_docs: dict[str, list[str]],
    candidates: dict[str, list[tuple[str, float]]]
) -> float:
    """
    Find optimal similarity threshold by maximizing F1 score.
    
    Args:
        queries: List of test queries
        relevant_docs: Ground truth - which docs are relevant for each query
        candidates: Retrieved candidates with similarity scores
    
    Returns:
        Optimal threshold value
    """
    # Test different thresholds
    thresholds = np.arange(0.5, 0.95, 0.05)
    best_f1 = 0
    best_threshold = 0.7
    
    for threshold in thresholds:
        total_precision = 0
        total_recall = 0
        
        for query in queries:
            # Apply threshold
            retrieved = [
                doc for doc, score in candidates[query]
                if score >= threshold
            ]
            
            # Calculate metrics
            relevant_set = set(relevant_docs[query])
            retrieved_set = set(retrieved)
            
            true_positives = len(relevant_set & retrieved_set)
            
            if len(retrieved_set) > 0:
                precision = true_positives / len(retrieved_set)
            else:
                precision = 0
            
            if len(relevant_set) > 0:
                recall = true_positives / len(relevant_set)
            else:
                recall = 0
            
            total_precision += precision
            total_recall += recall
        
        # Average metrics
        avg_precision = total_precision / len(queries)
        avg_recall = total_recall / len(queries)
        
        # F1 score
        if avg_precision + avg_recall > 0:
            f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall)
        else:
            f1 = 0
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    print(f"Optimal threshold: {best_threshold:.2f} (F1: {best_f1:.3f})")
    return best_threshold
```

**Context-Specific Thresholds**:
```python
# Different thresholds for different use cases

# High precision needed (customer-facing, safety-critical)
STRICT_THRESHOLD = 0.85  # Only very confident matches

# Balanced (general RAG)
STANDARD_THRESHOLD = 0.7  # Good relevance

# High recall needed (exploratory search, research)
LENIENT_THRESHOLD = 0.55  # Broader results

# Adaptive based on query type
def get_threshold_for_query(query: str) -> float:
    """Choose threshold based on query characteristics."""
    if is_factual_query(query):
        return 0.85  # Strict for facts
    elif is_exploratory_query(query):
        return 0.6   # Lenient for exploration
    else:
        return 0.7   # Standard
```

## Think of It Like This
Imagine you're a librarian helping someone find books similar to one they enjoyed.

**Without similarity scores**, you can only say "yes, this is similar" or "no, it's not." Every book is either similar or not, with no way to express degrees of similarity.

**With similarity scores**, you can say:
- "This book is 0.95 similar—almost identical genre, theme, and style"
- "This one is 0.78 similar—same genre, different tone"
- "This is 0.42 similar—shares one theme but otherwise quite different"
- "This is 0.12 similar—barely related at all"

The scores let you rank recommendations (show highest scores first), set thresholds ("only show books above 0.7 similarity"), and make informed decisions about which books to recommend. In AI systems, similarity scores do the same—they quantify how similar items are in vector space, enabling ranking, filtering, and informed retrieval decisions.

## The "So What?" Factor
**If you understand and use similarity scores effectively:**
- You can set appropriate thresholds for retrieval quality (high precision vs high recall)
- You debug poor retrieval by inspecting score distributions (are scores too low? too uniform?)
- You rank results meaningfully—showing most relevant items first
- You implement adaptive strategies—adjusting behavior based on score magnitudes
- You combine multiple signals—similarity scores + metadata + keywords
- You evaluate system quality objectively—measuring precision/recall at different thresholds
- You detect when embeddings are poor—unusually low or uniform scores
- You optimize retrieval—balancing score thresholds with latency and cost
- You explain retrieval decisions—"retrieved because similarity was 0.87"
- You A/B test retrieval strategies—comparing score distributions across approaches

**If you don't understand similarity scores:**
- Retrieval thresholds are arbitrary—0.7 "feels right" without justification
- Poor retrieval is mysterious—you don't know if scores are low, uniform, or biased
- Results are unsorted or arbitrarily sorted—missing the ranking signal
- Strategies are rigid—can't adapt behavior based on confidence
- Retrieval is one-dimensional—ignoring other valuable signals
- Quality evaluation is subjective—no objective measurement framework
- Embedding problems go undetected—you don't recognize when vectors are poor
- Over-retrieval or under-retrieval due to wrong thresholds
- Can't explain to stakeholders why certain documents were retrieved
- Can't systematically improve—no data to guide optimization

## Practical Checklist
Before relying on similarity scores, ask yourself:
- [ ] Do I know which similarity metric my vector database uses (cosine, euclidean, dot product)?
- [ ] Have I empirically determined appropriate thresholds for my use case?
- [ ] Am I inspecting score distributions to understand retrieval quality?
- [ ] Do I normalize embeddings if using dot product similarity?
- [ ] Have I tested similarity scores on known similar/dissimilar pairs?
- [ ] Am I considering score magnitude alongside metadata and other signals?
- [ ] Do I understand the range of my similarity metric (-1 to 1? 0 to 1? 0 to ∞)?
- [ ] Have I evaluated precision and recall at different threshold values?
- [ ] Am I monitoring score distributions over time for degradation?
- [ ] Do I have strategies for queries with uniformly low similarity scores?
- [ ] Am I using scores for ranking, not just binary filtering?
- [ ] Have I documented threshold choices and their rationale?

## Watch Out For
⚠️ **Absolute interpretation**: Treating similarity scores as absolute measures ("0.8 = 80% similar"). Scores are relative rankings within an embedding space, not universal percentages. Use for comparison and thresholding, not absolute claims.

⚠️ **Ignoring metric differences**: Comparing cosine similarity 0.7 to Euclidean distance 0.7 as if they're equivalent. Different metrics have different ranges and meanings. Know your metric and interpret accordingly.

⚠️ **Universal thresholds**: Using 0.7 as a threshold everywhere without validation. Optimal thresholds vary by use case, embedding model, and data distribution. Empirically determine thresholds for your specific context.

⚠️ **Uniform score distributions**: All similarity scores clustering around 0.5-0.6 with little variance. This suggests poor embeddings that don't discriminate between relevant and irrelevant items. Investigate embedding quality.

⚠️ **Ignoring outliers**: Very high scores (>0.98) might indicate duplicates or near-duplicates. Very low scores (<0.3) for expected matches indicate embedding issues. Investigate anomalies.

⚠️ **Magnitude confusion with dot product**: Using dot product similarity without normalizing embeddings. Unnormalized dot product is influenced by vector magnitude, not just direction. Normalize vectors or use cosine explicitly.

⚠️ **No score calibration**: Assuming scores from different embedding models are comparable. GPT-4 embeddings and Sentence-BERT embeddings produce different score distributions for the same comparisons. Calibrate thresholds per model.

⚠️ **Binary thinking**: Using similarity scores only as pass/fail (above/below threshold). Scores carry ranking information—use them to sort results, not just filter.

⚠️ **Embedding drift**: Similarity scores change when you switch embedding models or retrain. Document which embedding model was used and recalibrate thresholds when models change.

⚠️ **Curse of dimensionality**: In very high-dimensional spaces (3000+ dimensions), Euclidean distance becomes less discriminative—all points seem far apart. Prefer cosine similarity for high-dimensional embeddings.

## Connections
**Builds On:**
- [embeddings](../Foundational_AI & ML/embeddings.md) - Vector representations being compared
- Vector mathematics and distance metrics
- Linear algebra (dot products, norms)

**Works With:**
- [vector_database](vector_database.md) - Databases compute and return similarity scores
- [semantic_search](semantic_search.md) - Uses similarity scores to rank results
- [reranking](reranking.md) - Refines initial similarity-based retrieval
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - RAG relies on similarity scores for context retrieval
- [evaluation_metrics](../Testing_and_Evaluation/evaluation_metrics.md) - Similarity scores used to evaluate quality
- Nearest neighbor algorithms

**Leads To:**
- Ranking algorithms
- Threshold optimization
- Retrieval quality metrics (precision@k, recall@k, NDCG)
- Multi-vector search strategies
- Hybrid search (combining similarity with other signals)

**Related Patterns:**
- [confidence_threshold](../Safety_and_Control/confidence_threshold.md) - Similar concept for confidence scores
- Information retrieval theory
- Recommendation systems
- Duplicate detection
- Clustering algorithms

## Quick Decision Guide
**Pay close attention to similarity scores when:**
- Building RAG systems where retrieval quality is critical
- Debugging poor retrieval performance (low relevance, missing documents)
- Optimizing threshold values for precision/recall trade-offs
- Implementing adaptive retrieval strategies
- Evaluating embedding model quality
- A/B testing different retrieval approaches
- Explaining why specific documents were retrieved

**Treat scores as secondary when:**
- Other signals (metadata, keywords, recency) dominate relevance
- Using reranking that overrides initial similarity ranking
- Scores are uniformly high (everything above threshold)
- Building prototypes where rough relevance suffices
- Scores are just one input to a complex ranking function
- End users don't need to understand retrieval mechanics

## Further Exploration
- 📖 "Introduction to Information Retrieval" (Manning et al.) - Distance metrics and similarity measures
- 🎯 scikit-learn metrics documentation - Similarity and distance functions
- 💡 "Understanding Cosine Similarity" - Deep dive on the most common metric
- 📖 Vector database documentation (Pinecone, Qdrant, Weaviate) - Similarity metric implementations
- 🎯 "The Curse of Dimensionality in Distance Metrics" - Understanding high-dimensional similarity
- 💡 "Calibrating Similarity Scores" - Making scores interpretable
- 📖 "Evaluating Retrieval Quality" - Precision, recall, and NDCG using similarity scores
- 🎯 "Hybrid Search Strategies" - Combining similarity with other signals
- 💡 "Optimal Threshold Selection" - Methods for threshold tuning
- 📖 "Embeddings and Semantic Similarity" - Connection between embeddings and scores

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
