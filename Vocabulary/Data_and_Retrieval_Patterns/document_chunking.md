# Document Chunking

## At a Glance
| | |
|---|---|
| **Category** | Data Preparation Technique |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for fundamentals, practice for optimization |
| **Prerequisites** | Understanding of [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md), [semantic_search](semantic_search.md), [embeddings](../Foundational_AI & ML/embeddings.md) |

## One-Sentence Summary
Document chunking is the process of splitting large documents into smaller, overlapping segments optimized for retrieval—so when a user asks "What's the refund policy?", your RAG system retrieves the specific 500-token chunk containing refund details rather than a 50-page policy document, improving both relevance and fitting within LLM context windows.

## Why This Matters to You
When you build RAG systems in 2026, document chunking is the difference between useful and useless retrieval. Without chunking, you'd retrieve entire 20-page documents for every query—most content is irrelevant, you waste LLM context window capacity, and similarity scores are diluted (document mentions "refunds" once but has 10,000 words about other topics). With proper chunking, you retrieve precisely the 3-4 paragraphs that answer the user's question—high relevance, efficient context usage, and accurate similarity matching. But chunking strategy matters enormously: chunk too small (< 200 tokens) and you lose critical context (answer requires info split across chunks), chunk too large (> 1000 tokens) and you include too much irrelevant information (dilutes retrieval signal), use no overlap and you risk cutting sentences in half or losing context at boundaries. The sweet spot—typically 400-600 tokens with 10-20% overlap—varies by document type (technical docs need different chunking than conversational transcripts). Bad chunking is the silent killer of RAG systems: your embeddings are perfect, your vector database is fast, your LLM is powerful, but users get wrong answers because chunking split related information across unretrievable boundaries or lumped irrelevant content together. Understanding document chunking strategies, overlap techniques, and domain-specific optimizations is essential for building RAG systems that actually retrieve the right information at the right granularity.

## The Core Idea
### What It Is
Document chunking is the process of dividing large documents into smaller, semantically coherent segments (chunks) that can be independently embedded, stored in vector databases, and retrieved based on similarity to user queries. The goal is to create chunks that are small enough to be focused and relevant, large enough to contain sufficient context, and strategically overlapped to prevent information loss at boundaries.

**Why Chunking is Necessary:**

1. **Context Window Limits**: LLMs have finite context windows (typically 8k-128k tokens). If you retrieve entire documents, you quickly exhaust available space. Chunking lets you retrieve multiple relevant segments from different documents within context limits.

2. **Retrieval Precision**: Semantic similarity between query and document is calculated at the chunk level. A 50-page document mentioning "authentication" on page 37 will have low overall similarity to "How do I authenticate?". A 500-token chunk focused on authentication has high similarity.

3. **Embedding Quality**: Embedding models work best on coherent, focused text. A chunk about one topic produces a clear embedding. A document covering 20 topics produces a muddled average embedding.

4. **Cost Efficiency**: Retrieving and processing smaller chunks reduces token usage in LLM calls, lowering costs.

**Core Chunking Strategies:**

**Strategy 1: Fixed-Size Chunking with Token Overlap**
```python
import tiktoken

def chunk_by_tokens(
    text: str,
    chunk_size: int = 512,
    overlap: int = 50,
    encoding_name: str = "cl100k_base"  # GPT-4 tokenizer
) -> list[dict]:
    """
    Split text into fixed-size token chunks with overlap.
    
    Pros:
    - Simple, predictable chunk sizes
    - Easy to implement and debug
    - Consistent retrieval behavior
    
    Cons:
    - May split mid-sentence or mid-thought
    - Doesn't respect semantic boundaries
    - Can break code blocks, lists, tables
    """
    # Load tokenizer
    encoding = tiktoken.get_encoding(encoding_name)
    
    # Tokenize entire document
    tokens = encoding.encode(text)
    
    chunks = []
    start_idx = 0
    
    while start_idx < len(tokens):
        # Extract chunk
        end_idx = min(start_idx + chunk_size, len(tokens))
        chunk_tokens = tokens[start_idx:end_idx]
        
        # Decode back to text
        chunk_text = encoding.decode(chunk_tokens)
        
        chunks.append({
            "text": chunk_text,
            "start_token": start_idx,
            "end_token": end_idx,
            "token_count": len(chunk_tokens)
        })
        
        # Move start position (with overlap)
        start_idx += chunk_size - overlap
    
    return chunks

# Example usage
document = """Our refund policy allows returns within 30 days of purchase. 
Items must be unused and in original packaging. To request a refund, 
email support@company.com with your order number. Refunds are processed 
within 5-7 business days after we receive the returned item.

For enterprise customers, extended return windows up to 90 days may be 
available. Contact your account manager for details.

Shipping costs are non-refundable except in cases of defective products 
or shipping errors on our part. If you receive a damaged item, please 
contact support within 48 hours with photos of the damage."""

chunks = chunk_by_tokens(document, chunk_size=100, overlap=20)

print(f"Created {len(chunks)} chunks from document")
for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i} ({chunk['token_count']} tokens):")
    print(chunk['text'][:150] + "...")
```

**Strategy 2: Sentence-Based Chunking**
```python
import re
import nltk
from nltk.tokenize import sent_tokenize

# Download required NLTK data (run once)
# nltk.download('punkt')

def chunk_by_sentences(
    text: str,
    target_chunk_size: int = 500,
    overlap_sentences: int = 2
) -> list[dict]:
    """
    Split text into chunks at sentence boundaries.
    
    Pros:
    - Respects natural language boundaries
    - No mid-sentence splits
    - More semantically coherent chunks
    
    Cons:
    - Variable chunk sizes (some might be too small/large)
    - Depends on sentence detection accuracy
    - May not work well for non-prose (code, lists, data)
    """
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    encoding = tiktoken.get_encoding("cl100k_base")
    
    for sentence in sentences:
        sentence_tokens = len(encoding.encode(sentence))
        
        # If adding this sentence exceeds target, save current chunk
        if current_tokens + sentence_tokens > target_chunk_size and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "sentence_count": len(current_chunk),
                "token_count": current_tokens
            })
            
            # Start new chunk with overlap
            # Keep last N sentences for context
            current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
            current_tokens = sum(len(encoding.encode(s)) for s in current_chunk)
        
        current_chunk.append(sentence)
        current_tokens += sentence_tokens
    
    # Don't forget last chunk
    if current_chunk:
        chunks.append({
            "text": " ".join(current_chunk),
            "sentence_count": len(current_chunk),
            "token_count": current_tokens
        })
    
    return chunks

# Example usage
chunks = chunk_by_sentences(document, target_chunk_size=100, overlap_sentences=1)

print(f"Created {len(chunks)} sentence-based chunks")
for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i} ({chunk['sentence_count']} sentences, {chunk['token_count']} tokens):")
    print(chunk['text'][:150] + "...")
```

**Strategy 3: Semantic Chunking (Topic-Aware)**
```python
from sentence_transformers import SentenceTransformer
import numpy as np

def chunk_by_semantic_similarity(
    text: str,
    similarity_threshold: float = 0.7,
    min_chunk_size: int = 200,
    max_chunk_size: int = 800
) -> list[dict]:
    """
    Split text where semantic similarity drops, indicating topic shifts.
    
    Pros:
    - Respects semantic/topic boundaries
    - Each chunk focuses on one concept
    - Best for retrieval quality
    
    Cons:
    - Computationally expensive (embed every sentence)
    - Variable chunk sizes (may need min/max constraints)
    - Sensitive to threshold tuning
    """
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    
    # Embed all sentences
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    
    # Calculate similarity between consecutive sentences
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = np.dot(embeddings[i], embeddings[i+1]) / (
            np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i+1])
        )
        similarities.append(sim)
    
    # Find split points where similarity drops below threshold
    split_indices = [0]
    for i, sim in enumerate(similarities):
        if sim < similarity_threshold:
            split_indices.append(i + 1)
    split_indices.append(len(sentences))
    
    # Create chunks
    encoding = tiktoken.get_encoding("cl100k_base")
    chunks = []
    
    for i in range(len(split_indices) - 1):
        start_idx = split_indices[i]
        end_idx = split_indices[i + 1]
        
        chunk_sentences = sentences[start_idx:end_idx]
        chunk_text = " ".join(chunk_sentences)
        token_count = len(encoding.encode(chunk_text))
        
        # Enforce min/max constraints
        if token_count < min_chunk_size and chunks:
            # Merge with previous chunk
            chunks[-1]["text"] += " " + chunk_text
            chunks[-1]["token_count"] = len(encoding.encode(chunks[-1]["text"]))
            chunks[-1]["sentence_count"] += len(chunk_sentences)
        elif token_count > max_chunk_size:
            # Split into smaller chunks using sentence-based method
            sub_chunks = chunk_by_sentences(
                chunk_text,
                target_chunk_size=max_chunk_size // 2,
                overlap_sentences=1
            )
            chunks.extend(sub_chunks)
        else:
            chunks.append({
                "text": chunk_text,
                "sentence_count": len(chunk_sentences),
                "token_count": token_count
            })
    
    return chunks

# Example usage
chunks = chunk_by_semantic_similarity(
    document,
    similarity_threshold=0.6,
    min_chunk_size=50,
    max_chunk_size=200
)

print(f"Created {len(chunks)} semantic chunks")
for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i} ({chunk['token_count']} tokens):")
    print(chunk['text'][:150] + "...")
```

**Strategy 4: Structure-Aware Chunking (Markdown/HTML)**
```python
import re

def chunk_by_markdown_structure(
    markdown_text: str,
    max_chunk_size: int = 600
) -> list[dict]:
    """
    Split markdown by headers, preserving document structure.
    
    Pros:
    - Respects document organization
    - Each chunk is a complete section
    - Preserves header hierarchy context
    
    Cons:
    - Only works for structured documents
    - Sections may be too large or too small
    - Requires post-processing for size constraints
    """
    # Split by headers (# Header, ## Subheader, etc.)
    sections = re.split(r'(^#{1,6}\s+.+$)', markdown_text, flags=re.MULTILINE)
    
    chunks = []
    current_header = None
    current_content = []
    encoding = tiktoken.get_encoding("cl100k_base")
    
    for section in sections:
        # Check if this is a header
        if re.match(r'^#{1,6}\s+.+$', section):
            # Save previous section if exists
            if current_header and current_content:
                chunk_text = current_header + "\n\n" + "\n".join(current_content)
                token_count = len(encoding.encode(chunk_text))
                
                # If too large, split content further
                if token_count > max_chunk_size:
                    # Split content into smaller chunks, preserving header
                    sub_chunks = chunk_by_sentences(
                        "\n".join(current_content),
                        target_chunk_size=max_chunk_size - 50,  # Leave room for header
                        overlap_sentences=1
                    )
                    for sub in sub_chunks:
                        chunks.append({
                            "text": current_header + "\n\n" + sub["text"],
                            "header": current_header,
                            "token_count": len(encoding.encode(current_header)) + sub["token_count"]
                        })
                else:
                    chunks.append({
                        "text": chunk_text,
                        "header": current_header,
                        "token_count": token_count
                    })
            
            # Start new section
            current_header = section
            current_content = []
        else:
            # Accumulate content under current header
            if section.strip():
                current_content.append(section.strip())
    
    # Don't forget last section
    if current_header and current_content:
        chunk_text = current_header + "\n\n" + "\n".join(current_content)
        chunks.append({
            "text": chunk_text,
            "header": current_header,
            "token_count": len(encoding.encode(chunk_text))
        })
    
    return chunks

# Example with structured markdown
markdown_doc = """# Refund Policy

Our standard refund policy applies to all retail customers.

## Return Window

Returns are accepted within 30 days of purchase. Items must be unused and in original packaging.

## Process

To request a refund:
1. Email support@company.com
2. Include your order number
3. Describe the reason for return

## Timeline

Refunds are processed within 5-7 business days after we receive the item.

## Enterprise Customers

Extended return windows up to 90 days may be available. Contact your account manager.

## Exceptions

Shipping costs are non-refundable except for defective products or our shipping errors."""

chunks = chunk_by_markdown_structure(markdown_doc, max_chunk_size=150)

print(f"Created {len(chunks)} structure-aware chunks")
for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i} - {chunk['header']} ({chunk['token_count']} tokens):")
    print(chunk['text'][:150] + "...")
```

**Strategy 5: Hybrid Chunking with Metadata Preservation**
```python
class HybridChunker:
    """
    Combine multiple strategies with metadata preservation.
    
    Best for production RAG systems where different document
    types need different chunking strategies.
    """
    
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def chunk_document(
        self,
        text: str,
        metadata: dict,
        strategy: str = "auto",
        chunk_size: int = 512,
        overlap: int = 50
    ) -> list[dict]:
        """
        Chunk document using appropriate strategy based on content type.
        
        Strategies:
        - auto: Detect best strategy from content
        - fixed: Fixed-size token chunking
        - sentence: Sentence-based chunking
        - semantic: Topic-aware semantic chunking
        - structure: Markdown/HTML structure-aware
        """
        # Auto-detect strategy if not specified
        if strategy == "auto":
            strategy = self._detect_strategy(text, metadata)
        
        # Apply chosen strategy
        if strategy == "structure" and self._is_structured(text):
            chunks = chunk_by_markdown_structure(text, max_chunk_size=chunk_size)
        elif strategy == "semantic":
            chunks = chunk_by_semantic_similarity(
                text,
                similarity_threshold=0.7,
                max_chunk_size=chunk_size
            )
        elif strategy == "sentence":
            chunks = chunk_by_sentences(
                text,
                target_chunk_size=chunk_size,
                overlap_sentences=max(1, overlap // 100)
            )
        else:  # fixed
            chunks = chunk_by_tokens(
                text,
                chunk_size=chunk_size,
                overlap=overlap
            )
        
        # Enrich chunks with preserved metadata
        enriched_chunks = []
        for i, chunk in enumerate(chunks):
            enriched_chunks.append({
                **chunk,
                "chunk_id": f"{metadata.get('doc_id', 'unknown')}_{i}",
                "chunk_index": i,
                "total_chunks": len(chunks),
                "source_metadata": metadata,
                "chunking_strategy": strategy
            })
        
        return enriched_chunks
    
    def _detect_strategy(self, text: str, metadata: dict) -> str:
        """Detect best chunking strategy from content."""
        # Check if structured document
        if self._is_structured(text):
            return "structure"
        
        # Check document type from metadata
        file_type = metadata.get("file_type", "")
        if file_type in [".md", ".html"]:
            return "structure"
        elif file_type == ".py":
            return "fixed"  # Code chunks better with fixed size
        
        # Check document length
        token_count = len(self.encoding.encode(text))
        if token_count < 1000:
            return "sentence"  # Short docs don't need complex chunking
        elif token_count > 10000:
            return "semantic"  # Long docs benefit from topic segmentation
        
        # Default to sentence-based for medium-length prose
        return "sentence"
    
    def _is_structured(self, text: str) -> bool:
        """Check if document has markdown/HTML structure."""
        # Look for markdown headers
        has_headers = bool(re.search(r'^#{1,6}\s+.+$', text, re.MULTILINE))
        # Look for HTML tags
        has_html = bool(re.search(r'<[^>]+>', text))
        
        return has_headers or has_html

# Example usage
chunker = HybridChunker()

# Chunk different document types
documents = [
    {
        "text": markdown_doc,
        "metadata": {
            "doc_id": "doc_001",
            "file_type": ".md",
            "source": "refund_policy.md"
        }
    },
    {
        "text": document,
        "metadata": {
            "doc_id": "doc_002",
            "file_type": ".txt",
            "source": "general_info.txt"
        }
    }
]

for doc in documents:
    chunks = chunker.chunk_document(
        doc["text"],
        doc["metadata"],
        strategy="auto"
    )
    
    print(f"\nDocument: {doc['metadata']['source']}")
    print(f"Strategy: {chunks[0]['chunking_strategy']}")
    print(f"Created {len(chunks)} chunks")
```

**Chunking with Overlap Visualization:**
```python
def visualize_chunking_with_overlap(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20
):
    """
    Visualize how overlap prevents information loss at boundaries.
    """
    chunks = chunk_by_tokens(text, chunk_size=chunk_size, overlap=overlap)
    
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    
    print(f"Document: {len(tokens)} tokens")
    print(f"Chunk size: {chunk_size} tokens")
    print(f"Overlap: {overlap} tokens ({overlap/chunk_size*100:.1f}%)")
    print(f"Created: {len(chunks)} chunks\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: tokens {chunk['start_token']}-{chunk['end_token']}")
        print(f"Text: {chunk['text'][:100]}...")
        
        if i < len(chunks):
            # Show overlap with next chunk
            overlap_start = chunk['end_token'] - overlap
            overlap_end = chunk['end_token']
            overlap_text = encoding.decode(tokens[overlap_start:overlap_end])
            print(f"Overlap with Chunk {i+1}: ...{overlap_text}...")
        print()

# Demonstrate overlap benefit
sample_text = """The refund policy states that returns are accepted within 30 days. 
Items must be unused and in original packaging. Contact support@company.com to 
initiate a return. Processing takes 5-7 business days after receipt."""

visualize_chunking_with_overlap(sample_text, chunk_size=30, overlap=10)
```

### What It Isn't
Document chunking is not **splitting at arbitrary character counts without thought**. Simply dividing every N characters often splits mid-word, mid-sentence, or mid-thought, creating incoherent chunks that embed poorly and retrieve uselessly.

It's not **one-size-fits-all**. Different document types need different chunking strategies: technical documentation benefits from structure-aware chunking (respecting headers), conversational transcripts need sentence-based chunking, code files need syntax-aware chunking that respects functions/classes, data files might not need chunking at all.

Document chunking is not **optional for RAG systems**. Some think "just embed the whole document." This fails because: (1) similarity is diluted (document covers 20 topics, only 1 relevant), (2) context window exceeded (can't fit 10 full documents in prompt), (3) poor retrieval precision (user wants one paragraph, gets entire document).

It's not **guaranteed to preserve all context**. Even with overlap, critical information spanning chunk boundaries can be partially lost. This is why overlap percentage matters—too little (< 10%) risks losing context, too much (> 30%) wastes embedding/storage space with redundancy.

Document chunking is not **the same as summarization**. Chunking preserves original text, just split into pieces. Summarization condenses content, losing details. RAG systems need original text (not summaries) for accurate answers.

Finally, chunking is not **set once and forgotten**. As you monitor RAG system performance, you'll discover that certain chunk sizes work better for specific document types or query patterns. Chunking strategy should evolve based on retrieval quality metrics and user feedback.

## How It Works

### Choosing Optimal Chunk Size

**Rule of Thumb Decision Tree:**
```python
def recommend_chunk_size(
    document_type: str,
    avg_query_specificity: str,  # "broad" or "specific"
    document_avg_length: int  # in tokens
) -> dict:
    """
    Recommend chunk size based on document characteristics.
    
    Guidelines:
    - Smaller chunks (200-400): Specific queries, diverse topics
    - Medium chunks (400-600): General purpose, balanced
    - Larger chunks (600-1000): Broad queries, cohesive content
    """
    recommendations = {
        "technical_docs": {
            "specific": {"size": 400, "overlap": 50, "reason": "Users ask specific technical questions"},
            "broad": {"size": 600, "overlap": 100, "reason": "May need surrounding context"}
        },
        "conversational": {
            "specific": {"size": 300, "overlap": 30, "reason": "Natural topic shifts, focused retrieval"},
            "broad": {"size": 500, "overlap": 50, "reason": "Conversation flow needs continuity"}
        },
        "legal_documents": {
            "specific": {"size": 500, "overlap": 100, "reason": "Precise language, need full clauses"},
            "broad": {"size": 800, "overlap": 150, "reason": "Legal context often spans paragraphs"}
        },
        "code": {
            "specific": {"size": 600, "overlap": 100, "reason": "Complete functions/classes"},
            "broad": {"size": 1000, "overlap": 200, "reason": "Need imports and dependencies"}
        },
        "general": {
            "specific": {"size": 400, "overlap": 50, "reason": "Balanced for most use cases"},
            "broad": {"size": 600, "overlap": 100, "reason": "Standard retrieval"}
        }
    }
    
    doc_type = document_type.lower()
    specificity = avg_query_specificity.lower()
    
    # Get recommendation
    if doc_type in recommendations:
        rec = recommendations[doc_type][specificity]
    else:
        rec = recommendations["general"][specificity]
    
    # Adjust for very short or very long documents
    if document_avg_length < 500:
        rec["size"] = min(rec["size"], document_avg_length // 2)
        rec["reason"] += " (adjusted for short documents)"
    elif document_avg_length > 10000:
        rec["overlap"] = int(rec["overlap"] * 1.5)
        rec["reason"] += " (increased overlap for long documents)"
    
    return rec

# Example usage
rec = recommend_chunk_size(
    document_type="technical_docs",
    avg_query_specificity="specific",
    document_avg_length=5000
)

print(f"Recommended chunk size: {rec['size']} tokens")
print(f"Recommended overlap: {rec['overlap']} tokens ({rec['overlap']/rec['size']*100:.1f}%)")
print(f"Reason: {rec['reason']}")
```

**Empirical Testing for Your Domain:**
```python
class ChunkingOptimizer:
    """
    Test different chunking strategies to find optimal configuration.
    """
    
    def __init__(self, test_queries: list[dict]):
        """
        test_queries format:
        [
            {
                "query": "What is the refund policy?",
                "relevant_doc_ids": ["doc_1", "doc_3"],
                "expected_chunks": ["doc_1_chunk_2"]  # Ground truth
            }
        ]
        """
        self.test_queries = test_queries
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def test_chunking_strategy(
        self,
        documents: list[dict],
        chunk_size: int,
        overlap: int,
        strategy: str = "sentence"
    ) -> dict:
        """
        Test retrieval quality with specific chunking parameters.
        
        Returns precision, recall, and MRR metrics.
        """
        # Chunk all documents
        chunker = HybridChunker()
        all_chunks = []
        
        for doc in documents:
            chunks = chunker.chunk_document(
                doc["text"],
                doc["metadata"],
                strategy=strategy,
                chunk_size=chunk_size,
                overlap=overlap
            )
            all_chunks.extend(chunks)
        
        # Embed chunks
        chunk_texts = [c["text"] for c in all_chunks]
        chunk_embeddings = self.model.encode(chunk_texts)
        
        # Test retrieval for each query
        precisions = []
        recalls = []
        reciprocal_ranks = []
        
        for test in self.test_queries:
            query = test["query"]
            expected_chunks = set(test["expected_chunks"])
            
            # Retrieve top K chunks
            query_embedding = self.model.encode(query)
            similarities = [
                np.dot(query_embedding, chunk_emb) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(chunk_emb)
                )
                for chunk_emb in chunk_embeddings
            ]
            
            # Get top 5 chunks
            top_indices = np.argsort(similarities)[::-1][:5]
            retrieved_chunk_ids = {all_chunks[i]["chunk_id"] for i in top_indices}
            
            # Calculate metrics
            true_positives = len(retrieved_chunk_ids & expected_chunks)
            precision = true_positives / len(retrieved_chunk_ids) if retrieved_chunk_ids else 0
            recall = true_positives / len(expected_chunks) if expected_chunks else 0
            
            precisions.append(precision)
            recalls.append(recall)
            
            # Calculate MRR
            for rank, idx in enumerate(top_indices, 1):
                if all_chunks[idx]["chunk_id"] in expected_chunks:
                    reciprocal_ranks.append(1 / rank)
                    break
            else:
                reciprocal_ranks.append(0)
        
        return {
            "chunk_size": chunk_size,
            "overlap": overlap,
            "strategy": strategy,
            "avg_precision": np.mean(precisions),
            "avg_recall": np.mean(recalls),
            "mrr": np.mean(reciprocal_ranks),
            "f1": 2 * np.mean(precisions) * np.mean(recalls) / (np.mean(precisions) + np.mean(recalls)) if (np.mean(precisions) + np.mean(recalls)) > 0 else 0
        }
    
    def optimize(
        self,
        documents: list[dict],
        chunk_sizes: list[int] = [200, 400, 600, 800],
        overlaps: list[int] = [20, 50, 100, 150],
        strategies: list[str] = ["fixed", "sentence", "semantic"]
    ) -> list[dict]:
        """
        Test all combinations and return ranked results.
        """
        results = []
        
        for strategy in strategies:
            for chunk_size in chunk_sizes:
                for overlap in overlaps:
                    # Skip invalid combinations (overlap >= chunk_size)
                    if overlap >= chunk_size:
                        continue
                    
                    result = self.test_chunking_strategy(
                        documents,
                        chunk_size,
                        overlap,
                        strategy
                    )
                    results.append(result)
        
        # Sort by F1 score (balance of precision and recall)
        results.sort(key=lambda x: x["f1"], reverse=True)
        
        return results

# Example usage
# (Would need actual test data in production)
"""
optimizer = ChunkingOptimizer(test_queries)
results = optimizer.optimize(documents)

print("Top 5 Chunking Configurations:")
for i, result in enumerate(results[:5], 1):
    print(f"\n{i}. Strategy: {result['strategy']}, Size: {result['chunk_size']}, Overlap: {result['overlap']}")
    print(f"   Precision: {result['avg_precision']:.3f}, Recall: {result['avg_recall']:.3f}, MRR: {result['mrr']:.3f}, F1: {result['f1']:.3f}")
"""
```

## Think of It Like This
Imagine you're organizing a massive reference library for researchers.

**Without chunking**, you hand researchers entire encyclopedia volumes (20 pages each) whenever they ask a question. They ask "What's the capital of France?" and you give them Volume F covering France, French history, French culture—they have to read 20 pages to find "Paris" mentioned on page 14. Inefficient and frustrating.

**With poor chunking** (too small, no overlap), you tear pages into pieces randomly—ripping sentences in half, splitting important information across unretrievable fragments. A researcher asks about "the French Revolution's impact on European politics" but the cause is in one fragment, the impact in another separated fragment, and they can't find the complete answer.

**With good chunking** (optimal size, appropriate overlap), you organize the library into focused articles of 2-3 pages each, with some content overlap at boundaries. Each article covers one coherent topic. When a researcher asks about the French Revolution, they receive 3 focused articles covering causes, events, and impact—complete, relevant, and manageable.

Document chunking is that organization strategy—splitting knowledge into retrievable, coherent pieces sized appropriately for the questions people ask.

## The "So What?" Factor
**If you implement proper document chunking:**
- Retrieval precision increases 30-50% (chunks focused on specific topics match queries better)
- LLM answers improve dramatically (receives relevant context, not diluted full documents)
- Context window usage optimizes (fit 5-10 focused chunks vs 2 full documents)
- Embedding quality improves (focused text produces clearer semantic vectors)
- Storage costs decrease (smaller embeddings, efficient vector database usage)
- Query latency reduces (smaller chunks = faster similarity computation)
- User satisfaction increases (answers cite specific, relevant sections)
- Debugging becomes possible (track which chunks retrieved, identify bad splits)
- Scalability improves (chunk once, reuse embeddings across many queries)
- Domain adaptation is easier (tune chunk size for specific document types)

**If you ignore chunking strategy:**
- Retrieval precision is poor (whole documents match weakly to specific queries)
- LLM answers are vague or wrong (context includes too much irrelevant info)
- Context window exhausted quickly (2-3 full documents max)
- Embedding quality suffers (muddled average of multiple topics)
- Storage costs explode (massive embeddings for full documents)
- Query latency increases (compute similarity for huge vectors)
- User dissatisfaction (wrong answers, no citations to relevant sections)
- Debugging impossible (can't tell why wrong document retrieved)
- Scaling blocked (can't embed and search millions of full documents)
- One-size-fits-all chunking fails across document types

## Practical Checklist
Before implementing document chunking, ask yourself:
- [ ] Have I analyzed my document types and query patterns?
- [ ] Have I tested different chunk sizes (200, 400, 600, 800 tokens)?
- [ ] Have I implemented overlap (typically 10-20% of chunk size)?
- [ ] Am I chunking at semantic boundaries (sentences, paragraphs, sections)?
- [ ] Have I preserved metadata (source, section, page number) in chunks?
- [ ] Do I handle structured documents (markdown, HTML) specially?
- [ ] Have I tested retrieval quality with different chunking strategies?
- [ ] Am I monitoring which chunks are retrieved most often?
- [ ] Do I track queries where no relevant chunks are found?
- [ ] Have I validated that critical information isn't split across chunks?
- [ ] Am I using consistent tokenization (same as LLM's tokenizer)?
- [ ] Do I have different strategies for different document types?

## Watch Out For
⚠️ **Chunk size is domain-specific**: Technical docs need different sizes than conversational transcripts. Test with your actual documents and queries—don't blindly use 512 tokens because someone said so.

⚠️ **Overlap is critical**: Without overlap, important information at chunk boundaries is lost. Too little overlap (< 10%) risks losing context, too much (> 30%) wastes space. Aim for 10-20% overlap.

⚠️ **Tokenizer matters**: Use the same tokenizer as your LLM. GPT-4 uses `cl100k_base`, other models use different tokenizers. Mismatch means your chunks don't fit context window as expected.

⚠️ **Structure-unaware chunking breaks formatting**: Splitting markdown in the middle of a code block, list, or table creates malformed chunks that confuse LLMs. Use structure-aware chunking for formatted documents.

⚠️ **Metadata preservation**: Each chunk must retain source document metadata (filename, section, page, date) so users can verify and trace answers back to original sources.

⚠️ **Variable chunk sizes complicate retrieval**: If chunks range from 100 to 2000 tokens, similarity scores aren't comparable. Either normalize scores or enforce size constraints.

⚠️ **Semantic chunking is expensive**: Embedding every sentence to find topic boundaries is computationally costly. Use for high-value documents where retrieval quality justifies the cost.

⚠️ **Testing is mandatory**: Don't guess optimal chunk size—test with real queries and measure precision/recall. What works for one domain fails in another.

⚠️ **Re-chunking is expensive**: Changing chunk strategy requires re-embedding and re-indexing entire knowledge base. Get it right early, or plan for gradual migration.

⚠️ **Context loss at boundaries**: Even with overlap, some information spanning long passages can't be fully captured. Consider query reformulation or multi-hop retrieval for complex questions.

## Connections
**Builds On:**
- [embeddings](../Foundational_AI & ML/embeddings.md) - Chunks are converted to embeddings for search
- Natural language processing (NLP) - Sentence tokenization, semantic analysis

**Works With:**
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - Chunking is essential preparation for RAG
- [semantic_search](semantic_search.md) - Chunks are the units of retrieval
- [vector_database](vector_database.md) - Stores chunk embeddings for fast search
- [reranking](reranking.md) - Reranks retrieved chunks for quality
- [metadata](metadata.md) - Chunk metadata enables filtering
- [context_window](context_window.md) - Chunk sizes must fit LLM context limits

**Leads To:**
- Advanced chunking (recursive, hierarchical, graph-based)
- Multi-resolution retrieval (different chunk sizes simultaneously)
- Chunk optimization via reinforcement learning
- Domain-specific chunking strategies

**Related Patterns:**
- [query_optimization](query_optimization.md) - Better queries improve chunk retrieval
- Document preprocessing and normalization
- Hierarchical document representation
- [hallucination](hallucination.md) - Poor chunking increases hallucination risk

## Quick Decision Guide
**Use fixed-size chunking when:**
- You need simple, predictable implementation
- Documents are unstructured prose
- Chunk size consistency is important
- Processing speed is priority

**Use sentence-based chunking when:**
- Natural language boundaries matter
- You want semantically coherent chunks
- Documents are well-formatted prose
- Slight size variation is acceptable

**Use semantic chunking when:**
- Retrieval quality is top priority
- Documents cover multiple distinct topics
- You have computational resources for embedding
- Documents are long and diverse

**Use structure-aware chunking when:**
- Documents have clear structure (markdown, HTML)
- Headers and sections are meaningful
- You want to preserve formatting
- Document organization aids understanding

**Chunk size guidelines:**
- **Small (200-400 tokens)**: Specific queries, diverse topics, narrow retrieval
- **Medium (400-600 tokens)**: General purpose, balanced trade-off
- **Large (600-1000 tokens)**: Broad queries, cohesive content, more context needed

**Overlap guidelines:**
- **10-15%**: Minimum to prevent boundary loss
- **15-20%**: Standard for most applications
- **20-30%**: Extra safety for critical information
- **> 30%**: Wasteful redundancy

## Further Exploration
- 📖 "Chunking Strategies for Retrieval-Augmented Generation" - LangChain documentation
- 🎯 LlamaIndex chunking guides - Practical implementation patterns
- 💡 "The Impact of Chunking on RAG Performance" - Empirical studies
- 📖 "Recursive Character Text Splitter" - Advanced chunking algorithms
- 🎯 Pinecone chunking best practices - Production recommendations
- 💡 "Semantic Text Splitting with Embeddings" - Topic-aware chunking
- 📖 "Structure-Preserving Document Chunking" - Markdown/HTML strategies
- 🎯 "Optimizing Chunk Size for Question Answering" - Domain-specific tuning
- 💡 "Hierarchical Document Representation" - Multi-resolution retrieval
- 📖 "Measuring Chunking Quality" - Metrics and evaluation frameworks

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
