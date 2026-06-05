# Health Checks

## At a Glance
| | |
|---|---|
| **Category** | Operational Pattern / Monitoring |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 2-4 hours for fundamentals, days for production patterns |
| **Prerequisites** | HTTP basics, system monitoring concepts, understanding of distributed systems |

## One-Sentence Summary
Health checks are automated diagnostic endpoints or mechanisms that external systems (load balancers, orchestrators, monitoring tools) query periodically to determine if a service instance is alive, ready to handle traffic, and functioning correctly—enabling automatic traffic routing, self-healing, and preventing requests from being sent to degraded instances that would fail or timeout.

## Why This Matters to You
When you build AI agent systems in 2026, health checks are the difference between systems that automatically recover from failures and systems where every minor issue requires manual intervention and causes user-facing outages. Without health checks, when one of your agent server pods crashes or becomes overloaded, the load balancer continues sending traffic to it—users see timeouts and 500 errors, response times spike from 500ms to 30+ seconds, cascading failures spread as retry storms overwhelm remaining servers, and you get paged at 3am to manually remove the failed instance. With health checks, the load balancer detects the unhealthy instance within 5-10 seconds, stops routing traffic automatically, Kubernetes restarts the failed pod, and the system self-heals without user impact or human intervention—no one gets paged, users experience no degradation, and your agent system maintains 99.9%+ uptime. This matters at every operational event: pod crashes (hardware failures, OOM kills, bugs), overload conditions (traffic spikes, slow dependencies), startup delays (model loading takes 30-60 seconds), rolling deployments (gradual traffic shift), database failures (dependency unavailable), and transient errors (temporary network issues). At production scale serving 10,000+ requests/second across 50+ agent pods, health checks enable: automatic failover (unhealthy pods removed in 5-10s), zero-downtime deployments (readiness checks prevent traffic to not-ready pods), auto-scaling reliability (new pods don't receive traffic until ready), cascade failure prevention (detect overload before total failure), and self-healing infrastructure (Kubernetes restarts unhealthy pods automatically). This matters economically: without health checks, a single pod crash affects 2% of traffic (1/50 pods) for minutes until manual intervention—at 10k requests/sec that's 200 requests/sec failing = 12,000 failed requests/minute × $0.50 support cost = $6,000 in support burden per incident × 10 incidents/month = $60k/month operational burden. With health checks, same pod crash detected in 10 seconds, automatic removal, 200 failed requests total × $0.50 = $100 impact (vs $6000). But health checks add complexity: must implement endpoints (HTTP /health, /ready), tune timing parameters (check interval, timeout, failure threshold), handle startup delays (models loading), check dependencies appropriately (database, cache), avoid false positives (temporary errors shouldn't mark unhealthy), and coordinate with graceful shutdown (fail health checks during drain). Understanding health check types (liveness vs readiness vs startup), implementation patterns (shallow vs deep checks), timing configuration (interval, timeout, threshold), dependency checking strategies (fail fast vs graceful degradation), and production coordination (load balancer, Kubernetes, monitoring) determines whether your agent system self-heals automatically or requires constant manual intervention to maintain uptime.

## The Core Idea
### What It Is
Health checks are automated diagnostic mechanisms—typically HTTP endpoints like `/health` or `/ready`—that external systems query periodically to assess whether a service instance is functioning correctly and capable of handling traffic. They return simple success/failure signals used for traffic routing and recovery decisions.

**The Problem: Traffic to Failed Instances**

```python
# WITHOUT health checks:

# Scenario: 3 agent server pods behind load balancer
# Pod 1: Healthy (responding in 500ms)
# Pod 2: Crashed (OOM kill)
# Pod 3: Healthy (responding in 500ms)

# Load balancer has no health information
# Routes traffic evenly: 33% Pod 1, 33% Pod 2, 33% Pod 3

# Result:
# ❌ 33% of requests sent to crashed Pod 2 (timeout after 30s)
# ❌ Users experience: 33% requests take 30+ seconds
# ❌ Retry storms (clients retry → more load)
# ❌ Cascading failures (retries overwhelm Pod 1, Pod 3)
# ❌ Manual intervention required (someone must remove Pod 2)
# ❌ Incident duration: Until someone notices and acts (minutes to hours)
```

**Solution: Automated Health Detection**

```
WITH health checks:

Load balancer checks /health every 5 seconds:
- GET http://pod1:8000/health → 200 OK ✓
- GET http://pod2:8000/health → timeout ✗
- GET http://pod3:8000/health → 200 OK ✓

After 2 consecutive failures (10 seconds):
- Pod 2 marked unhealthy
- Removed from rotation
- Traffic: 50% Pod 1, 50% Pod 3

Kubernetes detects Pod 2 unhealthy:
- Restarts pod
- New pod starts, loads model (30s)
- Health check passes
- Added back to rotation

Result:
✓ Failed requests: Only ~10 requests (during detection)
✓ User impact: Minimal (most retries succeed on healthy pods)
✓ Auto-recovery: Pod restarted automatically
✓ No manual intervention: System self-heals
✓ Incident duration: 10s detection + 30s restart = 40s total
```

**Example 1: Basic HTTP Health Check**

```python
from fastapi import FastAPI, Response
import time

app = FastAPI()

# Simple health check endpoint
@app.get("/health")
async def health_check():
    """
    Basic health check.
    
    Returns 200 if server running, 503 if not ready.
    """
    return {"status": "healthy", "timestamp": time.time()}

# Usage by load balancer:
# Every 5 seconds: GET http://server:8000/health
# Response 200 → healthy (route traffic)
# Response 503 or timeout → unhealthy (stop traffic)
```

**Example 2: Readiness vs Liveness Checks**

```python
from fastapi import FastAPI, Response
import asyncio

class AgentServerHealth:
    """
    Health check coordinator for agent server.
    
    Tracks startup, readiness, and liveness.
    """
    
    def __init__(self):
        self.startup_complete = False
        self.is_ready = False
        self.is_alive = True
        self.last_request_time = time.time()
    
    async def initialize(self):
        """
        Startup initialization.
        
        Simulates: load model, connect to database, warm cache.
        """
        print("🔄 Initializing server...")
        
        # Load AI model (30 seconds)
        print("  Loading model...")
        await asyncio.sleep(30)
        
        # Connect to database
        print("  Connecting to database...")
        await asyncio.sleep(2)
        
        # Warm cache
        print("  Warming cache...")
        await asyncio.sleep(3)
        
        self.startup_complete = True
        self.is_ready = True
        print("✓ Server ready")

app = FastAPI()
health = AgentServerHealth()

@app.on_event("startup")
async def startup():
    """Run initialization on startup."""
    await health.initialize()

@app.get("/health/startup")
async def startup_probe():
    """
    Startup probe (Kubernetes).
    
    Returns 200 only after initialization complete.
    Used during initial startup to delay liveness checks.
    """
    if health.startup_complete:
        return {"status": "started"}
    else:
        return Response(
            content='{"status": "starting"}',
            status_code=503
        )

@app.get("/health/ready")
async def readiness_probe():
    """
    Readiness probe (load balancer + Kubernetes).
    
    Returns 200 when ready to handle traffic.
    Returns 503 during:
    - Startup (not ready yet)
    - Overload (too many requests)
    - Graceful shutdown (draining)
    - Dependency failures (database down)
    """
    if not health.is_ready:
        return Response(
            content='{"status": "not_ready"}',
            status_code=503
        )
    
    return {"status": "ready"}

@app.get("/health/live")
async def liveness_probe():
    """
    Liveness probe (Kubernetes).
    
    Returns 200 if server is alive and functioning.
    Returns 503 if server is deadlocked, corrupted, or stuck.
    
    Kubernetes restarts pod if liveness fails.
    """
    if not health.is_alive:
        return Response(
            content='{"status": "dead"}',
            status_code=503
        )
    
    # Check if server is stuck (no requests in 60s = deadlock?)
    time_since_request = time.time() - health.last_request_time
    if time_since_request > 60:
        return Response(
            content='{"status": "possibly_stuck"}',
            status_code=503
        )
    
    return {"status": "alive"}

@app.post("/agent/query")
async def handle_query(query: dict):
    """
    Handle agent query.
    
    Update last_request_time for liveness check.
    """
    health.last_request_time = time.time()
    
    # Process query
    await asyncio.sleep(2)
    
    return {"response": "Agent response"}

# Kubernetes configuration:
# apiVersion: v1
# kind: Pod
# spec:
#   containers:
#   - name: agent-server
#     startupProbe:           # Check during startup
#       httpGet:
#         path: /health/startup
#         port: 8000
#       periodSeconds: 5      # Check every 5s
#       failureThreshold: 12  # Allow 60s (12 × 5s) for startup
#     
#     readinessProbe:         # Check if ready for traffic
#       httpGet:
#         path: /health/ready
#         port: 8000
#       periodSeconds: 5      # Check every 5s
#       failureThreshold: 2   # 2 failures = unhealthy (10s)
#     
#     livenessProbe:          # Check if alive
#       httpGet:
#         path: /health/live
#         port: 8000
#       periodSeconds: 10     # Check every 10s
#       failureThreshold: 3   # 3 failures = restart (30s)
```

**Three Types of Health Checks:**

1. **Startup Probe** (Kubernetes)
   - **Purpose**: Delay other checks until initialization complete
   - **Use case**: Model loading takes 30-60s
   - **Failure action**: Keep waiting (no restart)
   - **Typical timing**: Check every 5s, allow 60s total

2. **Readiness Probe** (Load Balancer + Kubernetes)
   - **Purpose**: Determine if ready to handle traffic
   - **Use case**: Temporary overload, dependencies down, graceful shutdown
   - **Failure action**: Remove from load balancer (stop traffic)
   - **Typical timing**: Check every 5s, 2 failures = unhealthy

3. **Liveness Probe** (Kubernetes)
   - **Purpose**: Detect if process is alive and functioning
   - **Use case**: Deadlock, memory corruption, infinite loop
   - **Failure action**: Restart pod (kill and restart)
   - **Typical timing**: Check every 10s, 3 failures = restart

**Example 3: Shallow vs Deep Health Checks**

```python
from fastapi import FastAPI
import httpx
import asyncio

class HealthChecker:
    """
    Health checker with shallow and deep modes.
    
    Shallow: Fast, basic checks (server responding)
    Deep: Comprehensive dependency checks
    """
    
    def __init__(self):
        self.db_client = None  # Placeholder for DB connection
        self.cache_client = None  # Placeholder for Redis
        self.model_loaded = True
    
    async def shallow_check(self) -> tuple[bool, dict]:
        """
        Shallow health check (fast).
        
        Only checks if server is responding.
        Used for high-frequency checks (every 5s).
        
        Returns: (healthy, details)
        """
        return True, {
            "type": "shallow",
            "status": "healthy",
            "checks": {
                "server": "responding"
            }
        }
    
    async def deep_check(self) -> tuple[bool, dict]:
        """
        Deep health check (comprehensive but slow).
        
        Checks all dependencies:
        - Database connection
        - Cache availability
        - Model loaded
        - External API reachable
        
        Used for monitoring dashboards, not load balancing.
        
        Returns: (healthy, details)
        """
        checks = {}
        overall_healthy = True
        
        # Check database
        try:
            # Simulate DB query
            await asyncio.sleep(0.1)  # Real: await db.execute("SELECT 1")
            checks["database"] = "healthy"
        except Exception as e:
            checks["database"] = f"unhealthy: {e}"
            overall_healthy = False
        
        # Check cache
        try:
            # Simulate cache ping
            await asyncio.sleep(0.05)  # Real: await cache.ping()
            checks["cache"] = "healthy"
        except Exception as e:
            checks["cache"] = f"unhealthy: {e}"
            # Cache failure doesn't mark overall unhealthy (degraded mode)
        
        # Check model
        if self.model_loaded:
            checks["model"] = "loaded"
        else:
            checks["model"] = "not_loaded"
            overall_healthy = False
        
        # Check external API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.openai.com/v1/models",
                    timeout=2.0
                )
                if response.status_code == 200:
                    checks["openai_api"] = "reachable"
                else:
                    checks["openai_api"] = f"status_{response.status_code}"
        except Exception as e:
            checks["openai_api"] = f"unreachable: {e}"
            # External API failure doesn't mark unhealthy (can degrade)
        
        return overall_healthy, {
            "type": "deep",
            "status": "healthy" if overall_healthy else "unhealthy",
            "checks": checks
        }

app = FastAPI()
health_checker = HealthChecker()

@app.get("/health")
async def shallow_health():
    """
    Shallow health check (load balancer).
    
    Fast check for traffic routing.
    """
    healthy, details = await health_checker.shallow_check()
    
    if healthy:
        return details
    else:
        return Response(content=json.dumps(details), status_code=503)

@app.get("/health/deep")
async def deep_health():
    """
    Deep health check (monitoring).
    
    Comprehensive check for dashboards, NOT for load balancing.
    Too slow for high-frequency checks.
    """
    healthy, details = await health_checker.deep_check()
    
    if healthy:
        return details
    else:
        return Response(content=json.dumps(details), status_code=503)

# Load balancer config:
# - Check /health every 5s (shallow, fast)
# 
# Monitoring dashboard:
# - Check /health/deep every 60s (deep, slow)
```

**Shallow vs Deep Trade-offs:**

| Aspect | Shallow | Deep |
|--------|---------|------|
| **Speed** | <10ms | 100-500ms |
| **Checks** | Server responding | All dependencies |
| **Frequency** | Every 5s | Every 60s |
| **Used By** | Load balancer | Monitoring |
| **Failure Impact** | Remove from rotation | Alert ops team |
| **False Positives** | Lower (simple) | Higher (transient errors) |

**Example 4: Dependency Health with Graceful Degradation**

```python
from enum import Enum
from fastapi import FastAPI
import time

class ComponentStatus(Enum):
    """Component health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class DependencyHealthChecker:
    """
    Health checker with dependency tracking.
    
    Pattern: Essential dependencies fail health check,
    non-essential dependencies degrade gracefully.
    """
    
    def __init__(self):
        self.database_healthy = True
        self.cache_healthy = True
        self.external_api_healthy = True
        self.model_loaded = True
    
    def check_health(self) -> tuple[ComponentStatus, dict]:
        """
        Check overall health with dependency awareness.
        
        Returns: (status, details)
        
        Status levels:
        - HEALTHY: All systems operational
        - DEGRADED: Non-essential dependencies down, can serve requests
        - UNHEALTHY: Essential dependencies down, cannot serve requests
        """
        details = {
            "timestamp": time.time(),
            "components": {}
        }
        
        # Check essential dependencies
        essential_unhealthy = False
        
        # Database (ESSENTIAL)
        if self.database_healthy:
            details["components"]["database"] = {
                "status": "healthy",
                "essential": True
            }
        else:
            details["components"]["database"] = {
                "status": "unhealthy",
                "essential": True,
                "impact": "Cannot serve requests without database"
            }
            essential_unhealthy = True
        
        # Model (ESSENTIAL)
        if self.model_loaded:
            details["components"]["model"] = {
                "status": "healthy",
                "essential": True
            }
        else:
            details["components"]["model"] = {
                "status": "unhealthy",
                "essential": True,
                "impact": "Cannot generate responses without model"
            }
            essential_unhealthy = True
        
        # Check non-essential dependencies
        degraded = False
        
        # Cache (NON-ESSENTIAL - can serve without it, just slower)
        if self.cache_healthy:
            details["components"]["cache"] = {
                "status": "healthy",
                "essential": False
            }
        else:
            details["components"]["cache"] = {
                "status": "unhealthy",
                "essential": False,
                "impact": "Slower responses, increased database load"
            }
            degraded = True
        
        # External API (NON-ESSENTIAL - can fallback to local models)
        if self.external_api_healthy:
            details["components"]["external_api"] = {
                "status": "healthy",
                "essential": False
            }
        else:
            details["components"]["external_api"] = {
                "status": "unhealthy",
                "essential": False,
                "impact": "Using local models, may have reduced quality"
            }
            degraded = True
        
        # Determine overall status
        if essential_unhealthy:
            status = ComponentStatus.UNHEALTHY
            details["overall"] = "unhealthy"
            details["message"] = "Essential dependencies unavailable"
        elif degraded:
            status = ComponentStatus.DEGRADED
            details["overall"] = "degraded"
            details["message"] = "Operating with reduced functionality"
        else:
            status = ComponentStatus.HEALTHY
            details["overall"] = "healthy"
            details["message"] = "All systems operational"
        
        return status, details

app = FastAPI()
health_checker = DependencyHealthChecker()

@app.get("/health")
async def health_check():
    """
    Health check with graceful degradation.
    
    Returns:
    - 200: HEALTHY or DEGRADED (can serve traffic)
    - 503: UNHEALTHY (cannot serve traffic)
    """
    status, details = health_checker.check_health()
    
    # Return 200 for both HEALTHY and DEGRADED
    # (can serve traffic, even if degraded)
    if status in [ComponentStatus.HEALTHY, ComponentStatus.DEGRADED]:
        return details
    else:
        # Return 503 for UNHEALTHY (remove from load balancer)
        return Response(
            content=json.dumps(details),
            status_code=503
        )

# Example scenarios:
#
# Scenario 1: Cache fails
# → Status: DEGRADED (200)
# → Load balancer: Keeps routing traffic
# → Impact: Slower responses, but functional
#
# Scenario 2: Database fails
# → Status: UNHEALTHY (503)
# → Load balancer: Stops routing traffic
# → Impact: Pod marked unhealthy, traffic to other pods
#
# Scenario 3: Cache + External API fail
# → Status: DEGRADED (200)
# → Load balancer: Keeps routing traffic
# → Impact: Slower responses, local models only
```

**Example 5: Circuit Breaker Integration**

```python
from fastapi import FastAPI
import time
from enum import Enum

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """
    Circuit breaker for dependency health.
    
    Pattern: Track failures, open circuit after threshold,
    attempt recovery after timeout.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
    
    def record_success(self):
        """Record successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            
            if self.success_count >= self.success_threshold:
                # Recovered! Close circuit
                print("✓ Circuit recovered, closing")
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0
    
    def record_failure(self):
        """Record failed operation."""
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.CLOSED:
            self.failure_count += 1
            
            if self.failure_count >= self.failure_threshold:
                # Too many failures, open circuit
                print(f"⚠️  Circuit opened after {self.failure_count} failures")
                self.state = CircuitState.OPEN
        
        elif self.state == CircuitState.HALF_OPEN:
            # Failed during recovery, back to open
            print("⚠️  Recovery failed, circuit still open")
            self.state = CircuitState.OPEN
            self.success_count = 0
    
    def can_attempt(self) -> bool:
        """Check if can attempt operation."""
        if self.state == CircuitState.CLOSED:
            return True
        
        elif self.state == CircuitState.HALF_OPEN:
            return True
        
        elif self.state == CircuitState.OPEN:
            # Check if recovery timeout elapsed
            if self.last_failure_time is None:
                return False
            
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.recovery_timeout:
                print("⏱️  Recovery timeout elapsed, trying half-open")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                return True
            
            return False
        
        return False
    
    def is_healthy(self) -> bool:
        """Check if circuit is healthy."""
        return self.state == CircuitState.CLOSED

class HealthWithCircuitBreaker:
    """
    Health check with circuit breaker for dependencies.
    
    Pattern: Don't repeatedly check failing dependencies,
    use circuit breaker to fail fast.
    """
    
    def __init__(self):
        self.database_circuit = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=30,
            success_threshold=2
        )
        self.external_api_circuit = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60,
            success_threshold=3
        )
    
    async def check_database(self) -> bool:
        """
        Check database health with circuit breaker.
        
        If circuit open, don't attempt check (fail fast).
        """
        if not self.database_circuit.can_attempt():
            # Circuit open, don't even try
            return False
        
        try:
            # Simulate database check
            await asyncio.sleep(0.1)
            
            # Success
            self.database_circuit.record_success()
            return True
        
        except Exception:
            # Failure
            self.database_circuit.record_failure()
            return False
    
    async def check_external_api(self) -> bool:
        """Check external API with circuit breaker."""
        if not self.external_api_circuit.can_attempt():
            return False
        
        try:
            # Simulate API check
            await asyncio.sleep(0.2)
            
            self.external_api_circuit.record_success()
            return True
        
        except Exception:
            self.external_api_circuit.record_failure()
            return False
    
    async def overall_health(self) -> tuple[bool, dict]:
        """
        Check overall health.
        
        Uses circuit breakers to avoid repeated checks of failing systems.
        """
        db_healthy = await self.check_database()
        api_healthy = await self.check_external_api()
        
        details = {
            "database": {
                "healthy": db_healthy,
                "circuit": self.database_circuit.state.value
            },
            "external_api": {
                "healthy": api_healthy,
                "circuit": self.external_api_circuit.state.value
            }
        }
        
        # Database essential, external API not
        overall_healthy = db_healthy
        
        return overall_healthy, details

app = FastAPI()
health = HealthWithCircuitBreaker()

@app.get("/health")
async def health_check():
    """
    Health check with circuit breaker.
    
    Benefits:
    - Fail fast when dependency down (don't wait for timeout)
    - Reduce load on failing dependencies (stop hammering)
    - Automatic recovery testing (half-open state)
    """
    healthy, details = await health.overall_health()
    
    if healthy:
        return details
    else:
        return Response(
            content=json.dumps(details),
            status_code=503
        )

# Example flow:
#
# t=0s: Database healthy, circuit CLOSED
# t=10s: Database fails (1st time)
# t=15s: Database fails (2nd time)
# t=20s: Database fails (3rd time) → Circuit OPEN
# t=25s: Health check returns immediately (circuit open, fail fast)
# t=30s: Health check returns immediately (circuit open)
# t=50s: Recovery timeout (30s) elapsed → Circuit HALF_OPEN
# t=50s: Health check attempts database (testing recovery)
# t=50s: Database succeeds (1st recovery)
# t=55s: Database succeeds (2nd recovery) → Circuit CLOSED
# t=60s: Normal operation resumed
```

### What It Isn't
Health checks are not **the same as monitoring**. Health checks are simple pass/fail signals for routing decisions; monitoring is comprehensive metrics collection and alerting.

They're not **infallible**. Health checks can have false positives (mark healthy instance unhealthy) and false negatives (mark unhealthy instance healthy). Tune thresholds carefully.

Health checks are not **instant**. Detection takes time: check interval × failure threshold (typically 10-30 seconds). Not suitable for sub-second failover.

They're not **free**. Health checks add load (every 5s × 50 pods = 10 checks/sec), can overwhelm dependencies (deep checks), and require maintenance (keep endpoints updated).

Finally, health checks are not **sufficient alone**. Must combine with: monitoring (metrics), logging (debugging), tracing (request flow), and alerting (human notification).

## How It Works

### Timing and Threshold Configuration

```python
# Kubernetes probe configuration
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10   # Wait 10s before first check
  periodSeconds: 5          # Check every 5 seconds
  timeoutSeconds: 2         # Wait 2s for response
  successThreshold: 1       # 1 success = healthy
  failureThreshold: 2       # 2 failures = unhealthy

# Detection time calculation:
# Time to mark unhealthy = periodSeconds × failureThreshold
# Example: 5s × 2 = 10 seconds to detect failure
#
# Time to mark healthy = periodSeconds × successThreshold
# Example: 5s × 1 = 5 seconds to recover

# Trade-offs:
# - Lower periodSeconds = faster detection, more load
# - Higher failureThreshold = fewer false positives, slower detection
# - Lower timeoutSeconds = faster detection, more false positives
```

**Typical Configurations:**

**Startup Probe:**
- Purpose: Allow long initialization (model loading)
- Interval: 5-10s
- Failure threshold: 12-36 (allow 60-360s for startup)
- Timeout: 5-10s

**Readiness Probe:**
- Purpose: Traffic routing (fast detection)
- Interval: 5s
- Failure threshold: 2-3 (10-15s detection)
- Timeout: 2-5s

**Liveness Probe:**
- Purpose: Restart detection (avoid unnecessary restarts)
- Interval: 10-30s
- Failure threshold: 3-5 (30-150s before restart)
- Timeout: 5-10s

### Load Balancer Integration

```python
# Load balancer health check (conceptual)

# HAProxy configuration:
backend agent_servers
    balance roundrobin
    option httpchk GET /health  # Health check endpoint
    http-check expect status 200  # Expect 200 OK
    
    server pod1 10.0.0.1:8000 check inter 5s fall 2 rise 1
    server pod2 10.0.0.2:8000 check inter 5s fall 2 rise 1
    server pod3 10.0.0.3:8000 check inter 5s fall 2 rise 1

# Parameters:
# inter 5s = check every 5 seconds
# fall 2 = mark down after 2 failures
# rise 1 = mark up after 1 success

# Behavior:
# - Check /health every 5s on each pod
# - If pod returns non-200 or timeout: failure
# - After 2 consecutive failures (10s): mark down, stop routing
# - After 1 success: mark up, resume routing
```

## Think of It Like This
Imagine a traffic light system at a highway on-ramp.

**Without health checks**: All on-ramps always green, even if highway section ahead has massive accident blocking all lanes. Cars merge into stopped traffic, creating more congestion, backup spreads, everyone stuck.

**With health checks**: Traffic sensors every 500 meters check "is this section flowing?" If section blocked (accident, construction, too much volume), sensor marks "unhealthy." Traffic lights at on-ramps turn red, preventing more cars from entering congested section. Alternative routes suggested. Once blockage clears, sensor marks "healthy," on-ramps turn green again.

**Shallow checks**: Quick sensor—"are cars moving?" (speed > 5mph = healthy). Fast, simple, checked every 30 seconds.

**Deep checks**: Comprehensive sensor—"check speed, volume, accident reports, weather conditions, construction schedules." Slow, complex, checked every 5 minutes. Used for highway management dashboard, not immediate traffic lights.

**Liveness checks**: Check if sensor itself is working. If sensor offline (no readings for 10 minutes), send crew to inspect/replace sensor. (Kubernetes restarting the pod.)

Health checks give your agent system that traffic management—automatically detecting congestion/failures, routing around problems, and self-healing when issues resolve.

## The "So What?" Factor
**If you implement health checks properly:**
- Automatic failover (unhealthy instances removed in seconds)
- Zero-downtime deployments (readiness prevents traffic to not-ready pods)
- Self-healing infrastructure (Kubernetes restarts failed pods)
- Load balancer efficiency (traffic only to healthy instances)
- Reduced manual intervention (system handles failures automatically)
- Faster incident detection (unhealthy before total failure)
- Better user experience (no traffic to failing instances)
- Safe auto-scaling (new pods ready before receiving traffic)
- Graceful degradation (detect overload early)
- Clear operational status (health endpoint shows system state)

**If you skip health checks:**
- Traffic to failed instances (timeouts and errors)
- Manual intervention required (someone must remove failed instance)
- Slow failure detection (wait for user reports)
- Deployment downtime (traffic to not-ready pods)
- Cascading failures (traffic overwhelms remaining pods)
- Poor user experience (requests fail unpredictably)
- Scaling issues (traffic sent before ready)
- Higher operational burden (constant manual adjustments)
- Unclear system state (is it healthy or not?)
- Increased support costs (users report failures)

## Practical Checklist
Before deploying to production:
- [ ] Do you have `/health` or `/ready` endpoint returning 200/503?
- [ ] Are startup, readiness, and liveness probes configured in Kubernetes?
- [ ] Is startup probe lenient enough for initialization (model loading)?
- [ ] Is readiness probe fast enough (<100ms response time)?
- [ ] Does readiness probe fail during graceful shutdown?
- [ ] Is liveness probe conservative (avoid unnecessary restarts)?
- [ ] Are essential dependencies checked (database, model)?
- [ ] Are non-essential dependencies handled gracefully (cache, external API)?
- [ ] Do you use shallow checks for load balancer (fast)?
- [ ] Do you use deep checks for monitoring (comprehensive)?
- [ ] Are check intervals tuned (balance detection speed vs load)?
- [ ] Are failure thresholds set (avoid false positives)?
- [ ] Do timeouts prevent slow checks from blocking?
- [ ] Are circuit breakers used for failing dependencies?
- [ ] Is health check load acceptable (check frequency × pod count)?

## Watch Out For
⚠️ **Deep Checks on Load Balancer**: Checking all dependencies every 5s overwhelms systems. Use shallow checks for load balancer.

⚠️ **Liveness Too Sensitive**: Aggressive liveness checks cause restart loops. Be conservative (30s+ detection).

⚠️ **Startup Probe Too Strict**: Model loading takes 60s, startup probe allows 30s. Pod restarted forever. Allow sufficient time.

⚠️ **Not Failing During Shutdown**: Readiness stays healthy during graceful shutdown. Load balancer sends traffic. Fail readiness immediately on shutdown signal.

⚠️ **False Positives from Transients**: Single slow dependency query marks unhealthy. Use failure thresholds (2-3 consecutive failures).

⚠️ **Checking Non-Essential Dependencies**: Cache down marks unhealthy, even though can serve requests. Mark degraded (200) not unhealthy (503).

⚠️ **Synchronous Dependency Checks**: Health check queries all dependencies sequentially (500ms total). Timeout. Check in parallel.

⚠️ **No Timeout on Checks**: Dependency check hangs forever, health check never returns. Always set timeouts.

⚠️ **Health Check Cascade**: Health check calls another service's health check, which calls another. Circular dependencies or cascading failures.

⚠️ **Ignoring Circuit Breakers**: Hammering failed dependency every 5s. Use circuit breakers to fail fast.

## Connections
**Builds On:**
- HTTP status codes (200 = healthy, 503 = unhealthy)
- Load balancing principles
- System monitoring concepts
- Distributed systems patterns

**Works With:**
- [graceful_shutdown](graceful_shutdown.md) - Health checks fail during shutdown to drain traffic
- [request_queuing](request_queuing.md) - Health checks reflect queue depth/overload
- [backpressure](backpressure.md) - Health checks fail under excessive load
- [concurrency_control](concurrency_control.md) - Health checks verify resource availability
- [streaming_responses](streaming_responses.md) - Health checks for streaming endpoints
- Circuit breakers (fail fast on unhealthy dependencies)
- Retry mechanisms (retry on health check failure)
- Monitoring systems (deep checks for dashboards)

**Leads To:**
- Auto-scaling decisions (scale up if all pods unhealthy)
- Chaos engineering (kill pods, verify recovery)
- Blue-green deployments (health checks verify new version)
- Self-healing architectures (automatic recovery)
- Service mesh patterns (Istio, Linkerd health checks)

**Related Patterns:**
- Heartbeat patterns (periodic health signals)
- Watchdog timers (detect hung processes)
- Health check aggregation (parent checks children)
- Dependency health propagation (cascade health status)

## Quick Decision Guide
**Implement health checks when:**
- Running behind load balancer (always)
- Deploying to Kubernetes (always)
- Multiple service instances (always)
- Auto-scaling enabled (always)
- Production system (always)

**Use shallow checks for:**
- Load balancer routing (fast, frequent)
- Kubernetes readiness probe
- High-frequency checks (every 5s)
- Traffic routing decisions

**Use deep checks for:**
- Monitoring dashboards
- Operational visibility
- Low-frequency checks (every 60s)
- Human consumption

**Configure startup probe when:**
- Initialization takes >10s (model loading)
- Complex startup sequence (DB migration, cache warm)
- Want to delay liveness checks until ready

**Configure readiness probe for:**
- Load balancer routing
- Zero-downtime deployments
- Graceful shutdown coordination
- Overload detection

**Configure liveness probe for:**
- Deadlock detection
- Memory corruption recovery
- Auto-restart on stuck process

**Typical timing:**
- Startup: Check every 5s, allow 60s total
- Readiness: Check every 5s, 2 failures = unhealthy
- Liveness: Check every 10s, 3 failures = restart

## Further Exploration
- 📖 **"Kubernetes Best Practices" by Burns & Villalba** - Chapter on health checks and probes
- 🎯 **Implement Health Endpoints** - Add /health, /ready, /live to your agent server
- 💡 **Test Failure Scenarios** - Kill dependencies, verify health checks detect failures
- 📖 **Kubernetes Probe Configuration** - Deep dive into probe parameters and tuning
- 🎯 **Circuit Breaker Integration** - Combine health checks with circuit breakers
- 💡 **Monitor Health Check Metrics** - Track: check duration, failure rate, false positives
- 📖 **"Release It!" by Michael Nygard** - Chapter on stability patterns including health checks
- 🎯 **Load Balancer Health Checks** - Configure HAProxy, nginx, or cloud load balancer
- 💡 **Chaos Engineering Health Checks** - Use chaos-monkey to verify auto-recovery
- 📖 **Service Mesh Health Checks** - Study Istio, Linkerd health check integration

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
