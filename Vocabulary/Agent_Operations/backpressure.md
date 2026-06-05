# Backpressure

## At a Glance
| | |
|---|---|
| **Category** | Flow Control Pattern / System Resilience |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 hours for fundamentals, weeks for distributed patterns |
| **Prerequisites** | Understanding of queues, async programming, streaming, rate limiting |

## One-Sentence Summary
Backpressure is the feedback mechanism that allows downstream components (slow consumers) to signal upstream components (fast producers) to slow down or stop sending data—preventing memory exhaustion, cascading failures, and system collapse when production rate exceeds consumption capacity, transforming "fast producer overwhelms slow consumer until crash" failures into graceful degradation where systems automatically throttle to sustainable rates.

## Why This Matters to You
When you build AI agent systems in 2026, backpressure is the difference between systems that gracefully handle overload and systems that collapse consuming all available memory until they crash. Without backpressure, when your LLM generates tokens at 50 tokens/second but your frontend can only render 10 tokens/second, the buffered tokens accumulate in memory—after 60 seconds you have 2400 buffered tokens (96 KB), after 10 minutes you have 24,000 tokens (960 KB per connection), with 1000 concurrent users that's 960 MB just in output buffers, exhausting RAM and crashing. With backpressure, the frontend signals "I'm falling behind" and the backend pauses generation until the frontend catches up, keeping buffer size bounded at ~100 tokens (4 KB) regardless of duration. This matters at every system boundary: agent → queue (don't accept unlimited requests), queue → worker (don't pull faster than processing), LLM → streaming endpoint (don't generate faster than transmission), database → application (don't read faster than processing), external API → your service (respect rate limits). At production scale serving 10,000+ users, lack of backpressure causes: out-of-memory crashes ($10,000+ in lost revenue per incident), cascading failures (one slow consumer brings down entire cluster), retry storms (crashed consumers retry, amplifying load 10x), TCP connection exhaustion (buffers fill, new connections rejected), and unpredictable latency (deep queues cause seconds of lag). Backpressure prevents this using strategies like: reject requests when queues full (fast failure, user retries), delay accepting new work (pause producer until consumer ready), reduce production rate (slow down to match consumer), buffer with limits (small bounded queues), and explicit flow control (consumer pulls at its pace). This matters economically: a single OOM crash during peak hours loses thousands in revenue; cascading failures require expensive incident response; retry storms 10x your API costs. But backpressure adds complexity: must propagate signals across boundaries, coordinate producer/consumer rates, handle partial failures (some consumers slow, not all), and balance throughput vs latency. Understanding backpressure patterns (push vs pull models), implementation techniques (async iterators, bounded queues, rate windows), propagation strategies (TCP flow control, HTTP 429 responses, queue depth metrics), and monitoring approaches (buffer depths, consumer lag, rejection rates) determines whether your multi-agent system scales reliably or collapses unpredictably under real-world load. In 2026, with AI agents streaming large responses, coordinating multi-step workflows, and processing high-volume event streams, backpressure is fundamental infrastructure—not optional optimization.

## The Core Idea
### What It Is
Backpressure is a flow control pattern where consumers of data signal producers to slow down when the consumer cannot keep pace with production rate. It's the "please slow down, I'm falling behind" feedback loop that prevents buffer overflow and resource exhaustion.

**The Fundamental Problem:**

Systems have multiple stages with different processing rates:

```
Producer (fast)  →  Buffer  →  Consumer (slow)
   50 items/sec      ???        10 items/sec

Without backpressure:
- Buffer grows unbounded: 0 → 40 → 80 → 120 → ... → OOM crash
- System fails when memory exhausted

With backpressure:
- Consumer signals "slow down" when buffer reaches limit
- Producer pauses or slows to match consumer rate
- Buffer stays bounded, system remains stable
```

**Example: Unbounded Buffer Problem**

```python
import asyncio
import time
from collections import deque

class UnboundedBufferDemo:
    """
    Demonstrate memory exhaustion without backpressure.
    
    Fast producer, slow consumer, no flow control.
    """
    
    def __init__(self):
        self.buffer = deque()
        self.items_produced = 0
        self.items_consumed = 0
    
    async def fast_producer(self):
        """
        Fast producer: generates 50 items/second.
        
        No backpressure: keeps producing regardless of buffer size.
        """
        while True:
            # Generate item (simulate LLM token generation)
            item = f"token_{self.items_produced}"
            self.buffer.append(item)
            self.items_produced += 1
            
            # Fast rate: 50 items/second
            await asyncio.sleep(0.02)
            
            if self.items_produced % 100 == 0:
                buffer_size = len(self.buffer)
                print(f"Produced {self.items_produced}, buffer size: {buffer_size}")
                
                # Simulate OOM when buffer too large
                if buffer_size > 10000:
                    print("💥 OUT OF MEMORY! System crashed.")
                    return
    
    async def slow_consumer(self):
        """
        Slow consumer: processes 10 items/second.
        
        Cannot keep up with producer.
        """
        while True:
            if self.buffer:
                item = self.buffer.popleft()
                self.items_consumed += 1
                
                # Slow processing: 10 items/second
                await asyncio.sleep(0.1)
            else:
                await asyncio.sleep(0.01)
    
    async def run(self):
        """Run producer and consumer."""
        await asyncio.gather(
            self.fast_producer(),
            self.slow_consumer()
        )

# Demo
demo = UnboundedBufferDemo()
# asyncio.run(demo.run())

# Output:
# Produced 100, buffer size: 40
# Produced 200, buffer size: 80
# Produced 300, buffer size: 120
# ...
# Produced 10100, buffer size: 10040
# 💥 OUT OF MEMORY! System crashed.
```

**Solution 1: Bounded Queue with Backpressure**

```python
import asyncio

class BoundedQueueWithBackpressure:
    """
    Bounded queue that applies backpressure to producer.
    
    When queue full, producer blocks until consumer makes space.
    """
    
    def __init__(self, max_size: int = 100):
        self.queue = asyncio.Queue(maxsize=max_size)
        self.items_produced = 0
        self.items_consumed = 0
        self.producer_blocked_count = 0
    
    async def producer(self):
        """
        Producer with backpressure.
        
        Blocks when queue full (automatic backpressure from asyncio.Queue).
        """
        while True:
            item = f"token_{self.items_produced}"
            
            # This blocks if queue is full (backpressure!)
            queue_size_before = self.queue.qsize()
            await self.queue.put(item)
            
            if queue_size_before == self.queue.maxsize:
                self.producer_blocked_count += 1
                print(f"⚠️  Producer blocked (queue full at {self.queue.maxsize})")
            
            self.items_produced += 1
            
            # Fast rate: 50 items/second
            await asyncio.sleep(0.02)
            
            if self.items_produced % 100 == 0:
                print(f"Produced {self.items_produced}, "
                      f"queue size: {self.queue.qsize()}, "
                      f"blocked {self.producer_blocked_count} times")
    
    async def consumer(self):
        """
        Slow consumer: processes 10 items/second.
        """
        while True:
            item = await self.queue.get()
            self.items_consumed += 1
            
            # Slow processing: 10 items/second
            await asyncio.sleep(0.1)
    
    async def run(self, duration: int = 10):
        """Run for fixed duration."""
        producer_task = asyncio.create_task(self.producer())
        consumer_task = asyncio.create_task(self.consumer())
        
        await asyncio.sleep(duration)
        
        producer_task.cancel()
        consumer_task.cancel()
        
        print(f"\n✓ Finished: produced {self.items_produced}, "
              f"consumed {self.items_consumed}, "
              f"queue size: {self.queue.qsize()}")
        print(f"  Max queue size: {self.queue.maxsize} (bounded, no OOM!)")

# Demo
demo = BoundedQueueWithBackpressure(max_size=100)
# asyncio.run(demo.run(duration=10))

# Output:
# Produced 100, queue size: 100, blocked 0 times
# ⚠️  Producer blocked (queue full at 100)
# Produced 200, queue size: 100, blocked 43 times
# ...
# ✓ Finished: produced 500, consumed 100, queue size: 100
#   Max queue size: 100 (bounded, no OOM!)
```

**Solution 2: Explicit Backpressure Signaling**

```python
import asyncio
import time

class ExplicitBackpressureSystem:
    """
    System where consumer explicitly signals producer to slow down.
    
    Pattern: Consumer monitors its processing rate and signals backpressure.
    """
    
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=200)
        self.backpressure_active = False
        self.items_produced = 0
        self.items_consumed = 0
        self.slow_downs = 0
    
    async def adaptive_producer(self):
        """
        Producer that responds to backpressure signals.
        
        Slows down when consumer signals backpressure.
        """
        while True:
            # Check backpressure signal
            if self.backpressure_active:
                # Slow down production
                production_rate = 0.1  # 10 items/second
                self.slow_downs += 1
            else:
                # Normal rate
                production_rate = 0.02  # 50 items/second
            
            item = f"item_{self.items_produced}"
            await self.queue.put(item)
            self.items_produced += 1
            
            await asyncio.sleep(production_rate)
            
            if self.items_produced % 100 == 0:
                status = "🐌 SLOWED" if self.backpressure_active else "🚀 FAST"
                print(f"{status} - Produced {self.items_produced}, "
                      f"queue: {self.queue.qsize()}, "
                      f"slowdowns: {self.slow_downs}")
    
    async def consumer_with_backpressure_signaling(self):
        """
        Consumer that signals backpressure based on queue depth.
        
        Strategy:
        - Queue > 80% full → activate backpressure
        - Queue < 50% full → deactivate backpressure
        """
        HIGH_WATER_MARK = int(self.queue.maxsize * 0.8)  # 160
        LOW_WATER_MARK = int(self.queue.maxsize * 0.5)   # 100
        
        while True:
            item = await self.queue.get()
            self.items_consumed += 1
            
            # Check queue depth and signal backpressure
            queue_size = self.queue.qsize()
            
            if queue_size > HIGH_WATER_MARK and not self.backpressure_active:
                self.backpressure_active = True
                print(f"\n⚠️  BACKPRESSURE ACTIVATED (queue: {queue_size}/{self.queue.maxsize})\n")
            
            elif queue_size < LOW_WATER_MARK and self.backpressure_active:
                self.backpressure_active = False
                print(f"\n✓ Backpressure deactivated (queue: {queue_size}/{self.queue.maxsize})\n")
            
            # Variable processing speed (simulate load variation)
            processing_time = 0.1  # 10 items/second
            await asyncio.sleep(processing_time)
    
    async def run(self, duration: int = 30):
        """Run system with backpressure."""
        producer_task = asyncio.create_task(self.adaptive_producer())
        consumer_task = asyncio.create_task(self.consumer_with_backpressure_signaling())
        
        await asyncio.sleep(duration)
        
        producer_task.cancel()
        consumer_task.cancel()
        
        print(f"\n✓ Finished: produced {self.items_produced}, "
              f"consumed {self.items_consumed}")
        print(f"  Queue stayed bounded: max {self.queue.maxsize}")
        print(f"  Producer slowed down {self.slow_downs} times")

# Demo
system = ExplicitBackpressureSystem()
# asyncio.run(system.run(duration=30))

# Output shows producer automatically slowing when consumer falls behind
```

**Solution 3: Pull-Based Backpressure (Consumer-Controlled)**

```python
import asyncio

class PullBasedBackpressure:
    """
    Pull model: consumer requests items at its own pace.
    
    Producer only generates when consumer requests (natural backpressure).
    """
    
    def __init__(self):
        self.request_queue = asyncio.Queue()  # Consumer requests
        self.response_queue = asyncio.Queue()  # Producer responses
        self.items_produced = 0
        self.items_consumed = 0
    
    async def producer(self):
        """
        Producer waits for consumer requests.
        
        Only produces when consumer pulls (perfect backpressure).
        """
        while True:
            # Wait for consumer to request item
            request = await self.request_queue.get()
            
            # Generate item
            item = f"item_{self.items_produced}"
            self.items_produced += 1
            
            # Simulate generation time (e.g., LLM inference)
            await asyncio.sleep(0.02)
            
            # Send to consumer
            await self.response_queue.put(item)
            
            if self.items_produced % 50 == 0:
                print(f"Producer: generated {self.items_produced} items (on-demand)")
    
    async def consumer(self):
        """
        Consumer pulls items at its own pace.
        
        Natural backpressure: only requests when ready to process.
        """
        while True:
            # Request item from producer
            await self.request_queue.put("REQUEST")
            
            # Wait for item
            item = await self.response_queue.get()
            self.items_consumed += 1
            
            # Process at slow rate
            await asyncio.sleep(0.1)  # 10 items/second
            
            if self.items_consumed % 50 == 0:
                print(f"Consumer: processed {self.items_consumed} items")
    
    async def run(self, duration: int = 10):
        """Run pull-based system."""
        producer_task = asyncio.create_task(self.producer())
        consumer_task = asyncio.create_task(self.consumer())
        
        await asyncio.sleep(duration)
        
        producer_task.cancel()
        consumer_task.cancel()
        
        print(f"\n✓ Pull-based system: produced {self.items_produced}, "
              f"consumed {self.items_consumed}")
        print(f"  No unbounded buffers (consumer controlled rate)")

# Demo
pull_system = PullBasedBackpressure()
# asyncio.run(pull_system.run(duration=10))

# Consumer processes ~100 items, producer generates ~100 items (matched rates)
```

**Solution 4: HTTP Streaming with Backpressure**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def generate_tokens_with_backpressure():
    """
    Generate tokens with natural HTTP streaming backpressure.
    
    TCP flow control provides automatic backpressure:
    - Client slow to read → TCP buffers fill → send() blocks
    - Generator pauses until client catches up
    """
    for i in range(1000):
        token = f"token_{i} "
        
        # Yield token (blocks if client slow to read)
        yield f"data: {token}\n\n"
        
        # Fast generation rate
        await asyncio.sleep(0.01)
        
        if i % 100 == 0:
            print(f"Generated {i} tokens (may have paused for slow client)")

@app.get("/stream")
async def stream_with_backpressure():
    """
    Streaming endpoint with natural backpressure.
    
    If client reads slowly, generator automatically pauses.
    """
    return StreamingResponse(
        generate_tokens_with_backpressure(),
        media_type="text/event-stream"
    )

# Client that simulates slow reading
async def slow_client():
    """
    Client that reads slowly (backpressure to server).
    """
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/stream') as response:
            async for line in response.content:
                # Process slowly (10 tokens/second)
                print(f"Received: {line.decode()}")
                await asyncio.sleep(0.1)
                
                # Server automatically paused when client was slow!
```

**Solution 5: Rate Limiting as Backpressure**

```python
import asyncio
import time
from collections import deque

class RateLimiterBackpressure:
    """
    Rate limiter applies backpressure to prevent overwhelming APIs.
    
    Pattern: Enforce maximum rate, reject/delay excess requests.
    """
    
    def __init__(self, max_requests_per_second: int = 10):
        self.max_requests_per_second = max_requests_per_second
        self.request_times = deque()
        self.requests_processed = 0
        self.requests_delayed = 0
    
    async def _wait_for_capacity(self):
        """
        Wait until rate limit allows next request.
        
        Implements backpressure: caller blocks until rate allows.
        """
        while True:
            current_time = time.time()
            one_second_ago = current_time - 1
            
            # Remove old timestamps
            while self.request_times and self.request_times[0] < one_second_ago:
                self.request_times.popleft()
            
            # Check if under limit
            if len(self.request_times) < self.max_requests_per_second:
                self.request_times.append(current_time)
                return
            
            # Over limit: wait (backpressure!)
            self.requests_delayed += 1
            oldest_request = self.request_times[0]
            wait_time = 1 - (current_time - oldest_request)
            
            if wait_time > 0:
                await asyncio.sleep(wait_time)
    
    async def make_request(self, request_id: int):
        """
        Make request with rate limiting backpressure.
        
        Automatically throttles to respect rate limit.
        """
        # Wait if over rate limit (backpressure applied here)
        await self._wait_for_capacity()
        
        # Make request
        self.requests_processed += 1
        print(f"Request {request_id} processed (total: {self.requests_processed})")
        
        # Simulate API call
        await asyncio.sleep(0.05)
    
    async def burst_requests(self):
        """
        Simulate burst of requests (tests backpressure).
        
        Sends 100 requests rapidly, rate limiter applies backpressure.
        """
        tasks = []
        for i in range(100):
            task = asyncio.create_task(self.make_request(i))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        print(f"\n✓ Completed {self.requests_processed} requests")
        print(f"  Rate limit: {self.max_requests_per_second} req/sec")
        print(f"  Delays applied: {self.requests_delayed} times")
        print(f"  Backpressure prevented rate limit violations!")

# Demo
rate_limiter = RateLimiterBackpressure(max_requests_per_second=10)
# asyncio.run(rate_limiter.burst_requests())

# Output shows requests automatically throttled to 10/sec
```

### What It Isn't
Backpressure is not **the same as rate limiting**. Rate limiting caps incoming requests; backpressure is feedback from consumer to producer about processing capacity. (They often work together.)

It's not **always necessary**. If producer and consumer rates are naturally matched, or if unbounded buffering is acceptable (rare), backpressure isn't needed.

Backpressure is not **always implemented as blocking**. Other strategies: reject excess, drop old items, sample/downsample, signal to slow down without blocking.

It's not **only about memory**. Backpressure also prevents: CPU exhaustion, network saturation, disk I/O overload, database connection exhaustion, external API rate limit violations.

Finally, backpressure is not **free**. It adds latency (waiting for consumer), complexity (propagating signals), and may reduce throughput (intentionally slowing down).

## How It Works

### Backpressure Strategies

**Strategy 1: Reject (Fast Failure)**

```python
import asyncio

class RejectBackpressure:
    """
    Reject new items when buffer full.
    
    Strategy: Fail fast, let client retry with backoff.
    """
    
    def __init__(self, max_queue_size: int = 100):
        self.queue = []
        self.max_queue_size = max_queue_size
        self.rejected_count = 0
        self.accepted_count = 0
    
    def try_enqueue(self, item) -> dict:
        """
        Try to add item to queue.
        
        Returns:
            {"status": "accepted"} or {"status": "rejected", "reason": "queue_full"}
        """
        if len(self.queue) >= self.max_queue_size:
            self.rejected_count += 1
            return {
                "status": "rejected",
                "reason": "queue_full",
                "queue_size": len(self.queue),
                "retry_after": 1  # Suggest retry after 1 second
            }
        
        self.queue.append(item)
        self.accepted_count += 1
        return {
            "status": "accepted",
            "queue_size": len(self.queue)
        }
    
    def dequeue(self):
        """Remove item from queue."""
        if self.queue:
            return self.queue.pop(0)
        return None

# Usage: API endpoint with backpressure
reject_queue = RejectBackpressure(max_queue_size=100)

# Fast producer
for i in range(200):
    result = reject_queue.try_enqueue(f"item_{i}")
    
    if result["status"] == "rejected":
        print(f"Item {i}: REJECTED (queue full)")
        # Client should retry with backoff
    else:
        print(f"Item {i}: accepted (queue: {result['queue_size']})")

print(f"\nAccepted: {reject_queue.accepted_count}, Rejected: {reject_queue.rejected_count}")
```

**Strategy 2: Drop (Lossy Backpressure)**

```python
from collections import deque

class DropOldestBackpressure:
    """
    Drop oldest items when buffer full.
    
    Strategy: Keep most recent data, acceptable for real-time streams.
    """
    
    def __init__(self, max_size: int = 100):
        self.buffer = deque(maxlen=max_size)  # Automatically drops oldest
        self.items_added = 0
        self.items_dropped = 0
    
    def add(self, item):
        """
        Add item, dropping oldest if full.
        
        Good for: Real-time metrics, sensor data, logs.
        """
        if len(self.buffer) >= self.buffer.maxlen:
            self.items_dropped += 1
            print(f"⚠️  Dropped oldest item (buffer full at {self.buffer.maxlen})")
        
        self.buffer.append(item)
        self.items_added += 1
    
    def get_stats(self) -> dict:
        """Get drop statistics."""
        return {
            "buffer_size": len(self.buffer),
            "items_added": self.items_added,
            "items_dropped": self.items_dropped,
            "drop_rate": self.items_dropped / self.items_added if self.items_added > 0 else 0
        }

# Usage: Real-time metrics buffering
metrics_buffer = DropOldestBackpressure(max_size=1000)

# Fast producer (metrics every 10ms)
for i in range(10000):
    metrics_buffer.add({"timestamp": i, "value": i * 10})

stats = metrics_buffer.get_stats()
print(f"Stats: {stats}")
# Most recent 1000 metrics kept, oldest 9000 dropped
```

**Strategy 3: Sampling (Adaptive Backpressure)**

```python
class AdaptiveSamplingBackpressure:
    """
    Sample/downsample when consumer falls behind.
    
    Strategy: Reduce data rate by sampling, preserving throughput.
    """
    
    def __init__(self, target_buffer_size: int = 100):
        self.buffer = []
        self.target_buffer_size = target_buffer_size
        self.sampling_rate = 1  # 1 = keep all, 10 = keep 1 in 10
        self.items_received = 0
        self.items_sampled = 0
    
    def add(self, item):
        """
        Add item with adaptive sampling.
        
        Automatically increases sampling rate when buffer grows.
        """
        self.items_received += 1
        
        # Adapt sampling rate based on buffer size
        buffer_size = len(self.buffer)
        
        if buffer_size > self.target_buffer_size * 0.9:
            # Buffer nearly full: aggressive sampling
            self.sampling_rate = 10
        elif buffer_size > self.target_buffer_size * 0.7:
            # Buffer filling: moderate sampling
            self.sampling_rate = 5
        elif buffer_size < self.target_buffer_size * 0.3:
            # Buffer light: no sampling
            self.sampling_rate = 1
        
        # Sample: keep 1 in N items
        if self.items_received % self.sampling_rate == 0:
            self.buffer.append(item)
            self.items_sampled += 1
        
        if self.items_received % 1000 == 0:
            print(f"Received {self.items_received}, "
                  f"sampled {self.items_sampled}, "
                  f"buffer: {len(self.buffer)}, "
                  f"sampling rate: 1/{self.sampling_rate}")
    
    def consume(self):
        """Consume item from buffer."""
        if self.buffer:
            return self.buffer.pop(0)
        return None

# Usage: High-frequency sensor data
sensor_buffer = AdaptiveSamplingBackpressure(target_buffer_size=1000)

# Fast sensor (1000 samples/sec), slow consumer (100 samples/sec)
# Adaptive sampling keeps buffer bounded
```

## Think of It Like This
Imagine a busy restaurant kitchen during dinner rush.

**Without backpressure** (no communication): Waiters keep bringing orders to the kitchen at full speed (50 orders/hour). The kitchen can only cook 20 meals/hour. Orders pile up on the counter—100, 200, 300 orders stacked everywhere. Kitchen runs out of counter space, orders fall on the floor, chaos ensues. Eventually the kitchen is so overwhelmed it shuts down (out of memory crash).

**With backpressure** (kitchen signals "slow down"): When the kitchen has 30 orders queued, the head chef tells the front desk "We're backed up, slow down seating new customers." Front desk waits 5 minutes between seating parties. Kitchen catches up, signals "ready for normal pace again." Restaurant stays orderly, customers wait longer to be seated but actually get their food.

**Reject strategy**: Front desk says "No more reservations tonight, we're fully booked" (reject new requests when capacity reached).

**Drop oldest strategy**: Kitchen tosses old tickets that have been waiting too long (drop old data, keep processing fresh).

**Pull-based strategy**: Kitchen calls to the front "send next order" only when ready (consumer controls rate).

Backpressure gives your agent system that kitchen feedback loop—allowing slow components to signal "I'm overwhelmed, please slow down" before catastrophic failure.

## The "So What?" Factor
**If you implement backpressure properly:**
- No out-of-memory crashes (bounded buffers)
- System gracefully handles overload
- Cascading failures prevented
- Predictable resource usage
- Fast components don't overwhelm slow ones
- Can operate at sustainable rate indefinitely
- Clear feedback when system overloaded
- Automatic adaptation to consumer capacity
- Retry storms avoided (reject vs queue forever)
- Cost-controlled (don't buffer infinite data)

**If you skip backpressure:**
- Out-of-memory crashes under load
- Cascading failures (one slow consumer affects all)
- Unpredictable resource consumption
- Fast producers overwhelm slow consumers
- Buffer growth until system failure
- No way to detect overload until crash
- Retry storms amplify problems
- Latency becomes unbounded (deep queues)
- System appears to work until catastrophic failure
- Cannot operate reliably at scale

## Practical Checklist
Before deploying systems with producer/consumer patterns:
- [ ] Have you identified all producer-consumer boundaries?
- [ ] Are buffers bounded (max size limits)?
- [ ] Do producers respect consumer capacity signals?
- [ ] Is backpressure propagated across system boundaries?
- [ ] Are rejection strategies defined (HTTP 429, queue full)?
- [ ] Do you monitor buffer depths and consumer lag?
- [ ] Is there graceful degradation when overloaded (not crashes)?
- [ ] Are pull-based patterns used where appropriate?
- [ ] Do streaming endpoints have natural flow control?
- [ ] Are rate limiters coordinated with backpressure?
- [ ] Have you tested with mismatched producer/consumer rates?
- [ ] Are backpressure signals observable (metrics, logs)?
- [ ] Can you tune high/low water marks for your workload?

## Watch Out For
⚠️ **Unbounded Buffers**: Any buffer without a size limit eventually causes OOM. Always set maxsize.

⚠️ **Backpressure Not Propagated**: Applying backpressure at one layer but not others. Must propagate through entire chain.

⚠️ **Deadlock with Circular Dependencies**: System A waits for B, B waits for A, both applying backpressure. Need timeout or circuit breaking.

⚠️ **High/Low Water Marks Too Close**: Hysteresis too small causes rapid oscillation (on/off/on/off). Need reasonable gap (e.g., 80%/50%).

⚠️ **Blocking Forever**: Producer blocks waiting for consumer with no timeout. System hangs if consumer dies.

⚠️ **Ignoring Backpressure Signals**: Producer receives 429 but immediately retries. Must respect retry-after headers and backoff.

⚠️ **Memory Leaks in "Bounded" Buffers**: Buffer item size grows over time (unbounded item size). Need memory limits, not just item count.

⚠️ **No Observability**: Can't see when backpressure activating or buffer depths. Must monitor queue sizes and consumer lag.

⚠️ **Losing Critical Data**: Using drop strategy for data that must not be lost (financial transactions). Drop only acceptable for lossy data.

⚠️ **TCP Buffer Hiding Problems**: TCP flow control masks application-level backpressure needs. Monitor application buffers, not just network.

## Connections
**Builds On:**
- Queue data structures
- Async programming patterns
- TCP flow control concepts
- Producer-consumer pattern

**Works With:**
- [request_queuing](request_queuing.md) - Queues implement backpressure via bounded size
- [streaming_responses](streaming_responses.md) - Streaming has natural backpressure via TCP flow control
- [concurrency_control](concurrency_control.md) - Semaphores limit concurrent work (form of backpressure)
- [idempotency](idempotency.md) - Rejecting with backpressure requires idempotent retry
- Rate limiting (applies backpressure to prevent overload)
- Load balancing (distributes load when backpressure activates)

**Leads To:**
- Adaptive rate limiting
- Circuit breaker patterns
- Bulkhead isolation
- Graceful degradation strategies
- Auto-scaling based on backpressure signals

**Related Patterns:**
- [caching](../Data_and_Retrieval_Patterns/caching.md) - Reduces load, less backpressure needed
- Reactive streams (standardized backpressure)
- Flow control in networking
- Token bucket rate limiting
- Load shedding

## Quick Decision Guide
**Use bounded queues when:**
- Want natural backpressure (producer blocks when full)
- Can tolerate producer pausing
- Need simplicity (asyncio.Queue handles it)
- Single-threaded or single-process

**Use reject strategy when:**
- Need fast failure feedback
- Client can retry with backoff
- Want clear overload signal (HTTP 429)
- Cannot block producer

**Use drop-oldest strategy when:**
- Data is lossy (metrics, logs, sensor data)
- Latest data more valuable than old
- Cannot block or reject
- Real-time constraints

**Use pull-based when:**
- Consumer controls rate naturally
- Processing time highly variable
- Want perfect flow matching
- Can refactor to pull model

**Use adaptive sampling when:**
- Can reduce data fidelity
- Volume more important than precision
- Time-series or streaming data
- Consumer capacity varies

**Use explicit signaling when:**
- Need producer awareness
- Can adjust production rate
- Multiple consumers with different rates
- Want observable backpressure events

## Further Exploration
- 📖 **Reactive Streams Specification** - Standardized backpressure protocol
- 🎯 **Implement Bounded Queue System** - Build producer/consumer with monitoring, test OOM without backpressure
- 💡 **Test TCP Flow Control** - Stream large response, throttle client, observe server buffering
- 📖 **"Reactive Design Patterns" by Kuhn & Hanafee** - Chapter on flow control
- 🎯 **RxPY with Backpressure** - Reactive extensions for Python with backpressure operators
- 💡 **HTTP/2 Flow Control** - Study window-based flow control in HTTP/2 streams
- 📖 **Kafka Consumer Lag** - How Kafka implements backpressure for stream processing
- 🎯 **Implement Adaptive Sampling** - Build system that downsamples when consumer lags
- 💡 **Monitor Buffer Depths** - Add metrics for queue sizes, consumer lag, backpressure activation
- 📖 **"Designing Data-Intensive Applications" by Kleppmann** - Chapter 11 on stream processing

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
