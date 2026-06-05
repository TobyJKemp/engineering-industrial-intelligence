# Request Queuing

## At a Glance
| | |
|---|---|
| **Category** | Resource Management Pattern / Reliability |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 4-6 hours for fundamentals, weeks for optimization |
| **Prerequisites** | Understanding of concurrency, async programming, rate limiting, system design |

## One-Sentence Summary
Request queuing is the pattern of accepting incoming agent requests immediately but processing them sequentially or in controlled batches through queues—preventing system overload, managing rate limits, enforcing priorities, and ensuring fair resource allocation when demand exceeds capacity, transforming "sorry, system unavailable" rejections into "your request is queued, position #47, estimated wait 3 minutes" user experiences that maintain service quality under load.

## Why This Matters to You
When you build AI agent systems in 2026, request queuing is the difference between systems that collapse under load and systems that gracefully handle traffic spikes. Without queuing, when 1000 users simultaneously request agent responses, your system tries processing all 1000 concurrently—exhausting API rate limits (OpenAI allows 10,000 tokens/minute), overwhelming databases, consuming all memory, and ultimately failing with timeout errors for everyone. With queuing, those 1000 requests enter a queue and process at sustainable rate (100 concurrent, based on your limits), with users receiving "Position #847, estimated wait 2 minutes" feedback instead of cryptic 429 errors. This matters economically: LLM APIs cost $0.01-0.10 per request, and without queuing, retry storms from failures can 10x your costs—users retry failed requests, creating cascading overload. Queuing prevents this: failed requests stay in queue and retry automatically with backoff. It also enables sophisticated resource management: priority queues ensure paying customers get faster service than free tier users, fair scheduling prevents one user from monopolizing resources, and rate limiting protects your budget by capping spending. At production scale serving 10,000+ users, queuing is mandatory—the alternative is random failures, angry users, and massive cloud bills. But queuing adds complexity: latency increases (waiting in queue), monitoring becomes critical (queue depth, processing rates, wait times), and queue persistence is needed (don't lose requests on crash). Understanding queue implementations (in-memory vs Redis vs SQS), scheduling policies (FIFO, priority, fair queuing), backpressure strategies (reject vs delay), and performance tuning (worker pool sizes, timeout management) determines whether your agent system scales reliably or collapses unpredictably. In 2026, with AI agents handling everything from customer support to code generation, request queuing is fundamental infrastructure—the difference between systems that work under real-world load and systems that only work in demos.

## The Core Idea
### What It Is
Request queuing is a resource management pattern where incoming requests are placed in a data structure (queue) and processed asynchronously by a pool of workers, rather than being handled immediately upon arrival. The queue acts as a buffer between request arrival rate (which can spike unpredictably) and processing capacity (which is limited by API rate limits, compute resources, and cost constraints).

**The Fundamental Problem:**

AI agent systems face resource constraints:
- **API rate limits**: OpenAI GPT-4 typically limits to 10,000 tokens/minute, 500 requests/minute
- **Cost constraints**: $0.01-0.10 per request means 10,000 requests = $100-1000
- **Compute limits**: Each agent execution consumes CPU, memory, database connections
- **External dependencies**: Vector databases, search APIs, tools have their own limits

When request arrival rate exceeds processing capacity, systems have two choices:

**Without queuing (Reject immediately):**
```
1000 requests arrive → Try processing all → Hit rate limit → 900 requests fail with 429 errors
→ Users retry → 2700 requests total → More failures → Retry storm → System collapse
```

**With queuing (Accept and process fairly):**
```
1000 requests arrive → Accept all into queue → Process at sustainable rate (100 concurrent)
→ Queue position feedback → Predictable wait times → No retry storms → Stable system
```

**Basic Queue Implementation:**

```python
import asyncio
from collections import deque
from typing import Callable, Any, Optional
import time

class SimpleRequestQueue:
    """
    Basic FIFO queue for agent requests.
    
    Pattern: Accept requests fast, process at controlled rate.
    """
    
    def __init__(
        self,
        max_concurrent: int = 10,
        max_queue_size: int = 1000
    ):
        """
        Args:
            max_concurrent: Maximum concurrent processing
            max_queue_size: Maximum queued requests (reject beyond this)
        """
        self.queue = deque()
        self.max_concurrent = max_concurrent
        self.max_queue_size = max_queue_size
        self.active_tasks = 0
        self.processed_count = 0
        self.rejected_count = 0
    
    async def submit(
        self,
        request_id: str,
        handler: Callable,
        *args,
        **kwargs
    ) -> dict:
        """
        Submit request to queue.
        
        Returns:
            {
                "status": "queued" | "rejected",
                "request_id": str,
                "position": int,  # if queued
                "estimated_wait_seconds": float  # if queued
            }
        """
        # Check if queue full
        if len(self.queue) >= self.max_queue_size:
            self.rejected_count += 1
            return {
                "status": "rejected",
                "request_id": request_id,
                "reason": "Queue full",
                "queue_size": len(self.queue),
                "max_queue_size": self.max_queue_size
            }
        
        # Add to queue
        self.queue.append({
            "request_id": request_id,
            "handler": handler,
            "args": args,
            "kwargs": kwargs,
            "submitted_at": time.time()
        })
        
        position = len(self.queue)
        
        # Estimate wait time
        # Assumption: average 5 seconds per request
        estimated_wait = position * 5 / self.max_concurrent
        
        return {
            "status": "queued",
            "request_id": request_id,
            "position": position,
            "estimated_wait_seconds": estimated_wait,
            "queue_size": len(self.queue)
        }
    
    async def _worker(self, worker_id: int):
        """
        Worker that processes requests from queue.
        
        Runs continuously, taking requests and executing them.
        """
        print(f"Worker {worker_id} started")
        
        while True:
            # Wait for request in queue
            if not self.queue:
                await asyncio.sleep(0.1)
                continue
            
            # Get next request
            request = self.queue.popleft()
            self.active_tasks += 1
            
            try:
                # Process request
                start_time = time.time()
                result = await request["handler"](
                    *request["args"],
                    **request["kwargs"]
                )
                duration = time.time() - start_time
                
                wait_time = start_time - request["submitted_at"]
                
                self.processed_count += 1
                
                print(f"Worker {worker_id} completed {request['request_id']} "
                      f"(waited {wait_time:.1f}s, processed {duration:.1f}s)")
                
            except Exception as e:
                print(f"Worker {worker_id} error on {request['request_id']}: {e}")
                
            finally:
                self.active_tasks -= 1
    
    async def start(self):
        """Start worker pool to process queue."""
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_concurrent)
        ]
        
        # Run forever (or until cancelled)
        await asyncio.gather(*workers, return_exceptions=True)
    
    def get_stats(self) -> dict:
        """Get queue statistics."""
        return {
            "queue_length": len(self.queue),
            "active_tasks": self.active_tasks,
            "processed_count": self.processed_count,
            "rejected_count": self.rejected_count,
            "max_concurrent": self.max_concurrent
        }

# Usage example
queue = SimpleRequestQueue(max_concurrent=5, max_queue_size=100)

async def process_agent_request(user_id: int, query: str):
    """Simulate agent request processing."""
    print(f"Processing query from user {user_id}: {query[:50]}...")
    await asyncio.sleep(3)  # Simulate LLM call
    return {"answer": f"Response to: {query[:30]}..."}

async def main():
    # Start queue workers
    asyncio.create_task(queue.start())
    
    # Simulate burst of requests
    for i in range(50):
        result = await queue.submit(
            request_id=f"req_{i}",
            handler=process_agent_request,
            user_id=i,
            query=f"User {i} question about topic {i % 10}"
        )
        
        if result["status"] == "queued":
            print(f"Request {i}: Queued at position {result['position']}, "
                  f"estimated wait {result['estimated_wait_seconds']:.1f}s")
        else:
            print(f"Request {i}: Rejected - {result['reason']}")
        
        await asyncio.sleep(0.1)  # Requests arrive over time
    
    # Let queue drain
    await asyncio.sleep(30)
    
    # Show stats
    stats = queue.get_stats()
    print(f"\nFinal stats: {stats}")

# Run
# asyncio.run(main())
```

**Priority Queue Implementation:**

```python
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable
import asyncio
import time

@dataclass(order=True)
class PriorityRequest:
    """
    Request with priority for heap queue.
    
    Lower priority number = higher priority (processed first).
    """
    priority: int
    timestamp: float = field(compare=True)  # Tie-breaker (earlier first)
    request_id: str = field(compare=False)
    handler: Callable = field(compare=False)
    args: tuple = field(compare=False, default_factory=tuple)
    kwargs: dict = field(compare=False, default_factory=dict)

class PriorityRequestQueue:
    """
    Priority queue for agent requests.
    
    Use cases:
    - Paying customers get priority over free tier
    - Interactive requests prioritized over batch
    - High-value operations prioritized
    """
    
    def __init__(self, max_concurrent: int = 10):
        self.heap = []
        self.max_concurrent = max_concurrent
        self.active_tasks = 0
        self.stats_by_priority = {}
    
    async def submit(
        self,
        request_id: str,
        priority: int,  # 0 = highest, 10 = lowest
        handler: Callable,
        *args,
        **kwargs
    ) -> dict:
        """
        Submit request with priority.
        
        Priority levels:
        0-2: Premium/paying customers
        3-5: Standard users
        6-8: Free tier
        9-10: Background/batch jobs
        """
        request = PriorityRequest(
            priority=priority,
            timestamp=time.time(),
            request_id=request_id,
            handler=handler,
            args=args,
            kwargs=kwargs
        )
        
        heapq.heappush(self.heap, request)
        
        # Count position at this priority level
        position_at_priority = sum(
            1 for r in self.heap if r.priority <= priority
        )
        
        return {
            "status": "queued",
            "request_id": request_id,
            "priority": priority,
            "position_at_priority": position_at_priority,
            "total_queue_size": len(self.heap)
        }
    
    async def _worker(self, worker_id: int):
        """Worker processing requests in priority order."""
        while True:
            if not self.heap:
                await asyncio.sleep(0.1)
                continue
            
            # Get highest priority request (lowest number)
            request = heapq.heappop(self.heap)
            self.active_tasks += 1
            
            try:
                start_time = time.time()
                result = await request.handler(
                    *request.args,
                    **request.kwargs
                )
                duration = time.time() - start_time
                wait_time = start_time - request.timestamp
                
                # Track stats by priority
                if request.priority not in self.stats_by_priority:
                    self.stats_by_priority[request.priority] = {
                        "count": 0,
                        "total_wait": 0,
                        "total_duration": 0
                    }
                
                stats = self.stats_by_priority[request.priority]
                stats["count"] += 1
                stats["total_wait"] += wait_time
                stats["total_duration"] += duration
                
                print(f"Worker {worker_id} completed {request.request_id} "
                      f"(priority {request.priority}, waited {wait_time:.1f}s)")
                
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
            finally:
                self.active_tasks -= 1
    
    async def start(self):
        """Start worker pool."""
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_concurrent)
        ]
        await asyncio.gather(*workers, return_exceptions=True)
    
    def get_stats(self) -> dict:
        """Get statistics by priority level."""
        stats = {}
        for priority, data in self.stats_by_priority.items():
            avg_wait = data["total_wait"] / data["count"] if data["count"] > 0 else 0
            avg_duration = data["total_duration"] / data["count"] if data["count"] > 0 else 0
            
            stats[f"priority_{priority}"] = {
                "count": data["count"],
                "avg_wait_seconds": round(avg_wait, 2),
                "avg_duration_seconds": round(avg_duration, 2)
            }
        
        return stats

# Usage with priority tiers
priority_queue = PriorityRequestQueue(max_concurrent=5)

# Priority levels
PRIORITY_PREMIUM = 1
PRIORITY_STANDARD = 5
PRIORITY_FREE = 8
PRIORITY_BATCH = 10

# Submit requests with different priorities
# Premium customer (processed first)
await priority_queue.submit(
    request_id="premium_1",
    priority=PRIORITY_PREMIUM,
    handler=process_agent_request,
    user_id=999,
    query="Premium customer urgent question"
)

# Free tier user (processed after premium/standard)
await priority_queue.submit(
    request_id="free_1",
    priority=PRIORITY_FREE,
    handler=process_agent_request,
    user_id=123,
    query="Free tier user question"
)

# Batch job (processed when idle)
await priority_queue.submit(
    request_id="batch_1",
    priority=PRIORITY_BATCH,
    handler=process_agent_request,
    user_id=0,
    query="Background batch processing"
)
```

**Rate-Limited Queue:**

```python
import asyncio
import time
from collections import deque

class RateLimitedQueue:
    """
    Queue with rate limiting to respect API limits.
    
    Example: OpenAI limits to 500 requests/minute
    This queue ensures we never exceed that limit.
    """
    
    def __init__(
        self,
        max_requests_per_minute: int = 500,
        max_concurrent: int = 10
    ):
        self.queue = deque()
        self.max_requests_per_minute = max_requests_per_minute
        self.max_concurrent = max_concurrent
        
        # Track request timestamps for rate limiting
        self.request_times = deque()
        self.active_tasks = 0
    
    def _can_make_request(self) -> bool:
        """
        Check if we can make another request within rate limit.
        
        Uses sliding window: count requests in last 60 seconds.
        """
        current_time = time.time()
        one_minute_ago = current_time - 60
        
        # Remove timestamps older than 1 minute
        while self.request_times and self.request_times[0] < one_minute_ago:
            self.request_times.popleft()
        
        # Check if under limit
        return len(self.request_times) < self.max_requests_per_minute
    
    def _wait_time_for_next_request(self) -> float:
        """
        Calculate how long to wait before next request allowed.
        
        Returns seconds to wait (0 if can proceed immediately).
        """
        if len(self.request_times) < self.max_requests_per_minute:
            return 0
        
        # Wait until oldest request is 60 seconds old
        oldest_request = self.request_times[0]
        time_since_oldest = time.time() - oldest_request
        wait_time = max(0, 60 - time_since_oldest)
        
        return wait_time
    
    async def submit(self, request_id: str, handler: Callable, *args, **kwargs):
        """Submit request to rate-limited queue."""
        self.queue.append({
            "request_id": request_id,
            "handler": handler,
            "args": args,
            "kwargs": kwargs,
            "submitted_at": time.time()
        })
        
        return {
            "status": "queued",
            "request_id": request_id,
            "position": len(self.queue),
            "current_rate": f"{len(self.request_times)}/{self.max_requests_per_minute} per minute"
        }
    
    async def _worker(self, worker_id: int):
        """Worker with rate limiting."""
        while True:
            if not self.queue:
                await asyncio.sleep(0.1)
                continue
            
            # Check rate limit before processing
            if not self._can_make_request():
                wait_time = self._wait_time_for_next_request()
                print(f"Worker {worker_id} rate limited, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time + 0.1)
                continue
            
            # Check concurrent limit
            if self.active_tasks >= self.max_concurrent:
                await asyncio.sleep(0.1)
                continue
            
            # Process request
            request = self.queue.popleft()
            self.active_tasks += 1
            self.request_times.append(time.time())
            
            try:
                result = await request["handler"](
                    *request["args"],
                    **request["kwargs"]
                )
                print(f"Worker {worker_id} completed {request['request_id']}")
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
            finally:
                self.active_tasks -= 1
    
    async def start(self):
        """Start rate-limited workers."""
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_concurrent)
        ]
        await asyncio.gather(*workers, return_exceptions=True)

# Usage
rate_limited_queue = RateLimitedQueue(
    max_requests_per_minute=500,  # OpenAI limit
    max_concurrent=10
)

# Submits are accepted immediately, but processing respects rate limits
for i in range(1000):
    await rate_limited_queue.submit(
        request_id=f"req_{i}",
        handler=call_openai_api,
        prompt=f"Query {i}"
    )

# Workers automatically throttle to stay within 500 req/min
```

**Production Queue with Redis:**

```python
import redis
import json
import asyncio
from typing import Optional, Callable
import time

class RedisRequestQueue:
    """
    Distributed queue using Redis for persistence and coordination.
    
    Advantages:
    - Persists requests (survive server restart)
    - Shared across multiple workers/servers
    - Supports priority queues (sorted sets)
    - Built-in pub/sub for real-time updates
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        queue_name: str = "agent_requests"
    ):
        self.redis = redis_client
        self.queue_name = queue_name
        self.processing_set = f"{queue_name}:processing"
    
    async def submit(
        self,
        request_id: str,
        handler_name: str,  # Can't serialize functions, use name
        payload: dict,
        priority: int = 5
    ) -> dict:
        """
        Submit request to Redis queue.
        
        Args:
            request_id: Unique request identifier
            handler_name: Name of handler function
            payload: JSON-serializable data
            priority: Lower = higher priority
        """
        request_data = {
            "request_id": request_id,
            "handler_name": handler_name,
            "payload": payload,
            "submitted_at": time.time(),
            "priority": priority
        }
        
        # Add to Redis sorted set (score = priority + timestamp for tie-breaking)
        score = priority + (time.time() / 1000000)  # Microsecond precision
        
        self.redis.zadd(
            self.queue_name,
            {json.dumps(request_data): score}
        )
        
        # Get position in queue
        position = self.redis.zrank(self.queue_name, json.dumps(request_data))
        queue_size = self.redis.zcard(self.queue_name)
        
        return {
            "status": "queued",
            "request_id": request_id,
            "position": position + 1 if position is not None else None,
            "queue_size": queue_size
        }
    
    def get_next_request(self) -> Optional[dict]:
        """
        Get next request from queue (highest priority).
        
        Returns request and moves to processing set.
        """
        # Pop lowest score (highest priority) from queue
        items = self.redis.zpopmin(self.queue_name, count=1)
        
        if not items:
            return None
        
        request_json, score = items[0]
        request_data = json.loads(request_json)
        
        # Move to processing set with timeout
        self.redis.zadd(
            self.processing_set,
            {request_json: time.time() + 300}  # 5 minute timeout
        )
        
        return request_data
    
    def mark_completed(self, request_id: str):
        """Mark request as completed (remove from processing set)."""
        # Remove from processing set
        # (In production, scan processing set for matching request_id)
        pass
    
    def requeue_stuck_requests(self):
        """
        Requeue requests stuck in processing set.
        
        Run periodically to handle worker crashes.
        """
        current_time = time.time()
        
        # Get requests with timeout < current time
        stuck_requests = self.redis.zrangebyscore(
            self.processing_set,
            min=0,
            max=current_time
        )
        
        for request_json in stuck_requests:
            request_data = json.loads(request_json)
            
            # Requeue with same priority
            score = request_data["priority"] + (time.time() / 1000000)
            self.redis.zadd(self.queue_name, {request_json: score})
            
            # Remove from processing
            self.redis.zrem(self.processing_set, request_json)
            
            print(f"Requeued stuck request: {request_data['request_id']}")
    
    def get_stats(self) -> dict:
        """Get queue statistics."""
        return {
            "queued": self.redis.zcard(self.queue_name),
            "processing": self.redis.zcard(self.processing_set)
        }

# Worker process using Redis queue
async def redis_worker(
    redis_queue: RedisRequestQueue,
    handlers: dict[str, Callable]
):
    """
    Worker that processes requests from Redis queue.
    
    Args:
        redis_queue: RedisRequestQueue instance
        handlers: Mapping of handler_name → handler function
    """
    while True:
        request = redis_queue.get_next_request()
        
        if not request:
            await asyncio.sleep(1)
            continue
        
        handler_name = request["handler_name"]
        handler = handlers.get(handler_name)
        
        if not handler:
            print(f"Unknown handler: {handler_name}")
            continue
        
        try:
            # Process request
            result = await handler(request["payload"])
            
            # Mark completed
            redis_queue.mark_completed(request["request_id"])
            
            print(f"Completed: {request['request_id']}")
            
        except Exception as e:
            print(f"Error processing {request['request_id']}: {e}")
            # Could requeue with exponential backoff

# Setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)
queue = RedisRequestQueue(redis_client)

# Handler registry
handlers = {
    "process_agent_query": process_agent_request,
    "generate_summary": generate_summary,
    "analyze_sentiment": analyze_sentiment
}

# Start workers (can run on multiple servers)
# asyncio.run(redis_worker(queue, handlers))
```

### What It Isn't
Request queuing is not **a replacement for horizontal scaling**. Queuing manages request flow for given capacity; if capacity is fundamentally insufficient, you need more workers/servers, not just better queuing.

It's not **the same as caching**. Caching serves identical requests from stored results; queuing manages the order and rate of processing unique requests.

Queuing is not **always beneficial**. For low-traffic systems where requests rarely exceed capacity, queuing adds latency and complexity unnecessarily. Queue when load exceeds capacity, not preemptively.

It's not **transparent to users**. Queuing adds wait time—users must be informed of queue position and estimated wait. Silent queuing without feedback creates bad UX.

Finally, queuing is not **a guarantee of processing**. Queues can still fill up and reject requests. It shifts the problem from "process everything immediately or fail" to "buffer some overload gracefully, reject extreme overload."

## How It Works

### Advanced Queue Patterns

**Pattern 1: Fair Queuing (Prevent User Monopolization)**

```python
from collections import defaultdict, deque
import asyncio

class FairQueue:
    """
    Fair queuing ensures no single user monopolizes resources.
    
    Algorithm: Round-robin across users, FIFO within each user.
    """
    
    def __init__(self, max_concurrent: int = 10):
        self.user_queues = defaultdict(deque)  # user_id → queue
        self.max_concurrent = max_concurrent
        self.active_by_user = defaultdict(int)  # user_id → active count
    
    async def submit(self, user_id: str, request_id: str, handler: Callable, *args, **kwargs):
        """Submit request for specific user."""
        self.user_queues[user_id].append({
            "request_id": request_id,
            "handler": handler,
            "args": args,
            "kwargs": kwargs
        })
        
        return {
            "status": "queued",
            "user_id": user_id,
            "position_for_user": len(self.user_queues[user_id]),
            "total_users_queued": len(self.user_queues)
        }
    
    def _get_next_request(self):
        """
        Get next request using fair round-robin.
        
        Cycles through users, taking one request from each.
        """
        # Get users with queued requests
        users_with_requests = [
            user_id for user_id, queue in self.user_queues.items()
            if queue
        ]
        
        if not users_with_requests:
            return None
        
        # Simple round-robin: take from each user in turn
        for user_id in users_with_requests:
            queue = self.user_queues[user_id]
            if queue:
                request = queue.popleft()
                request["user_id"] = user_id
                return request
        
        return None
    
    async def _worker(self, worker_id: int):
        """Fair queuing worker."""
        while True:
            request = self._get_next_request()
            
            if not request:
                await asyncio.sleep(0.1)
                continue
            
            user_id = request["user_id"]
            self.active_by_user[user_id] += 1
            
            try:
                result = await request["handler"](
                    *request["args"],
                    **request["kwargs"]
                )
                print(f"Worker {worker_id} completed {request['request_id']} for user {user_id}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                self.active_by_user[user_id] -= 1
    
    async def start(self):
        """Start fair queue workers."""
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_concurrent)
        ]
        await asyncio.gather(*workers, return_exceptions=True)

# Example: One user submits 100 requests, another submits 10
# Fair queuing ensures second user's requests don't wait behind all 100
```

**Pattern 2: Backpressure and Circuit Breaking**

```python
class BackpressureQueue:
    """
    Queue with backpressure: slow down or reject when overloaded.
    
    Prevents cascading failures and memory exhaustion.
    """
    
    def __init__(
        self,
        max_queue_size: int = 1000,
        max_concurrent: int = 10,
        high_water_mark: float = 0.8,  # 80% full
        low_water_mark: float = 0.5    # 50% full
    ):
        self.queue = deque()
        self.max_queue_size = max_queue_size
        self.max_concurrent = max_concurrent
        self.high_water_mark = int(max_queue_size * high_water_mark)
        self.low_water_mark = int(max_queue_size * low_water_mark)
        
        self.backpressure_active = False
        self.circuit_open = False
        self.error_count = 0
        self.error_threshold = 10
    
    async def submit(self, request_id: str, handler: Callable, *args, **kwargs) -> dict:
        """
        Submit with backpressure.
        
        Returns different responses based on load:
        - Normal: queued immediately
        - High water: queued with warning (slow down)
        - Full: rejected (apply backpressure)
        - Circuit open: rejected (system unhealthy)
        """
        # Circuit breaker: reject all if system unhealthy
        if self.circuit_open:
            return {
                "status": "rejected",
                "reason": "circuit_breaker_open",
                "message": "System temporarily unavailable due to errors"
            }
        
        # Queue full: hard reject
        if len(self.queue) >= self.max_queue_size:
            return {
                "status": "rejected",
                "reason": "queue_full",
                "queue_size": len(self.queue),
                "max_queue_size": self.max_queue_size
            }
        
        # Add to queue
        self.queue.append({
            "request_id": request_id,
            "handler": handler,
            "args": args,
            "kwargs": kwargs
        })
        
        queue_size = len(self.queue)
        
        # Check backpressure threshold
        if queue_size >= self.high_water_mark and not self.backpressure_active:
            self.backpressure_active = True
            print(f"⚠️  Backpressure activated (queue: {queue_size}/{self.max_queue_size})")
        elif queue_size < self.low_water_mark and self.backpressure_active:
            self.backpressure_active = False
            print(f"✓ Backpressure deactivated (queue: {queue_size}/{self.max_queue_size})")
        
        return {
            "status": "queued",
            "request_id": request_id,
            "position": queue_size,
            "backpressure": self.backpressure_active,
            "message": "System under high load, please slow down requests" if self.backpressure_active else None
        }
    
    async def _worker(self, worker_id: int):
        """Worker with circuit breaker."""
        while True:
            if not self.queue:
                await asyncio.sleep(0.1)
                continue
            
            request = self.queue.popleft()
            
            try:
                result = await request["handler"](
                    *request["args"],
                    **request["kwargs"]
                )
                
                # Success: reset error count
                self.error_count = 0
                if self.circuit_open:
                    self.circuit_open = False
                    print("✓ Circuit breaker closed (errors resolved)")
                
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
                
                # Track errors for circuit breaker
                self.error_count += 1
                
                if self.error_count >= self.error_threshold:
                    self.circuit_open = True
                    print(f"⚠️  Circuit breaker opened ({self.error_count} consecutive errors)")
    
    async def start(self):
        """Start workers with backpressure."""
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_concurrent)
        ]
        await asyncio.gather(*workers, return_exceptions=True)
```

## Think of It Like This
Imagine a popular coffee shop during morning rush hour.

**Without queuing** (reject when busy): Customers arrive, but barista can only make 2 drinks at once. When 50 customers show up simultaneously, barista says "Sorry, too busy, come back later" to 48 people. Those 48 leave, try again in 5 minutes, now 60 people show up (original 48 + 12 new), even more rejected. Nobody gets coffee, chaos ensues.

**With queuing**: Customers arrive, join the line (queue), and wait their turn. Barista still makes 2 drinks at once (same capacity), but everyone waits in order. Customers can see their position (#15 in line), estimate wait (7 minutes), and decide whether to wait. Some leave (cancelation), but most wait because they see progress. System is stable, predictable, and everyone eventually gets served.

**Priority queuing**: Regular customers join normal line, but rewards program members get priority lane (processed first). Both systems work, but loyalty is rewarded.

**Rate limiting**: Barista knows the coffee machine overheats after 500 drinks/hour. Queue processes requests but never exceeds that rate—waits a few seconds between batches to keep machine healthy.

Request queuing gives your agent system that coffee shop line—orderly, predictable, fair handling of bursts that exceed processing capacity.

## The "So What?" Factor
**If you implement request queuing:**
- System handles traffic spikes gracefully (no crashes)
- Users get position feedback instead of cryptic errors
- Can control costs (process at affordable rate)
- API rate limits respected automatically
- Fair resource allocation across users
- Priority support for paying customers
- Retry storms prevented (no cascading failures)
- Observability into load (queue depth metrics)
- Predictable performance under load
- System scales smoothly as demand grows

**If you skip queuing:**
- System collapses under load (all requests fail)
- 429 rate limit errors when traffic spikes
- Retry storms amplify failures (10x traffic)
- No way to prioritize important requests
- Users can monopolize resources (unfair)
- Unpredictable costs (burst spending)
- No visibility into overload conditions
- Can't scale gracefully (binary: works or fails)
- Poor user experience during peaks
- Manual intervention required for load issues

## Practical Checklist
Before deploying request queuing:
- [ ] Have you measured peak request rates vs processing capacity?
- [ ] Is queue size limit set appropriately (prevent memory exhaustion)?
- [ ] Do you provide users with queue position and estimated wait time?
- [ ] Are you using appropriate queue discipline (FIFO, priority, fair)?
- [ ] Is queue persistent (Redis, SQS) or acceptable to lose on restart?
- [ ] Are workers scaling based on queue depth?
- [ ] Do you have monitoring/alerting on queue depth and wait times?
- [ ] Is there backpressure feedback when queue is filling?
- [ ] Are rate limits implemented to protect APIs?
- [ ] Can you handle stuck requests (timeouts, requeuing)?
- [ ] Is priority queuing implemented for paid vs free tiers?
- [ ] Have you tested behavior when queue fills completely?
- [ ] Are costs under control with rate-limited processing?

## Watch Out For
⚠️ **Queue Memory Exhaustion**: Unbounded queues consume all RAM. Always set max_queue_size and reject beyond limit.

⚠️ **Lost Requests on Crash**: In-memory queues lose all requests on server crash. Use Redis, SQS, or database queues for production.

⚠️ **No Feedback to Users**: Silent queuing without position/wait time feedback frustrates users. Always communicate queue status.

⚠️ **Priority Inversion**: Low-priority requests blocking high-priority. Use priority queues, not FIFO, when priorities matter.

⚠️ **Stuck Request Accumulation**: Failed/hung workers don't release requests. Implement timeouts and requeuing of stuck requests.

⚠️ **Queue Depth Explosions**: If processing slower than arrival rate, queue grows forever. Need backpressure or rejection at some point.

⚠️ **Unfair Resource Allocation**: Single user submitting 1000 requests blocks others. Implement fair queuing or per-user rate limits.

⚠️ **No Observable Metrics**: Can't optimize what you don't measure. Track: queue depth, wait times, processing rates, rejection rates.

⚠️ **Rate Limit Miscalculation**: Setting worker count without considering API rate limits causes 429 errors. Calculate: workers × requests/sec < API limit.

⚠️ **Cold Start Latency**: First request after idle period may be slow (cold start). Keep-alive requests or warm pools help.

## Connections
**Builds On:**
- Async programming patterns
- Data structures (queues, heaps, deques)
- Distributed systems concepts
- Rate limiting algorithms

**Works With:**
- [streaming_responses](streaming_responses.md) - Queue requests, stream responses
- [idempotency](idempotency.md) - Queued requests must be idempotent for retries
- [handoff_protocol](handoff_protocol.md) - Queue agent handoffs
- [message_queue](../System_Architecture/message_queue.md) - Infrastructure for distributed queues
- [load_balancing](../System_Architecture/load_balancing.md) - Distribute queue workers
- [scalability](../System_Architecture/scalability.md) - Queuing enables horizontal scaling

**Leads To:**
- Auto-scaling based on queue depth
- Priority-based resource allocation
- Multi-tenant fairness guarantees
- Cost-aware request scheduling
- Adaptive rate limiting

**Related Patterns:**
- [caching](../Data_and_Retrieval_Patterns/caching.md) - Reduce requests entering queue
- Circuit breakers (prevent cascading failures)
- Bulkhead pattern (isolate queue failures)
- Token bucket rate limiting
- Backpressure propagation

## Quick Decision Guide
**Use in-memory queues when:**
- Single-server deployment
- Can tolerate request loss on crash
- Low to medium traffic (< 1000 requests/minute)
- Prototyping or development
- Latency critical (minimize hops)

**Use Redis queues when:**
- Multi-server deployment (shared queue)
- Must persist requests (survive restarts)
- Medium to high traffic
- Need distributed coordination
- Priority queuing with sorted sets

**Use SQS/cloud queues when:**
- Fully managed service preferred
- Very high traffic (millions of requests)
- Need built-in retries, dead letter queues
- Multi-region deployment
- Cost-effective at scale

**Use priority queuing when:**
- Different user tiers (paid vs free)
- Mix of interactive and batch workloads
- Some requests more valuable than others
- Need SLA differentiation

**Use fair queuing when:**
- Multiple users sharing resources
- Prevent one user monopolizing system
- Equal priority users but want fairness
- Multi-tenant systems

**Implement rate limiting when:**
- External APIs have rate limits
- Cost control critical (LLM APIs expensive)
- Need to prevent abuse
- Protect downstream services

## Further Exploration
- 📖 **"The Art of Scalability" by Abbott & Fisher** - Queue management for web scale
- 🎯 **Redis Queue Patterns** - RPUSH/LPOP, sorted sets for priorities
- 💡 **Implement Priority Queue with Monitoring** - Build queue with Prometheus metrics (depth, wait times, throughput)
- 📖 **AWS SQS Best Practices** - Managed queue service patterns
- 🎯 **Celery Distributed Task Queue** - Production-grade Python task queuing
- 💡 **Load Test Queue System** - Simulate 10x normal load, measure: rejection rate, wait times, throughput
- 📖 **"Site Reliability Engineering" by Google** - Chapter on handling overload
- 🎯 **RabbitMQ Priority Queues** - Message broker with sophisticated routing
- 💡 **Fair Queuing Algorithms** - WFQ (Weighted Fair Queuing), DRR (Deficit Round Robin)
- 📖 **Rate Limiting Algorithms** - Token bucket, leaky bucket, sliding window

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
