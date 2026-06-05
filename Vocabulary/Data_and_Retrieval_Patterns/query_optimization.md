# Query Optimization

## At a Glance
| | |
|---|---|
| **Category** | Retrieval Enhancement Technique |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 2-4 hours for fundamentals, weeks for mastery |
| **Prerequisites** | Understanding of [semantic_search](semantic_search.md), [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md), [embeddings](../Foundational_AI & ML/embeddings.md) |

## One-Sentence Summary
Query optimization transforms user queries into better search queries through techniques like reformulation, expansion, and decomposition—so the vague question "fix API problems" becomes specific searches for "API authentication errors," "API rate limiting solutions," and "API timeout troubleshooting," dramatically improving retrieval quality.

## Why This Matters to You
When you build RAG systems in 2026, users rarely phrase queries optimally for retrieval. A user asks "car won't start," but your knowledge base uses terms like "ignition failure," "battery issues," and "starter motor problems"—vocabulary mismatch means poor retrieval. A user types "improve performance," which is hopelessly ambiguous without context (database performance? API performance? UI performance?). A complex question like "How do I secure and scale my API?" needs decomposition into separate searches for authentication, rate limiting, infrastructure scaling, and monitoring. Query optimization solves this by transforming raw user input into optimized queries that match how your knowledge base is structured and worded. Techniques include reformulation (rewrite query for clarity), expansion (add synonyms and related terms), decomposition (break complex questions into sub-queries), contextualization (add user/session context), and specification (add filters and constraints). The impact is dramatic: Studies show query optimization can improve retrieval precision by 30-50% in RAG systems. Your agent can understand that "auth broken" means "authentication failures," expand it to include "login errors" and "access denied," and add context like "for production API." Without query optimization, you're searching with user's exact words—often too vague, too broad, or using wrong terminology. With it, you're searching with refined, targeted queries that retrieve genuinely relevant information, leading to better agent answers and higher user satisfaction.

## The Core Idea
### What It Is
Query optimization is the process of transforming, enhancing, or decomposing user queries to improve retrieval quality by bridging vocabulary gaps, adding context, reducing ambiguity, and matching queries to how knowledge bases are structured.

**Five Core Query Optimization Strategies:**

**1. Query Reformulation - Rewrite for Clarity**
```python
from openai import OpenAI

openai_client = OpenAI()

def reformulate_query(raw_query: str, domain: str = "general") -> str:
    """
    Reformulate vague or poorly-worded queries for better retrieval.
    
    Use LLM to:
    - Fix spelling/grammar
    - Expand abbreviations  
    - Clarify intent
    - Use domain-appropriate terminology
    """
    prompt = f"""You are a query optimization expert for a {domain} knowledge base.

Reformulate this user query to be clearer and more specific for semantic search. Use standard terminology, expand abbreviations, and clarify intent. Return only the reformulated query.

Original query: {raw_query}

Reformulated query:"""

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # Low temperature for consistency
    )
    
    return response.choices[0].message.content.strip()

# Examples showing dramatic improvement
examples = [
    "auth broken",          # → "authentication failures in API"
    "db slow",              # → "database query performance issues"
    "cant login",           # → "login authentication errors"
    "api timeout",          # → "API request timeout errors"
    "improve perf"          # → "improve system performance"
]

for query in examples:
    optimized = reformulate_query(query, domain="technical")
    print(f"Original: {query}")
    print(f"Optimized: {optimized}\n")

# Output shows clearer, more searchable queries:
# Original: auth broken
# Optimized: authentication failures in API endpoints
#
# Original: db slow  
# Optimized: database query performance optimization
```

**2. Query Expansion - Add Synonyms and Related Terms**
```python
def expand_query_with_synonyms(query: str) -> list[str]:
    """
    Expand query with synonyms and related terms.
    
    Strategy:
    - Generate semantic variations
    - Add domain-specific synonyms
    - Include common misspellings/abbreviations
    
    Returns multiple query variations for parallel search.
    """
    expansion_prompt = f"""Generate 3-5 semantic variations of this query using synonyms and related terms. Return as a Python list.

Query: {query}

Variations:"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": expansion_prompt}],
        temperature=0.5  # Moderate temperature for variety
    )
    
    # Parse response (simplified - would need robust parsing)
    variations = eval(response.choices[0].message.content.strip())
    
    return [query] + variations  # Original + expanded

# Example expansion
query = "authentication errors"
expanded = expand_query_with_synonyms(query)

print(f"Original: {query}")
print(f"Expanded to {len(expanded)} variations:")
for i, var in enumerate(expanded, 1):
    print(f"  {i}. {var}")

# Output:
# Original: authentication errors
# Expanded to 5 variations:
#   1. authentication errors
#   2. login failures  
#   3. access denied issues
#   4. credential validation problems
#   5. authorization failures

# Search with all variations, merge results
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def search_with_expansion(expanded_queries: list[str]) -> list[dict]:
    """Search with multiple query variations, merge results."""
    all_results = {}
    
    for query_var in expanded_queries:
        embedding = model.encode(query_var)
        results = vector_db.search(
            collection_name="knowledge_base",
            query_vector=embedding,
            limit=20
        )
        
        # Merge results by document ID, keep highest score
        for hit in results:
            doc_id = hit.id
            if doc_id not in all_results or hit.score > all_results[doc_id]["score"]:
                all_results[doc_id] = {
                    "id": doc_id,
                    "text": hit.payload["text"],
                    "score": hit.score,
                    "matched_query": query_var
                }
    
    # Sort by score
    merged = sorted(all_results.values(), key=lambda x: x["score"], reverse=True)
    
    return merged[:10]  # Top 10 after merging

results = search_with_expansion(expanded)
print(f"\nMerged {len(results)} unique results from {len(expanded)} query variations")
```

**3. Query Decomposition - Break Complex Questions Apart**
```python
def decompose_complex_query(complex_query: str) -> list[dict]:
    """
    Decompose complex multi-part questions into focused sub-queries.
    
    Example:
    "How do I secure and scale my API?"
    →  
    1. "API authentication and authorization methods"
    2. "API rate limiting implementation"  
    3. "API horizontal scaling strategies"
    4. "API security best practices"
    """
    decomposition_prompt = f"""This question has multiple aspects. Break it into 3-5 focused sub-questions that can be searched independently. Return as JSON array with format: [{{"aspect": "category", "query": "focused question"}}]

Complex question: {complex_query}

Sub-questions:"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": decomposition_prompt}],
        response_format={"type": "json_object"}
    )
    
    import json
    subqueries = json.loads(response.choices[0].message.content)
    
    return subqueries.get("questions", [])

# Example decomposition
complex_q = "How do I build a secure, scalable, and observable API?"

subqueries = decompose_complex_query(complex_q)

print(f"Complex query: {complex_q}\n")
print(f"Decomposed into {len(subqueries)} focused sub-queries:")
for i, sq in enumerate(subqueries, 1):
    print(f"  {i}. [{sq['aspect']}] {sq['query']}")

# Output:
# Complex query: How do I build a secure, scalable, and observable API?
#
# Decomposed into 4 focused sub-queries:
#   1. [Security] API authentication and authorization implementation
#   2. [Security] API input validation and security best practices
#   3. [Scalability] API horizontal scaling and load balancing
#   4. [Observability] API monitoring, logging, and tracing

def search_with_decomposition(subqueries: list[dict]) -> dict:
    """
    Search with each sub-query independently, organize by aspect.
    
    Returns comprehensive answer covering all aspects.
    """
    results_by_aspect = {}
    
    for sq in subqueries:
        aspect = sq["aspect"]
        query = sq["query"]
        
        # Search for this aspect
        embedding = model.encode(query)
        results = vector_db.search(
            collection_name="knowledge_base",
            query_vector=embedding,
            limit=5  # Fewer per sub-query
        )
        
        results_by_aspect[aspect] = {
            "query": query,
            "results": [
                {
                    "text": hit.payload["text"],
                    "score": hit.score
                }
                for hit in results
            ]
        }
    
    return results_by_aspect

# Search and organize by aspect
organized_results = search_with_decomposition(subqueries)

for aspect, data in organized_results.items():
    print(f"\n{aspect}:")
    print(f"  Query: {data['query']}")
    print(f"  Found: {len(data['results'])} relevant documents")
```

**4. Contextual Query Enhancement - Add User/Session Context**
```python
class ContextualQueryOptimizer:
    """
    Enhance queries with user and session context.
    
    Context sources:
    - User profile (role, department, permissions)
    - Session history (previous queries, viewed docs)
    - Current conversation (multi-turn context)
    - System state (environment, version)
    """
    
    def __init__(self):
        self.session_history = {}
    
    def optimize_with_context(
        self,
        query: str,
        user_id: str,
        session_id: str,
        conversation_history: list[str] = None
    ) -> dict:
        """Add contextual information to improve query."""
        
        # Get user context
        user_profile = self.get_user_profile(user_id)
        
        # Get session context
        session_context = self.session_history.get(session_id, {
            "previous_queries": [],
            "viewed_docs": [],
            "inferred_intent": None
        })
        
        # Build contextual enhancement
        context_parts = []
        
        # Add user role context
        if user_profile.get("role"):
            context_parts.append(f"for {user_profile['role']}")
        
        # Add department context
        if user_profile.get("department"):
            context_parts.append(f"in {user_profile['department']} context")
        
        # Add conversation context (multi-turn)
        if conversation_history and len(conversation_history) > 0:
            previous = conversation_history[-1]
            context_parts.append(f"following up on: {previous}")
        
        # Add session context (inferred intent)
        if session_context.get("inferred_intent"):
            context_parts.append(f"related to {session_context['inferred_intent']}")
        
        # Build enhanced query
        if context_parts:
            enhanced = f"{query} ({', '.join(context_parts)})"
        else:
            enhanced = query
        
        # Update session history
        session_context["previous_queries"].append(query)
        self.session_history[session_id] = session_context
        
        return {
            "original_query": query,
            "enhanced_query": enhanced,
            "context_applied": context_parts,
            "user_filters": {
                "department": user_profile.get("department"),
                "access_level": user_profile.get("access_level")
            }
        }
    
    def get_user_profile(self, user_id: str) -> dict:
        """Fetch user profile from system."""
        # Simplified - would query user management system
        return {
            "role": "software_engineer",
            "department": "engineering",
            "access_level": "internal"
        }

# Example with context
optimizer = ContextualQueryOptimizer()

# First query in session
result1 = optimizer.optimize_with_context(
    query="authentication setup",
    user_id="user123",
    session_id="session_abc"
)

print("Query 1 (no conversation history):")
print(f"  Original: {result1['original_query']}")
print(f"  Enhanced: {result1['enhanced_query']}")

# Follow-up query (multi-turn)
result2 = optimizer.optimize_with_context(
    query="how to test it",
    user_id="user123",
    session_id="session_abc",
    conversation_history=["authentication setup"]
)

print("\nQuery 2 (with conversation history):")
print(f"  Original: {result2['original_query']}")
print(f"  Enhanced: {result2['enhanced_query']}")
print(f"  Context: {', '.join(result2['context_applied'])}")

# Output:
# Query 1 (no conversation history):
#   Original: authentication setup
#   Enhanced: authentication setup (for software_engineer, in engineering context)
#
# Query 2 (with conversation history):
#   Original: how to test it
#   Enhanced: how to test it (for software_engineer, in engineering context, following up on: authentication setup)
#   Context: for software_engineer, in engineering context, following up on: authentication setup
```

**5. Hybrid Query Optimization - Combine Multiple Techniques**
```python
class HybridQueryOptimizer:
    """
    Comprehensive query optimization combining multiple strategies.
    
    Pipeline:
    1. Reformulate (fix spelling, clarify)
    2. Add context (user, session)
    3. Expand or decompose (based on complexity)
    4. Add metadata filters
    """
    
    def __init__(self):
        self.contextual_optimizer = ContextualQueryOptimizer()
    
    def optimize(
        self,
        query: str,
        user_id: str,
        session_id: str,
        conversation_history: list[str] = None,
        complexity_threshold: int = 20  # word count
    ) -> dict:
        """
        Full optimization pipeline.
        
        Returns:
            Optimized query/queries with metadata filters
        """
        # Step 1: Reformulate for clarity
        reformulated = reformulate_query(query, domain="technical")
        
        # Step 2: Add context
        contextualized = self.contextual_optimizer.optimize_with_context(
            reformulated,
            user_id,
            session_id,
            conversation_history
        )
        
        # Step 3: Determine if decomposition needed
        word_count = len(reformulated.split())
        
        if word_count > complexity_threshold or " and " in reformulated.lower():
            # Complex query - decompose
            subqueries = decompose_complex_query(reformulated)
            
            optimization_result = {
                "strategy": "decomposition",
                "original_query": query,
                "reformulated_query": reformulated,
                "subqueries": subqueries,
                "context": contextualized["context_applied"],
                "metadata_filters": contextualized["user_filters"]
            }
        else:
            # Simple query - expand
            expanded = expand_query_with_synonyms(reformulated)
            
            optimization_result = {
                "strategy": "expansion",
                "original_query": query,
                "reformulated_query": reformulated,
                "expanded_queries": expanded,
                "context": contextualized["context_applied"],
                "metadata_filters": contextualized["user_filters"]
            }
        
        return optimization_result

# Full pipeline example
hybrid_optimizer = HybridQueryOptimizer()

# Simple query → Expansion
simple_result = hybrid_optimizer.optimize(
    query="auth errors",
    user_id="user123",
    session_id="session_xyz"
)

print("Simple Query Optimization:")
print(f"  Original: {simple_result['original_query']}")
print(f"  Reformulated: {simple_result['reformulated_query']}")
print(f"  Strategy: {simple_result['strategy']}")
print(f"  Variations: {len(simple_result['expanded_queries'])}")

# Complex query → Decomposition
complex_result = hybrid_optimizer.optimize(
    query="how secure scale and monitor apis",
    user_id="user123",
    session_id="session_xyz"
)

print("\nComplex Query Optimization:")
print(f"  Original: {complex_result['original_query']}")
print(f"  Reformulated: {complex_result['reformulated_query']}")
print(f"  Strategy: {complex_result['strategy']}")
print(f"  Sub-queries: {len(complex_result['subqueries'])}")
for sq in complex_result['subqueries']:
    print(f"    - [{sq['aspect']}] {sq['query']}")
```

### What It Isn't
Query optimization is not **query rewriting that changes user intent**. If a user asks about "Python," don't optimize it to "Python snake species" when they clearly mean the programming language. Respect user intent—enhance, don't replace.

It's not **always necessary**. If users already write clear, specific queries and your retrieval works well, don't over-optimize. Adding complexity without benefit hurts performance and maintainability.

Query optimization is not **a replacement for good embeddings**. No amount of query optimization fixes fundamentally poor embeddings or knowledge base organization. Optimize queries within a solid retrieval foundation.

It's not **free from errors**. LLM-based reformulation can misunderstand queries, add wrong context, or introduce biases. Always validate optimization quality on test sets.

Query optimization is not **deterministic**. LLM-based techniques produce slightly different results each time. For reproducibility, use low temperature and cache optimized queries when possible.

Finally, it's not **transparent to users by default**. Users may not understand why their query was changed. Consider showing both original and optimized queries, or explaining optimization in UI.

## How It Works

### Building a Query Optimization System

**Step 1: Identify Query Quality Problems**
```python
def analyze_query_quality(queries: list[str]) -> dict:
    """
    Analyze common query quality issues in your system.
    
    Issues to detect:
    - Too vague (< 3 words)
    - Too complex (> 20 words)
    - Contains typos
    - Uses abbreviations
    - Ambiguous intent
    """
    issues = {
        "too_vague": [],
        "too_complex": [],
        "has_typos": [],
        "has_abbreviations": [],
        "poor_results": []
    }
    
    for query in queries:
        words = query.split()
        
        # Too vague
        if len(words) < 3:
            issues["too_vague"].append(query)
        
        # Too complex
        if len(words) > 20:
            issues["too_complex"].append(query)
        
        # Has abbreviations (simple heuristic)
        if any(w.isupper() and len(w) <= 4 for w in words):
            issues["has_abbreviations"].append(query)
    
    return {
        "total_queries": len(queries),
        "issues_found": sum(len(v) for v in issues.values()),
        "breakdown": {k: len(v) for k, v in issues.items()},
        "examples": {k: v[:3] for k, v in issues.items()}  # Show 3 examples each
    }

# Analyze production queries
production_queries = [
    "auth",
    "db slow",
    "API",
    "how do I implement authentication authorization rate limiting monitoring and logging for my REST API",
    "perf issues",
    "cant login pls help"
]

analysis = analyze_query_quality(production_queries)

print(f"Analyzed {analysis['total_queries']} queries")
print(f"Found {analysis['issues_found']} issues:\n")
for issue_type, count in analysis['breakdown'].items():
    if count > 0:
        print(f"  {issue_type}: {count}")
        print(f"    Examples: {analysis['examples'][issue_type]}")
```

**Step 2: Choose Optimization Strategies by Query Type**
```python
def determine_optimization_strategy(query: str) -> str:
    """
    Choose best optimization strategy based on query characteristics.
    
    Decision tree:
    - Very short (< 3 words) → Reformulate + Expand
    - Very long (> 15 words) → Decompose
    - Contains "and" / multiple aspects → Decompose
    - Contains abbreviations → Reformulate
    - Ambiguous → Add context
    - Default → Expand
    """
    words = query.split()
    word_count = len(words)
    
    # Very short queries need reformulation + expansion
    if word_count < 3:
        return "reformulate_and_expand"
    
    # Very long or multi-aspect queries need decomposition
    if word_count > 15 or " and " in query.lower():
        return "decompose"
    
    # Queries with abbreviations need reformulation
    if any(w.isupper() and len(w) <= 4 for w in words):
        return "reformulate"
    
    # Default: expand with synonyms
    return "expand"

# Test strategy selection
test_queries = {
    "auth": "reformulate_and_expand",
    "API rate limit guide": "expand",
    "how to implement security and scalability": "decompose",
    "database performance": "expand"
}

for query, expected in test_queries.items():
    strategy = determine_optimization_strategy(query)
    match = "✓" if strategy == expected else "✗"
    print(f"{match} '{query}' → {strategy}")
```

**Step 3: Measure Optimization Effectiveness**
```python
def evaluate_query_optimization(
    test_cases: list[dict],
    with_optimization: bool = True
) -> dict:
    """
    A/B test query optimization impact.
    
    Each test case: {
        "query": "original query",
        "relevant_docs": [list of relevant doc IDs],
        "user_context": {...}
    }
    
    Metrics:
    - Precision@5: Are top 5 results relevant?
    - MRR: Position of first relevant result
    - User satisfaction (if available)
    """
    import numpy as np
    
    precisions = []
    reciprocal_ranks = []
    
    for test in test_cases:
        query = test["query"]
        relevant_docs = set(test["relevant_docs"])
        
        if with_optimization:
            # Optimize query
            optimized = hybrid_optimizer.optimize(
                query,
                user_id=test.get("user_id", "test_user"),
                session_id="test_session"
            )
            
            # Search with optimized query
            if optimized["strategy"] == "expansion":
                results = search_with_expansion(optimized["expanded_queries"])
            else:  # decomposition
                # Simplified - would search all subqueries and merge
                results = search_with_decomposition(optimized["subqueries"])
        else:
            # Search with original query (baseline)
            embedding = model.encode(query)
            results = vector_db.search(
                collection_name="knowledge_base",
                query_vector=embedding,
                limit=5
            )
            results = [{"id": r.id} for r in results]
        
        # Calculate precision@5
        retrieved_ids = [r["id"] for r in results[:5]]
        relevant_retrieved = len(set(retrieved_ids) & relevant_docs)
        precision = relevant_retrieved / 5
        precisions.append(precision)
        
        # Calculate MRR
        for rank, doc_id in enumerate(retrieved_ids, 1):
            if doc_id in relevant_docs:
                reciprocal_ranks.append(1 / rank)
                break
        else:
            reciprocal_ranks.append(0)
    
    return {
        "precision@5": np.mean(precisions),
        "mrr": np.mean(reciprocal_ranks),
        "queries_evaluated": len(test_cases)
    }

# Compare baseline vs optimized
baseline_metrics = evaluate_query_optimization(test_suite, with_optimization=False)
optimized_metrics = evaluate_query_optimization(test_suite, with_optimization=True)

print("Baseline (no optimization):")
print(f"  Precision@5: {baseline_metrics['precision@5']:.3f}")
print(f"  MRR: {baseline_metrics['mrr']:.3f}")

print("\nWith Query Optimization:")
print(f"  Precision@5: {optimized_metrics['precision@5']:.3f}")
print(f"  MRR: {optimized_metrics['mrr']:.3f}")

improvement = {
    "precision": (optimized_metrics['precision@5'] - baseline_metrics['precision@5']) / baseline_metrics['precision@5'] * 100,
    "mrr": (optimized_metrics['mrr'] - baseline_metrics['mrr']) / baseline_metrics['mrr'] * 100
}

print(f"\nImprovement:")
print(f"  Precision@5: +{improvement['precision']:.1f}%")
print(f"  MRR: +{improvement['mrr']:.1f}%")
```

**Step 4: Cache and Monitor Optimizations**
```python
class OptimizationCache:
    """
    Cache optimized queries to:
    - Reduce LLM API calls
    - Improve latency
    - Track common queries
    """
    
    def __init__(self):
        self.cache = {}
        self.hit_counts = {}
    
    def get_or_optimize(
        self,
        query: str,
        optimizer_func,
        ttl_seconds: int = 3600
    ) -> dict:
        """
        Check cache first, optimize if miss.
        
        Args:
            query: Original query
            optimizer_func: Function to call if cache miss
            ttl_seconds: Cache time-to-live
        """
        import time
        import hashlib
        
        # Create cache key
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        # Check cache
        if cache_key in self.cache:
            cached_entry = self.cache[cache_key]
            
            # Check TTL
            if time.time() - cached_entry["cached_at"] < ttl_seconds:
                self.hit_counts[cache_key] = self.hit_counts.get(cache_key, 0) + 1
                return {
                    "result": cached_entry["optimized"],
                    "cache_hit": True,
                    "hit_count": self.hit_counts[cache_key]
                }
        
        # Cache miss - optimize
        optimized = optimizer_func(query)
        
        # Store in cache
        self.cache[cache_key] = {
            "original": query,
            "optimized": optimized,
            "cached_at": time.time()
        }
        
        return {
            "result": optimized,
            "cache_hit": False,
            "hit_count": 0
        }
    
    def get_cache_stats(self) -> dict:
        """Analytics on cached queries."""
        total_entries = len(self.cache)
        total_hits = sum(self.hit_counts.values())
        
        # Find most common queries
        top_queries = sorted(
            self.cache.items(),
            key=lambda x: self.hit_counts.get(x[0], 0),
            reverse=True
        )[:10]
        
        return {
            "total_cached_queries": total_entries,
            "total_cache_hits": total_hits,
            "cache_hit_rate": total_hits / (total_entries + total_hits) if (total_entries + total_hits) > 0 else 0,
            "top_queries": [
                {
                    "query": entry[1]["original"],
                    "hit_count": self.hit_counts.get(entry[0], 0)
                }
                for entry in top_queries
            ]
        }

cache = OptimizationCache()

# Use with caching
result1 = cache.get_or_optimize("auth errors", reformulate_query)
print(f"Cache hit: {result1['cache_hit']}")  # False (first time)

result2 = cache.get_or_optimize("auth errors", reformulate_query)
print(f"Cache hit: {result2['cache_hit']}")  # True (cached)

# View cache analytics
stats = cache.get_cache_stats()
print(f"\nCache stats:")
print(f"  Cached queries: {stats['total_cached_queries']}")
print(f"  Total hits: {stats['total_cache_hits']}")
print(f"  Hit rate: {stats['cache_hit_rate']:.1%}")
```

## Think of It Like This
Imagine you're a reference librarian helping people find books.

**Without query optimization**, someone walks up and says "car." You search for books with "car" in the title and hand them what you find—maybe automotive repair manuals, maybe children's books about toy cars, maybe history of automobiles. The patron is frustrated because they wanted "car insurance comparison guides" but didn't articulate it clearly.

**With query optimization**, when someone says "car," you ask clarifying questions: "Are you looking for repair information, insurance, purchasing guides, or something else?" They say "insurance." You reformulate their request to "car insurance comparison guides," expand it to include related terms like "auto insurance" and "vehicle coverage," and add context like "for new drivers" based on their library card showing they're 18. Now you find exactly what they need.

In AI systems, query optimization is that clarifying conversation—transforming vague input into specific, searchable queries that retrieve genuinely relevant information.

## The "So What?" Factor
**If you implement query optimization:**
- Retrieval quality improves 30-50% as queries match knowledge base vocabulary
- Users get relevant results even with vague or poorly-worded queries
- Complex questions decompose into focused searches, covering all aspects
- Context awareness means "performance" is disambiguated (database? API? UI?)
- Vocabulary gaps close—"auth broken" finds "authentication failures"
- RAG answers improve dramatically because retrieved context is actually relevant
- User frustration decreases—fewer "zero results" or irrelevant results
- System handles abbreviations, typos, and informal language gracefully
- Multi-turn conversations work—follow-up questions understand previous context
- You can measure and improve optimization effectiveness over time

**If you skip query optimization:**
- Users must guess exact terminology used in knowledge base
- Vague queries like "performance" return irrelevant mixed results
- Complex questions overwhelm system—"How do I X, Y, and Z?" fails
- Vocabulary mismatches kill retrieval—"auth" misses "authentication"
- RAG systems generate poor answers from irrelevant retrieved context
- User frustration increases—lots of reformulation trial-and-error
- "Zero results" is common when users phrase things differently
- System can't handle abbreviations, typos, or informal language
- Multi-turn conversations fail—no memory of previous queries
- No visibility into why searches fail or how to improve

## Practical Checklist
Before implementing query optimization, ask yourself:
- [ ] Have I analyzed common query quality issues in my system?
- [ ] Do I understand the main reasons searches fail (vocabulary mismatch, ambiguity, complexity)?
- [ ] Have I chosen optimization strategies appropriate for my query types?
- [ ] Am I measuring baseline retrieval quality to quantify improvement?
- [ ] Do I have test cases with known relevant documents for evaluation?
- [ ] Am I caching optimized queries to reduce latency and costs?
- [ ] Have I implemented monitoring to track optimization effectiveness?
- [ ] Am I preserving user intent during optimization (not changing what they meant)?
- [ ] Do I handle errors gracefully when optimization fails?
- [ ] Am I transparent with users about how their queries were optimized?
- [ ] Have I tested optimization with actual user queries, not just synthetic?
- [ ] Do I have a feedback loop to improve optimization over time?

## Watch Out For
⚠️ **Changing user intent**: Reformulating "Python" to "Python programming" when user meant the snake species. Always respect what the user actually meant—enhance, don't replace intent.

⚠️ **Over-optimization**: Adding complexity when original queries work fine. Start simple, add optimization only where retrieval quality issues exist.

⚠️ **Latency overhead**: LLM-based optimization adds 100-500ms per query. Cache aggressively and consider async optimization for acceptable UX.

⚠️ **LLM costs**: Every query reformulation/expansion costs money with API-based LLMs. Cache common queries and use local models for high-volume applications.

⚠️ **Non-determinism**: LLM-based optimization produces different results each run. Use low temperature (0.3) for consistency, cache results for reproducibility.

⚠️ **Context window limits**: Adding too much context (user profile, session history, conversation) can exceed prompt limits. Prioritize most relevant context.

⚠️ **Hallucinated expansions**: LLM may generate query variations that don't match user intent. Validate expansion quality on test sets.

⚠️ **Ignoring domain vocabulary**: Generic reformulation misses domain-specific terms. Fine-tune or prompt with domain examples.

⚠️ **No fallback**: If optimization fails (LLM error, timeout), fall back to original query. Don't fail the entire search.

⚠️ **Missing feedback loop**: Without measuring impact, you don't know if optimization helps or hurts. A/B test and track metrics continuously.

## Connections
**Builds On:**
- [semantic_search](semantic_search.md) - What query optimization improves
- [embeddings](../Foundational_AI & ML/embeddings.md) - Understanding semantic similarity
- Natural language processing (NLP) - Query understanding techniques

**Works With:**
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - Query optimization improves RAG quality
- [reranking](reranking.md) - Optimize query → retrieve candidates → rerank
- [metadata](metadata.md) - Adding metadata filters in optimized queries
- [vector_database](vector_database.md) - Executing optimized queries
- [document_chunking](document_chunking.md) - Matching queries to chunk granularity
- [context_window](context_window.md) - Managing context in multi-turn optimization

**Leads To:**
- Conversational search systems
- Intent understanding and classification
- Personalized search (user-specific optimization)
- Active learning (improving optimization from feedback)

**Related Patterns:**
- [caching](caching.md) - Caching optimized queries
- Query suggestion / autocomplete
- Search analytics and query logs
- [hallucination](hallucination.md) - Risk in LLM-based optimization
- Feedback loops and continuous improvement

## Quick Decision Guide
**Use query optimization when:**
- Users write vague or poorly-worded queries
- Vocabulary mismatch between queries and knowledge base
- Complex multi-part questions need decomposition
- Retrieval quality metrics are low (precision, MRR < 70%)
- Users frequently reformulate queries (sign of poor initial results)
- Building conversational systems needing multi-turn context
- Domain-specific terminology requires translation

**Start with these optimizations:**
- Query reformulation (fix spelling, expand abbreviations)
- Query expansion (add synonyms for key terms)
- Metadata filtering (add department, date range from context)

**Add these for complex systems:**
- Query decomposition (break multi-aspect questions)
- Contextual enhancement (user profile, session history)
- Hybrid strategies (combine multiple techniques)

**Skip optimization when:**
- Users already write clear, specific queries
- Retrieval quality is already high (P@5 > 90%)
- Added latency is unacceptable (real-time requirements)
- Queries are already highly structured (e.g., SQL-like)
- Knowledge base is small and well-organized (< 1000 docs)

## Further Exploration
- 📖 "Query Understanding for Search Engines" - Google's query understanding techniques
- 🎯 "Query Expansion and Reformulation" - Stanford IR course materials
- 💡 "Improving RAG with Query Optimization" - LangChain query transformation patterns
- 📖 "Dense Passage Retrieval with Query Augmentation" - Academic research on query enhancement
- 🎯 "Conversational Search and Context Management" - Multi-turn query optimization
- 💡 "Query Decomposition for Complex Questions" - Breaking down multi-aspect queries
- 📖 "Intent Classification and Query Understanding" - Understanding what users mean
- 🎯 LlamaIndex query engines - Implementation examples
- 💡 "A/B Testing Search Relevance" - Measuring optimization impact
- 📖 "Learning to Optimize Queries" - ML approaches to query reformulation

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
