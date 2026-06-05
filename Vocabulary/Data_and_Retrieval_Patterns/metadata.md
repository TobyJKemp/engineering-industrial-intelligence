# Metadata

## At a Glance
| | |
|---|---|
| **Category** | Data Organization / Information Management |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for concepts, ongoing practice for effective design |
| **Prerequisites** | Basic understanding of data structures, databases |

## One-Sentence Summary
Metadata is structured information about your data—like tags, timestamps, categories, and source information—that enables filtering, organizing, tracking, and contextualizing content without examining the content itself, so you can instantly retrieve "all customer support documents from Q1 2026" without reading every document.

## Why This Matters to You
When you build AI systems in 2026, metadata transforms your data from an unorganized pile into a searchable, filterable, auditable knowledge base. Your RAG system retrieves 50 documents about "API authentication," but without metadata, you can't filter to "only production documentation" or "written after our 2025 security update" or "approved by engineering team." Your agent cites a source but can't tell users when it was written, who wrote it, or if it's still current. Your compliance team asks "which documents contain customer PII?" and you have no way to answer without reading everything. Metadata solves this by attaching structured information to every piece of content—creation date, author, version, category, access level, data classification, source system, approval status. This enables powerful filtering in [semantic_search](semantic_search.md) (find similar documents AND from last 6 months), access control (only show documents user has permission to see), audit trails (track who accessed what when), and contextual retrieval (surface not just content but its provenance and freshness). In [vector_databases](vector_database.md), metadata filtering happens before expensive similarity searches, dramatically reducing compute costs. In RAG systems, metadata enriches LLM context with "This document was written by engineering team on 2026-01-15 and marked as 'production ready.'" Without metadata, your knowledge base is a black box; with it, you have a structured, queryable, auditable system that users and compliance teams can trust.

## The Core Idea
### What It Is
Metadata is structured data that describes, categorizes, and provides context about other data. It answers questions like "Who created this?", "When?", "What category?", "What version?", "Who can access it?", "What's the source?" without examining the actual content.

**Common Metadata Fields in AI Systems:**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    """
    Comprehensive metadata schema for AI/ML knowledge base documents.
    
    Categories:
    - Descriptive: What is this content?
    - Administrative: Who, when, version
    - Access Control: Who can see this?
    - Provenance: Where did this come from?
    - Semantic: How is this classified/tagged?
    """
    # Descriptive metadata
    title: str
    description: Optional[str] = None
    language: str = "en"
    content_type: str  # "documentation", "code", "api_spec", "policy"
    
    # Administrative metadata
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
    version: str = "1.0"
    status: str  # "draft", "review", "approved", "archived"
    
    # Access control metadata
    access_level: str  # "public", "internal", "confidential", "restricted"
    department: str  # "engineering", "sales", "hr", "legal"
    allowed_roles: List[str] = []  # ["engineer", "manager", "admin"]
    
    # Provenance metadata
    source_system: str  # "confluence", "sharepoint", "github", "jira"
    source_url: Optional[str] = None
    ingestion_date: datetime
    
    # Semantic metadata
    categories: List[str] = []  # ["api", "authentication", "security"]
    tags: List[str] = []  # ["production", "critical", "customer-facing"]
    priority: Optional[str] = None  # "high", "medium", "low"
    
    # Content classification
    contains_pii: bool = False
    contains_phi: bool = False  # Protected Health Information
    data_classification: str = "internal"  # "public", "internal", "confidential"
    retention_years: int = 7
    
    # Quality metadata
    review_status: str = "pending"  # "pending", "approved", "needs_update"
    last_reviewed_by: Optional[str] = None
    last_reviewed_at: Optional[datetime] = None
    accuracy_score: Optional[float] = None

# Example document with metadata
document = {
    "id": "doc_12345",
    "text": "To authenticate API requests, include Bearer token in Authorization header...",
    "metadata": DocumentMetadata(
        title="API Authentication Guide",
        description="Production API authentication procedures",
        content_type="documentation",
        created_at=datetime(2026, 1, 15),
        updated_at=datetime(2026, 3, 10),
        created_by="engineering@company.com",
        updated_by="security@company.com",
        version="2.1",
        status="approved",
        access_level="internal",
        department="engineering",
        allowed_roles=["engineer", "product_manager"],
        source_system="confluence",
        source_url="https://wiki.company.com/api-auth",
        ingestion_date=datetime(2026, 3, 11),
        categories=["api", "authentication", "security"],
        tags=["production", "critical"],
        priority="high",
        contains_pii=False,
        data_classification="internal",
        review_status="approved",
        last_reviewed_by="security_team",
        last_reviewed_at=datetime(2026, 3, 10)
    )
}
```

**Using Metadata for Filtering in Vector Search:**

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

vector_db = QdrantClient(host="localhost", port=6333)

def search_with_metadata_filters(
    query_embedding: list[float],
    filters: dict = None
) -> list[dict]:
    """
    Search with metadata filtering - dramatically reduces search space.
    
    Example: Instead of searching 1M documents, filter to 10K, then search.
    Result: 100x faster, more relevant results.
    """
    # Build filter conditions from metadata
    filter_conditions = []
    
    if filters:
        # Date range filter
        if "date_after" in filters:
            filter_conditions.append(
                FieldCondition(
                    key="metadata.created_at",
                    range=Range(gte=filters["date_after"])
                )
            )
        
        # Category filter (exact match)
        if "category" in filters:
            filter_conditions.append(
                FieldCondition(
                    key="metadata.categories",
                    match=MatchValue(value=filters["category"])
                )
            )
        
        # Access level filter (security)
        if "max_access_level" in filters:
            allowed_levels = ["public", "internal"]
            if filters["max_access_level"] == "confidential":
                allowed_levels.append("confidential")
            
            filter_conditions.append(
                FieldCondition(
                    key="metadata.access_level",
                    match=MatchValue(any=allowed_levels)
                )
            )
        
        # Status filter (only approved docs)
        if "only_approved" in filters and filters["only_approved"]:
            filter_conditions.append(
                FieldCondition(
                    key="metadata.status",
                    match=MatchValue(value="approved")
                )
            )
        
        # Department filter
        if "department" in filters:
            filter_conditions.append(
                FieldCondition(
                    key="metadata.department",
                    match=MatchValue(value=filters["department"])
                )
            )
    
    # Search with filters
    results = vector_db.search(
        collection_name="knowledge_base",
        query_vector=query_embedding,
        query_filter=Filter(must=filter_conditions) if filter_conditions else None,
        limit=10
    )
    
    return [
        {
            "id": hit.id,
            "text": hit.payload["text"],
            "score": hit.score,
            "metadata": hit.payload["metadata"]
        }
        for hit in results
    ]

# Example: Filtered search
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
query = "How do I authenticate API requests?"
query_embedding = model.encode(query)

# Search with multiple metadata filters
results = search_with_metadata_filters(
    query_embedding,
    filters={
        "date_after": "2025-01-01",  # Only recent docs
        "category": "api",            # Only API docs
        "only_approved": True,        # Only approved docs
        "department": "engineering",  # Only engineering docs
        "max_access_level": "internal"  # User can only see up to internal
    }
)

print(f"Found {len(results)} documents matching filters:")
for result in results:
    meta = result["metadata"]
    print(f"\nTitle: {meta['title']}")
    print(f"  Created: {meta['created_at']} by {meta['created_by']}")
    print(f"  Status: {meta['status']} | Access: {meta['access_level']}")
    print(f"  Categories: {', '.join(meta['categories'])}")
    print(f"  Score: {result['score']:.3f}")
```

**Metadata in RAG Systems:**

```python
from openai import OpenAI

openai_client = OpenAI()

def rag_with_metadata_context(question: str, user_role: str = "engineer") -> dict:
    """
    RAG system that uses metadata for:
    1. Filtering (access control, recency)
    2. Context enrichment (tell LLM about source quality)
    3. Citation tracking (provide source provenance)
    """
    # Generate query embedding
    query_embedding = model.encode(question)
    
    # Search with metadata filters
    results = search_with_metadata_filters(
        query_embedding,
        filters={
            "date_after": "2025-01-01",
            "only_approved": True,
            "max_access_level": get_access_level_for_role(user_role)
        }
    )
    
    # Build context with metadata enrichment
    context_parts = []
    
    for i, result in enumerate(results, 1):
        meta = result["metadata"]
        
        # Include metadata in context for LLM
        context_parts.append(f"""
[Source {i}]
Title: {meta['title']}
Created: {meta['created_at'].strftime('%Y-%m-%d')} by {meta['created_by']}
Last Updated: {meta['updated_at'].strftime('%Y-%m-%d')}
Status: {meta['status']} | Version: {meta['version']}
Categories: {', '.join(meta['categories'])}

Content:
{result['text']}
""")
    
    context = "\n---\n".join(context_parts)
    
    # Generate answer with metadata-enriched context
    prompt = f"""Answer the question using the provided sources. When citing sources, reference them by number [1], [2], etc.

Sources:
{context}

Question: {question}

Answer (cite sources and note their recency/status):"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": [
            {
                "title": r["metadata"]["title"],
                "created": r["metadata"]["created_at"],
                "status": r["metadata"]["status"],
                "url": r["metadata"].get("source_url")
            }
            for r in results
        ]
    }

# Example with metadata-aware response
result = rag_with_metadata_context(
    "How do I handle API rate limiting?",
    user_role="engineer"
)

print(result["answer"])
# Output includes metadata context:
# "According to the API Rate Limiting Guide [1] (approved, last updated 2026-02-15),
# you should implement exponential backoff..."

print("\nSources:")
for source in result["sources"]:
    print(f"- {source['title']} ({source['status']}, {source['created']})")
```

**Metadata for Audit Trails and Compliance:**

```python
from datetime import datetime
import json

class MetadataAuditLog:
    """Track all access to documents for compliance/security."""
    
    def log_access(
        self,
        document_id: str,
        user_id: str,
        action: str,
        metadata_snapshot: dict
    ):
        """Log document access with full metadata context."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "document_id": document_id,
            "user_id": user_id,
            "action": action,  # "view", "search", "cite"
            "metadata": {
                "title": metadata_snapshot.get("title"),
                "access_level": metadata_snapshot.get("access_level"),
                "contains_pii": metadata_snapshot.get("contains_pii"),
                "department": metadata_snapshot.get("department")
            }
        }
        
        # Store in audit log
        self._store_log(log_entry)
        
        # Alert if sensitive access
        if metadata_snapshot.get("contains_pii") or \
           metadata_snapshot.get("access_level") == "confidential":
            self._alert_security_team(log_entry)
    
    def compliance_report(self, start_date: str, end_date: str) -> dict:
        """Generate compliance report using metadata."""
        logs = self._query_logs(start_date, end_date)
        
        return {
            "total_accesses": len(logs),
            "pii_accesses": len([l for l in logs if l["metadata"]["contains_pii"]]),
            "confidential_accesses": len([
                l for l in logs 
                if l["metadata"]["access_level"] == "confidential"
            ]),
            "accesses_by_department": self._group_by(logs, "metadata.department"),
            "top_accessed_documents": self._top_documents(logs, limit=10)
        }

audit = MetadataAuditLog()

# Log every search/retrieval
audit.log_access(
    document_id="doc_12345",
    user_id="user@company.com",
    action="search_result",
    metadata_snapshot=document["metadata"].dict()
)

# Generate monthly compliance report
report = audit.compliance_report("2026-05-01", "2026-05-31")
print(f"PII accesses: {report['pii_accesses']}")
print(f"Confidential accesses: {report['confidential_accesses']}")
```

### What It Isn't
Metadata is not **the actual content**. It describes content but doesn't contain the information you're searching for. You can't answer "What's the API authentication process?" from metadata alone—you need the actual document content.

It's not **automatically accurate or maintained**. Metadata is only as good as the processes creating it. Stale metadata ("marked as reviewed in 2024 but actually outdated") is worse than no metadata—it gives false confidence.

Metadata is not **free**. Every metadata field adds storage, indexing overhead, and maintenance burden. Don't add fields "just in case"—design metadata schemas based on actual filtering, auditing, and organizational needs.

It's not **a replacement for good search**. Metadata enables filtering, but you still need quality content, embeddings, and ranking. Metadata narrows the search space; semantic search finds the best matches within that space.

Metadata is not **universally standardized**. Different systems, domains, and organizations use different metadata schemas. "Category" in one system might be "Type" in another. Establish consistent schemas within your organization.

Finally, it's not **automatically enforced**. Without validation and governance, metadata quality degrades—users enter free text in structured fields, leave required fields empty, or use inconsistent values. Implement validation, controlled vocabularies, and regular audits.

## How It Works

### Designing Effective Metadata Schemas

**Step 1: Identify Use Cases**
```python
# Start with questions you need to answer:

use_cases = {
    "filtering": [
        "Show me only production documentation",
        "Find docs updated in last 6 months",
        "Only engineering department content"
    ],
    "access_control": [
        "What can this user access based on role?",
        "Which docs contain sensitive information?"
    ],
    "audit": [
        "Who accessed what when?",
        "Track all PII document access"
    ],
    "quality": [
        "Which docs need review?",
        "What's been approved vs draft?"
    ],
    "context": [
        "When was this written?",
        "Who's the authoritative source?",
        "Is this still current?"
    ]
}

# Design metadata to answer these questions
```

**Step 2: Choose Metadata Fields Strategically**
```python
class MetadataDesign:
    """
    Design metadata with the USEFUL principle:
    - Useful: Answers real questions
    - Searchable: Can filter/query on it
    - Enforceable: Can validate values
    - Feasible: Users can/will populate it
    - Updatable: Can maintain over time
    - Lightweight: Not excessive burden
    """
    
    # Good metadata fields (commonly used, easy to populate)
    essential_fields = {
        "created_at": "datetime",      # Automatic
        "updated_at": "datetime",      # Automatic
        "created_by": "string",        # From auth system
        "department": "enum",          # Controlled list
        "status": "enum",              # ["draft", "approved", "archived"]
        "categories": "list[string]",  # Controlled taxonomy
        "access_level": "enum"         # ["public", "internal", "confidential"]
    }
    
    # Optional fields (add if specific need exists)
    optional_fields = {
        "review_due_date": "datetime",     # For regulated content
        "contains_pii": "boolean",         # For compliance
        "version": "string",               # For versioned docs
        "language": "string",              # For multilingual
        "priority": "enum",                # For triage
        "related_docs": "list[string]"    # For knowledge graphs
    }
    
    # Avoid these (hard to maintain, rarely used)
    avoid_fields = {
        "keywords": "free text",           # Use categories instead
        "abstract": "free text",           # Use description or AI summary
        "custom_field_17": "unknown",      # Unclear purpose
        "importance": "subjective",        # Too subjective, use priority
        "tags": "uncontrolled free text"  # Use controlled vocabulary
    }
```

**Step 3: Implement Metadata Validation**
```python
from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import List, Optional

class ValidatedMetadata(BaseModel):
    """Metadata with validation rules enforced."""
    
    # Required fields with validation
    title: str = Field(..., min_length=5, max_length=200)
    content_type: str = Field(..., regex="^(documentation|code|policy|guide)$")
    department: str = Field(..., regex="^(engineering|sales|hr|legal|product)$")
    access_level: str = Field(..., regex="^(public|internal|confidential|restricted)$")
    
    # Controlled vocabularies
    categories: List[str] = Field(default_factory=list)
    status: str = Field(default="draft", regex="^(draft|review|approved|archived)$")
    
    # Timestamps (auto-populated)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator('categories')
    def validate_categories(cls, v):
        """Ensure categories from controlled list."""
        allowed_categories = {
            "api", "authentication", "security", "deployment",
            "database", "networking", "monitoring", "testing"
        }
        
        for cat in v:
            if cat not in allowed_categories:
                raise ValueError(
                    f"Category '{cat}' not in allowed list: {allowed_categories}"
                )
        
        return v
    
    @validator('updated_at')
    def updated_must_be_recent(cls, v, values):
        """Ensure updated_at >= created_at."""
        if 'created_at' in values and v < values['created_at']:
            raise ValueError("updated_at cannot be before created_at")
        return v
    
    class Config:
        # Reject unknown fields (strict schema)
        extra = 'forbid'

# Usage with validation
try:
    metadata = ValidatedMetadata(
        title="API Guide",
        content_type="documentation",
        department="engineering",
        access_level="internal",
        categories=["api", "authentication"],
        status="approved"
    )
    print("✓ Metadata valid")
except ValueError as e:
    print(f"✗ Validation error: {e}")

# Invalid metadata caught at creation time
try:
    bad_metadata = ValidatedMetadata(
        title="API Guide",
        content_type="unknown_type",  # Not in allowed list
        department="engineering",
        access_level="internal",
        categories=["invalid_category"]  # Not in allowed list
    )
except ValueError as e:
    print(f"✗ Caught invalid metadata: {e}")
```

**Step 4: Metadata Lifecycle Management**
```python
class MetadataManager:
    """Manage metadata throughout document lifecycle."""
    
    def create_document(self, content: str, initial_metadata: dict) -> dict:
        """Create document with validated metadata."""
        metadata = ValidatedMetadata(**initial_metadata)
        
        return {
            "id": generate_id(),
            "content": content,
            "metadata": metadata.dict(),
            "version_history": []
        }
    
    def update_document(self, doc_id: str, new_content: str) -> dict:
        """Update document and metadata."""
        doc = self.get_document(doc_id)
        
        # Archive old version
        doc["version_history"].append({
            "content": doc["content"],
            "metadata": doc["metadata"],
            "archived_at": datetime.now()
        })
        
        # Update content and metadata
        doc["content"] = new_content
        doc["metadata"]["updated_at"] = datetime.now()
        doc["metadata"]["version"] = increment_version(doc["metadata"]["version"])
        
        return doc
    
    def review_document(self, doc_id: str, reviewer: str, approved: bool) -> dict:
        """Update review metadata."""
        doc = self.get_document(doc_id)
        
        doc["metadata"]["review_status"] = "approved" if approved else "needs_update"
        doc["metadata"]["last_reviewed_by"] = reviewer
        doc["metadata"]["last_reviewed_at"] = datetime.now()
        
        if approved:
            doc["metadata"]["status"] = "approved"
        
        return doc
    
    def archive_document(self, doc_id: str, reason: str) -> dict:
        """Archive document with metadata trail."""
        doc = self.get_document(doc_id)
        
        doc["metadata"]["status"] = "archived"
        doc["metadata"]["archived_at"] = datetime.now()
        doc["metadata"]["archive_reason"] = reason
        
        return doc
    
    def metadata_health_check(self) -> dict:
        """Audit metadata quality across all documents."""
        docs = self.get_all_documents()
        
        issues = {
            "stale_docs": [],      # Not reviewed in 1+ year
            "missing_categories": [],  # No categories assigned
            "drafts_too_old": [],  # Drafts > 30 days old
            "missing_owner": []    # No created_by
        }
        
        for doc in docs:
            meta = doc["metadata"]
            
            # Check staleness
            if meta.get("last_reviewed_at"):
                days_since_review = (datetime.now() - meta["last_reviewed_at"]).days
                if days_since_review > 365:
                    issues["stale_docs"].append(doc["id"])
            
            # Check categories
            if not meta.get("categories"):
                issues["missing_categories"].append(doc["id"])
            
            # Check draft age
            if meta.get("status") == "draft":
                days_old = (datetime.now() - meta["created_at"]).days
                if days_old > 30:
                    issues["drafts_too_old"].append(doc["id"])
            
            # Check ownership
            if not meta.get("created_by"):
                issues["missing_owner"].append(doc["id"])
        
        return {
            "total_docs": len(docs),
            "issues_found": sum(len(v) for v in issues.values()),
            "issues": issues
        }

manager = MetadataManager()

# Run health check
health = manager.metadata_health_check()
print(f"Metadata health: {health['issues_found']} issues in {health['total_docs']} docs")
```

## Think of It Like This
Imagine you're organizing a massive library.

**Without metadata**, books are just piled on shelves. To find "recent books about Python programming," you must physically examine each book—read the title page, check the copyright date, skim the content. With 100,000 books, this is impossible.

**With metadata**, each book has a card with structured information: Title, Author, Publication Year, Category, Dewey Decimal, Keywords, Reading Level, Language. Now you can instantly answer:
- "Show me Python books from 2025-2026" (filter by category + year)
- "Find beginner-level programming books" (filter by reading level + category)
- "Which books are checked out?" (status metadata)
- "Who donated this book?" (provenance metadata)

The **card catalog** (metadata) lets you filter, organize, and find books without reading them. In AI systems, metadata serves the same purpose—enabling instant filtering, access control, audit trails, and context without processing actual content.

## The "So What?" Factor
**If you implement rich metadata:**
- Searches return more relevant results through pre-filtering (reduce 1M docs to 10K, then search)
- Access control is automatic—users only see what they're authorized to see
- Compliance is auditable—track all PII access, generate reports on demand
- Context is richer—LLMs know "this is approved, from 2026, by engineering team"
- Performance improves—filter before expensive similarity search
- Quality is trackable—identify stale docs, missing reviews, orphaned content
- Users trust results—see when created, who approved, how current
- Debugging is easier—trace documents through lifecycle with metadata trails
- Personalization works—filter by user's department, role, permissions
- ROI is measurable—track document usage, access patterns, value

**If you skip metadata or implement poorly:**
- Every search scans everything—slow, expensive, returns irrelevant results
- Access control is manual or broken—security risks, compliance violations
- Audit questions are unanswerable—"who accessed this?" → "no idea"
- Context is missing—agents cite sources without provenance or freshness
- Stale content pollutes results—outdated docs rank equally with current
- Quality degrades invisibly—no way to identify docs needing review
- Users distrust results—can't verify source, date, authority
- Debugging is impossible—can't trace document issues or changes
- Performance suffers—must search entire corpus every time
- Compliance failures—can't prove due diligence, risk fines

## Practical Checklist
Before implementing metadata, ask yourself:
- [ ] Have I identified specific use cases (filtering, access control, audit)?
- [ ] Are my metadata fields answering real questions or just "nice to have"?
- [ ] Have I designed a controlled vocabulary for categorical fields?
- [ ] Am I auto-populating fields when possible (timestamps, user IDs)?
- [ ] Have I implemented validation to enforce schema rules?
- [ ] Can users easily populate required metadata (not excessive burden)?
- [ ] Have I documented what each metadata field means and how to use it?
- [ ] Do I have a plan for maintaining metadata quality over time?
- [ ] Am I storing metadata efficiently (not duplicating in every system)?
- [ ] Have I implemented metadata-based access control properly?
- [ ] Can I generate audit reports from metadata?
- [ ] Have I tested metadata filtering performance at scale?

## Watch Out For
⚠️ **Metadata bloat**: Don't add fields "just in case." Every field adds maintenance burden. Design based on actual use cases, not theoretical ones.

⚠️ **Free text in structured fields**: "Category" becomes useless if users enter "APIs", "api", "API docs", "api documentation" (all meaning the same). Use enums or controlled vocabularies.

⚠️ **Stale metadata**: "Reviewed on 2023-01-15" but content changed in 2026—metadata is now misleading. Implement triggers to flag metadata when content changes.

⚠️ **Over-reliance on manual entry**: Required fields users must fill = incomplete metadata. Auto-populate whenever possible (timestamps, user IDs, system of record).

⚠️ **Inconsistent schemas**: Different teams using different metadata structures makes aggregation impossible. Establish organization-wide standards.

⚠️ **No validation**: Without validation, "access_level" contains "Public", "public", "PUBLIC", "pub", "everyone" (all meaning the same). Enforce schema validation at write time.

⚠️ **Ignoring metadata in UI**: If users can't see/use metadata (filter by date, sort by priority), they won't maintain it. Surface metadata prominently in interfaces.

⚠️ **Forgetting versioning**: Metadata changes over time (document marked confidential later). Track metadata history for audit trails.

⚠️ **Storage inefficiency**: Storing full metadata with every embedding/chunk wastes space. Store once, reference by ID.

⚠️ **Access control bypass**: Metadata filtering happens in application—ensure database-level enforcement so users can't bypass filters via direct queries.

## Connections
**Builds On:**
- Database schemas and data modeling
- Information architecture principles
- [json_schema](json_schema.md) - Structured schema definitions

**Works With:**
- [semantic_search](semantic_search.md) - Metadata filtering before/during search
- [vector_database](vector_database.md) - Storing and filtering on metadata
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - Enriching context with metadata
- [reranking](reranking.md) - Using metadata in reranking logic
- [document_chunking](document_chunking.md) - Preserving metadata across chunks
- [indexing](indexing.md) - Creating indexes on metadata fields
- [knowledge_graph](knowledge_graph.md) - Metadata as graph properties

**Leads To:**
- Data catalogs and discovery systems
- Access control and security frameworks
- Compliance and audit systems
- Provenance tracking and lineage
- Data quality monitoring

**Related Patterns:**
- [caching](caching.md) - Caching metadata-filtered results
- [data_pipeline](data_pipeline.md) - Enriching data with metadata in pipelines
- Controlled vocabularies and taxonomies
- Master data management (MDM)
- Data governance frameworks

## Quick Decision Guide
**Prioritize these metadata fields:**
- **Always**: created_at, updated_at, created_by, status, access_level
- **Usually**: department, categories, content_type, version
- **Compliance**: contains_pii, data_classification, retention_period
- **Quality**: review_status, last_reviewed_at, last_reviewed_by
- **Provenance**: source_system, ingestion_date, source_url

**Start simple, expand based on need:**
- Phase 1: Basic (timestamps, creator, status)
- Phase 2: Access control (permissions, classification)
- Phase 3: Quality (review tracking, versioning)
- Phase 4: Advanced (provenance, relationships, custom fields)

**Use controlled vocabularies for:**
- Status, priority, content type, department, access level, categories

**Auto-populate when possible:**
- Timestamps, user IDs, system of record, ingestion date

**Skip metadata when:**
- Temporary/scratch data (no long-term value)
- Computational burden outweighs benefits
- No actual filtering/audit use cases
- Data is already fully structured (metadata IS the data)

## Further Exploration
- 📖 "Dublin Core Metadata Initiative" - Standard metadata schema for digital resources
- 🎯 "Metadata Management in Data Warehouses" - Enterprise metadata patterns
- 💡 "Vector Database Metadata Filtering Best Practices" - Qdrant, Pinecone docs
- 📖 "Data Governance and Metadata Management" - Organizational metadata strategies
- 🎯 JSON Schema documentation - Metadata schema validation
- 💡 "Metadata-Driven RAG Systems" - Using metadata to improve retrieval
- 📖 "Linked Data and Metadata" - Semantic web metadata approaches
- 🎯 "Audit Logging Best Practices" - Using metadata for compliance
- 💡 "Data Catalogs: Finding and Understanding Data" - Metadata for discovery
- 📖 "Provenance in Data Systems" - Tracking data lineage with metadata

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
