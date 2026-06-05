# Graceful Shutdown

## At a Glance
| | |
|---|---|
| **Category** | Operational Pattern / Reliability |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 hours for fundamentals, weeks for distributed coordination |
| **Prerequisites** | Understanding of signals, async programming, resource management, system lifecycle |

## One-Sentence Summary
Graceful shutdown is the pattern of cleanly stopping a running system in response to termination signals—completing in-flight work, draining request queues, saving critical state, releasing resources, and notifying dependencies—transforming abrupt "kill -9" crashes that lose data and corrupt state into orderly shutdowns where every conversation completes, every transaction commits, and every resource releases properly before the process exits.

## Why This Matters to You
When you build AI agent systems in 2026, graceful shutdown is the difference between systems that lose user data during deployments and systems that maintain data integrity through routine operations. Without graceful shutdown, when your Kubernetes cluster scales down or you deploy a new version, running agent conversations terminate mid-sentence—users lose context, database transactions rollback, streaming responses cut off, GPU memory leaks accumulate, and conversation history corrupts. With graceful shutdown, the same deployment waits for agent responses to complete (up to 30 seconds), saves conversation state to database, releases GPU allocations, completes streaming tokens, and only exits after confirming all work finished—users never notice the deployment happened. This matters at every operational event: deployments (10-50x per day in CI/CD), auto-scaling (pod terminations during scale-down), node replacements (hardware maintenance), crash recovery (OOM or panic), and manual restarts (configuration changes). At production scale serving 10,000+ concurrent users, abrupt terminations cause: lost conversations requiring expensive recovery ($50+ support time per incident × 100 incidents/month = $5000/month), corrupted database records (partial writes, orphaned locks), resource leaks (GPU memory accumulates until node restart), poor user experience (mid-conversation disconnects), and data loss (unsaved agent state, cached results). Graceful shutdown prevents this using signal handlers (catch SIGTERM, trigger cleanup), drain phases (stop accepting new work, complete existing), timeout enforcement (force exit after 30s), state persistence (save to durable storage), and resource cleanup (close connections, release locks). This matters economically: a single corrupted database state can require hours of manual recovery; GPU memory leaks force expensive node restarts; poor deployment UX loses customers. But graceful shutdown adds complexity: must coordinate multiple components (web server, queue workers, database), handle timeouts (some work won't finish), propagate signals (parent → child processes), and test scenarios (normal shutdown, timeout, signal during startup). Understanding shutdown lifecycle (receive signal → stop accepting work → drain queues → save state → release resources → exit), implementation patterns (signal handlers, async cleanup, timeout context), coordination strategies (health checks, connection draining, graceful termination propagation), and testing approaches (chaos engineering, timeout scenarios) determines whether your agent system handles routine operations reliably or creates data loss incidents every deployment. In 2026, with continuous deployment, auto-scaling, and distributed agent systems, graceful shutdown is not optional—it's foundational operational hygiene.

## The Core Idea
### What It Is
Graceful shutdown is the controlled termination of a running process or system in response to shutdown signals (SIGTERM, SIGINT), ensuring all in-flight work completes, critical state persists, and resources release properly before the process exits. It contrasts with abrupt termination (SIGKILL) which immediately stops execution without cleanup.

**The Problem: Abrupt Termination**

```python
# What happens WITHOUT graceful shutdown:

# Server running with 100 active requests
# User deploys new version: kubectl rollout restart

# Kubernetes sends SIGTERM → process ignores signal
# Waits 30 seconds → sends SIGKILL (force kill)

# Result:
# ❌ 100 requests fail with connection errors
# ❌ Database transactions rollback
# ❌ Agent conversation state lost (unsaved to DB)
# ❌ GPU memory not released (leak)
# ❌ Streaming responses cut off mid-token
# ❌ Queue messages lost (not acknowledged)
# ❌ File handles not closed (possible corruption)
# ❌ Connection pool not drained (orphaned connections)
```

**Solution: Graceful Shutdown Lifecycle**

```
1. RECEIVE SIGNAL
   └─> SIGTERM (polite request to shutdown)
   └─> SIGINT (Ctrl+C from terminal)

2. STOP ACCEPTING NEW WORK
   └─> Mark health check as unhealthy
   └─> Stop accepting new HTTP requests
   └─> Pause queue consumption

3. DRAIN IN-FLIGHT WORK
   └─> Complete active requests (with timeout)
   └─> Process remaining queue items
   └─> Finish database transactions

4. SAVE CRITICAL STATE
   └─> Persist agent conversation state
   └─> Flush caches to durable storage
   └─> Save partial computation results

5. RELEASE RESOURCES
   └─> Close database connections
   └─> Release GPU memory
   └─> Acknowledge queue messages
   └─> Close file handles

6. EXIT CLEANLY
   └─> Return exit code 0 (success)
   └─> Log shutdown completion
```

**Example 1: Basic Signal Handling**

```python
import signal
import sys
import time

class GracefulShutdownHandler:
    """
    Handle shutdown signals gracefully.
    
    Catches SIGTERM/SIGINT, triggers cleanup, exits cleanly.
    """
    
    def __init__(self):
        self.shutdown_requested = False
        self.active_requests = 0
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """
        Handle shutdown signal.
        
        Called when SIGTERM or SIGINT received.
        """
        signal_name = "SIGTERM" if signum == signal.SIGTERM else "SIGINT"
        print(f"\n⚠️  Received {signal_name}, initiating graceful shutdown...")
        
        self.shutdown_requested = True
    
    def should_continue(self) -> bool:
        """Check if should continue processing."""
        return not self.shutdown_requested
    
    def wait_for_completion(self, timeout: int = 30):
        """
        Wait for in-flight work to complete.
        
        Args:
            timeout: Maximum seconds to wait
        """
        start_time = time.time()
        
        while self.active_requests > 0:
            elapsed = time.time() - start_time
            
            if elapsed > timeout:
                print(f"⏱️  Timeout reached ({timeout}s), "
                      f"{self.active_requests} requests still active")
                break
            
            print(f"⏳ Waiting for {self.active_requests} active requests "
                  f"({elapsed:.1f}s elapsed)...")
            time.sleep(1)
        
        if self.active_requests == 0:
            print("✓ All requests completed")
        else:
            print(f"⚠️  Forcing shutdown with {self.active_requests} active requests")

# Usage
shutdown_handler = GracefulShutdownHandler()

def process_request(request_id: int):
    """Process request with graceful shutdown support."""
    shutdown_handler.active_requests += 1
    
    try:
        print(f"Processing request {request_id}...")
        time.sleep(5)  # Simulate work
        print(f"Completed request {request_id}")
    finally:
        shutdown_handler.active_requests -= 1

# Main loop
try:
    request_id = 0
    while shutdown_handler.should_continue():
        process_request(request_id)
        request_id += 1
        time.sleep(1)

except KeyboardInterrupt:
    pass

# Graceful shutdown
print("\n🛑 Shutdown initiated")
shutdown_handler.wait_for_completion(timeout=30)
print("👋 Exiting cleanly")
sys.exit(0)

# Test: Run this, press Ctrl+C during processing
# Output:
# Processing request 3...
# ⚠️  Received SIGINT, initiating graceful shutdown...
# Completed request 3
# 🛑 Shutdown initiated
# ✓ All requests completed
# 👋 Exiting cleanly
```

**Example 2: Web Server Graceful Shutdown**

```python
from fastapi import FastAPI
import asyncio
import signal
import uvicorn
from contextlib import asynccontextmanager

class AgentServer:
    """
    Agent server with graceful shutdown.
    
    Completes in-flight requests before shutdown.
    """
    
    def __init__(self):
        self.app = FastAPI(lifespan=self.lifespan)
        self.active_requests = set()
        self.shutdown_event = asyncio.Event()
        
        # Routes
        self.app.post("/agent/query")(self.handle_query)
        self.app.get("/health")(self.health_check)
    
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """
        Application lifespan (startup and shutdown).
        
        FastAPI's recommended way to handle lifecycle.
        """
        # Startup
        print("🚀 Server starting...")
        
        yield  # Server runs
        
        # Shutdown
        print("🛑 Server shutting down...")
        await self.graceful_shutdown()
    
    async def handle_query(self, query: dict):
        """
        Handle agent query with tracking.
        
        Track request for graceful shutdown.
        """
        request_id = query.get("request_id", "unknown")
        
        # Track request
        self.active_requests.add(request_id)
        
        try:
            print(f"Processing query {request_id}...")
            
            # Simulate agent processing
            await asyncio.sleep(10)
            
            return {
                "request_id": request_id,
                "response": "Agent response here"
            }
        
        finally:
            self.active_requests.discard(request_id)
            print(f"Completed query {request_id}")
    
    async def health_check(self):
        """
        Health check endpoint.
        
        Returns unhealthy during shutdown (load balancer stops routing).
        """
        if self.shutdown_event.is_set():
            return {"status": "shutting_down"}, 503
        
        return {"status": "healthy"}
    
    async def graceful_shutdown(self, timeout: int = 30):
        """
        Graceful shutdown process.
        
        1. Mark unhealthy (stop new traffic)
        2. Wait for active requests
        3. Force exit after timeout
        """
        print("⚠️  Graceful shutdown initiated")
        
        # Mark unhealthy (load balancer stops sending traffic)
        self.shutdown_event.set()
        print("🔴 Health check marked unhealthy")
        
        # Wait for active requests
        start_time = asyncio.get_event_loop().time()
        
        while self.active_requests:
            elapsed = asyncio.get_event_loop().time() - start_time
            
            if elapsed > timeout:
                print(f"⏱️  Timeout reached, {len(self.active_requests)} requests remaining")
                break
            
            print(f"⏳ Waiting for {len(self.active_requests)} active requests...")
            await asyncio.sleep(1)
        
        if not self.active_requests:
            print("✓ All requests completed")
        
        print("👋 Shutdown complete")

# Run server
server = AgentServer()

# uvicorn will handle SIGTERM automatically with lifespan
# uvicorn main:server.app --host 0.0.0.0 --port 8000

# When Kubernetes sends SIGTERM:
# 1. Health check returns 503 (load balancer stops traffic)
# 2. Active requests complete (up to 30s)
# 3. Server exits cleanly
```

**Example 3: Queue Worker Graceful Shutdown**

```python
import asyncio
import signal
from typing import Optional

class GracefulQueueWorker:
    """
    Queue worker with graceful shutdown.
    
    Drains queue before stopping.
    """
    
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self.running = False
        self.shutdown_event = asyncio.Event()
        self.active_task: Optional[asyncio.Task] = None
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signal."""
        print("\n⚠️  Shutdown signal received")
        self.shutdown_event.set()
    
    async def process_message(self, message: dict):
        """
        Process queue message.
        
        Simulates agent task processing.
        """
        print(f"Processing message: {message}")
        await asyncio.sleep(5)  # Simulate work
        print(f"Completed message: {message}")
    
    async def run(self, drain_timeout: int = 30):
        """
        Run worker with graceful shutdown.
        
        1. Process queue messages
        2. On shutdown signal, stop accepting new messages
        3. Drain remaining messages (with timeout)
        4. Exit cleanly
        """
        self.running = True
        print("🚀 Queue worker started")
        
        try:
            while not self.shutdown_event.is_set():
                try:
                    # Wait for message with timeout (check shutdown signal)
                    message = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=1.0
                    )
                    
                    # Process message
                    self.active_task = asyncio.create_task(
                        self.process_message(message)
                    )
                    await self.active_task
                    
                    # Mark task done
                    self.queue.task_done()
                    
                except asyncio.TimeoutError:
                    continue  # Check shutdown signal
        
        except asyncio.CancelledError:
            print("⚠️  Worker cancelled")
        
        # Graceful shutdown: drain queue
        print(f"\n🛑 Draining queue ({self.queue.qsize()} messages remaining)...")
        
        start_time = asyncio.get_event_loop().time()
        
        while not self.queue.empty():
            elapsed = asyncio.get_event_loop().time() - start_time
            
            if elapsed > drain_timeout:
                print(f"⏱️  Drain timeout ({drain_timeout}s), "
                      f"{self.queue.qsize()} messages remaining")
                break
            
            try:
                message = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                await self.process_message(message)
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue
        
        if self.queue.empty():
            print("✓ Queue drained successfully")
        else:
            print(f"⚠️  {self.queue.qsize()} messages not processed")
        
        print("👋 Worker shutdown complete")

# Usage
async def main():
    queue = asyncio.Queue()
    
    # Add messages to queue
    for i in range(10):
        await queue.put({"id": i, "data": f"task_{i}"})
    
    # Start worker
    worker = GracefulQueueWorker(queue)
    
    # Run worker (Ctrl+C to trigger shutdown)
    await worker.run(drain_timeout=30)

# asyncio.run(main())

# Test: Run and press Ctrl+C after a few messages
# Output:
# 🚀 Queue worker started
# Processing message: {'id': 0, 'data': 'task_0'}
# Completed message: {'id': 0, 'data': 'task_0'}
# Processing message: {'id': 1, 'data': 'task_1'}
# ⚠️  Shutdown signal received
# Completed message: {'id': 1, 'data': 'task_1'}
# 🛑 Draining queue (8 messages remaining)...
# Processing message: {'id': 2, 'data': 'task_2'}
# ... (drains remaining messages)
# ✓ Queue drained successfully
# 👋 Worker shutdown complete
```

**Example 4: Multi-Component Shutdown Coordination**

```python
import asyncio
import signal
from typing import List, Callable

class ShutdownCoordinator:
    """
    Coordinate graceful shutdown across multiple components.
    
    Pattern: Register cleanup functions, execute in order during shutdown.
    """
    
    def __init__(self):
        self.cleanup_functions: List[tuple[str, Callable]] = []
        self.shutdown_event = asyncio.Event()
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signal."""
        self.shutdown_event.set()
    
    def register_cleanup(self, name: str, cleanup_fn: Callable):
        """
        Register cleanup function.
        
        Functions executed in reverse order (last registered, first executed).
        """
        self.cleanup_functions.append((name, cleanup_fn))
        print(f"✓ Registered cleanup: {name}")
    
    async def wait_for_shutdown(self):
        """Wait for shutdown signal."""
        await self.shutdown_event.wait()
    
    async def cleanup(self, timeout: int = 30):
        """
        Execute all cleanup functions.
        
        Runs in reverse order with per-component timeout.
        """
        print("\n🛑 Executing graceful shutdown...")
        
        # Execute in reverse order
        for name, cleanup_fn in reversed(self.cleanup_functions):
            print(f"⏳ Cleaning up: {name}...")
            
            try:
                # Execute with timeout
                await asyncio.wait_for(
                    cleanup_fn(),
                    timeout=timeout
                )
                print(f"✓ Cleaned up: {name}")
            
            except asyncio.TimeoutError:
                print(f"⏱️  Timeout cleaning up: {name}")
            
            except Exception as e:
                print(f"❌ Error cleaning up {name}: {e}")
        
        print("👋 Shutdown complete")

# Usage: Agent system with multiple components
async def main():
    coordinator = ShutdownCoordinator()
    
    # Component 1: Web server
    async def cleanup_web_server():
        print("  - Marking health check unhealthy")
        await asyncio.sleep(1)
        print("  - Completing active requests")
        await asyncio.sleep(2)
        print("  - Closing HTTP connections")
    
    coordinator.register_cleanup("Web Server", cleanup_web_server)
    
    # Component 2: Queue workers
    async def cleanup_queue_workers():
        print("  - Stopping queue consumption")
        await asyncio.sleep(1)
        print("  - Draining pending messages")
        await asyncio.sleep(3)
        print("  - Acknowledging final messages")
    
    coordinator.register_cleanup("Queue Workers", cleanup_queue_workers)
    
    # Component 3: Database connections
    async def cleanup_database():
        print("  - Committing pending transactions")
        await asyncio.sleep(1)
        print("  - Closing connection pool")
    
    coordinator.register_cleanup("Database", cleanup_database)
    
    # Component 4: GPU resources
    async def cleanup_gpu():
        print("  - Releasing GPU memory")
        await asyncio.sleep(1)
        print("  - Clearing CUDA cache")
    
    coordinator.register_cleanup("GPU Resources", cleanup_gpu)
    
    # Component 5: Agent state
    async def save_agent_state():
        print("  - Saving conversation state to DB")
        await asyncio.sleep(2)
        print("  - Flushing caches")
    
    coordinator.register_cleanup("Agent State", save_agent_state)
    
    print("\n🚀 System running (press Ctrl+C to shutdown)...")
    
    # Wait for shutdown signal
    await coordinator.wait_for_shutdown()
    
    # Execute coordinated cleanup
    await coordinator.cleanup(timeout=10)

# asyncio.run(main())

# Output when pressing Ctrl+C:
# 🚀 System running (press Ctrl+C to shutdown)...
# ^C
# 🛑 Executing graceful shutdown...
# ⏳ Cleaning up: Agent State...
#   - Saving conversation state to DB
#   - Flushing caches
# ✓ Cleaned up: Agent State
# ⏳ Cleaning up: GPU Resources...
#   - Releasing GPU memory
#   - Clearing CUDA cache
# ✓ Cleaned up: GPU Resources
# ⏳ Cleaning up: Database...
#   - Committing pending transactions
#   - Closing connection pool
# ✓ Cleaned up: Database
# ⏳ Cleaning up: Queue Workers...
#   - Stopping queue consumption
#   - Draining pending messages
#   - Acknowledging final messages
# ✓ Cleaned up: Queue Workers
# ⏳ Cleaning up: Web Server...
#   - Marking health check unhealthy
#   - Completing active requests
#   - Closing HTTP connections
# ✓ Cleaned up: Web Server
# 👋 Shutdown complete
```

**Example 5: Kubernetes Deployment with Graceful Shutdown**

```yaml
# Kubernetes deployment with proper shutdown configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: agent
        image: agent-server:latest
        
        # Graceful shutdown configuration
        lifecycle:
          preStop:
            exec:
              # Optional: Custom pre-stop hook
              # Runs before SIGTERM sent
              command: ["/bin/sh", "-c", "sleep 5"]
        
        # Readiness probe (load balancer uses this)
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        
        # Liveness probe
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
      
      # Graceful shutdown timeout
      terminationGracePeriodSeconds: 30  # Wait up to 30s before SIGKILL

# Shutdown sequence:
# 1. Pod marked for termination
# 2. Removed from Service endpoints (no new traffic)
# 3. preStop hook runs (optional delay for load balancer propagation)
# 4. SIGTERM sent to container
# 5. Application drains requests (up to 30s)
# 6. SIGKILL sent if still running after 30s
```

### What It Isn't
Graceful shutdown is not **the same as auto-restart**. Graceful shutdown is clean termination; auto-restart is starting new instance after crash.

It's not **guaranteed to complete**. Timeout may expire before work finishes—must handle force termination.

Graceful shutdown is not **only about signals**. Also includes: connection draining, state persistence, resource cleanup, dependency notification.

It's not **zero downtime**. Work completes, but new work may be rejected during drain period. (Zero downtime requires additional deployment strategies.)

Finally, graceful shutdown is not **optional in production**. Without it, every deployment causes data loss and resource leaks.

## How It Works

### Production Shutdown Patterns

**Pattern 1: Connection Draining (Load Balancer Coordination)**

```python
import asyncio
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class ConnectionDrainingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for connection draining.
    
    Rejects new connections during shutdown.
    """
    
    def __init__(self, app, health_checker):
        super().__init__(app)
        self.health_checker = health_checker
    
    async def dispatch(self, request: Request, call_next):
        # Reject new requests during shutdown
        if self.health_checker.is_shutting_down():
            return {
                "error": "Server shutting down",
                "retry_after": 5
            }, 503
        
        # Process request normally
        return await call_next(request)

class HealthChecker:
    """Health check with shutdown awareness."""
    
    def __init__(self):
        self.shutting_down = False
    
    def is_shutting_down(self) -> bool:
        return self.shutting_down
    
    def mark_shutting_down(self):
        """Mark as shutting down (health check fails, load balancer stops traffic)."""
        self.shutting_down = True

# Setup
health = HealthChecker()
app = FastAPI()
app.add_middleware(ConnectionDrainingMiddleware, health_checker=health)

@app.get("/health")
async def health_check():
    if health.is_shutting_down():
        return {"status": "shutting_down"}, 503
    return {"status": "healthy"}

# On shutdown:
# 1. health.mark_shutting_down()
# 2. Load balancer stops routing (sees 503)
# 3. Complete existing connections
# 4. Exit
```

**Pattern 2: Timeout Enforcement**

```python
async def graceful_shutdown_with_timeout(
    cleanup_fn: Callable,
    timeout: int = 30
):
    """
    Execute graceful shutdown with timeout.
    
    If cleanup doesn't finish, force exit.
    """
    print(f"⏳ Starting graceful shutdown (timeout: {timeout}s)...")
    
    try:
        await asyncio.wait_for(cleanup_fn(), timeout=timeout)
        print("✓ Graceful shutdown completed")
        exit(0)
    
    except asyncio.TimeoutError:
        print(f"⏱️  Graceful shutdown timeout ({timeout}s), forcing exit")
        exit(1)  # Non-zero exit code indicates forced shutdown
```

## Think of It Like This
Imagine a restaurant at closing time.

**Abrupt shutdown** (turn off lights immediately): Clock hits 10pm, owner flips main breaker. Lights go out, kitchen stops mid-meal, customers eating dessert left in dark, half-cooked food ruined, cash register drawer still open, back door unlocked. Chaos, food wasted, customers angry, unsafe closing.

**Graceful shutdown**: Clock hits 10pm, owner announces "Last call, no new orders." Staff locks front door (no new customers), completes meals for diners already seated (in-flight work), processes final payments, cleans kitchen, secures cash register, locks all doors, confirms everyone out safely. Takes 30 minutes but everything clean, safe, and ready for tomorrow.

**Timeout enforcement**: If kitchen still cooking at 10:45pm (15 minutes past closing), owner says "Sorry, we must leave now" and forces close (some food wasted, but can't stay all night).

**Connection draining**: Put "Closed" sign at 9:45pm so new customers don't enter. Serve diners already inside. At 10pm, no new arrivals and fewer people to finish serving.

Graceful shutdown gives your agent system that orderly closing—completing work in progress, securing resources, and leaving system in consistent state before exiting.

## The "So What?" Factor
**If you implement graceful shutdown properly:**
- No data loss during deployments
- Database stays consistent (transactions complete)
- Users don't notice deployments
- Resources release properly (no leaks)
- Conversation state persists correctly
- Queue messages acknowledged (no duplicates)
- Clean logs (orderly shutdown, not crash)
- Can deploy 50+ times/day safely
- Auto-scaling works reliably
- Zero-downtime deployments possible (with orchestration)

**If you skip graceful shutdown:**
- Data loss every deployment
- Corrupted database state
- Users see mid-conversation disconnects
- GPU memory leaks accumulate
- Queue message duplication (not acknowledged)
- Crash logs (looks like system failure)
- Cannot deploy frequently (too risky)
- Auto-scaling causes data loss
- Support burden from lost work
- Production incidents from routine operations

## Practical Checklist
Before deploying to production:
- [ ] Do you handle SIGTERM and SIGINT signals?
- [ ] Does health check return 503 during shutdown?
- [ ] Are in-flight requests tracked and completed?
- [ ] Is there a timeout for shutdown (typically 30s)?
- [ ] Are database transactions committed before exit?
- [ ] Are queue messages acknowledged properly?
- [ ] Is agent conversation state saved?
- [ ] Are GPU resources released?
- [ ] Are file handles closed?
- [ ] Are connection pools drained?
- [ ] Do logs clearly show shutdown phases?
- [ ] Is terminationGracePeriodSeconds set in Kubernetes?
- [ ] Have you tested shutdown under load?
- [ ] Is there monitoring for shutdown timeouts?
- [ ] Are cleanup functions coordinated in correct order?

## Watch Out For
⚠️ **Ignoring SIGTERM**: Not handling signals means SIGKILL after timeout (abrupt termination).

⚠️ **Timeout Too Short**: Work doesn't finish before force kill. Increase terminationGracePeriodSeconds.

⚠️ **Timeout Too Long**: Slow deployments. Balance completion vs deployment speed.

⚠️ **No Health Check Coordination**: Load balancer sends traffic during shutdown. Mark unhealthy immediately.

⚠️ **Blocking Shutdown**: Infinite wait for work to complete (no timeout). Always enforce timeout.

⚠️ **Not Saving State**: Agent conversation lost. Persist critical state early in shutdown.

⚠️ **Resource Leak on Timeout**: If shutdown times out, resources not released. Need cleanup even on force exit.

⚠️ **Signal Handling in Threads**: Signals only delivered to main thread. Use threading.Event for coordination.

⚠️ **Multiple Signal Handlers**: Registering multiple handlers can cause conflicts. Use single coordinator.

⚠️ **Deadlock During Shutdown**: Cleanup code waits for lock never released. Timeout per cleanup phase.

## Connections
**Builds On:**
- Unix signals (SIGTERM, SIGINT, SIGKILL)
- Async programming patterns
- Resource management
- System lifecycle

**Works With:**
- [request_queuing](request_queuing.md) - Drain queues during shutdown
- [streaming_responses](streaming_responses.md) - Complete streams before exit
- [concurrency_control](concurrency_control.md) - Release locks during shutdown
- [idempotency](idempotency.md) - Failed shutdowns can retry safely if idempotent
- [backpressure](backpressure.md) - Stop accepting work during drain phase
- [batching](batching.md) - Complete batches before exit
- Health checks (mark unhealthy during shutdown)
- Load balancing (connection draining)

**Leads To:**
- Zero-downtime deployments
- Blue-green deployments
- Rolling updates
- Chaos engineering patterns
- Self-healing systems

**Related Patterns:**
- Circuit breakers (fail fast instead of waiting)
- Retry mechanisms (handle shutdown-related failures)
- State persistence strategies
- Connection pooling (drain pools)
- Kubernetes lifecycle hooks

## Quick Decision Guide
**Handle signals when:**
- Running in production (always)
- Deploying via Kubernetes, Docker
- Using auto-scaling
- Processing critical data
- Managing stateful resources

**Set timeout based on:**
- Longest typical request time
- Database transaction duration
- Queue drain time
- State persistence time
- Balance: completion vs deployment speed

**Typical timeouts:**
- Interactive web services: 30s
- Background workers: 60-120s
- Batch processors: 300s (5 min)
- Emergency shutdown: 10s

**Coordinate shutdown when:**
- Multiple components (web + worker + DB)
- Shared resources (connection pools)
- Dependent services (notify consumers)
- Stateful operations (save before exit)

**Test shutdown by:**
- Send SIGTERM during processing
- Kill pod during high load
- Simulate timeout scenarios
- Verify state persistence
- Check resource cleanup

## Further Exploration
- 📖 **"Kubernetes Best Practices" by Burns & Villalba** - Chapter on pod lifecycle
- 🎯 **Implement Graceful Shutdown** - Add signal handling to your agent server
- 💡 **Test Deployment Scenarios** - Kill pods during load, verify no data loss
- 📖 **Unix Signal Handling** - Deep dive into SIGTERM, SIGINT, SIGKILL
- 🎯 **Connection Draining Patterns** - Study nginx, envoy, haproxy connection management
- 💡 **Chaos Engineering** - Use tools like chaos-monkey to test shutdown reliability
- 📖 **"Site Reliability Engineering" by Google** - Chapter on graceful degradation
- 🎯 **Kubernetes PreStop Hooks** - Study lifecycle hooks for coordinated shutdown
- 💡 **Monitor Shutdown Metrics** - Track: shutdown duration, completion rate, timeout frequency
- 📖 **Zero-Downtime Deployment Strategies** - Rolling updates, blue-green, canary

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
