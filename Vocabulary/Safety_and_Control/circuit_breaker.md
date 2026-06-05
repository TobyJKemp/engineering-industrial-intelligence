# Circuit Breaker

## At a Glance
| | |
|---|---|
| **Category** | Resilience Pattern / Fault Tolerance Mechanism |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 days for concepts, 3-5 days for production implementation |
| **Prerequisites** | Distributed systems basics, API integration, error handling |

## One-Sentence Summary
A circuit breaker is a software resilience pattern—inspired by electrical circuit breakers—that monitors calls to external services (APIs, databases, LLMs, tools) and automatically stops sending requests ("opens the circuit") after detecting a threshold of failures, allowing the failing service time to recover while preventing cascading failures, resource exhaustion, and poor user experience from repeated timeout attempts—then periodically tests if the service has recovered ("half-open state") before resuming normal operation ("closed state")—transforming "agent repeatedly calls failing API for 30 seconds per request, blocking user, exhausting retry budgets, and cascading failures to other services" into "agent fails fast after detecting service down, returns fallback immediately, periodically checks recovery, resumes normal operation when service healthy"—the difference between system-wide outages and graceful degradation.

## Why This Matters to You
Your AI agent orchestrates a customer support workflow: receives question, calls external knowledge base API to fetch relevant docs (3-second timeout), passes docs to LLM for answer synthesis, returns response to user. System operates beautifully at 95% success rate—users happy, operations smooth. Then: knowledge base API experiences database issues, starts timing out on 90% of requests (10% still work sporadically—service degraded, not completely dead). Without circuit breaker, every customer request triggers: agent calls knowledge base API, waits 3 seconds (timeout—wasted time), retry #1 (3 more seconds—still failing), retry #2 (3 more seconds—still failing), eventually gives up after 9-15 seconds (no knowledge base access—can't answer question), returns error to user. Impact at scale—1000 concurrent users: **9,000 API calls per minute to failing service** (hammering degraded system—making recovery impossible, "thundering herd"), **9-15 second response time per request** (users frustrated—abandoning support, calling phone instead), **LLM costs wasted** (some requests timeout during synthesis—billed for incomplete work), **thread/worker exhaustion** (all agent workers blocked waiting on timeouts—can't handle new requests, cascading failure to your entire service), and **no graceful degradation** (could answer questions without knowledge base—use general knowledge, previous interactions—but can't because stuck waiting on timeout). Operations team discovers outage 20 minutes in (customers already churning—reputation damage), external service recovers but your thundering herd of retry requests immediately overwhelms it again (prevents recovery—extends outage for hours), and incident cost: $50,000 in lost revenue, 10,000 frustrated customers, 40 engineer-hours fighting fire, permanent churn from worst experience. **Problem: system keeps trying to use failing dependency, causing cascading failures, resource exhaustion, and prolonged outages.**

Now you implement circuit breaker for knowledge base API: monitor failure rate (track success/failure per time window—e.g., last 30 seconds), set threshold (if >50% of calls fail in 30 seconds, trip circuit—open state), fail fast when open (immediately return error without calling API—no waiting on timeout), implement half-open testing (after 60 seconds in open state, try single probe request—test if service recovered), and close circuit on success (probe succeeds → service healthy → resume normal operation). Same incident occurs—knowledge base API degrades: **First 10 requests**: Mixture of success/failure as degradation begins (circuit still closed—normal behavior), circuit breaker monitoring kicks in (failure rate crosses 50% threshold after 20 failures in 30 seconds—pattern detected), **circuit opens** (stops calling API immediately—no more requests sent). **Next 1000 requests** (while circuit open): Agent detects circuit open, skips knowledge base call entirely (0 seconds instead of 3-9 seconds—instant), invokes [fallback strategy](../Agent_Operations/fallback_strategy.md) (use LLM's general knowledge, return "I can't access our knowledge base right now, but here's what I can tell you..." + best-effort answer—graceful degradation), returns response in <2 seconds (acceptable experience—not ideal but usable). After 60 seconds: circuit breaker sends probe request to knowledge base API (single test—low risk), probe times out (service still down—circuit remains open, reset timer for next probe). After another 60 seconds: next probe succeeds (service recovered!—response in <500ms), circuit closes (resume normal operation—all future requests call API normally), system automatically returns to full functionality (no manual intervention—self-healing). **Impact with circuit breaker**: Only ~30 API calls sent to failing service (vs 9,000—97% reduction, allows service to recover), response time 2 seconds instead of 9-15 (acceptable degradation—users stay engaged), no thread exhaustion (workers return immediately instead of blocking—handle full request volume), graceful degradation (users get some answer instead of total failure—maintain service), automatic recovery detection (system heals itself when service restores—no manual intervention), and incident cost ~$2,000 (minor degradation, quick recovery—vs $50,000 catastrophic failure). **This is circuit breaker**—detecting failures, stopping the bleeding, failing fast, gracefully degrading, testing for recovery, and automatically healing—transforming cascading failures into managed, temporary degradation while protecting both your system and the failing dependency from thundering herd death spirals. In 2026, with AI agents orchestrating dozens of API calls across cloud services, circuit breakers shift from advanced pattern to fundamental requirement—the difference between resilient, production-grade systems and brittle, cascade-prone prototypes that fail spectacularly under real-world failure scenarios.

## The Core Idea

### What It Is
A circuit breaker is a stateful wrapper around remote calls that automatically stops sending requests to failing services and provides fast failure responses, implementing a state machine with three states: **Closed** (normal operation, requests pass through), **Open** (service considered failing, requests blocked), and **Half-Open** (testing if service recovered).

The pattern originated in Michael Nygard's seminal book "Release It!" (2007) as an adaptation of electrical circuit breakers: when electrical current exceeds safe levels (overload), circuit breaker trips (opens circuit), stopping current flow and preventing damage (fire, equipment destruction). Software circuit breaker applies same principle: when failure rate exceeds threshold (overload), circuit opens (blocks calls), preventing damage (cascading failures, resource exhaustion, poor UX).

**Core Mechanism:**

**Closed State** (Normal Operation):
- Circuit breaker passes all requests through to downstream service (transparent proxy—normal behavior)
- Monitors outcomes: success or failure (tracks in rolling window—last N requests or last T seconds)
- If failure rate exceeds threshold (e.g., >50% failures in 30 seconds), transition to Open state
- Otherwise remains Closed indefinitely (healthy service—no intervention)

Example: Last 30 seconds had 20 successes, 5 failures (20% failure rate—below 50% threshold). Circuit remains closed, continues monitoring.

**Open State** (Service Considered Failed):
- Circuit breaker immediately fails all requests without calling downstream service (fail fast—no waiting on timeout)
- Returns predefined error response or triggers [fallback strategy](../Agent_Operations/fallback_strategy.md) (graceful degradation)
- Saves time (no 3-second timeout—instant response), reduces load on failing service (stops hammering—allows recovery), and prevents resource exhaustion (no blocked threads waiting on timeouts)
- After timeout period (e.g., 60 seconds in Open state), transition to Half-Open state (test recovery)

Example: Circuit opened after detecting 50% failures. Next 1,000 requests over 60 seconds: all immediately return error (0 calls to downstream service—protected). After 60 seconds, move to Half-Open.

**Half-Open State** (Testing Recovery):
- Circuit breaker allows limited number of probe requests through to test if service recovered (typically 1-3 requests—small risk)
- If probe succeeds: service healthy → transition to Closed state (resume normal operation—full traffic)
- If probe fails: service still down → transition back to Open state (reset timeout timer—wait another 60 seconds before next test)
- Critical: only limited probes to avoid re-overwhelming recently recovered service (gradual recovery)

Example: Half-Open state sends single probe request. If succeeds (<500ms response, valid data), circuit closes—next 1,000 requests all go through normally. If fails (timeout), circuit re-opens—wait another 60 seconds before next probe.

**Configuration Parameters:**

**Failure Threshold** - What constitutes "failing"?
- **Absolute threshold**: "5 failures in a row" (simple, but doesn't account for volume—5 failures out of 5 is bad, 5 out of 1000 is fine)
- **Percentage threshold**: "50% failures in time window" (more robust—adapts to volume, e.g., 10 failures out of 20 requests in 30 seconds)
- **Consecutive failures**: "3 consecutive failures" (quick reaction, but false positives from temporary blips)

Choose based on service characteristics: critical, low-volume services use absolute ("3 consecutive"), high-volume use percentage ("50% in 1 minute"), adjust based on acceptable failure tolerance.

**Time Window** - How long to observe failures before tripping:
- Short window (10-30 seconds): react quickly to failures (minimize impact—fast detection), but more sensitive to temporary blips (false positives)
- Long window (1-2 minutes): more stable decision (fewer false positives—only trip for sustained failures), but slower reaction (more impact before detection)

Balance: quick enough to prevent cascading failures, slow enough to avoid false positives from transient errors.

**Open State Timeout** - How long to wait before testing recovery:
- Too short (10 seconds): test before service likely recovered (wasted probes, premature close→reopen cycle)
- Too long (10 minutes): prolonged degradation even after service recovered (miss recovery window—poor UX)
- Typical: 30-120 seconds depending on service recovery characteristics (how long does service typically take to recover from failures?—historical data)

Some implementations use exponential backoff: first probe at 30s, if fails next at 60s, then 120s, etc.—increasingly pessimistic if service not recovering.

**Probe Configuration** (Half-Open):
- Single probe vs multiple probes: single probe (simple, low risk), 3 probes (more reliable signal—2 of 3 must succeed)
- Gradual traffic ramp: start with 1%, then 5%, 10%, 50%, 100% (sophisticated—prevent re-overwhelming, but complex)
- Probe timeout: shorter than normal timeout (faster failure detection—if service still slow, fail probe quickly)

**Why This Pattern Matters:**

**Prevents Cascading Failures** - Failing service doesn't bring down dependent services: without circuit breaker, service A fails → service B (depends on A) blocks threads waiting on timeouts → service B exhausts thread pool → service B fails → service C (depends on B) experiences same → entire system collapses. Circuit breaker breaks chain: service A fails → circuit breaker in B opens → B fails fast, maintains capacity → B remains operational (degraded but functional) → C continues operating. Failure isolated, not cascaded.

**Fail Fast, Degrade Gracefully** - Better to fail quickly with fallback than slowly with timeout: 3-second timeout feels like eternity to user (abandoned request, frustration), repeated 3-second timeouts exhaust resources (blocked threads, memory), and failed requests after 3 seconds still fail (wasted 3 seconds for nothing). Circuit breaker: fail in <10ms (nearly instant—user informed immediately), invoke fallback (partial answer better than no answer—graceful degradation), and preserve resources (threads available for successful requests—maintain throughput).

**Protect Failing Service from Thundering Herd** - Circuit breaker stops hammering degraded service: service degrades (slow, dropping connections, database struggling), without circuit breaker: all clients continue sending requests (making problem worse—amplifying load), retry logic makes it worse (each failed request retries 3x—3x the load on dying service), service can't recover (overloaded with retries—death spiral). Circuit breaker: detects degradation, stops sending requests (drops load to near zero—gives service breathing room), service recovers (no longer overwhelmed—stabilizes), circuit breaker detects recovery, gradually restores traffic. Circuit breaker enables service recovery by removing load.

**Improve User Experience** - Users get fast failure + fallback instead of timeout + total failure: timeout scenario: user waits 9-15 seconds (multiple timeouts with retries—frustration), gets error message (no answer—worthless), abandons product (terrible UX—churn). Circuit breaker scenario: user waits 2 seconds (fast failure + fallback processing—acceptable), gets partial answer ("can't access knowledge base, here's what I know..."—some value), stays engaged (degraded but usable service—retention). Partial service beats no service.

**Observable System Health** - Circuit breaker state is clear signal: circuit closed = service healthy (normal operation—monitoring), circuit open = service failed (alert immediately—incident response), frequency of open→closed→open cycles = service flapping (instability—investigate), time spent in open state = service availability (SLA tracking). Circuit breaker state becomes key operational metric.

### What It Isn't
Circuit breakers aren't retry mechanisms—they're the opposite. Retry logic says "try again, maybe it'll work this time" (optimistic—assumes transient failure), circuit breaker says "this is failing systematically, stop trying" (pessimistic—assumes sustained failure). They work together: retry handles transient failures (1-2 quick retries for network blips—recover from transient issues), circuit breaker handles sustained failures (repeated failures over time window—stop hammering failing service). Pattern: retry 2-3 times with exponential backoff (handle transient errors), if still failing increment circuit breaker failure count (detect systematic failure), if circuit breaker threshold exceeded open circuit (stop retrying—protect system). Don't confuse: retries are request-level (try this request again), circuit breakers are service-level (stop calling this service).

Circuit breakers don't make services more reliable—they make *systems* more resilient to unreliable services. The downstream service is still failing (circuit breaker doesn't fix the root cause—doesn't restart database, doesn't fix network, doesn't deploy bug fix), but your system handles the failure gracefully (fails fast, degrades gracefully, recovers automatically—operational resilience). Circuit breaker is damage control, not repair. After circuit opens, still need to: investigate root cause (why is service failing?—troubleshoot), fix underlying issue (restart service, deploy fix, scale resources—remediation), monitor recovery (circuit breaker detects recovery, but verify quality—not just "responding" but "responding correctly"). Circuit breaker buys time and prevents cascading damage while you fix the real problem.

Circuit breakers aren't substitutes for proper error handling and [fallback strategies](../Agent_Operations/fallback_strategy.md). Circuit breaker detects failures and blocks calls (prevents hammering—protects system), but what happens to the request when circuit is open? Need fallback: return cached data (stale but useful—better than nothing), use alternative service (backup API, different provider—redundancy), degrade functionality (skip optional features, provide partial answer—graceful degradation), or return error with helpful message ("service temporarily unavailable, try again in 2 minutes"—transparent communication). Circuit breaker is the "when" decision (when to stop calling service), fallback strategy is the "what" decision (what to do instead). Both required for graceful degradation.

Circuit breakers don't eliminate the need for timeouts—they work together. Timeout is per-request protection ("don't wait forever for this single call"—prevents blocking), circuit breaker is aggregate protection ("this service is failing repeatedly, stop calling it"—prevents cumulative damage). Without timeouts: single call to broken service blocks forever (thread stuck—resource leak), even if circuit breaker would eventually open (after several requests), early requests still hang. Without circuit breaker: every request times out individually (wastes 3 seconds each—poor UX), resource exhaustion from many concurrent timeouts (thread pool drained—service degradation), and no learning (same timeout on 1000th request as 1st request—no adaptation). Use both: timeout (3-5 seconds) on each call (protect individual requests—prevent hanging), circuit breaker tracking timeout frequency (too many timeouts → open circuit—protect service-level).

Circuit breakers aren't one-size-fits-all—require tuning per service. Critical, low-latency service needs aggressive circuit breaker (trip after 3 failures—minimize impact), best-effort, high-latency service needs permissive circuit breaker (trip after 50% failures in 5 minutes—tolerate intermittent issues). Service with fast recovery (auto-scaling, health checks) needs short open timeout (30 seconds—test recovery quickly), service with slow recovery (manual intervention, database rebuild) needs long open timeout (5-10 minutes—don't waste probes on definitely-down service). Failure characteristics vary: API might fail fast (immediate 500 error—easy to detect), database might fail slow (1-second delays before timeout—harder to distinguish from legitimately slow queries). Tune circuit breaker parameters per dependency based on: service criticality (how bad if unavailable?—business impact), typical failure modes (how does it fail?—detection strategy), recovery characteristics (how fast recovers?—open timeout duration), and request patterns (volume, latency distribution—threshold tuning). Generic defaults fail in production—measure and tune.

Finally, circuit breakers don't automatically guarantee resilience—poorly configured circuit breakers cause problems: threshold too sensitive (trips on transient errors—false positives, excessive degradation), threshold too permissive (doesn't trip until catastrophic failure—defeats purpose, cascading failures happen anyway), open timeout too short (opens and closes rapidly—"flapping", instability), too long (stays degraded after service recovered—missed recovery, poor UX). Monitor circuit breaker behavior: false positive rate (circuit opens when service actually healthy—tune threshold less sensitive), false negative rate (circuit stays closed despite service failing—tune threshold more sensitive), time to recovery (how long between service recovery and circuit close?—tune open timeout), and flapping frequency (circuit oscillating open→closed→open—indicates service instability or threshold misconfiguration). Circuit breakers require monitoring and tuning like any complex system component—not deploy-and-forget.

## How It Works

Implementing circuit breaker pattern systematically:

**Step 1: Define Circuit Breaker State Machine**

Core state management:

```python
from enum import Enum
from datetime import datetime, timedelta
from collections import deque
import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Blocking all calls
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker for protecting external service calls."""
    
    def __init__(
        self,
        name: str,
        failure_threshold: float = 0.5,  # 50% failure rate
        window_seconds: int = 30,         # Observe last 30 seconds
        open_timeout_seconds: int = 60,   # Stay open for 60 seconds
        half_open_max_calls: int = 3      # Try 3 probes when half-open
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.window_seconds = window_seconds
        self.open_timeout_seconds = open_timeout_seconds
        self.half_open_max_calls = half_open_max_calls
        
        # State tracking
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
        self.opened_at = None
        self.half_open_calls = 0
        
        # Rolling window for failure tracking (last N seconds)
        self.call_history = deque()  # (timestamp, success: bool)
        
    def _cleanup_old_calls(self):
        """Remove calls outside the observation window."""
        cutoff_time = time.time() - self.window_seconds
        while self.call_history and self.call_history[0][0] < cutoff_time:
            self.call_history.popleft()
    
    def _get_failure_rate(self):
        """Calculate current failure rate in observation window."""
        self._cleanup_old_calls()
        
        if not self.call_history:
            return 0.0
        
        failures = sum(1 for _, success in self.call_history if not success)
        return failures / len(self.call_history)
    
    def _should_trip(self):
        """Check if circuit should trip to OPEN."""
        failure_rate = self._get_failure_rate()
        return failure_rate >= self.failure_threshold
    
    def _should_attempt_reset(self):
        """Check if circuit should move to HALF_OPEN."""
        if self.state != CircuitState.OPEN:
            return False
        
        if not self.opened_at:
            return False
        
        elapsed = time.time() - self.opened_at
        return elapsed >= self.open_timeout_seconds
    
    def record_success(self):
        """Record successful call."""
        self.call_history.append((time.time(), True))
        
        if self.state == CircuitState.HALF_OPEN:
            # Successful probe in half-open state
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                # Enough successful probes, close circuit
                print(f"[{self.name}] Circuit closing after {self.half_open_calls} successful probes")
                self.state = CircuitState.CLOSED
                self.half_open_calls = 0
                self.opened_at = None
    
    def record_failure(self):
        """Record failed call."""
        self.call_history.append((time.time(), False))
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            # Failed probe in half-open state
            print(f"[{self.name}] Probe failed, reopening circuit")
            self.state = CircuitState.OPEN
            self.opened_at = time.time()
            self.half_open_calls = 0
        
        elif self.state == CircuitState.CLOSED:
            # Check if should trip
            if self._should_trip():
                print(f"[{self.name}] Circuit opening (failure rate: {self._get_failure_rate():.1%})")
                self.state = CircuitState.OPEN
                self.opened_at = time.time()
    
    def can_attempt(self):
        """Check if call should be attempted."""
        # Clean up old history
        self._cleanup_old_calls()
        
        # Check if should move to half-open
        if self._should_attempt_reset():
            print(f"[{self.name}] Circuit entering half-open state for testing")
            self.state = CircuitState.HALF_OPEN
            self.half_open_calls = 0
        
        if self.state == CircuitState.CLOSED:
            return True  # Normal operation
        
        elif self.state == CircuitState.HALF_OPEN:
            # Allow limited probes
            return self.half_open_calls < self.half_open_max_calls
        
        else:  # OPEN
            return False  # Block all calls
    
    def get_state(self):
        """Get current state information."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_rate": self._get_failure_rate(),
            "calls_in_window": len(self.call_history),
            "opened_at": self.opened_at,
            "time_in_open_state": 
                time.time() - self.opened_at if self.opened_at else None
        }
```

**Step 2: Wrap External Calls with Circuit Breaker**

Integrate circuit breaker into service calls:

```python
import requests
from functools import wraps

class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open."""
    def __init__(self, circuit_name, state_info):
        self.circuit_name = circuit_name
        self.state_info = state_info
        super().__init__(
            f"Circuit breaker '{circuit_name}' is {state_info['state']}. "
            f"Failure rate: {state_info['failure_rate']:.1%}"
        )

def protected_by_circuit_breaker(circuit_breaker):
    """Decorator to protect function with circuit breaker."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if circuit allows attempt
            if not circuit_breaker.can_attempt():
                raise CircuitBreakerOpen(
                    circuit_breaker.name,
                    circuit_breaker.get_state()
                )
            
            try:
                # Attempt the call
                result = func(*args, **kwargs)
                circuit_breaker.record_success()
                return result
            
            except Exception as e:
                # Record failure
                circuit_breaker.record_failure()
                raise
        
        return wrapper
    return decorator

# Example: Protect external API call
knowledge_base_circuit = CircuitBreaker(
    name="knowledge_base_api",
    failure_threshold=0.5,  # Trip at 50% failures
    window_seconds=30,       # Observe last 30 seconds
    open_timeout_seconds=60  # Test recovery after 60 seconds
)

@protected_by_circuit_breaker(knowledge_base_circuit)
def query_knowledge_base(query: str):
    """Query external knowledge base API."""
    response = requests.get(
        "https://api.knowledge-base.example.com/search",
        params={"q": query},
        timeout=3  # 3-second timeout per request
    )
    response.raise_for_status()
    return response.json()
```

**Step 3: Implement Fallback Strategy**

Handle circuit breaker open state gracefully:

```python
def query_knowledge_base_with_fallback(query: str):
    """Query knowledge base with circuit breaker and fallback."""
    try:
        # Try primary service
        return query_knowledge_base(query)
    
    except CircuitBreakerOpen as e:
        # Circuit is open, use fallback
        print(f"Circuit breaker open: {e}")
        
        # Fallback option 1: Use cached data
        cached = get_from_cache(query)
        if cached:
            return {
                "source": "cache",
                "data": cached,
                "note": "Knowledge base temporarily unavailable, using cached data"
            }
        
        # Fallback option 2: Use alternative service
        try:
            alt_result = query_backup_knowledge_base(query)
            return {
                "source": "backup",
                "data": alt_result,
                "note": "Using backup knowledge base"
            }
        except Exception:
            pass
        
        # Fallback option 3: Graceful degradation
        return {
            "source": "degraded",
            "data": None,
            "note": "Knowledge base temporarily unavailable. Using general knowledge only."
        }
    
    except requests.exceptions.Timeout:
        # Timeout (circuit will record failure)
        raise
    
    except requests.exceptions.RequestException as e:
        # Other request failures (circuit will record failure)
        raise
```

**Step 4: Monitor Circuit Breaker State**

Track circuit breaker metrics:

```python
class CircuitBreakerMonitor:
    """Monitor circuit breaker health and behavior."""
    
    def __init__(self):
        self.state_changes = []  # Track state transitions
        self.trip_events = []     # Track when circuits open
        self.recovery_events = [] # Track when circuits close
    
    def record_state_change(self, circuit_name, old_state, new_state):
        """Record state transition."""
        event = {
            "timestamp": time.time(),
            "circuit": circuit_name,
            "old_state": old_state.value if old_state else None,
            "new_state": new_state.value
        }
        self.state_changes.append(event)
        
        if new_state == CircuitState.OPEN:
            self.trip_events.append(event)
            print(f"⚠️  ALERT: Circuit '{circuit_name}' opened!")
        
        elif new_state == CircuitState.CLOSED and old_state == CircuitState.HALF_OPEN:
            self.recovery_events.append(event)
            print(f"✅ Circuit '{circuit_name}' recovered!")
    
    def get_metrics(self, circuit_breaker):
        """Get circuit breaker metrics."""
        state_info = circuit_breaker.get_state()
        
        return {
            "name": circuit_breaker.name,
            "current_state": state_info["state"],
            "failure_rate": state_info["failure_rate"],
            "total_trips": len([e for e in self.trip_events 
                               if e["circuit"] == circuit_breaker.name]),
            "total_recoveries": len([e for e in self.recovery_events 
                                    if e["circuit"] == circuit_breaker.name]),
            "time_in_open_state": state_info["time_in_open_state"],
            "availability": self._calculate_availability(circuit_breaker.name)
        }
    
    def _calculate_availability(self, circuit_name):
        """Calculate service availability (time circuit was closed)."""
        # Calculate % of time circuit was closed (available)
        # Simplified implementation
        relevant_events = [e for e in self.state_changes 
                          if e["circuit"] == circuit_name]
        
        if not relevant_events:
            return 1.0  # 100% available
        
        # Count time in each state
        # (Full implementation would track time-weighted availability)
        closed_time = sum(1 for e in relevant_events 
                         if e["new_state"] == "closed")
        total_time = len(relevant_events)
        
        return closed_time / total_time if total_time > 0 else 1.0

# Usage
monitor = CircuitBreakerMonitor()

# Periodically log metrics
def log_circuit_breaker_metrics():
    metrics = monitor.get_metrics(knowledge_base_circuit)
    print(f"""
    Circuit Breaker: {metrics['name']}
    State: {metrics['current_state']}
    Failure Rate: {metrics['failure_rate']:.1%}
    Total Trips: {metrics['total_trips']}
    Availability: {metrics['availability']:.1%}
    """)
```

**Step 5: Tune Based on Service Characteristics**

Adjust parameters for each service:

```python
# Critical, low-latency service: aggressive circuit breaker
critical_api_circuit = CircuitBreaker(
    name="critical_api",
    failure_threshold=0.25,   # Trip at 25% failures (very sensitive)
    window_seconds=15,         # Short window (fast reaction)
    open_timeout_seconds=30,   # Test recovery quickly
    half_open_max_calls=1      # Single probe (minimize risk)
)

# Best-effort, high-latency service: permissive circuit breaker
analytics_circuit = CircuitBreaker(
    name="analytics_api",
    failure_threshold=0.7,     # Trip at 70% failures (tolerant)
    window_seconds=120,         # Long window (stable decision)
    open_timeout_seconds=300,   # Wait longer for recovery
    half_open_max_calls=5       # Multiple probes (reliable signal)
)

# LLM API: balance cost and reliability
llm_circuit = CircuitBreaker(
    name="llm_api",
    failure_threshold=0.4,     # Trip at 40% failures
    window_seconds=60,          # 1-minute window
    open_timeout_seconds=120,   # 2-minute recovery wait (give LLM time)
    half_open_max_calls=2       # 2 probes (balance cost vs confidence)
)
```

**Step 6: Handle Circuit Breaker in AI Agent Orchestration**

Integrate into agent workflow:

```python
class AIAgent:
    """AI agent with circuit breaker protection."""
    
    def __init__(self):
        self.knowledge_base_circuit = knowledge_base_circuit
        self.llm_circuit = llm_circuit
    
    async def handle_customer_query(self, query: str):
        """Handle customer query with circuit breaker protection."""
        context = []
        
        # Try to get knowledge base context (with circuit breaker)
        try:
            kb_result = query_knowledge_base_with_fallback(query)
            if kb_result["data"]:
                context.append(f"Knowledge Base: {kb_result['data']}")
            if kb_result.get("note"):
                # Service degraded, inform user
                degradation_note = kb_result["note"]
        except Exception as e:
            # Knowledge base completely unavailable
            degradation_note = "Knowledge base unavailable"
        
        # Call LLM with available context (with circuit breaker)
        try:
            @protected_by_circuit_breaker(self.llm_circuit)
            def call_llm():
                return self._generate_response(query, context)
            
            response = call_llm()
            
        except CircuitBreakerOpen:
            # LLM circuit open, use cached responses or simple fallback
            response = self._get_cached_response(query)
            if not response:
                response = "I'm experiencing technical difficulties. Please try again in a few moments."
        
        # Add degradation notice if applicable
        if degradation_note:
            response += f"\n\n(Note: {degradation_note})"
        
        return response
```

## Think of It Like This

Imagine an electrical circuit breaker in your home:

**Without circuit breaker**: You plug in a faulty appliance (short circuit, drawing massive current—equipment failure). Wires heat up (current overload—danger), insulation melts (wire damage—fire hazard), fire starts in walls (catastrophic failure—house burns down). Every faulty appliance risks burning your house down—terrifying.

**With circuit breaker**: You plug in faulty appliance, massive current starts flowing (overload detected—circuit breaker monitoring). Circuit breaker trips instantly (opens circuit, stops current flow—protection activated), appliance goes dead (no power—failure contained), wires safe (no heat buildup—damage prevented), house safe (no fire—protected). You investigate (find faulty appliance—root cause), remove faulty appliance (fix problem—remediation), reset circuit breaker (press button—test recovery), circuit closes (power restored—normal operation). Circuit breaker: detected dangerous condition (overload—threshold exceeded), stopped the damage (opened circuit—blocked current), allowed safe recovery (reset mechanism—test and restore), and protected entire system (fire prevented—cascading failure avoided).

Software circuit breaker identical: "faulty appliance" is failing external service (API down, database overloaded, LLM timeout—dependency failure), "massive current" is flood of requests to failing service (hammering degraded service—making worse), "wires heat up" is resource exhaustion in your system (threads blocked on timeouts, memory filling with retry queues—system degradation), "house fire" is cascading failure (your service fails, dependent services fail, entire system collapses—outage). Circuit breaker: detects failing service (failure rate threshold—monitoring), stops requests (opens circuit—blocks calls), prevents resource exhaustion (threads return immediately—preserved capacity), allows service recovery (stops hammering—gives breathing room), tests recovery (half-open probes—detect healing), and restores normal operation (closes circuit—resume traffic). Just as electrical circuit breaker prevents house fires by detecting and stopping dangerous current flow, software circuit breaker prevents system outages by detecting and stopping dangerous request flow to failing services.

## The "So What?" Factor

**If you implement circuit breakers:**
- **Prevent cascading failures** - Isolate service failures before they propagate: failing dependency doesn't exhaust your resources (threads return immediately instead of blocking on timeouts—capacity preserved), your service remains operational in degraded mode (handles requests with fallback—not completely down), downstream services unaffected (your service still responds—failure isolated to single dependency), and system resilience (one service failure doesn't cascade to system-wide outage—fault tolerance). Result: incidents contained (failing API affects only API-dependent features, not entire system—blast radius minimized), uptime maintained (99.9% uptime despite dependency failures—SLA met), and user experience preserved (degraded functionality better than total outage—service continuity).
- **Fail fast and improve responsiveness** - Eliminate wasteful timeout delays: circuit open returns error in <10ms instead of 3-second timeout (300× faster—responsive even during failures), user sees "temporarily unavailable" immediately (clear feedback—better than spinning loader), threads available for other work (not blocked waiting on timeouts—throughput preserved), and throughput maintained (process 1000 req/sec with failures instead of 100 req/sec with timeouts—10× better under failure). Result: better UX during incidents (fast degradation better than slow failure—user satisfaction), maintained capacity (serve successful requests even when dependencies fail—partial availability), and faster incident detection (fast failures visible immediately vs slow timeouts masking problems—observability).
- **Protect failing services from thundering herd** - Give failing services chance to recover: circuit opens after detecting failures (stops sending requests—removes load), failing service no longer overwhelmed (load drops to zero—breathing room), service recovers naturally (CPU/memory stabilize, queues drain—healing), half-open probes test recovery gently (1-3 requests instead of 1000—cautious), and gradual return to normal (circuit closes only after confirmed recovery—safe restoration). Result: faster incident recovery (services heal in minutes instead of hours—reduced MTTR), prevention of death spirals (stop hammering prevents total collapse—stability), and automatic healing (no manual intervention to "stop all clients"—self-correcting).
- **Improve observability and incident response** - Circuit breaker state signals system health: circuit open = dependency failed (clear alert—immediate notification), time in open state = outage duration (SLA tracking—quantifiable impact), trip frequency = service instability (chronic issues—identify problems), and recovery time = service resilience (how fast service heals—operational metric). Result: faster incident detection (circuits opening trigger alerts immediately—proactive), clear incident scope (which services affected? check circuit states—diagnosis), and quantifiable metrics (MTTR, availability, failure frequency—data-driven improvement).
- **Enable graceful degradation** - Continue operating with reduced functionality: primary service down, circuit open → invoke fallback (cached data, alternative service, partial functionality—maintain service), users get reduced service instead of no service (some value better than none—retention), and system adapts automatically (no manual failover—self-healing). Result: higher perceived availability (users see "some features unavailable" instead of "system down"—better experience), maintained revenue (degraded service still converts, total outage loses all revenue—business continuity), and user retention (users tolerate temporary degradation, not total failure—loyalty).
- **Reduce operational costs** - Minimize incident impact and response burden: fewer cascading failures means fewer incidents (smaller on-call burden—better work-life balance), faster automatic recovery means less manual intervention (no middle-of-night "restart all the things"—sleep), and contained failures mean smaller blast radius (fix one service, not entire system—scoped remediation). Result: lower incident response costs (fewer engineer-hours fighting fires—efficiency), reduced customer impact (less downtime = less churn, refunds, support load—revenue preservation), and team sustainability (predictable incidents instead of chaos—retention).
- **Support multi-tenancy and resource isolation** - Prevent noisy neighbors: tenant A's dependency fails → tenant A's circuit opens (isolated to A's traffic—protected), tenant B unaffected (separate circuit breaker—isolation), and resource pool not exhausted by A's failures (A's threads return fast—B gets full resources). Result: fair resource sharing (one tenant's problems don't impact others—multi-tenancy works), predictable performance (tenant B sees consistent latency despite A's issues—SLA met), and scalability (add tenants without failure blast radius growing—safe growth).

**If you don't implement circuit breakers:**
- **Cascading failures destroy system availability** - One service failure brings down everything: service A fails (API timeout, database overload—dependency down), service B (depends on A) blocks threads waiting on timeouts (all 100 worker threads blocked—capacity exhausted), service B stops responding (thread pool empty—now B is down), service C (depends on B) experiences same cascade (B timing out → C's threads block—chain reaction), and entire system collapses (10-minute cascading failure taking down 20 services—catastrophic outage). Result: multi-million dollar incidents (revenue loss, SLA penalties, emergency response—expensive), extended outages (cascading failures take hours to diagnose and fix—MTTR measured in hours), and unpredictable blast radius (one service failure becomes system-wide—can't isolate).
- **Resource exhaustion from repeated timeouts** - Threads/memory wasted waiting on failing services: 3-second timeout per request to failing service (blocking thread for 3 seconds—waste), 100 concurrent requests (100 threads blocked—pool exhausted), all threads blocked waiting on timeouts (no capacity for successful requests—total unavailability), and memory pressure from retry queues (requests backing up—OOM crash). Result: complete service unavailability (can't process any requests, even those not using failing dependency—total outage), expensive infrastructure scaling (add more servers to compensate for wasted threads—throwing money at symptom), and poor resource utilization (servers at 100% utilization but doing nothing useful—waste).
- **Poor user experience during failures** - Users wait through multiple timeouts: user submits request (expecting 1-second response—normal UX), service calls failing API (3-second timeout #1—user waits), retry #1 (3-second timeout #2—user still waiting), retry #2 (3-second timeout #3—user frustrated), finally fails after 9-15 seconds (returns error—worthless), user abandons (terrible experience—churn), and multiply by 1000 concurrent users (1000 frustrated users—reputation damage). Result: user churn (terrible experience drives users to competitors—revenue loss), support burden (users calling support about slow/failing system—operational cost), and reputational damage (social media complaints, review site negative reviews—brand harm).
- **Thundering herd prevents service recovery** - Keep hammering failing service: service degraded (50% capacity—struggling), without circuit breaker all clients keep sending full traffic (1000 req/sec to 50% capacity service—overwhelming), service gets worse (queues back up, memory exhausts—deteriorating), clients add retries (now 3000 req/sec hitting failing service—amplified load), service completely collapses (overloaded beyond recovery—death spiral), and remains down until manual intervention (operators must block all clients to allow recovery—manual remediation, hours). Result: extended outages (service can't recover while being hammered—prolonged incidents), manual intervention required (emergency war room to coordinate stopping all clients—expensive), and repeated failures (service recovers, clients resume, immediately collapse again—cycle repeats).
- **No automated recovery** - Manual intervention required for every incident: dependency fails (API down—incident starts), no circuit breaker to detect (failure continues until human notices—delayed detection), manual alerts (engineer paged, logs into system—precious minutes lost), manual diagnosis (check logs, metrics, traces—investigation time), manual remediation (manually route around failing service, deploy code to use fallback—complex, error-prone), and manual traffic resumption (once service recovers, manually restore traffic—coordination required). Result: high MTTR (mean time to recovery measured in hours—availability impact), expensive on-call burden (engineers constantly responding to incidents—burnout), and error-prone recovery (manual steps under pressure cause mistakes—incidents get worse).
- **No visibility into service health** - Failures opaque until catastrophic: service degrading slowly (failure rate climbing from 5% to 20% to 40%—gradual), no circuit breaker to detect pattern (just see increasing error logs—noise), hit 80% failure rate before someone notices (catastrophic by then—major incident), and no clear metrics (when did degradation start? how severe? which services?—blind). Result: slow incident detection (failures continue 30+ minutes before detected—prolonged impact), difficult diagnosis (scrambling to understand what's failing—wasted time), and reactive operations (constantly firefighting instead of monitoring leading indicators—chaos).
- **Competitive disadvantage** - Competitors with circuit breakers have better resilience: your system: single dependency failure → cascading outage → 2-hour system-wide downtime (users furious—churn), competitor's system: same dependency fails → circuit breaker opens → graceful degradation → "some features temporarily unavailable" → auto-recovery in 10 minutes (users barely notice—minimal impact). Over one year: you have 4 major outages (16 hours downtime—99.8% uptime, missed SLA), competitor has 0 major outages (same dependency failures but contained—99.99% uptime, met SLA). Result: lose customers (competitors market superior reliability—attrition), lose deals (enterprise buyers require 99.95%+ uptime—disqualified), and higher costs (more incidents = more support, more engineering, more customer concessions—operational burden).

## Practical Checklist

Before implementing circuit breakers, ask yourself:

- [ ] **Which external dependencies need circuit breakers?** - Identify critical integration points: external APIs (third-party services, internal microservices—failure-prone), database connections (primary DB, analytics DB, cache—can be overloaded), LLM providers (OpenAI, Anthropic, Azure OpenAI—expensive, rate-limited), tool services (search engines, knowledge bases, computation services—dependencies), and authentication services (SSO, OAuth providers—critical but can fail). Rule of thumb: any networked dependency that can fail or degrade should have circuit breaker (except truly optional features with no fallback value).
- [ ] **What are the failure characteristics of each service?** - Understand how services fail: fast failures (immediate 500 errors—easy to detect, short timeout), slow failures (1-3 second delays before timeout—harder to distinguish from legitimately slow), intermittent failures (50% failure rate—flapping risk), and complete outages (100% failures—obvious). Different failure modes need different circuit breaker tuning—fast failures use absolute thresholds ("3 consecutive"), slow failures use percentage thresholds ("50% in 1 minute").
- [ ] **What failure threshold should trip the circuit?** - Balance sensitivity vs false positives: aggressive (25-30% failure rate—quick reaction but false positives from transient errors), balanced (50% failure rate—standard, works for most services), permissive (70%+ failure rate—tolerant of intermittent issues, slow to react). Start conservative (50%), tune based on observed behavior—too many false positives, increase threshold; too slow to react, decrease threshold.
- [ ] **How long should observation window be?** - Time window for measuring failure rate: short (10-30 seconds—react quickly, but sensitive to temporary spikes), medium (30-90 seconds—balanced, standard for most services), long (2-5 minutes—stable decisions, but slow to react to sudden failures). Critical services need short windows (react fast—minimize impact), best-effort services tolerate long windows (avoid false positives—stability). Match window to service criticality and typical failure patterns.
- [ ] **How long should circuit stay open before testing recovery?** - Open state timeout duration: based on service recovery characteristics (how long does service typically take to recover?—historical data), 30-60 seconds for auto-scaling services (recover quickly—test soon), 2-5 minutes for services requiring manual intervention (operators need time—wait longer), and exponential backoff option (30s, 60s, 120s, 240s—increasingly pessimistic if service not recovering). Too short wastes probes, too long delays recovery—tune based on service behavior.
- [ ] **What happens when circuit is open?** - Fallback strategy critical: cached data (serve stale data—better than nothing), alternative service (backup API, different provider—redundancy), graceful degradation (skip optional features, provide partial answer—maintain some functionality), or informative error (clear message about service unavailable + estimated recovery time—transparency). Circuit breaker without fallback just fails faster—still fails. Design fallback before implementing circuit breaker.
- [ ] **How will I monitor circuit breaker state?** - Observability requirements: circuit state metrics (% time in each state—availability tracking), state transition events (circuit opened/closed—alerts), trip frequency (how often circuit opens—stability metric), failure rates that triggered trips (was threshold appropriate?—tuning data), and recovery times (how long from open to closed?—service resilience metric). Export to monitoring system (Datadog, Prometheus, CloudWatch—visibility), alert on state changes (circuit opened = incident—notify on-call), and dashboard showing circuit states (operational overview—real-time health).
- [ ] **How will I tune circuit breaker parameters?** - Continuous optimization: start with conservative defaults (50% threshold, 60s window, 90s open timeout—safe), measure false positives (circuit trips when service healthy—tune threshold higher or window longer), measure false negatives (circuit doesn't trip despite service failing—tune threshold lower or window shorter), measure recovery delays (circuit staying open after service recovered—tune open timeout shorter), and A/B test parameter changes (route 50% traffic to new settings—validate improvements). Document tuning decisions and rationale.
- [ ] **Do I have per-tenant or per-endpoint circuit breakers?** - Granularity decision: single circuit breaker per service (simple, but one tenant's failures affect all—coarse), per-tenant circuit breakers (tenant A's failures don't affect tenant B—isolation, but complex), per-endpoint circuit breakers (GET /users healthy, POST /orders failing—fine-grained routing), or adaptive (start coarse, add granularity where needed—pragmatic). Multi-tenant systems need per-tenant isolation (prevent noisy neighbors—fairness), single-tenant can use per-service (simpler—less overhead).
- [ ] **How do circuit breakers interact with retry logic?** - Coordination required: retry happens first (2-3 quick retries for transient failures—handle intermittent issues), if still failing after retries, increment circuit breaker failure count (persistent failure—systematic problem), circuit breaker trips after threshold (too many persistent failures—stop trying), and no retries while circuit open (circuit blocked = don't retry—fail fast). Don't confuse: retries are request-level (this specific request might work on retry—transient), circuit breakers are service-level (service is systematically failing—stop all requests).
- [ ] **What are my SLOs and how do circuit breakers help?** - Align with service objectives: if SLO is 99.9% availability (43 minutes downtime/month allowed), circuit breakers prevent cascading failures that exceed budget (contain 5-minute incident instead of 2-hour cascade—preserve SLO), if SLO is p99 latency <500ms, circuit breakers maintain latency during failures (fail fast at 10ms instead of timeout at 3000ms—meet latency SLO even during incidents), and if SLO is 99.5% success rate, circuit breakers with fallbacks maintain success (degraded response counts as success, timeout counts as failure—higher success rate). Circuit breakers are SLO protection mechanism—design around SLO requirements.
- [ ] **When should I alert on circuit breaker state?** - Alert strategy: always alert on circuit opening (service failure detected—incident notification), optional alert on circuit closing (recovery detected—incident resolved), alert on repeated open→close→open cycles (flapping—service instability, investigate), and alert on circuit stuck open (open for >10 minutes—service not recovering, escalate). Don't alert on half-open transitions (expected testing behavior—noise). Route alerts appropriately: critical services → page on-call, best-effort services → log/ticket, monitoring services → silent monitoring.

## Watch Out For

⚠️ **Threshold misconfiguration causing false positives** - Circuit breaker too sensitive: set failure threshold at 10% (very aggressive—any transient issue trips circuit), service has normal 5% error rate (network blips, rare edge cases—baseline noise), transient spike to 12% failures (temporary—recovers in seconds), and circuit trips immediately (opens on 12%—false positive, service actually healthy). Result: **unnecessary degradation** (users see fallback responses despite service working—poor UX), **flapping** (circuit opens, closes quickly, opens again—instability), **alert fatigue** (constant circuit breaker alerts on non-issues—ignoring real problems), and **loss of trust** (team tunes alerts to ignore circuit breakers—defeats purpose). Solution: analyze baseline failure rate (what's normal? 1%? 5%?—historical data), set threshold above baseline (if 5% normal, use 30-50% threshold—margin for noise), use percentage thresholds not absolute (3 consecutive failures triggers on low-volume services inappropriately—use 50% of requests in time window), and validate with production data (test threshold on historical data—would it have caught real incidents without false positives?). Conservative thresholds better than aggressive—better to catch real failures slightly slower than constantly false-positive.

⚠️ **Circuit breaker masking underlying problems** - Circuit opens, team says "circuit breaker working, incident contained" and moves on—problem persists: circuit opening is symptom, not solution (service is actually failing—need root cause analysis), circuit stays open or reopens frequently (service not actually recovering or chronically unreliable—needs fixing), and team normalizes circuit breaker being open ("oh that service always has circuit open"—acceptance of poor quality). Result: **chronic degradation** (users permanently see fallback instead of full service—poor experience becomes norm), **wasted infrastructure** (paying for service that's always circuit-broken—unused resources), **opportunity cost** (features dependent on that service never work—product gaps), and **hidden incidents** (circuit breaker prevents cascading failure but underlying service remains broken—no urgency to fix). Solution: treat circuit breaker opening as incident (investigate immediately—root cause analysis), measure MTTR (mean time to recovery—circuit close, not just "contained"), track frequency of trips (circuit opening daily = chronic problem—must fix service), and set SLOs around circuit state (circuit open >1% of time = breach—forcing remediation). Circuit breakers contain damage but don't fix problems—must still fix the underlying service failures.

⚠️ **No fallback strategy leaving users with nothing** - Circuit opens, blocks calls to failing service, returns error—user sees "service unavailable" with no degraded functionality: implemented circuit breaker but forgot fallback (pattern incomplete—only have "stop calling" part, not "what to do instead"), and users experience fast failure instead of slow failure, but still failure (technically better—10ms vs 3000ms, but functionally same—no value delivered). Result: **wasted potential** (circuit breaker could enable graceful degradation but instead just fails faster—partial benefit), **poor user experience** (users still see errors, just faster—still churn), **same support burden** (support tickets about "service unavailable" instead of "request timed out"—same volume, slightly different message), and **missed business continuity** (could maintain partial functionality but don't—lost revenue). Solution: design fallback first, then implement circuit breaker (fallback is the value—circuit breaker enables it), options include cached data (stale but useful), alternative service (backup API), degraded functionality (skip optional features), or clear error message (transparent communication + retry guidance). Circuit breaker + fallback = graceful degradation; circuit breaker alone = fast failure (better than slow failure but not actually resilient).

⚠️ **Open timeout too short causing flapping** - Circuit opens after failures, waits 10 seconds, tests recovery, service still down, reopens—cycle repeats rapidly: open timeout too short (10s—service takes 5 minutes to recover), circuit tests recovery every 10 seconds (optimistic—wasting probes), service not ready (still broken—fails probe), circuit reopens (back to open state—reset 10s timer), and repeat 30 times before service actually recovers (thrashing—instability). Result: **excessive probe traffic** (30 failed probes hammering recovering service—delaying recovery), **operational noise** (30 "circuit opening" alerts in 5 minutes—alert fatigue), **flapping metrics** (circuit state constantly changing—hard to understand actual availability), and **delayed recovery detection** (by time service recovers, team ignoring alerts—missed). Solution: tune open timeout to service recovery characteristics (database restart takes 2 minutes → use 120s open timeout—realistic), use exponential backoff (first probe at 30s, then 60s, 120s, 240s—increasingly cautious if not recovering), monitor time-to-recovery historically (how long does this service typically take to heal?—data-driven), and err on longer timeouts (waiting extra 60s to probe is fine, probing 30× too soon wastes resources—conservative). Better to wait bit longer than thrash.

⚠️ **Circuit breaker interfering with health checks** - Health check endpoint protected by circuit breaker: service has `/health` endpoint (for load balancer, orchestrator—liveness check), circuit breaker wraps all calls to service (including health checks—protection), circuit opens due to failures (service down—detection works), but health check also blocked (can't check `/health`—circuit open means "don't call service"), and orchestrator thinks service healthy (health check returns "circuit open" error which orchestrator interprets as success—false signal). Result: **load balancer keeps routing to failed service** (health checks passing—load balancer unaware), **orchestrator doesn't restart service** (liveness check passing—Kubernetes thinks service healthy), **manual intervention required** (circuit breaker detected failure but no automated remediation—incomplete solution), and **confused diagnostics** (service down but health checks green—contradictory signals). Solution: health checks should bypass circuit breaker (special case—not protected), or circuit breaker state exposed as health check (GET `/health` returns 503 when circuit open—accurate signal), or use passive health checks (orchestrator monitors actual traffic success rate, not dedicated endpoint—realistic). Health checks are exception to circuit breaker pattern—they exist to detect failures, circuit breaker shouldn't hide failures from them.

⚠️ **Resource leaks in circuit breaker implementation** - Circuit breaker tracks call history in unbounded queue: every call appends to history (timestamp, success/failure—tracking), never clean up old entries (keep all history forever—memory leak), after 1 million calls circuit breaker has 1 million history entries (consuming 100+ MB RAM—waste), multiply by 20 circuit breakers (2GB RAM in circuit breaker state—resource exhaustion), and eventually OOM crash (circuit breakers designed to prevent crashes, causing crashes—ironic failure). Result: **memory exhaustion** (circuit breakers themselves become failure point—self-defeating), **performance degradation** (iterating over 1M history entries to calculate failure rate—slow), **cascading failures** (OOM crash takes down service—circuit breakers caused what they meant to prevent). Solution: use bounded data structures (ring buffer, fixed-size queue—cap memory), implement sliding window (only keep last N seconds of history, discard older—bounded), clean up expired entries (periodically remove entries outside observation window—maintenance), and monitor circuit breaker memory usage (alert if growing unbounded—detect leaks). Circuit breaker state should be O(1) or O(window_size) memory, not O(total_requests)—bounded growth.

⚠️ **Circuit breaker per request instead of per service** - Create new circuit breaker for each request: every API call creates new CircuitBreaker() (isolated state per request—no sharing), each circuit breaker tracks only its own success/failure (no aggregate view—can't detect pattern), circuit breaker never trips (1 request = 1 call = no history to detect failures—useless), and thousands of circuit breaker objects created (memory waste, GC pressure—overhead). Result: **circuit breaker never opens** (can't detect failures without history—pattern broken), **resource waste** (thousands of objects tracking nothing useful—overhead), **false sense of security** ("we have circuit breakers"—but not working). Solution: circuit breakers are **singleton per service** (one circuit breaker for "knowledge_base_api" shared across all requests—aggregate state), store in application state (not local variable—persistent), share across threads/workers (global instance—coordinated), and name clearly (knowledge_base_circuit, llm_circuit, analytics_circuit—per-dependency). Circuit breaker is shared state machine tracking aggregate service health, not per-request tracking—fundamental pattern.

⚠️ **Testing only with healthy services** - Develop circuit breaker in environment where services never fail: circuit breaker implemented (code complete—looks good), tested in dev/staging (services always healthy—100% success rate), circuit never opens (no failures to detect—never exercises pattern), deployed to production, first real failure occurs, and circuit breaker doesn't work as expected (subtle bug, misconfiguration, unexpected edge case—discovered in production). Result: **false confidence** (thought circuit breaker working—actually untested), **production incident** (failures cascade despite circuit breaker—not protected), **emergency debugging** (fixing circuit breaker during incident—worst time), and **extended outage** (both service failure and circuit breaker failure—compounded). Solution: **chaos engineering** (intentionally inject failures in test environment—validate circuit breaker trips), **load testing with failures** (introduce 50% failure rate, verify circuit opens—functional test), **test all states** (closed → open transition, open → half-open transition, half-open → closed, half-open → open—state machine coverage), and **validate fallback** (when circuit open, does fallback actually work?—end-to-end). Circuit breaker that's never tripped is untested—must test with real failures.

⚠️ **No monitoring of circuit breaker effectiveness** - Implement circuit breaker, assume working, never measure: circuit breaker deployed (protecting services—assumed), no metrics on circuit state (% time open/closed—no visibility), no tracking of prevented cascading failures (would failure have cascaded without circuit breaker?—unknown impact), no measurement of false positives (circuit tripping unnecessarily?—unknown quality), and team blind to circuit breaker behavior (working? flapping? unused?—no data). Result: **unknown effectiveness** (is circuit breaker actually preventing failures?—can't prove value), **undetected misconfiguration** (circuit tripping too often or not often enough—never discover), **wasted investment** (built circuit breakers but maybe not helping—opportunity cost), and **can't optimize** (which thresholds to tune?—no data to guide). Solution: **comprehensive metrics** (circuit state, failure rates, trip frequency, time-in-state—full observability), **dashboards** (visualize circuit breaker health across all services—operational view), **alerts** (circuit opened = investigate immediately—action), **effectiveness analysis** (compare incidents before/after circuit breakers—quantify value), and **A/B testing** (some services with circuit breakers, some without—controlled comparison). Measure what you build—visibility enables improvement.

⚠️ **Circuit breaker becoming performance bottleneck** - Single circuit breaker instance with synchronous lock: every request acquires lock (mutual exclusion—protect state), updates call history (append to shared data structure—contention), checks failure threshold (iterate history—computation), and releases lock. At scale (1000 req/sec × 20 services = 20,000 lock acquisitions/sec—contention), result: **lock contention** (threads waiting for circuit breaker lock—serialized), **latency increase** (circuit breaker adds 5-10ms per request—overhead), **throughput reduction** (lock becomes bottleneck—can't scale), and **ironic failure** (circuit breaker meant to improve resilience, causing performance problems—self-defeating). Solution: **lock-free or low-contention implementations** (atomic counters, thread-local state aggregated periodically—minimize locking), **approximate state** (don't need exact failure count, approximate is fine—trade precision for speed), **batched updates** (update circuit breaker every 100ms instead of every request—amortize cost), and **sharded state** (multiple circuit breaker instances per service, aggregate at read time—parallelism). Circuit breaker is hot path—must be extremely fast (<1ms overhead)—optimize aggressively.

⚠️ **Legal/compliance issues from selective service degradation** - Circuit breaker opens, invokes fallback providing degraded service—not all users treated equally: User A's request: circuit closed, gets full service (complete knowledge base data—premium experience), User B's request 5 seconds later: circuit opened (after A's request triggered threshold), gets fallback (cached data or degraded response—lesser experience), both requests functionally identical, but different outcomes due to timing (first users get full service, later users get degraded—arbitrary). In regulated industries or protected characteristics: **discrimination concerns** (if degradation correlates with protected characteristics—race, geography, economic status—disparate impact), **SLA violations** (contract specifies full service, degraded service might breach—liability), **compliance issues** (regulations require consistent service level—circuit breaker creates inconsistency). Solution: **transparent degradation** (inform users service degraded—clear communication), **compensatory actions** (users receiving degraded service get discount/credit—fairness), **documented policy** (circuit breakers are safety mechanism, approved by legal/compliance—risk accepted), **track demographics** (monitor if degradation affects protected groups disproportionately—fairness audit), and **alternative approaches** (maintain redundancy so circuit breaker less likely to open—minimize degradation frequency). Balance safety (circuit breaker protects system) with fairness (consistent service level)—legal review recommended.

⚠️ **Distributed circuit breakers without coordination** - Microservices architecture, each instance has own circuit breaker: 10 instances of Service A, each with own circuit breaker for Service B (isolated state—no sharing), instance 1 sees failures, opens circuit (protects instance 1—local decision), instances 2-10 unaware (still sending full traffic to B—coordinated), Service B still overwhelmed (9 of 10 instances hammering—not protected), and circuit breakers not effective (meant to protect B, but only 10% reduction in traffic—insufficient). Result: **partial protection** (one instance protected, service still overwhelmed—ineffective), **inconsistent behavior** (user hitting instance 1 gets fallback, user hitting instance 2 gets full service—confusing), **wasted coordination opportunity** (instances could share intelligence—miss optimization). Solution: **distributed state sharing** (circuit breaker state in Redis, all instances coordinate—shared decision), **eventual consistency acceptable** (slightly stale state fine—balance consistency vs latency), **consensus protocol** (majority of instances seeing failures → open all circuits—coordinated response), or **centralized circuit breaker service** (dedicated service manages all circuit breakers—single source of truth, adds dependency). Distributed systems need distributed circuit breakers—local state insufficient at scale.

## Connections

**Builds On:**
- Timeout handling - Circuit breakers rely on timeouts to detect slow failures
- Error handling patterns - Circuit breakers are sophisticated error handling
- Service resilience patterns - Circuit breaker is one tool in resilience toolkit
- State machines - Circuit breaker implements three-state machine (closed/open/half-open)

**Works With:**
- [Fallback Strategy](../Agent_Operations/fallback_strategy.md) - What to do when circuit is open
- [Guardrails](guardrails.md) - Circuit breakers complement guardrails for comprehensive safety
- [Orchestration](../Agent_and_Orchestration/orchestration.md) - Circuit breakers in workflow error handling
- [Human-in-the-Loop](human-in-the-loop.md) - Circuit breaker can trigger human escalation
- Retry logic - Retries handle transient failures, circuit breakers handle persistent failures
- [Backpressure](../Agent_Operations/backpressure.md) - Both manage load, circuit breaker for external services
- [Concurrency Control](../Agent_Operations/concurrency_control.md) - Circuit breaker implementation needs thread-safe state

**Leads To:**
- Bulkhead pattern - Isolate resources per service (complement to circuit breaker)
- Rate limiting - Prevent overwhelming services before failures occur
- Chaos engineering - Testing circuit breakers with intentional failures
- Service mesh patterns - Infrastructure-level circuit breakers (Istio, Linkerd)
- Adaptive resilience - Dynamic threshold tuning based on service behavior
- Multi-level circuit breakers - Circuit breakers at different layers (client, gateway, service)

## Quick Decision Guide

**Implement circuit breakers when:**
- Calling external services or APIs (third-party, internal microservices—failure-prone dependencies)
- Service failures could cascade (one service down affects multiple services—blast radius risk)
- Timeouts are causing resource exhaustion (threads blocking, memory filling—capacity issues)
- Need graceful degradation (continue operating with reduced functionality—business continuity)
- Services have recovery characteristics (take time to heal, can be overwhelmed by traffic—need breathing room)
- Operating at scale (thousands of requests/sec—failures have major impact)
- Multi-tenant architecture (prevent one tenant's failures affecting others—isolation required)

**Skip circuit breakers when:**
- Calling local/in-process functions (no network, immediate response—no failure risk)
- Service is truly critical with no fallback (authentication, payment processing where degradation unacceptable—all-or-nothing)
- Ultra-low latency requirements (<1ms)—circuit breaker overhead unacceptable
- Services never fail (unrealistic, but if true—no benefit)
- Development/prototype phase (add later—premature optimization in early development)
- Simple scripts or batch jobs (no concurrency, low stakes—overhead not justified)

## Further Exploration

- 📖 **"Release It!" by Michael Nygard** - Original circuit breaker pattern and resilience patterns
- 🎯 **Netflix Hystrix** - Circuit breaker library (archived but foundational reference)
- 💡 **Polly (.NET)** - Modern resilience library with circuit breakers
- 📖 **"Circuit Breaker Pattern" - Martin Fowler** - Comprehensive pattern explanation
- 🎯 **Resilience4j (Java)** - Modern circuit breaker and resilience library
- 💡 **PyBreaker (Python)** - Circuit breaker implementation for Python
- 📖 **AWS re:Invent talks on resilience** - Real-world circuit breaker at scale
- 🎯 **Istio/Linkerd Service Mesh** - Infrastructure-level circuit breakers
- 💡 **Chaos Engineering practices** - Testing circuit breakers with failure injection
- 📖 **"The Phoenix Project"** - DevOps novel featuring cascading failures and resilience
- 🎯 **Grafana dashboards for circuit breakers** - Visualizing circuit state and failures
- 💡 **SRE principles on error budgets and resilience** - Context for circuit breaker value

---
*Added: May 20, 2026 | Updated: May 20, 2026 | Confidence: High*
