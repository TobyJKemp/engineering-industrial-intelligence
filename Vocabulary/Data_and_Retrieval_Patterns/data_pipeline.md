# Data Pipeline

## At a Glance
| | |
|---|---|
| **Category** | Infrastructure Pattern |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 4-8 hours for fundamentals, weeks for production expertise |
| **Prerequisites** | Understanding of [document_chunking](document_chunking.md), [embeddings](../Foundational_AI & ML/embeddings.md), [vector_database](vector_database.md), [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) |

## One-Sentence Summary
A data pipeline is an automated workflow that ingests, transforms, and loads data from sources to destinations—in RAG systems, this means continuously pulling documents from your knowledge base, cleaning and chunking them, generating embeddings, and indexing them in vector databases so your AI agents always have access to current, properly formatted information without manual intervention.

## Why This Matters to You
When you build RAG systems in 2026, data pipelines are the difference between a proof-of-concept demo and a production system. Without a pipeline, you manually run scripts to chunk documents, generate embeddings, and load vector databases—every time documents change, you repeat this tedious process, inevitably missing updates or making mistakes. With a data pipeline, new documents are automatically detected, processed, and indexed within minutes; updated documents trigger re-processing of affected chunks; deleted documents are removed from the index; and quality checks validate every step, alerting you to problems. Your knowledge base stays synchronized with source documents, embeddings use consistent parameters, chunk sizes remain optimal, and you have full observability into what's indexed and when. Data pipelines handle the unglamorous but critical infrastructure: monitoring SharePoint for new policy documents, extracting text from PDFs, splitting into chunks with proper overlap, generating embeddings with the right model, upserting to vector databases with deduplication, tracking lineage for debugging, and maintaining metadata for filtering. Without pipelines, your RAG system degrades silently—users ask about new features but the documentation isn't indexed, policies change but old chunks remain searchable, embeddings use inconsistent models creating incomparable similarity scores. With pipelines, your knowledge base is a living, reliable asset that scales from hundreds to millions of documents, updates automatically, maintains quality standards, and provides audit trails for compliance. Understanding data pipeline architecture, orchestration patterns, error handling, and monitoring is essential for operating RAG systems that businesses can trust in production.

## The Core Idea
### What It Is
A data pipeline is an automated, orchestrated sequence of operations that moves data from source systems through transformation stages to destination systems, with built-in error handling, monitoring, and quality validation. For RAG systems specifically, data pipelines automate the journey from raw documents to searchable vector embeddings.

**Typical RAG Data Pipeline Stages:**

```
Sources → Ingestion → Extraction → Chunking → Embedding → Indexing → Monitoring
   ↓          ↓            ↓           ↓            ↓          ↓          ↓
Files    Load docs    Parse text   Split into   Generate   Store in  Track health
DBs      Track new    Clean HTML   chunks with  vectors    vector    Alert issues
APIs     Handle       Normalize    overlap      Batch      database  Measure lag
```

**Stage 1: Ingestion - Load Documents from Sources**
```python
import os
from pathlib import Path
from datetime import datetime
import hashlib
import json

class DocumentIngester:
    """
    Load documents from various sources.
    
    Responsibilities:
    - Detect new/updated documents
    - Load document content
    - Track processing state
    - Handle errors gracefully
    """
    
    def __init__(self, state_file: str = "ingestion_state.json"):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load previous ingestion state (which docs processed)."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"processed_files": {}}
    
    def _save_state(self):
        """Save current state for incremental processing."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _compute_file_hash(self, file_path: str) -> str:
        """Compute hash to detect if file changed."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def ingest_from_directory(
        self,
        directory: str,
        extensions: list[str] = ['.txt', '.md', '.pdf'],
        incremental: bool = True
    ) -> list[dict]:
        """
        Ingest documents from local directory.
        
        Args:
            directory: Path to scan
            extensions: File types to process
            incremental: Only process new/changed files
        
        Returns:
            List of documents with metadata
        """
        documents = []
        processed_count = 0
        skipped_count = 0
        
        for file_path in Path(directory).rglob("*"):
            if file_path.suffix.lower() not in extensions:
                continue
            
            file_path_str = str(file_path)
            file_hash = self._compute_file_hash(file_path_str)
            
            # Check if already processed (incremental mode)
            if incremental:
                previous_hash = self.state["processed_files"].get(file_path_str)
                if previous_hash == file_hash:
                    skipped_count += 1
                    continue  # Skip unchanged files
            
            # Load document content
            try:
                if file_path.suffix == '.pdf':
                    content = self._extract_pdf(file_path_str)
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                
                # Create document record
                doc = {
                    "content": content,
                    "metadata": {
                        "source": file_path_str,
                        "file_name": file_path.name,
                        "file_type": file_path.suffix,
                        "file_size": os.path.getsize(file_path_str),
                        "modified_time": datetime.fromtimestamp(
                            os.path.getmtime(file_path_str)
                        ).isoformat(),
                        "ingestion_time": datetime.now().isoformat(),
                        "file_hash": file_hash
                    }
                }
                
                documents.append(doc)
                
                # Update state
                self.state["processed_files"][file_path_str] = file_hash
                processed_count += 1
                
            except Exception as e:
                print(f"Error ingesting {file_path}: {e}")
                continue
        
        # Save state for next run
        self._save_state()
        
        print(f"Ingestion complete: {processed_count} processed, {skipped_count} skipped")
        
        return documents
    
    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF (placeholder - would use PyPDF2/pdfplumber)."""
        # In production: use PyPDF2 or pdfplumber
        # from PyPDF2 import PdfReader
        # reader = PdfReader(file_path)
        # text = "\n".join(page.extract_text() for page in reader.pages)
        # return text
        return f"[PDF content from {file_path}]"
    
    def ingest_from_database(
        self,
        connection_string: str,
        query: str,
        text_column: str,
        metadata_columns: list[str]
    ) -> list[dict]:
        """
        Ingest documents from database query.
        
        Example:
            SELECT id, content, title, category, updated_at
            FROM knowledge_base
            WHERE updated_at > ?
        """
        # Placeholder - would use actual database connection
        documents = []
        
        # import sqlalchemy
        # engine = sqlalchemy.create_engine(connection_string)
        # result = engine.execute(query, last_run_time)
        # 
        # for row in result:
        #     doc = {
        #         "content": row[text_column],
        #         "metadata": {col: row[col] for col in metadata_columns}
        #     }
        #     documents.append(doc)
        
        return documents
    
    def ingest_from_api(
        self,
        api_url: str,
        api_key: str,
        since: datetime = None
    ) -> list[dict]:
        """
        Ingest documents from REST API.
        
        Example: Confluence, Notion, Google Docs APIs
        """
        import requests
        
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {}
        
        if since:
            params["updated_since"] = since.isoformat()
        
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            documents = []
            for item in data.get("results", []):
                doc = {
                    "content": item.get("content", ""),
                    "metadata": {
                        "source": "api",
                        "api_id": item.get("id"),
                        "title": item.get("title"),
                        "updated": item.get("updated_at")
                    }
                }
                documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"API ingestion error: {e}")
            return []

# Usage
ingester = DocumentIngester()

# Incremental ingestion - only process new/changed files
docs = ingester.ingest_from_directory(
    "./company_docs",
    extensions=['.txt', '.md', '.pdf'],
    incremental=True
)

print(f"Ingested {len(docs)} documents")
```

**Stage 2: Extraction & Cleaning - Prepare Text**
```python
import re
from bs4 import BeautifulSoup

class DocumentCleaner:
    """
    Extract and clean text from various formats.
    
    Responsibilities:
    - Remove HTML/markup
    - Normalize whitespace
    - Fix encoding issues
    - Remove boilerplate
    """
    
    def clean_html(self, html_content: str) -> str:
        """Extract clean text from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def clean_markdown(self, markdown_content: str) -> str:
        """Clean markdown (preserve structure or extract plain text)."""
        # Option 1: Keep markdown structure for structure-aware chunking
        # return markdown_content
        
        # Option 2: Convert to plain text
        # Remove links: [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', markdown_content)
        
        # Remove images: ![alt](url) -> ""
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
        
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        
        return text
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace and line breaks."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple line breaks with double (paragraph break)
        text = re.sub(r'\n\n+', '\n\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_boilerplate(self, text: str, patterns: list[str]) -> str:
        """
        Remove common boilerplate text.
        
        Examples:
        - Email signatures
        - Headers/footers
        - Copyright notices
        - Navigation text
        """
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text
    
    def process_document(self, document: dict) -> dict:
        """Process single document through cleaning pipeline."""
        content = document["content"]
        file_type = document["metadata"].get("file_type", "")
        
        # Clean based on file type
        if file_type in ['.html', '.htm']:
            content = self.clean_html(content)
        elif file_type == '.md':
            content = self.clean_markdown(content)
        
        # Normalize whitespace
        content = self.normalize_whitespace(content)
        
        # Remove common boilerplate
        boilerplate_patterns = [
            r'Copyright \d{4}.*',
            r'All rights reserved.*',
            r'Confidential and proprietary.*'
        ]
        content = self.remove_boilerplate(content, boilerplate_patterns)
        
        # Update document
        document["content"] = content
        document["metadata"]["cleaned"] = True
        document["metadata"]["cleaned_time"] = datetime.now().isoformat()
        
        return document

# Usage
cleaner = DocumentCleaner()

cleaned_docs = []
for doc in docs:
    cleaned_doc = cleaner.process_document(doc)
    cleaned_docs.append(cleaned_doc)

print(f"Cleaned {len(cleaned_docs)} documents")
```

**Stage 3: Chunking - Split Documents**
```python
from typing import Callable

class PipelineChunker:
    """
    Chunk documents as part of pipeline.
    
    Wraps chunking logic with pipeline-specific concerns:
    - Metadata preservation
    - Error handling
    - Progress tracking
    """
    
    def __init__(self, chunk_function: Callable):
        """
        Args:
            chunk_function: Function that chunks text
                Signature: (text: str, **kwargs) -> list[dict]
        """
        self.chunk_function = chunk_function
    
    def process_documents(
        self,
        documents: list[dict],
        chunk_size: int = 512,
        overlap: int = 50
    ) -> list[dict]:
        """
        Chunk all documents, preserving metadata.
        
        Returns:
            List of chunks with full lineage
        """
        all_chunks = []
        
        for doc_idx, doc in enumerate(documents):
            try:
                # Chunk document
                chunks = self.chunk_function(
                    doc["content"],
                    chunk_size=chunk_size,
                    overlap=overlap
                )
                
                # Enrich each chunk with metadata
                for chunk_idx, chunk in enumerate(chunks):
                    enriched_chunk = {
                        "text": chunk.get("text", chunk),  # Handle dict or string
                        "chunk_id": f"{doc['metadata'].get('source', 'unknown')}_{chunk_idx}",
                        "chunk_index": chunk_idx,
                        "total_chunks": len(chunks),
                        "source_document": doc["metadata"],
                        "chunking_params": {
                            "chunk_size": chunk_size,
                            "overlap": overlap
                        },
                        "pipeline_metadata": {
                            "chunked_time": datetime.now().isoformat(),
                            "doc_index": doc_idx
                        }
                    }
                    all_chunks.append(enriched_chunk)
                    
            except Exception as e:
                print(f"Error chunking document {doc_idx}: {e}")
                continue
        
        print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        
        return all_chunks

# Usage (assuming chunk_by_tokens from document_chunking.md)
from document_chunking import chunk_by_tokens

chunker = PipelineChunker(chunk_function=chunk_by_tokens)

chunks = chunker.process_documents(
    cleaned_docs,
    chunk_size=512,
    overlap=50
)

print(f"Pipeline produced {len(chunks)} chunks")
```

**Stage 4: Embedding - Generate Vectors**
```python
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import time

class EmbeddingGenerator:
    """
    Generate embeddings with batching and error handling.
    
    Responsibilities:
    - Batch processing for efficiency
    - Rate limiting for API-based models
    - Retry logic for transient failures
    - Progress tracking
    """
    
    def __init__(
        self,
        model_name: str = 'all-MiniLM-L6-v2',
        batch_size: int = 32
    ):
        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size
        self.model_name = model_name
    
    def generate_embeddings(
        self,
        chunks: list[dict],
        show_progress: bool = True
    ) -> list[dict]:
        """
        Generate embeddings for all chunks in batches.
        
        Returns:
            Chunks with 'embedding' field added
        """
        total_chunks = len(chunks)
        
        for i in range(0, total_chunks, self.batch_size):
            batch = chunks[i:i + self.batch_size]
            batch_texts = [chunk["text"] for chunk in batch]
            
            try:
                # Generate embeddings for batch
                embeddings = self.model.encode(
                    batch_texts,
                    show_progress_bar=False,
                    convert_to_numpy=True
                )
                
                # Add embeddings to chunks
                for chunk, embedding in zip(batch, embeddings):
                    chunk["embedding"] = embedding.tolist()
                    chunk["embedding_model"] = self.model_name
                    chunk["embedding_time"] = datetime.now().isoformat()
                
                if show_progress and (i + self.batch_size) % 100 == 0:
                    print(f"Embedded {min(i + self.batch_size, total_chunks)}/{total_chunks} chunks")
                    
            except Exception as e:
                print(f"Error embedding batch {i}-{i+self.batch_size}: {e}")
                # Mark chunks as failed
                for chunk in batch:
                    chunk["embedding_error"] = str(e)
                continue
        
        # Count successes
        embedded_count = sum(1 for c in chunks if "embedding" in c)
        print(f"Successfully embedded {embedded_count}/{total_chunks} chunks")
        
        return chunks

# Usage
embedder = EmbeddingGenerator(
    model_name='all-MiniLM-L6-v2',
    batch_size=32
)

embedded_chunks = embedder.generate_embeddings(chunks)

print(f"Generated {len(embedded_chunks)} embeddings")
```

**Stage 5: Indexing - Store in Vector Database**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

class VectorIndexer:
    """
    Index embeddings in vector database.
    
    Responsibilities:
    - Upsert to vector database
    - Handle duplicates
    - Batch operations
    - Verify indexing success
    """
    
    def __init__(
        self,
        vector_db_url: str,
        collection_name: str = "knowledge_base"
    ):
        self.client = QdrantClient(url=vector_db_url)
        self.collection_name = collection_name
    
    def initialize_collection(
        self,
        vector_size: int = 384,
        distance: Distance = Distance.COSINE,
        recreate: bool = False
    ):
        """Create or verify collection exists."""
        try:
            if recreate:
                self.client.delete_collection(self.collection_name)
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance
                )
            )
            print(f"Collection '{self.collection_name}' initialized")
            
        except Exception as e:
            print(f"Collection may already exist: {e}")
    
    def index_chunks(
        self,
        chunks: list[dict],
        batch_size: int = 100
    ) -> dict:
        """
        Index chunks in vector database.
        
        Returns:
            Statistics about indexing operation
        """
        points = []
        skipped = 0
        
        for chunk in chunks:
            # Skip chunks without embeddings
            if "embedding" not in chunk:
                skipped += 1
                continue
            
            # Create point for vector database
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=chunk["embedding"],
                payload={
                    "text": chunk["text"],
                    "chunk_id": chunk["chunk_id"],
                    "chunk_index": chunk["chunk_index"],
                    "source": chunk["source_document"].get("source"),
                    "metadata": chunk["source_document"],
                    "indexed_time": datetime.now().isoformat()
                }
            )
            points.append(point)
            
            # Batch upsert
            if len(points) >= batch_size:
                self._upsert_batch(points)
                points = []
        
        # Upsert remaining
        if points:
            self._upsert_batch(points)
        
        indexed_count = len(chunks) - skipped
        
        return {
            "indexed": indexed_count,
            "skipped": skipped,
            "total": len(chunks)
        }
    
    def _upsert_batch(self, points: list[PointStruct]):
        """Upsert batch of points to vector database."""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Indexed batch of {len(points)} chunks")
        except Exception as e:
            print(f"Error indexing batch: {e}")

# Usage
indexer = VectorIndexer(
    vector_db_url="http://localhost:6333",
    collection_name="company_knowledge"
)

# Initialize collection (first run only)
indexer.initialize_collection(vector_size=384, recreate=False)

# Index chunks
stats = indexer.index_chunks(embedded_chunks, batch_size=100)

print(f"Indexing complete: {stats['indexed']} indexed, {stats['skipped']} skipped")
```

**Complete End-to-End Pipeline:**
```python
class RAGDataPipeline:
    """
    Complete RAG data pipeline orchestrating all stages.
    
    Stages:
    1. Ingest documents from sources
    2. Clean and extract text
    3. Chunk documents
    4. Generate embeddings
    5. Index in vector database
    6. Monitor and log
    """
    
    def __init__(
        self,
        source_directory: str,
        vector_db_url: str,
        collection_name: str = "knowledge_base",
        chunk_size: int = 512,
        overlap: int = 50,
        embedding_model: str = 'all-MiniLM-L6-v2'
    ):
        self.ingester = DocumentIngester()
        self.cleaner = DocumentCleaner()
        self.chunker = PipelineChunker(chunk_by_tokens)
        self.embedder = EmbeddingGenerator(embedding_model)
        self.indexer = VectorIndexer(vector_db_url, collection_name)
        
        self.source_directory = source_directory
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Tracking
        self.run_history = []
    
    def run(
        self,
        incremental: bool = True,
        initialize_collection: bool = False
    ) -> dict:
        """
        Execute complete pipeline.
        
        Returns:
            Statistics about pipeline run
        """
        run_start = datetime.now()
        print(f"Starting pipeline run at {run_start.isoformat()}")
        
        stats = {
            "run_start": run_start.isoformat(),
            "ingested": 0,
            "cleaned": 0,
            "chunked": 0,
            "embedded": 0,
            "indexed": 0,
            "errors": []
        }
        
        try:
            # Stage 1: Ingest
            print("\n=== Stage 1: Ingestion ===")
            documents = self.ingester.ingest_from_directory(
                self.source_directory,
                incremental=incremental
            )
            stats["ingested"] = len(documents)
            
            if len(documents) == 0:
                print("No new documents to process")
                return stats
            
            # Stage 2: Clean
            print("\n=== Stage 2: Cleaning ===")
            cleaned_docs = []
            for doc in documents:
                try:
                    cleaned = self.cleaner.process_document(doc)
                    cleaned_docs.append(cleaned)
                except Exception as e:
                    stats["errors"].append(f"Cleaning error: {e}")
            stats["cleaned"] = len(cleaned_docs)
            
            # Stage 3: Chunk
            print("\n=== Stage 3: Chunking ===")
            chunks = self.chunker.process_documents(
                cleaned_docs,
                chunk_size=self.chunk_size,
                overlap=self.overlap
            )
            stats["chunked"] = len(chunks)
            
            # Stage 4: Embed
            print("\n=== Stage 4: Embedding ===")
            embedded_chunks = self.embedder.generate_embeddings(chunks)
            stats["embedded"] = sum(1 for c in embedded_chunks if "embedding" in c)
            
            # Stage 5: Index
            print("\n=== Stage 5: Indexing ===")
            if initialize_collection:
                self.indexer.initialize_collection(recreate=False)
            
            index_stats = self.indexer.index_chunks(embedded_chunks)
            stats["indexed"] = index_stats["indexed"]
            
        except Exception as e:
            stats["errors"].append(f"Pipeline error: {e}")
            print(f"Pipeline failed: {e}")
        
        # Record completion
        run_end = datetime.now()
        stats["run_end"] = run_end.isoformat()
        stats["duration_seconds"] = (run_end - run_start).total_seconds()
        
        self.run_history.append(stats)
        
        # Print summary
        print("\n=== Pipeline Summary ===")
        print(f"Duration: {stats['duration_seconds']:.2f} seconds")
        print(f"Ingested: {stats['ingested']} documents")
        print(f"Cleaned: {stats['cleaned']} documents")
        print(f"Chunked: {stats['chunked']} chunks")
        print(f"Embedded: {stats['embedded']} chunks")
        print(f"Indexed: {stats['indexed']} chunks")
        if stats["errors"]:
            print(f"Errors: {len(stats['errors'])}")
        
        return stats

# Usage
pipeline = RAGDataPipeline(
    source_directory="./company_docs",
    vector_db_url="http://localhost:6333",
    collection_name="company_knowledge",
    chunk_size=512,
    overlap=50,
    embedding_model='all-MiniLM-L6-v2'
)

# Run pipeline
stats = pipeline.run(
    incremental=True,  # Only process new/changed files
    initialize_collection=True  # First run only
)

# Run again later (incremental - fast)
# stats = pipeline.run(incremental=True)
```

**Scheduled Pipeline Execution:**
```python
import schedule
import time

def schedule_pipeline(
    pipeline: RAGDataPipeline,
    interval_minutes: int = 60
):
    """
    Run pipeline on a schedule.
    
    Example:
        - Every hour: Catch new documents quickly
        - Every night: Full refresh
    """
    def run_incremental():
        print(f"\n{'='*60}")
        print(f"Scheduled pipeline run: {datetime.now().isoformat()}")
        print(f"{'='*60}")
        stats = pipeline.run(incremental=True)
        print(f"Completed in {stats['duration_seconds']:.2f}s")
    
    # Schedule incremental runs
    schedule.every(interval_minutes).minutes.do(run_incremental)
    
    print(f"Pipeline scheduled to run every {interval_minutes} minutes")
    print("Press Ctrl+C to stop")
    
    # Run immediately on start
    run_incremental()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)

# Schedule pipeline to run every hour
# schedule_pipeline(pipeline, interval_minutes=60)
```

### What It Isn't
A data pipeline is not **a one-time script you run manually**. The whole point of a pipeline is automation—scheduled execution, incremental processing, error recovery, and monitoring without human intervention.

It's not **just about moving data**. Pipelines include validation (Is this text valid? Are embeddings the right dimension?), transformation (cleaning, chunking), enrichment (adding metadata), and quality checks throughout.

Data pipelines are not **zero-maintenance**. Pipelines need monitoring dashboards, alerting for failures, periodic optimization (Are chunks too small? Is embedding slow?), and evolution as requirements change.

They're not **fire-and-forget**. You must track what's indexed, when it was processed, which version of models was used, and maintain audit trails for debugging and compliance.

Data pipelines are not **the same as ETL for data warehouses**. While inspired by ETL (Extract, Transform, Load), RAG pipelines have unique concerns: semantic chunking strategies, embedding model management, vector database operations, and retrieval quality optimization.

Finally, pipelines are not **a substitute for good source data**. Garbage in, garbage out. Pipelines automate processing, but if source documents are incomplete, outdated, or poorly written, your RAG system retrieves garbage efficiently.

## How It Works

### Pipeline Orchestration Patterns

**Pattern 1: Workflow Orchestration with Airflow**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'rag_knowledge_base_pipeline',
    default_args=default_args,
    description='RAG knowledge base indexing pipeline',
    schedule_interval='@hourly',  # Run every hour
    catchup=False
)

def ingest_task(**context):
    """Airflow task for ingestion."""
    ingester = DocumentIngester()
    docs = ingester.ingest_from_directory(
        "./company_docs",
        incremental=True
    )
    # Pass to next task via XCom
    context['ti'].xcom_push(key='documents', value=docs)
    return len(docs)

def clean_task(**context):
    """Airflow task for cleaning."""
    docs = context['ti'].xcom_pull(key='documents', task_ids='ingest')
    cleaner = DocumentCleaner()
    cleaned = [cleaner.process_document(doc) for doc in docs]
    context['ti'].xcom_push(key='cleaned_documents', value=cleaned)
    return len(cleaned)

def chunk_task(**context):
    """Airflow task for chunking."""
    docs = context['ti'].xcom_pull(key='cleaned_documents', task_ids='clean')
    chunker = PipelineChunker(chunk_by_tokens)
    chunks = chunker.process_documents(docs, chunk_size=512, overlap=50)
    context['ti'].xcom_push(key='chunks', value=chunks)
    return len(chunks)

def embed_task(**context):
    """Airflow task for embedding."""
    chunks = context['ti'].xcom_pull(key='chunks', task_ids='chunk')
    embedder = EmbeddingGenerator()
    embedded = embedder.generate_embeddings(chunks)
    context['ti'].xcom_push(key='embedded_chunks', value=embedded)
    return len(embedded)

def index_task(**context):
    """Airflow task for indexing."""
    chunks = context['ti'].xcom_pull(key='embedded_chunks', task_ids='embed')
    indexer = VectorIndexer("http://localhost:6333", "company_knowledge")
    stats = indexer.index_chunks(chunks)
    return stats['indexed']

# Define task dependencies
ingest = PythonOperator(task_id='ingest', python_callable=ingest_task, dag=dag)
clean = PythonOperator(task_id='clean', python_callable=clean_task, dag=dag)
chunk = PythonOperator(task_id='chunk', python_callable=chunk_task, dag=dag)
embed = PythonOperator(task_id='embed', python_callable=embed_task, dag=dag)
index = PythonOperator(task_id='index', python_callable=index_task, dag=dag)

# Set up dependencies: ingest -> clean -> chunk -> embed -> index
ingest >> clean >> chunk >> embed >> index

# Airflow UI will show: http://localhost:8080
# - DAG graph visualization
# - Task execution logs
# - Retry history
# - Performance metrics
```

**Pattern 2: Event-Driven Pipeline (Streaming)**
```python
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue

class DocumentEventHandler(FileSystemEventHandler):
    """
    Watch filesystem for changes and trigger pipeline.
    
    Use case: Near-real-time indexing as documents are added/modified
    """
    
    def __init__(self, pipeline: RAGDataPipeline, event_queue: Queue):
        self.pipeline = pipeline
        self.event_queue = event_queue
    
    def on_created(self, event):
        """File created - queue for processing."""
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            self.event_queue.put(("created", event.src_path))
    
    def on_modified(self, event):
        """File modified - queue for reprocessing."""
        if not event.is_directory:
            print(f"Modified file detected: {event.src_path}")
            self.event_queue.put(("modified", event.src_path))
    
    def on_deleted(self, event):
        """File deleted - remove from index."""
        if not event.is_directory:
            print(f"Deleted file detected: {event.src_path}")
            self.event_queue.put(("deleted", event.src_path))

async def process_events(pipeline: RAGDataPipeline, event_queue: Queue):
    """
    Process queued events asynchronously.
    
    Batches events to avoid processing one file at a time.
    """
    batch = []
    batch_size = 10
    batch_timeout = 60  # seconds
    
    while True:
        try:
            # Wait for events (with timeout to flush batch)
            while len(batch) < batch_size:
                try:
                    event = event_queue.get(timeout=1)
                    batch.append(event)
                except:
                    break
            
            # Process batch if non-empty
            if batch:
                print(f"Processing batch of {len(batch)} events")
                # Run pipeline (would filter to only affected files)
                pipeline.run(incremental=True)
                batch = []
            
            await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            break

def run_event_driven_pipeline(
    pipeline: RAGDataPipeline,
    watch_directory: str
):
    """
    Run pipeline in event-driven mode.
    
    Watches directory and processes changes in real-time.
    """
    event_queue = Queue()
    
    # Set up filesystem watcher
    event_handler = DocumentEventHandler(pipeline, event_queue)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()
    
    print(f"Watching {watch_directory} for changes...")
    
    try:
        # Process events asynchronously
        asyncio.run(process_events(pipeline, event_queue))
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

# Usage
# run_event_driven_pipeline(pipeline, "./company_docs")
```

**Pattern 3: Pipeline Monitoring & Alerting**
```python
import json
from dataclasses import dataclass, asdict
from typing import Optional
import smtplib
from email.message import EmailMessage

@dataclass
class PipelineMetrics:
    """Track pipeline health metrics."""
    timestamp: str
    documents_processed: int
    chunks_created: int
    embeddings_generated: int
    chunks_indexed: int
    duration_seconds: float
    errors_count: int
    success_rate: float

class PipelineMonitor:
    """
    Monitor pipeline health and alert on issues.
    
    Tracks:
    - Processing lag (time since last successful run)
    - Error rates
    - Performance degradation
    - Data quality issues
    """
    
    def __init__(
        self,
        alert_email: str = None,
        metrics_file: str = "pipeline_metrics.jsonl"
    ):
        self.alert_email = alert_email
        self.metrics_file = metrics_file
        self.thresholds = {
            "max_lag_minutes": 120,  # Alert if > 2 hours since last run
            "min_success_rate": 0.95,  # Alert if < 95% success
            "max_duration_seconds": 3600  # Alert if run takes > 1 hour
        }
    
    def record_metrics(self, stats: dict):
        """Record pipeline run metrics."""
        metrics = PipelineMetrics(
            timestamp=stats["run_end"],
            documents_processed=stats["ingested"],
            chunks_created=stats["chunked"],
            embeddings_generated=stats["embedded"],
            chunks_indexed=stats["indexed"],
            duration_seconds=stats["duration_seconds"],
            errors_count=len(stats.get("errors", [])),
            success_rate=stats["indexed"] / stats["chunked"] if stats["chunked"] > 0 else 0
        )
        
        # Append to metrics file
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')
        
        # Check for alerting conditions
        self._check_alerts(metrics)
    
    def _check_alerts(self, metrics: PipelineMetrics):
        """Check if metrics trigger alerts."""
        alerts = []
        
        # Check success rate
        if metrics.success_rate < self.thresholds["min_success_rate"]:
            alerts.append(
                f"Low success rate: {metrics.success_rate:.1%} "
                f"(threshold: {self.thresholds['min_success_rate']:.1%})"
            )
        
        # Check duration
        if metrics.duration_seconds > self.thresholds["max_duration_seconds"]:
            alerts.append(
                f"Slow pipeline: {metrics.duration_seconds:.0f}s "
                f"(threshold: {self.thresholds['max_duration_seconds']}s)"
            )
        
        # Check errors
        if metrics.errors_count > 0:
            alerts.append(f"Pipeline errors: {metrics.errors_count} failures")
        
        # Send alerts if any
        if alerts and self.alert_email:
            self._send_alert(alerts, metrics)
    
    def _send_alert(self, alerts: list[str], metrics: PipelineMetrics):
        """Send email alert."""
        msg = EmailMessage()
        msg['Subject'] = f'RAG Pipeline Alert - {len(alerts)} issues'
        msg['From'] = 'pipeline-monitor@company.com'
        msg['To'] = self.alert_email
        
        body = f"""RAG Data Pipeline Alert

Timestamp: {metrics.timestamp}

Issues:
{''.join(f'- {alert}\n' for alert in alerts)}

Metrics:
- Documents: {metrics.documents_processed}
- Chunks: {metrics.chunks_created}
- Indexed: {metrics.chunks_indexed}
- Success rate: {metrics.success_rate:.1%}
- Duration: {metrics.duration_seconds:.0f}s
        """
        
        msg.set_content(body)
        
        # Send email (placeholder - configure SMTP)
        print(f"ALERT: {alerts}")
        # with smtplib.SMTP('smtp.company.com') as smtp:
        #     smtp.send_message(msg)
    
    def get_recent_metrics(self, hours: int = 24) -> list[PipelineMetrics]:
        """Get metrics from last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        metrics = []
        with open(self.metrics_file, 'r') as f:
            for line in f:
                m = json.loads(line)
                m_time = datetime.fromisoformat(m["timestamp"])
                if m_time >= cutoff:
                    metrics.append(PipelineMetrics(**m))
        
        return metrics
    
    def get_health_summary(self) -> dict:
        """Get pipeline health summary."""
        recent = self.get_recent_metrics(hours=24)
        
        if not recent:
            return {"status": "NO_DATA", "message": "No recent pipeline runs"}
        
        avg_success_rate = sum(m.success_rate for m in recent) / len(recent)
        avg_duration = sum(m.duration_seconds for m in recent) / len(recent)
        total_errors = sum(m.errors_count for m in recent)
        
        # Determine status
        if avg_success_rate < 0.9:
            status = "UNHEALTHY"
        elif avg_success_rate < 0.95:
            status = "DEGRADED"
        else:
            status = "HEALTHY"
        
        return {
            "status": status,
            "runs_last_24h": len(recent),
            "avg_success_rate": avg_success_rate,
            "avg_duration_seconds": avg_duration,
            "total_errors": total_errors,
            "last_run": recent[-1].timestamp
        }

# Usage with pipeline
monitor = PipelineMonitor(alert_email="team@company.com")

# Run pipeline and record metrics
stats = pipeline.run(incremental=True)
monitor.record_metrics(stats)

# Check health
health = monitor.get_health_summary()
print(f"Pipeline status: {health['status']}")
print(f"Runs in last 24h: {health['runs_last_24h']}")
print(f"Avg success rate: {health['avg_success_rate']:.1%}")
```

## Think of It Like This
Imagine you run a library where new books arrive daily.

**Without a data pipeline**, you personally check the loading dock every morning, manually carry books inside, sort them by hand, create catalog cards on a typewriter, and file them in the card catalog. You work weekends to catch up, sometimes forget new arrivals, occasionally misfile books, and have no system for tracking what's been processed. When someone asks "Do we have the new policy manual?", you're not sure—did you catalog it yet?

**With a data pipeline**, there's an automated system: new books trigger sensors at the loading dock, a conveyor belt moves them to the processing room, scanners extract metadata, printers generate catalog cards automatically, and a robotic system files them correctly in the catalog. The system runs 24/7, processes books within an hour of arrival, tracks every step, sends you alerts if anything jams, and maintains logs you can audit. When someone asks about the new policy manual, you check the dashboard: "Yes, received at 2pm, cataloged at 2:15pm, available now."

Data pipelines are that automated system—transforming manual, error-prone knowledge management into reliable, scalable infrastructure that keeps your RAG system's knowledge base current without your constant intervention.

## The "So What?" Factor
**If you implement data pipelines:**
- Knowledge base stays automatically synchronized with sources (no manual updates)
- New documents indexed within minutes/hours (not days/weeks)
- Updates to existing documents trigger re-processing of affected chunks
- Deleted documents removed from index (preventing retrieval of stale content)
- Consistent processing (same chunking, same embeddings, every time)
- Audit trails for compliance (what was indexed, when, from what source)
- Observability (dashboards showing pipeline health, performance, errors)
- Scalability (process thousands of documents without human intervention)
- Error recovery (retries, alerting, graceful degradation)
- Cost optimization (incremental processing, batch operations, efficient resource use)

**If you skip pipelines:**
- Manual processing required for every document update (unsustainable at scale)
- Knowledge base becomes stale (users ask about new features not yet indexed)
- Inconsistent processing (different chunking or embedding parameters over time)
- No audit trail (can't prove what information was available when)
- No visibility into problems (embedding failures go unnoticed for days)
- Doesn't scale (manual work increases linearly with document volume)
- Human errors inevitable (forgot to process a directory, wrong chunk size used)
- Compliance impossible (can't demonstrate due diligence)
- RAG system degrades silently (retrieval quality drops as index becomes stale)
- Team bottleneck (engineers spending time on operational toil, not features)

## Practical Checklist
Before deploying data pipelines, ask yourself:
- [ ] Have I identified all data sources that need ingestion (files, databases, APIs)?
- [ ] Do I have a strategy for incremental processing (only process new/changed documents)?
- [ ] Have I implemented proper error handling and retry logic at each stage?
- [ ] Am I tracking pipeline runs with metrics and logging?
- [ ] Do I have monitoring and alerting for pipeline failures?
- [ ] Have I validated data quality at each stage (clean text, valid embeddings, successful indexing)?
- [ ] Is metadata preserved throughout the pipeline for audit trails?
- [ ] Have I optimized batch sizes for performance (embeddings, vector database)?
- [ ] Do I have a strategy for handling deleted/renamed documents?
- [ ] Am I using workflow orchestration (Airflow, Prefect) for complex pipelines?
- [ ] Have I documented what happens at each pipeline stage?
- [ ] Do I have a rollback strategy if bad data gets indexed?

## Watch Out For
⚠️ **Incremental processing requires state tracking**: Must track which files processed, their hashes, and last processing time. Losing state means reprocessing everything or missing updates.

⚠️ **Embedding model changes break incremental updates**: If you switch embedding models, all chunks need re-embedding. You can't mix embeddings from different models in one vector database.

⚠️ **Pipeline failures can corrupt index**: Partial processing (some chunks indexed, others failed) creates inconsistent state. Need transactional semantics or ability to rollback.

⚠️ **Batch size tuning is critical**: Too small (process 1 document at a time) is slow, too large (1000 documents at once) causes memory issues or timeouts. Test to find optimal batch sizes.

⚠️ **Duplicate detection is necessary**: Same document from multiple sources or renamed files can create duplicate chunks. Track by content hash, not just filename.

⚠️ **Schema evolution is painful**: If chunk metadata structure changes, existing indexed chunks have old schema. Need migration strategy or versioned collections.

⚠️ **Cost monitoring essential**: Embedding API calls, vector database storage, and compute resources add up quickly at scale. Track costs per pipeline run.

⚠️ **Pipeline scheduling conflicts**: Running new pipeline while previous run still executing can cause race conditions. Ensure only one instance runs at a time or handle concurrency explicitly.

⚠️ **Monitoring fatigue**: Too many alerts (every small error) and teams ignore them. Alert only on conditions requiring human action.

⚠️ **Pipeline lag is inevitable**: There's always delay between document update and index availability. Set expectations with users about freshness guarantees.

## Connections
**Builds On:**
- [document_chunking](document_chunking.md) - Chunking stage in pipeline
- [embeddings](../Foundational_AI & ML/embeddings.md) - Embedding generation stage
- [vector_database](vector_database.md) - Indexing destination
- ETL patterns from data engineering

**Works With:**
- [Retrieval-Augmented_Generation](Retrieval-Augmented_Generation.md) - Pipeline keeps knowledge base current for RAG
- [metadata](metadata.md) - Preserved and enriched throughout pipeline
- [semantic_search](semantic_search.md) - Pipeline produces searchable chunks
- Workflow orchestration tools (Airflow, Prefect, Dagster)
- Monitoring systems (Prometheus, Grafana, Datadog)

**Leads To:**
- Real-time streaming pipelines
- Multi-tenant pipeline architectures
- Pipeline versioning and A/B testing
- Automated pipeline optimization
- MLOps integration for model updates

**Related Patterns:**
- [caching](caching.md) - Caching intermediate pipeline results
- Data quality validation frameworks
- Observability and monitoring patterns
- Error handling and retry strategies
- Cost optimization for AI workloads

## Quick Decision Guide
**Use batch pipelines when:**
- Documents update infrequently (hourly, daily)
- Tolerance for indexing lag (minutes to hours acceptable)
- Want simple orchestration (cron jobs, scheduled tasks)
- Processing large document collections overnight

**Use streaming pipelines when:**
- Near-real-time indexing required (seconds to minutes)
- Documents change frequently (event-driven)
- Users expect immediate availability of new documents
- Have infrastructure for stream processing (Kafka, event handlers)

**Choose orchestration tools when:**
- Complex multi-stage pipelines with dependencies
- Need retry logic, error handling, monitoring
- Multiple pipelines with shared infrastructure
- Team needs visibility into pipeline execution

**Build custom pipelines when:**
- Simple use case (single directory, infrequent updates)
- Don't want orchestration tool complexity
- Have specific performance or integration requirements
- Embedded in larger application

**Pipeline frequency guidelines:**
- **Real-time**: < 1 minute lag (event-driven, streaming)
- **Frequent**: 5-15 minute intervals (scheduled, incremental)
- **Standard**: 1-4 hour intervals (typical business documents)
- **Batch**: Daily/nightly (large archives, full reprocessing)

## Further Exploration
- 📖 "Data Pipelines Pocket Reference" - James Densmore (O'Reilly)
- 🎯 Apache Airflow documentation - Workflow orchestration
- 💡 "Building Data Pipelines with Python" - Practical implementation patterns
- 📖 Prefect documentation - Modern workflow orchestration
- 🎯 LangChain data loaders - Document ingestion patterns
- 💡 "Designing Data-Intensive Applications" - Martin Kleppmann (Chapter 10: Batch Processing)
- 📖 "Stream Processing with Apache Kafka" - Real-time pipeline patterns
- 🎯 Dagster documentation - Data pipeline orchestration with ML focus
- 💡 "MLOps: Continuous Delivery for Machine Learning" - Pipeline integration with ML systems
- 📖 "Fundamentals of Data Engineering" - Joe Reis & Matt Housley

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
