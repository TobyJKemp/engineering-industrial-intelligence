# Batching

## At a Glance
| | |
|---|---|
| **Category** | Performance Optimization Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-4 hours for fundamentals, weeks for optimization |
| **Prerequisites** | Understanding of throughput vs latency, async programming, GPU/parallel processing basics |

## One-Sentence Summary
Batching is the performance optimization pattern of grouping multiple independent operations together and processing them as a single unit—leveraging parallel hardware (GPUs), amortizing fixed overhead (API calls, network round-trips), and improving resource utilization, transforming "process 100 requests one-by-one taking 100 seconds" into "process 100 requests in one batch taking 10 seconds" while accepting the trade-off that individual requests wait for the batch to fill before processing begins.

## Why This Matters to You
When you build AI agent systems in 2026, batching is the difference between infrastructure that costs $50,000/month and infrastructure delivering the same throughput for $5,000/month. Without batching, when your agent system generates embeddings for 10,000 documents one-by-one, each taking 50ms, that's 500 seconds (8.3 minutes) and 10,000 API calls at $0.0001 each = $1.00. With batching (100 documents per batch), you make 100 API calls of 200ms each = 20 seconds total time (25x faster) and $0.10 cost (10x cheaper). This 10-25x improvement applies everywhere: embedding generation (batch 100+ documents), LLM inference (batch prompts), vector search (batch queries), database operations (batch inserts), and image processing (batch frames). At production scale serving 1 million embeddings/day, that's $10,000/month without batching vs $1,000/month with batching—a $108,000 annual difference. For LLM inference, GPUs achieve ~10x higher throughput with batching (1000 tokens/sec single prompt vs 10,000 tokens/sec batched), dramatically reducing per-token costs. But batching adds complexity and latency: requests must wait for batch to fill (100ms-1000ms typical), batch sizes must be tuned (too small = less benefit, too large = long waits), and batch formation strategies matter (static timeout vs dynamic sizing). At system boundaries, batching decisions cascade: batch embeddings but then need to batch vector searches, batch database writes but then need to batch cache invalidations. This matters for user experience: batching background operations (log processing, analytics) is easy, but batching user-facing requests (chat responses) trades latency for throughput—acceptable for high-load scenarios (100+ concurrent users) but not for interactive single-user experiences. Understanding batching patterns (static vs dynamic, opportunistic vs required), implementation techniques (async batching with timeouts, batch queues, GPU batch schedulers), size optimization (measure throughput/latency curves), and where to apply (high-volume, parallelizable operations) determines whether your agent infrastructure scales cost-effectively or wastes 10x resources processing operations sequentially. In 2026, with embedding models processing millions of documents, LLMs generating billions of tokens, and vector databases handling millions of searches, batching is not optional—it's the foundation of economically viable AI systems.

## The Core Idea
### What It Is
Batching is grouping multiple independent operations together and processing them as a single unit to improve throughput, reduce per-operation costs, and better utilize parallel hardware. Instead of "process item 1, wait for result, process item 2, wait for result," batching does "collect items 1-100, process all together, return 100 results."

**The Fundamental Problem:**

Many operations have overhead that's fixed regardless of how many items processed:

```
Sequential Processing (no batching):
- Operation 1: 5ms overhead + 2ms compute = 7ms
- Operation 2: 5ms overhead + 2ms compute = 7ms
- Operation 3: 5ms overhead + 2ms compute = 7ms
Total: 21ms for 3 operations

Batched Processing:
- Operations 1-3: 5ms overhead + 6ms compute (3 items parallel) = 11ms
Total: 11ms for 3 operations (2x faster)

Fixed overhead amortized across batch!
```

**Common Sources of Fixed Overhead:**

1. **Network round-trips**: HTTP connection setup, SSL handshake
2. **API rate limits**: Each call counts against quota
3. **GPU kernel launch**: Overhead to start computation
4. **Database transactions**: Connection acquisition, commit overhead
5. **Memory allocation**: Allocating structures for processing
6. **Context switching**: Thread/process switching costs

**Example 1: Embedding Generation Without Batching**

```python
import time
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def generate_embeddings_sequential(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings one-by-one (SLOW, EXPENSIVE).
    
    Each call: ~50ms network + API overhead, even for single text.
    """
    embeddings = []
    
    start_time = time.time()
    
    for i, text in enumerate(texts):
        # Individual API call for each text
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=[text]  # Single text
        )
        
        embedding = response.data[0].embedding
        embeddings.append(embedding)
        
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {i + 1} texts in {elapsed:.2f}s "
                  f"({(i + 1) / elapsed:.1f} texts/sec)")
    
    total_time = time.time() - start_time
    throughput = len(texts) / total_time
    
    print(f"\nSequential: {len(texts)} texts in {total_time:.2f}s "
          f"({throughput:.1f} texts/sec)")
    
    return embeddings

# Test with 100 texts
texts = [f"Document {i} content here" for i in range(100)]
embeddings_seq = generate_embeddings_sequential(texts)

# Output:
# Processed 10 texts in 0.52s (19.2 texts/sec)
# Processed 20 texts in 1.04s (19.2 texts/sec)
# ...
# Sequential: 100 texts in 5.21s (19.2 texts/sec)
# Cost: 100 API calls × $0.0001 = $0.01
```

**Example 2: Embedding Generation WITH Batching**

```python
def generate_embeddings_batched(
    texts: list[str],
    batch_size: int = 100
) -> list[list[float]]:
    """
    Generate embeddings in batches (FAST, CHEAP).
    
    Amortizes API overhead across multiple texts.
    """
    embeddings = []
    
    start_time = time.time()
    
    # Process in batches
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        # Single API call for entire batch
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch  # Multiple texts in one call
        )
        
        # Extract embeddings (order preserved)
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
        
        elapsed = time.time() - start_time
        processed = min(i + batch_size, len(texts))
        print(f"Processed {processed} texts in {elapsed:.2f}s "
              f"({processed / elapsed:.1f} texts/sec)")
    
    total_time = time.time() - start_time
    throughput = len(texts) / total_time
    
    print(f"\nBatched: {len(texts)} texts in {total_time:.2f}s "
          f"({throughput:.1f} texts/sec)")
    
    return embeddings

# Test with same 100 texts
embeddings_batch = generate_embeddings_batched(texts, batch_size=100)

# Output:
# Processed 100 texts in 0.21s (476.2 texts/sec)
# Batched: 100 texts in 0.21s (476.2 texts/sec)
# Cost: 1 API call × $0.0001 = $0.0001

# Comparison:
# Sequential: 5.21s (19.2 texts/sec), $0.01
# Batched:    0.21s (476.2 texts/sec), $0.0001
# Improvement: 25x faster, 100x cheaper!
```

**Example 3: Database Batch Insert**

```python
import sqlite3
import time

def insert_records_sequential(records: list[dict], db_path: str):
    """
    Insert records one-by-one (SLOW).
    
    Each insert: transaction overhead, index updates.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    start_time = time.time()
    
    for record in records:
        cursor.execute(
            "INSERT INTO documents (doc_id, content) VALUES (?, ?)",
            (record['doc_id'], record['content'])
        )
        conn.commit()  # Commit each record
    
    total_time = time.time() - start_time
    
    conn.close()
    
    print(f"Sequential: {len(records)} records in {total_time:.2f}s "
          f"({len(records) / total_time:.1f} records/sec)")

def insert_records_batched(records: list[dict], db_path: str):
    """
    Insert records in single transaction (FAST).
    
    Single transaction overhead, batch index updates.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    start_time = time.time()
    
    # Use executemany for batch insert
    cursor.executemany(
        "INSERT INTO documents (doc_id, content) VALUES (?, ?)",
        [(r['doc_id'], r['content']) for r in records]
    )
    
    conn.commit()  # Single commit for all records
    
    total_time = time.time() - start_time
    
    conn.close()
    
    print(f"Batched: {len(records)} records in {total_time:.2f}s "
          f"({len(records) / total_time:.1f} records/sec)")

# Test
records = [{'doc_id': i, 'content': f'Document {i}'} for i in range(1000)]

insert_records_sequential(records, 'test.db')
# Sequential: 1000 records in 2.45s (408.2 records/sec)

insert_records_batched(records, 'test.db')
# Batched: 1000 records in 0.12s (8333.3 records/sec)
# 20x faster!
```

**Example 4: Dynamic Batching (Async Accumulation)**

```python
import asyncio
import time
from typing import Any, Callable

class AsyncBatcher:
    """
    Dynamic batching: accumulate requests, process when batch full or timeout.
    
    Pattern: Balance latency (don't wait too long) vs throughput (bigger batches).
    """
    
    def __init__(
        self,
        process_batch_fn: Callable,
        max_batch_size: int = 32,
        max_wait_ms: int = 100
    ):
        """
        Args:
            process_batch_fn: Function that processes a batch
            max_batch_size: Max items before forcing batch
            max_wait_ms: Max time to wait for batch to fill
        """
        self.process_batch_fn = process_batch_fn
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms / 1000  # Convert to seconds
        
        self.pending_requests = []
        self.pending_futures = []
        self.batch_timer = None
        self.processing = False
        self.batches_processed = 0
        self.total_items_processed = 0
    
    async def submit(self, item: Any) -> Any:
        """
        Submit item for batched processing.
        
        Returns result when batch processes (may wait for batch to fill).
        """
        # Create future for this request
        future = asyncio.Future()
        
        # Add to pending batch
        self.pending_requests.append(item)
        self.pending_futures.append(future)
        
        # Check if batch full
        if len(self.pending_requests) >= self.max_batch_size:
            # Process immediately (batch full)
            await self._process_batch()
        else:
            # Start timer if not already running
            if self.batch_timer is None:
                self.batch_timer = asyncio.create_task(self._wait_and_process())
        
        # Wait for result
        return await future
    
    async def _wait_and_process(self):
        """Wait for timeout, then process batch."""
        await asyncio.sleep(self.max_wait_ms)
        await self._process_batch()
    
    async def _process_batch(self):
        """Process current batch."""
        if self.processing or not self.pending_requests:
            return
        
        self.processing = True
        
        # Cancel timer if running
        if self.batch_timer:
            self.batch_timer.cancel()
            self.batch_timer = None
        
        # Get current batch
        batch = self.pending_requests
        futures = self.pending_futures
        
        # Reset pending
        self.pending_requests = []
        self.pending_futures = []
        
        try:
            # Process batch
            start_time = time.time()
            results = await self.process_batch_fn(batch)
            duration = time.time() - start_time
            
            self.batches_processed += 1
            self.total_items_processed += len(batch)
            
            print(f"Batch {self.batches_processed}: processed {len(batch)} items "
                  f"in {duration * 1000:.1f}ms")
            
            # Set results on futures
            for future, result in zip(futures, results):
                future.set_result(result)
        
        except Exception as e:
            # Set error on all futures
            for future in futures:
                if not future.done():
                    future.set_exception(e)
        
        finally:
            self.processing = False

# Usage example
async def process_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Batch processing function."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]

batcher = AsyncBatcher(
    process_batch_fn=process_embeddings_batch,
    max_batch_size=32,
    max_wait_ms=100
)

async def process_request(request_id: int):
    """Individual request using batcher."""
    text = f"Request {request_id} text content"
    
    # Submit to batcher (automatically batches)
    embedding = await batcher.submit(text)
    
    return embedding

# Submit 100 requests rapidly
async def test_dynamic_batching():
    tasks = [process_request(i) for i in range(100)]
    results = await asyncio.gather(*tasks)
    
    print(f"\nProcessed {len(results)} requests")
    print(f"Total batches: {batcher.batches_processed}")
    print(f"Avg batch size: {batcher.total_items_processed / batcher.batches_processed:.1f}")

# asyncio.run(test_dynamic_batching())

# Output:
# Batch 1: processed 32 items in 215.3ms
# Batch 2: processed 32 items in 210.8ms
# Batch 3: processed 32 items in 218.1ms
# Batch 4: processed 4 items in 112.4ms  # Last batch (partial, hit timeout)
# Processed 100 requests
# Total batches: 4
# Avg batch size: 25.0
```

**Example 5: GPU Batch Processing**

```python
import torch
import time

class GPUBatchInference:
    """
    Batch inference on GPU for throughput optimization.
    
    GPUs process batches much faster than sequential (parallel compute).
    """
    
    def __init__(self, model):
        self.model = model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
    
    def inference_sequential(self, inputs: list[torch.Tensor]) -> list[torch.Tensor]:
        """
        Sequential inference (SLOW on GPU).
        
        GPU sits mostly idle, no parallel utilization.
        """
        results = []
        
        start_time = time.time()
        
        with torch.no_grad():
            for i, input_tensor in enumerate(inputs):
                input_tensor = input_tensor.to(self.device)
                output = self.model(input_tensor.unsqueeze(0))  # Batch size 1
                results.append(output.squeeze(0))
                
                if (i + 1) % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"Sequential: {i + 1} inferences in {elapsed:.2f}s "
                          f"({(i + 1) / elapsed:.1f} inferences/sec)")
        
        total_time = time.time() - start_time
        throughput = len(inputs) / total_time
        
        print(f"Sequential total: {len(inputs)} inferences in {total_time:.2f}s "
              f"({throughput:.1f} inferences/sec)")
        
        return results
    
    def inference_batched(
        self,
        inputs: list[torch.Tensor],
        batch_size: int = 32
    ) -> list[torch.Tensor]:
        """
        Batched inference (FAST on GPU).
        
        GPU processes multiple inputs in parallel (high utilization).
        """
        results = []
        
        start_time = time.time()
        
        with torch.no_grad():
            for i in range(0, len(inputs), batch_size):
                batch = inputs[i:i + batch_size]
                
                # Stack into batch tensor
                batch_tensor = torch.stack(batch).to(self.device)
                
                # Process batch in parallel
                batch_output = self.model(batch_tensor)
                
                # Unstack results
                results.extend([output for output in batch_output])
                
                processed = min(i + batch_size, len(inputs))
                elapsed = time.time() - start_time
                print(f"Batched: {processed} inferences in {elapsed:.2f}s "
                      f"({processed / elapsed:.1f} inferences/sec)")
        
        total_time = time.time() - start_time
        throughput = len(inputs) / total_time
        
        print(f"Batched total: {len(inputs)} inferences in {total_time:.2f}s "
              f"({throughput:.1f} inferences/sec)")
        
        return results

# Test
# model = YourModel()  # Your PyTorch model
# gpu_inference = GPUBatchInference(model)

# inputs = [torch.randn(3, 224, 224) for _ in range(100)]  # 100 images

# Sequential: 100 inferences in 5.24s (19.1 inferences/sec)
# Batched: 100 inferences in 0.52s (192.3 inferences/sec)
# 10x faster with batching!
```

### What It Isn't
Batching is not **the same as parallelism**. Parallelism processes multiple items simultaneously; batching groups them for efficient processing (which often uses parallelism internally).

It's not **always faster**. For small batch sizes or operations dominated by computation (not overhead), batching may not help and can add latency.

Batching is not **free**. It adds latency (waiting for batch to fill), memory (holding batch in buffer), and complexity (batch coordination logic).

It's not **appropriate for all operations**. Operations with dependencies (output of one needed for next) or requiring immediate response cannot be batched effectively.

Finally, batching is not **just for GPUs**. While GPUs benefit dramatically, batching helps anywhere there's fixed overhead: APIs, databases, network, disk I/O.

## How It Works

### Advanced Batching Patterns

**Pattern 1: Opportunistic Batching (Best Effort)**

```python
import asyncio
from collections import deque
import time

class OpportunisticBatcher:
    """
    Opportunistic batching: batch if requests waiting, otherwise process immediately.
    
    Good for: Variable load (batch during peaks, fast response during quiet).
    """
    
    def __init__(
        self,
        process_fn: Callable,
        check_interval_ms: int = 10
    ):
        self.process_fn = process_fn
        self.check_interval = check_interval_ms / 1000
        self.queue = asyncio.Queue()
        self.running = False
    
    async def submit(self, item: Any) -> Any:
        """Submit item for processing."""
        future = asyncio.Future()
        await self.queue.put((item, future))
        return await future
    
    async def run(self):
        """Process items with opportunistic batching."""
        self.running = True
        
        while self.running:
            # Wait for at least one item
            if self.queue.empty():
                await asyncio.sleep(self.check_interval)
                continue
            
            # Collect batch (everything currently waiting)
            batch_items = []
            batch_futures = []
            
            # Get first item
            item, future = await self.queue.get()
            batch_items.append(item)
            batch_futures.append(future)
            
            # Collect any other waiting items (opportunistic)
            while not self.queue.empty():
                try:
                    item, future = self.queue.get_nowait()
                    batch_items.append(item)
                    batch_futures.append(future)
                except asyncio.QueueEmpty:
                    break
            
            # Process batch (size 1 to N)
            try:
                print(f"Processing opportunistic batch of {len(batch_items)} items")
                results = await self.process_fn(batch_items)
                
                for future, result in zip(batch_futures, results):
                    future.set_result(result)
            
            except Exception as e:
                for future in batch_futures:
                    if not future.done():
                        future.set_exception(e)
    
    def stop(self):
        """Stop processing."""
        self.running = False

# During quiet period: processes immediately (batch size 1)
# During peak: automatically batches 10-50 items
```

**Pattern 2: Batch Size Optimization**

```python
import time
import numpy as np

def find_optimal_batch_size(
    process_fn: Callable,
    test_data: list,
    min_batch: int = 1,
    max_batch: int = 256
) -> dict:
    """
    Find optimal batch size by measuring throughput/latency.
    
    Returns: {
        "optimal_batch_size": int,
        "max_throughput": float,
        "measurements": list
    }
    """
    measurements = []
    
    batch_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    batch_sizes = [b for b in batch_sizes if min_batch <= b <= max_batch]
    
    for batch_size in batch_sizes:
        # Measure throughput and latency
        latencies = []
        
        for i in range(0, len(test_data), batch_size):
            batch = test_data[i:i + batch_size]
            
            start = time.time()
            results = process_fn(batch)
            end = time.time()
            
            batch_latency = (end - start) * 1000  # ms
            per_item_latency = batch_latency / len(batch)
            
            latencies.append(per_item_latency)
        
        avg_latency = np.mean(latencies)
        throughput = 1000 / avg_latency  # items/sec
        
        measurements.append({
            "batch_size": batch_size,
            "avg_latency_ms": round(avg_latency, 2),
            "throughput": round(throughput, 1)
        })
        
        print(f"Batch size {batch_size:3d}: "
              f"{avg_latency:6.2f}ms latency, "
              f"{throughput:8.1f} items/sec")
    
    # Find optimal (max throughput)
    optimal = max(measurements, key=lambda x: x["throughput"])
    
    return {
        "optimal_batch_size": optimal["batch_size"],
        "max_throughput": optimal["throughput"],
        "measurements": measurements
    }

# Usage
# optimal = find_optimal_batch_size(process_embeddings, test_texts)
# Output:
# Batch size   1:   52.31ms latency,     19.1 items/sec
# Batch size   2:   28.15ms latency,     35.5 items/sec
# Batch size   4:   16.42ms latency,     60.9 items/sec
# Batch size   8:   10.21ms latency,     97.9 items/sec
# Batch size  16:    7.15ms latency,    139.9 items/sec
# Batch size  32:    5.42ms latency,    184.5 items/sec  ← Optimal
# Batch size  64:    5.89ms latency,    169.8 items/sec  (diminishing returns)
# Batch size 128:    6.21ms latency,    161.0 items/sec
```

**Pattern 3: Adaptive Batching (Load-Based)**

```python
class AdaptiveBatcher:
    """
    Adaptive batching: adjust batch size based on load.
    
    High load → larger batches (throughput)
    Low load → smaller batches (latency)
    """
    
    def __init__(self, process_fn: Callable):
        self.process_fn = process_fn
        self.queue = asyncio.Queue()
        
        # Adaptive parameters
        self.min_batch_size = 1
        self.max_batch_size = 64
        self.current_batch_size = 8
        
        # Load tracking
        self.recent_queue_sizes = deque(maxlen=10)
        self.running = False
    
    async def submit(self, item: Any) -> Any:
        """Submit item."""
        future = asyncio.Future()
        await self.queue.put((item, future))
        return await future
    
    def _adapt_batch_size(self):
        """Adjust batch size based on queue depth."""
        queue_size = self.queue.qsize()
        self.recent_queue_sizes.append(queue_size)
        
        avg_queue_size = sum(self.recent_queue_sizes) / len(self.recent_queue_sizes)
        
        # High queue depth → increase batch size (favor throughput)
        if avg_queue_size > self.current_batch_size * 2:
            self.current_batch_size = min(
                self.current_batch_size * 2,
                self.max_batch_size
            )
            print(f"📈 Increased batch size to {self.current_batch_size} (queue: {queue_size})")
        
        # Low queue depth → decrease batch size (favor latency)
        elif avg_queue_size < self.current_batch_size / 4:
            self.current_batch_size = max(
                self.current_batch_size // 2,
                self.min_batch_size
            )
            print(f"📉 Decreased batch size to {self.current_batch_size} (queue: {queue_size})")
    
    async def run(self):
        """Process with adaptive batching."""
        self.running = True
        
        while self.running:
            # Adapt batch size
            self._adapt_batch_size()
            
            # Collect batch
            batch_items = []
            batch_futures = []
            
            for _ in range(self.current_batch_size):
                try:
                    item, future = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=0.1
                    )
                    batch_items.append(item)
                    batch_futures.append(future)
                except asyncio.TimeoutError:
                    break
            
            if not batch_items:
                continue
            
            # Process batch
            try:
                results = await self.process_fn(batch_items)
                for future, result in zip(batch_futures, results):
                    future.set_result(result)
            except Exception as e:
                for future in batch_futures:
                    if not future.done():
                        future.set_exception(e)

# System automatically adjusts:
# - Low load: batch size 1-4 (fast response)
# - Medium load: batch size 8-16 (balanced)
# - High load: batch size 32-64 (high throughput)
```

## Think of It Like This
Imagine a ferry crossing a river.

**Without batching** (individual rowboat trips): Each person gets their own rowboat and rows across individually. If 100 people need to cross, that's 100 separate trips, each taking 5 minutes = 500 minutes total. Each person starts immediately (0 wait time) but the system is inefficient (100 trips × rowboat setup overhead).

**With batching** (ferry): Ferry waits until 50 people board (or 10 minutes pass), then crosses with everyone. Total time: wait for 50 people (5 minutes) + cross (5 minutes) = 10 minutes for 50 people. Second batch: wait + cross = another 10 minutes for remaining 50. Total: 20 minutes for 100 people (25x faster than rowboats). But individuals wait 0-10 minutes to board (latency) vs immediate rowboat departure.

**Dynamic batching**: Ferry waits for either 50 people OR 3 minutes (whichever comes first). During rush hour, batches of 50 depart every 3 minutes (high throughput). During quiet times, small batches of 5-10 depart every 3 minutes (low latency).

**Opportunistic batching**: If people are waiting when ferry returns, load them immediately and depart. If nobody waiting, depart as soon as first person boards (no wait).

Batching gives your agent system that ferry efficiency—grouping operations to amortize overhead and improve throughput, with the trade-off that individual operations may wait for the batch to form.

## The "So What?" Factor
**If you implement batching properly:**
- 10-100x throughput improvement
- 10-100x cost reduction (fewer API calls)
- Better GPU utilization (80-95% vs 10-20%)
- Lower per-operation latency (amortized overhead)
- More predictable resource usage
- Can handle higher load with same infrastructure
- Reduced API rate limit violations
- Better energy efficiency
- Scalable to millions of operations
- Economically viable at production scale

**If you skip batching:**
- 10-100x higher costs (sequential API calls)
- 10-100x lower throughput
- Poor GPU utilization (idle time)
- Higher per-operation costs
- Hit API rate limits quickly
- Need 10x infrastructure for same load
- Unpredictable costs at scale
- Cannot scale economically
- Wasted compute resources
- Uncompetitive with batched systems

## Practical Checklist
Before deploying batched systems:
- [ ] Have you identified high-volume operations suitable for batching?
- [ ] Have you measured throughput/latency for different batch sizes?
- [ ] Is batch size configurable and tuned for your workload?
- [ ] Are you using dynamic batching for variable load?
- [ ] Do you have timeout protection (don't wait forever for batch)?
- [ ] Are partial batches handled correctly (last batch may be small)?
- [ ] Is batching transparent to callers (async interface)?
- [ ] Do you monitor: batch sizes, wait times, utilization?
- [ ] Are errors handled per-item (one failure doesn't fail batch)?
- [ ] Have you tested with single-item requests (edge case)?
- [ ] Is there graceful degradation if batching fails (fallback)?
- [ ] Are batch size limits enforced (memory constraints)?
- [ ] Have you documented latency implications for users?

## Watch Out For
⚠️ **Excessive Latency**: Large batches = long waits. Balance throughput vs latency with timeouts.

⚠️ **Memory Exhaustion**: Large batches consume proportional memory. Monitor and limit batch size.

⚠️ **Partial Batch Handling**: Last batch may be smaller than batch_size. Handle edge case.

⚠️ **Order Preservation**: Some operations require order. Ensure batching preserves input order.

⚠️ **Error Handling Complexity**: One item failure in batch—fail all or continue? Need per-item error tracking.

⚠️ **Timeout Tuning**: Too short = small batches (low throughput), too long = high latency. Measure and tune.

⚠️ **Batch Size Too Large**: Exceeds API limits, memory constraints, or GPU capacity. Test maximum.

⚠️ **Batch Size Too Small**: Doesn't amortize overhead enough. Measure optimal size for your operation.

⚠️ **Ignoring Tail Latency**: Batch wait time affects p99 latency. Monitor percentiles, not just averages.

⚠️ **Batching Already-Batched APIs**: Some APIs batch internally. Double-batching may not help and complicates logic.

## Connections
**Builds On:**
- Async programming patterns
- Queue data structures
- Parallel processing concepts
- GPU computing fundamentals

**Works With:**
- [request_queuing](request_queuing.md) - Queues naturally collect items for batching
- [backpressure](backpressure.md) - Batch processing respects consumer capacity
- [streaming_responses](streaming_responses.md) - Can batch-generate tokens before streaming
- [concurrency_control](concurrency_control.md) - Batch operations need coordination
- Parallel processing frameworks
- GPU schedulers

**Leads To:**
- Dynamic batch sizing algorithms
- Adaptive resource allocation
- Multi-stage pipeline optimization
- Cost-aware batch scheduling
- Auto-scaling based on batch metrics

**Related Patterns:**
- [caching](../Data_and_Retrieval_Patterns/caching.md) - Cache batch results for reuse
- Map-reduce patterns (batch processing)
- Data parallelism
- Pipeline optimization
- Lazy evaluation

## Quick Decision Guide
**Batch when:**
- Processing 100+ similar operations
- Operations have high fixed overhead (API calls, network)
- Using GPUs or parallel hardware
- Cost per operation significant ($0.0001+)
- Latency tolerance 100ms-1000ms
- High throughput more important than low latency

**Don't batch when:**
- Operations have dependencies (sequential)
- Latency critical (< 10ms required)
- Very low volume (< 10 operations total)
- Operations are already fast (< 1ms)
- Memory constrained (cannot buffer items)

**Use static batching when:**
- Batch size known in advance
- Fixed batch intervals acceptable
- Predictable load patterns
- Simplicity preferred

**Use dynamic batching when:**
- Variable load (peaks and quiet periods)
- Need to balance latency vs throughput
- Want adaptive behavior
- Have sophisticated monitoring

**Optimal batch size:**
- Measure throughput curve (batch 1, 2, 4, 8, 16, 32...)
- Find plateau (diminishing returns)
- Consider: GPU memory, API limits, timeout constraints
- Monitor and retune in production

## Further Exploration
- 📖 **"Deep Learning" by Goodfellow et al.** - Chapter on mini-batch gradient descent
- 🎯 **Implement Dynamic Batcher** - Build AsyncBatcher with configurable timeout/size
- 💡 **Measure Batch Size vs Throughput** - Plot curves for your operations
- 📖 **NVIDIA CUDA Batching Best Practices** - GPU batch optimization techniques
- 🎯 **OpenAI Batch API Documentation** - Study production batching patterns
- 💡 **Test Latency vs Throughput Trade-offs** - Measure p50/p95/p99 latencies at different batch sizes
- 📖 **"Designing Data-Intensive Applications" by Kleppmann** - Chapter on batch processing
- 🎯 **PyTorch DataLoader** - Study batch loading for training
- 💡 **Build Adaptive Batch Sizing** - Automatically adjust based on queue depth
- 📖 **Database Bulk Insert Performance** - Compare single vs batch insert patterns

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
