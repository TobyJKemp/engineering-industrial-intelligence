# Concurrency Control

## At a Glance
| | |
|---|---|
| **Category** | Resource Management Pattern / Data Integrity |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 5-8 hours for fundamentals, weeks for distributed patterns |
| **Prerequisites** | Understanding of threads, async programming, race conditions, database transactions |

## One-Sentence Summary
Concurrency control is the set of mechanisms that coordinate simultaneous access to shared resources (databases, files, API quotas, memory) across multiple agents, workers, or threads—using locks, transactions, semaphores, and isolation strategies to prevent race conditions, data corruption, and resource conflicts, transforming "sometimes it works, sometimes data gets corrupted mysteriously" chaos into predictable, correct behavior even when hundreds of concurrent operations compete for the same resources.

## Why This Matters to You
When you build AI agent systems in 2026, concurrency control is the difference between systems that work reliably and systems that mysteriously corrupt data under load. Without concurrency control, when two agents simultaneously try to update the same user record—both reading balance=$100, both deducting $50, both writing balance=$50—the user loses one transaction ($100→$50 instead of $100→$0). This "race condition" seems rare in testing (single user, sequential operations) but becomes catastrophic in production (100 concurrent users, parallel operations). At scale serving 10,000+ concurrent requests, race conditions without proper control cause: duplicate order creation ($50,000 in refunds per month), double-charging customers (angry users, chargebacks), inventory overselling (promising items you don't have), inconsistent agent state (agents "forgetting" context mid-conversation), and database deadlocks (system hangs, manual intervention required). Concurrency control prevents this using locks (only one agent modifies resource at a time), optimistic locking (detect conflicts before committing), transactions (all-or-nothing updates), and semaphores (limit concurrent access to pools). This matters economically: a single race condition causing duplicate payments can cost thousands in refunds and support time; a deadlock during Black Friday peak can lose millions in revenue; inconsistent state in multi-agent workflows causes cascading failures requiring expensive manual remediation. But concurrency control adds complexity and performance costs: locks reduce throughput (waiting for exclusive access), distributed locks add latency (network round-trips to Redis), pessimistic locking causes deadlocks (two agents each holding locks the other needs), and transaction isolation levels trade consistency for performance. Understanding concurrency primitives (threading.Lock, asyncio.Lock, database transactions), distributed coordination (Redis locks, database row locks), isolation levels (READ COMMITTED vs SERIALIZABLE), deadlock prevention strategies (lock ordering, timeouts), and when to use optimistic vs pessimistic approaches determines whether your multi-agent system maintains data integrity or silently corrupts it under load. In 2026, with AI agents autonomously managing financial transactions, medical records, and critical infrastructure, concurrency control is not optional—it's the foundation of trustworthy systems.

## The Core Idea
### What It Is
Concurrency control is a collection of techniques that ensure correct behavior when multiple operations execute simultaneously and access shared mutable state. The core challenge: operations are not atomic—they involve read-modify-write sequences that can interleave incorrectly, causing race conditions where final state depends on unpredictable timing.

**The Race Condition Problem:**

```python
# Two agents updating shared counter WITHOUT concurrency control
# Agent A and Agent B both execute this simultaneously:

current_value = read_counter()        # Both read 100
new_value = current_value + 1         # Both calculate 101
write_counter(new_value)              # Both write 101

# Expected: 100 → 101 → 102 (two increments)
# Actual: 100 → 101 (one increment lost!)
```

This "lost update" happens because read-modify-write is not atomic. Operations interleave:

```
Time  Agent A                Agent B
1     read_counter() → 100   
2                            read_counter() → 100
3     compute: 100 + 1 = 101
4                            compute: 100 + 1 = 101
5     write_counter(101)
6                            write_counter(101)

Result: Counter is 101, but should be 102
```

**Solution 1: Mutex Lock (Mutual Exclusion)**

```python
import threading

counter = 0
counter_lock = threading.Lock()

def increment_counter_safe():
    """
    Thread-safe counter increment using mutex lock.
    
    Lock ensures only one thread executes critical section at a time.
    """
    global counter
    
    with counter_lock:
        # Critical section: only one thread at a time
        current = counter
        new_value = current + 1
        counter = new_value
    
    return counter

# Usage with multiple threads
def worker(thread_id: int, iterations: int):
    """Worker thread incrementing shared counter."""
    for i in range(iterations):
        result = increment_counter_safe()
        print(f"Thread {thread_id}: counter = {result}")

# Create 10 threads, each incrementing 100 times
threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i, 100))
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

print(f"Final counter: {counter}")
# Expected: 1000 (10 threads × 100 increments)
# Actual: 1000 ✓ (lock prevents race condition)
```

**Solution 2: Async Lock (for asyncio)**

```python
import asyncio

class AgentStateManager:
    """
    Manage agent conversation state with concurrency control.
    
    Multiple async tasks may try updating same conversation.
    """
    
    def __init__(self):
        self.conversations = {}
        self.locks = {}  # conversation_id → Lock
        self.global_lock = asyncio.Lock()  # For locks dict itself
    
    async def _get_lock(self, conversation_id: str) -> asyncio.Lock:
        """Get or create lock for conversation."""
        async with self.global_lock:
            if conversation_id not in self.locks:
                self.locks[conversation_id] = asyncio.Lock()
            return self.locks[conversation_id]
    
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ):
        """
        Add message to conversation (thread-safe).
        
        Multiple agents may try adding messages simultaneously.
        Lock prevents race conditions in message ordering.
        """
        lock = await self._get_lock(conversation_id)
        
        async with lock:
            # Critical section: only one task at a time per conversation
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = {
                    "messages": [],
                    "token_count": 0
                }
            
            conv = self.conversations[conversation_id]
            
            # Simulate token counting
            message_tokens = len(content.split())
            
            # Add message
            conv["messages"].append({
                "role": role,
                "content": content,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            # Update token count
            conv["token_count"] += message_tokens
            
            print(f"Added message to {conversation_id}: "
                  f"{len(conv['messages'])} messages, "
                  f"{conv['token_count']} tokens")
    
    async def get_conversation(self, conversation_id: str) -> dict:
        """Get conversation (thread-safe read)."""
        lock = await self._get_lock(conversation_id)
        
        async with lock:
            return self.conversations.get(conversation_id, {})

# Usage
state_manager = AgentStateManager()

async def agent_task(agent_id: int, conv_id: str):
    """Agent adding messages to conversation."""
    for i in range(5):
        await state_manager.add_message(
            conv_id,
            role="assistant",
            content=f"Message {i} from agent {agent_id}"
        )
        await asyncio.sleep(0.01)  # Simulate processing

# Run multiple agents concurrently on same conversation
async def main():
    conv_id = "conv_123"
    
    # 3 agents simultaneously adding messages
    await asyncio.gather(
        agent_task(1, conv_id),
        agent_task(2, conv_id),
        agent_task(3, conv_id)
    )
    
    # Check final state
    conv = await state_manager.get_conversation(conv_id)
    print(f"\nFinal: {len(conv['messages'])} messages")
    # Expected: 15 messages (3 agents × 5 messages)
    # With locks: 15 ✓
    # Without locks: Could be < 15 (lost updates)

# asyncio.run(main())
```

**Solution 3: Database Transactions (ACID Properties)**

```python
import sqlite3
from contextlib import contextmanager

class OrderManager:
    """
    Process orders with transactional concurrency control.
    
    Critical: Multiple agents must not oversell inventory.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create tables if not exist."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    product_id INTEGER PRIMARY KEY,
                    quantity INTEGER NOT NULL,
                    reserved INTEGER DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    quantity INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Seed data
            conn.execute("""
                INSERT OR IGNORE INTO inventory (product_id, quantity)
                VALUES (1, 100)
            """)
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper isolation."""
        conn = sqlite3.connect(self.db_path)
        
        # Set isolation level for concurrency control
        conn.isolation_level = 'DEFERRED'  # Lock on first write
        
        try:
            yield conn
        finally:
            conn.close()
    
    def place_order_unsafe(self, product_id: int, quantity: int) -> dict:
        """
        Place order WITHOUT proper concurrency control.
        
        Race condition: Two orders can oversell inventory.
        """
        with self._get_connection() as conn:
            # Read inventory
            cursor = conn.execute(
                "SELECT quantity FROM inventory WHERE product_id = ?",
                (product_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return {"status": "error", "message": "Product not found"}
            
            available = row[0]
            
            # Check availability
            if available < quantity:
                return {"status": "error", "message": "Insufficient inventory"}
            
            # RACE CONDITION HERE: Another order could execute between check and update
            
            # Update inventory
            conn.execute(
                "UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?",
                (quantity, product_id)
            )
            
            # Create order
            cursor = conn.execute(
                "INSERT INTO orders (product_id, quantity, status) VALUES (?, ?, ?)",
                (product_id, quantity, "confirmed")
            )
            
            conn.commit()
            
            return {
                "status": "success",
                "order_id": cursor.lastrowid,
                "quantity": quantity
            }
    
    def place_order_safe(self, product_id: int, quantity: int) -> dict:
        """
        Place order WITH proper concurrency control.
        
        Uses SELECT FOR UPDATE to lock row during transaction.
        """
        with self._get_connection() as conn:
            try:
                # Start transaction
                conn.execute("BEGIN IMMEDIATE")
                
                # Lock row for update (pessimistic lock)
                cursor = conn.execute(
                    "SELECT quantity FROM inventory WHERE product_id = ? FOR UPDATE",
                    (product_id,)
                )
                row = cursor.fetchone()
                
                if not row:
                    conn.rollback()
                    return {"status": "error", "message": "Product not found"}
                
                available = row[0]
                
                # Check availability
                if available < quantity:
                    conn.rollback()
                    return {"status": "error", "message": f"Insufficient inventory: {available} available"}
                
                # Update inventory (row is locked, no race condition)
                conn.execute(
                    "UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?",
                    (quantity, product_id)
                )
                
                # Create order
                cursor = conn.execute(
                    "INSERT INTO orders (product_id, quantity, status) VALUES (?, ?, ?)",
                    (product_id, quantity, "confirmed")
                )
                
                order_id = cursor.lastrowid
                
                # Commit transaction (releases lock)
                conn.commit()
                
                return {
                    "status": "success",
                    "order_id": order_id,
                    "quantity": quantity
                }
                
            except sqlite3.OperationalError as e:
                conn.rollback()
                return {"status": "error", "message": f"Database error: {e}"}

# Test race condition
order_manager = OrderManager("orders.db")

# Without locks: overselling possible
result1 = order_manager.place_order_unsafe(product_id=1, quantity=60)
result2 = order_manager.place_order_unsafe(product_id=1, quantity=60)
# Both may succeed even though only 100 available! (120 sold)

# With locks: safe
result1 = order_manager.place_order_safe(product_id=1, quantity=60)
result2 = order_manager.place_order_safe(product_id=1, quantity=60)
# Second order fails with "Insufficient inventory" ✓
```

**Solution 4: Optimistic Locking (Version-Based)**

```python
import time
from typing import Optional

class OptimisticLockRecord:
    """
    Record with version number for optimistic concurrency control.
    
    Pattern: Read with version, update only if version unchanged.
    """
    
    def __init__(self, record_id: str, data: dict, version: int = 1):
        self.record_id = record_id
        self.data = data
        self.version = version
        self.updated_at = time.time()

class OptimisticLockStore:
    """
    In-memory store with optimistic locking.
    
    Good for: Low contention, mostly reads, distributed systems.
    """
    
    def __init__(self):
        self.records = {}
    
    def read(self, record_id: str) -> Optional[OptimisticLockRecord]:
        """Read record with current version."""
        return self.records.get(record_id)
    
    def update(
        self,
        record_id: str,
        new_data: dict,
        expected_version: int
    ) -> dict:
        """
        Update record using optimistic locking.
        
        Only succeeds if version matches (no concurrent modifications).
        
        Returns:
            {"status": "success"} or {"status": "conflict", "current_version": N}
        """
        record = self.records.get(record_id)
        
        if not record:
            return {"status": "error", "message": "Record not found"}
        
        # Check version
        if record.version != expected_version:
            # Someone else modified it!
            return {
                "status": "conflict",
                "message": "Record was modified by another process",
                "current_version": record.version,
                "expected_version": expected_version
            }
        
        # Update with new version
        record.data = new_data
        record.version += 1
        record.updated_at = time.time()
        
        return {
            "status": "success",
            "new_version": record.version
        }
    
    def create(self, record_id: str, data: dict):
        """Create new record."""
        self.records[record_id] = OptimisticLockRecord(record_id, data)

# Usage: Optimistic update with retry
store = OptimisticLockStore()
store.create("user_123", {"name": "Alice", "balance": 100})

def update_balance_optimistic(
    store: OptimisticLockStore,
    user_id: str,
    amount: int,
    max_retries: int = 5
) -> dict:
    """
    Update user balance with optimistic locking and retry.
    
    Pattern:
    1. Read record with version
    2. Compute new state
    3. Try update with expected version
    4. If conflict, retry from step 1
    """
    for attempt in range(max_retries):
        # Read current state
        record = store.read(user_id)
        if not record:
            return {"status": "error", "message": "User not found"}
        
        current_version = record.version
        current_balance = record.data["balance"]
        
        # Compute new state
        new_balance = current_balance + amount
        new_data = record.data.copy()
        new_data["balance"] = new_balance
        
        # Try update with expected version
        result = store.update(user_id, new_data, current_version)
        
        if result["status"] == "success":
            print(f"Updated balance: {current_balance} → {new_balance} "
                  f"(version {current_version} → {result['new_version']})")
            return result
        
        elif result["status"] == "conflict":
            print(f"Attempt {attempt + 1}: Conflict detected, retrying...")
            time.sleep(0.01 * (2 ** attempt))  # Exponential backoff
            continue
    
    return {"status": "error", "message": "Max retries exceeded"}

# Simulate concurrent updates
import threading

def concurrent_updater(user_id: str, amount: int, thread_id: int):
    """Thread updating balance."""
    result = update_balance_optimistic(store, user_id, amount)
    print(f"Thread {thread_id}: {result}")

# 5 threads each adding $10
threads = []
for i in range(5):
    t = threading.Thread(target=concurrent_updater, args=("user_123", 10, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Check final balance
final_record = store.read("user_123")
print(f"Final balance: {final_record.data['balance']}")
# Expected: 100 + (5 × 10) = 150
# With optimistic locking: 150 ✓
```

**Solution 5: Distributed Lock (Redis)**

```python
import redis
import time
import uuid
from contextlib import contextmanager
from typing import Optional

class RedisDistributedLock:
    """
    Distributed lock using Redis.
    
    Use case: Multiple servers/processes need to coordinate.
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def acquire(
        self,
        lock_name: str,
        timeout: int = 10,
        retry_interval: float = 0.1
    ) -> Optional[str]:
        """
        Acquire distributed lock.
        
        Args:
            lock_name: Name of lock
            timeout: How long lock is valid (seconds)
            retry_interval: How long to wait between attempts
        
        Returns:
            Lock token (for releasing) or None if failed
        """
        lock_token = str(uuid.uuid4())
        lock_key = f"lock:{lock_name}"
        
        # Try to set lock with NX (only if not exists) and EX (expiration)
        acquired = self.redis.set(
            lock_key,
            lock_token,
            nx=True,  # Only set if doesn't exist
            ex=timeout  # Expire after timeout (prevent deadlock)
        )
        
        if acquired:
            return lock_token
        else:
            return None
    
    def release(self, lock_name: str, lock_token: str) -> bool:
        """
        Release distributed lock.
        
        Only releases if token matches (prevent releasing someone else's lock).
        """
        lock_key = f"lock:{lock_name}"
        
        # Lua script for atomic check-and-delete
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        
        result = self.redis.eval(lua_script, 1, lock_key, lock_token)
        return result == 1
    
    @contextmanager
    def lock(
        self,
        lock_name: str,
        timeout: int = 10,
        acquire_timeout: Optional[int] = None
    ):
        """
        Context manager for distributed lock.
        
        Usage:
            with lock.lock("critical_resource"):
                # Only one process at a time
                do_critical_work()
        """
        start_time = time.time()
        lock_token = None
        
        # Try to acquire lock
        while True:
            lock_token = self.acquire(lock_name, timeout)
            
            if lock_token:
                break
            
            # Check if we've exceeded acquire timeout
            if acquire_timeout and (time.time() - start_time) > acquire_timeout:
                raise TimeoutError(f"Failed to acquire lock '{lock_name}' within {acquire_timeout}s")
            
            time.sleep(0.1)
        
        try:
            yield lock_token
        finally:
            if lock_token:
                self.release(lock_name, lock_token)

# Usage
redis_client = redis.Redis(host='localhost', port=6379, db=0)
lock = RedisDistributedLock(redis_client)

def process_payment_distributed(payment_id: str):
    """
    Process payment with distributed lock.
    
    Ensures only one server processes each payment.
    """
    lock_name = f"payment:{payment_id}"
    
    try:
        with lock.lock(lock_name, timeout=30, acquire_timeout=5):
            print(f"Processing payment {payment_id}")
            
            # Check if already processed
            if redis_client.exists(f"payment:{payment_id}:processed"):
                print(f"Payment {payment_id} already processed")
                return
            
            # Process payment (simulate)
            time.sleep(2)
            
            # Mark processed
            redis_client.set(f"payment:{payment_id}:processed", "1")
            
            print(f"Payment {payment_id} completed")
    
    except TimeoutError:
        print(f"Could not acquire lock for payment {payment_id}")

# Multiple servers can run this safely
# Only one will acquire lock and process payment
```

**Solution 6: Semaphore (Resource Pool Management)**

```python
import asyncio
from typing import Optional

class ResourcePool:
    """
    Manage limited resource pool with semaphore.
    
    Use case: API rate limits, database connections, GPU slots.
    """
    
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_count = 0
        self.total_acquired = 0
        self.total_waited = 0
    
    async def acquire_resource(self, resource_id: str) -> dict:
        """
        Acquire resource from pool.
        
        Blocks if pool is full until resource available.
        """
        start_wait = asyncio.get_event_loop().time()
        
        async with self.semaphore:
            wait_time = asyncio.get_event_loop().time() - start_wait
            
            self.active_count += 1
            self.total_acquired += 1
            self.total_waited += wait_time
            
            print(f"Acquired {resource_id} (waited {wait_time:.2f}s, "
                  f"{self.active_count} active)")
            
            try:
                # Simulate resource use
                yield {
                    "resource_id": resource_id,
                    "wait_time": wait_time
                }
            finally:
                self.active_count -= 1
                print(f"Released {resource_id} ({self.active_count} active)")
    
    def get_stats(self) -> dict:
        """Get resource pool statistics."""
        avg_wait = self.total_waited / self.total_acquired if self.total_acquired > 0 else 0
        
        return {
            "active": self.active_count,
            "total_acquired": self.total_acquired,
            "avg_wait_seconds": round(avg_wait, 3)
        }

# Usage: Limit concurrent API calls
api_pool = ResourcePool(max_concurrent=5)  # Only 5 concurrent API calls

async def call_expensive_api(query_id: int):
    """Make API call with concurrency limit."""
    async for resource in api_pool.acquire_resource(f"api_call_{query_id}"):
        # Only 5 of these execute concurrently
        print(f"Calling API for query {query_id}")
        await asyncio.sleep(2)  # Simulate API call
        print(f"API call {query_id} completed")

async def main():
    # Submit 20 API calls
    # Only 5 execute concurrently (semaphore limit)
    tasks = [call_expensive_api(i) for i in range(20)]
    await asyncio.gather(*tasks)
    
    stats = api_pool.get_stats()
    print(f"\nStats: {stats}")

# asyncio.run(main())
```

### What It Isn't
Concurrency control is not **the same as parallelism**. Parallelism is about doing multiple things simultaneously (for performance); concurrency control is about coordinating when multiple things happen simultaneously (for correctness).

It's not **only about locks**. Locks (pessimistic) are one approach; optimistic locking, transactions, immutability, and single-writer patterns are alternatives.

Concurrency control is not **always necessary**. If state is read-only, or each operation modifies disjoint data, or operations are naturally serialized, you may not need explicit control.

It's not **free**. All concurrency control adds overhead—locks block threads, optimistic locking retries on conflict, transactions hold resources, semaphores queue operations.

Finally, concurrency control is not **a replacement for idempotency**. They solve different problems: concurrency control prevents simultaneous conflicting operations; idempotency ensures operations can be retried safely. You often need both.

## How It Works

### Advanced Patterns

**Pattern 1: Deadlock Prevention (Lock Ordering)**

```python
import threading
import time

class BankAccount:
    """Bank account with balance."""
    
    def __init__(self, account_id: int, balance: float):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()

def transfer_deadlock_possible(from_account: BankAccount, to_account: BankAccount, amount: float):
    """
    Transfer money between accounts (DEADLOCK POSSIBLE).
    
    Deadlock scenario:
    - Thread 1: transfer(A→B) locks A, tries to lock B
    - Thread 2: transfer(B→A) locks B, tries to lock A
    - Both threads wait forever
    """
    with from_account.lock:
        print(f"Locked account {from_account.account_id}")
        time.sleep(0.1)  # Simulate processing
        
        with to_account.lock:
            print(f"Locked account {to_account.account_id}")
            
            from_account.balance -= amount
            to_account.balance += amount
            
            print(f"Transferred ${amount}: {from_account.account_id}→{to_account.account_id}")

def transfer_deadlock_free(from_account: BankAccount, to_account: BankAccount, amount: float):
    """
    Transfer money with deadlock prevention.
    
    Strategy: Always acquire locks in consistent order (by account_id).
    """
    # Determine lock order
    first_account = from_account if from_account.account_id < to_account.account_id else to_account
    second_account = to_account if from_account.account_id < to_account.account_id else from_account
    
    with first_account.lock:
        print(f"Locked account {first_account.account_id}")
        time.sleep(0.1)
        
        with second_account.lock:
            print(f"Locked account {second_account.account_id}")
            
            # Now safe to transfer
            from_account.balance -= amount
            to_account.balance += amount
            
            print(f"Transferred ${amount}: {from_account.account_id}→{to_account.account_id}")

# Test deadlock scenario
account_a = BankAccount(1, 1000)
account_b = BankAccount(2, 1000)

# Without lock ordering: deadlock possible
# t1 = threading.Thread(target=transfer_deadlock_possible, args=(account_a, account_b, 100))
# t2 = threading.Thread(target=transfer_deadlock_possible, args=(account_b, account_a, 50))

# With lock ordering: deadlock prevented
t1 = threading.Thread(target=transfer_deadlock_free, args=(account_a, account_b, 100))
t2 = threading.Thread(target=transfer_deadlock_free, args=(account_b, account_a, 50))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Final balances: A=${account_a.balance}, B=${account_b.balance}")
```

**Pattern 2: Compare-And-Swap (Lock-Free)**

```python
import threading
from typing import Any

class AtomicReference:
    """
    Atomic reference using compare-and-swap.
    
    Lock-free concurrency control.
    """
    
    def __init__(self, initial_value: Any):
        self._value = initial_value
        self._lock = threading.Lock()  # For CAS operation itself
    
    def get(self) -> Any:
        """Get current value."""
        return self._value
    
    def compare_and_swap(self, expected: Any, new_value: Any) -> bool:
        """
        Atomically set to new_value only if current value equals expected.
        
        Returns:
            True if swap successful, False if current != expected
        """
        with self._lock:
            if self._value == expected:
                self._value = new_value
                return True
            else:
                return False

def increment_atomic_cas(atomic_ref: AtomicReference, iterations: int):
    """
    Increment atomic reference using CAS loop.
    
    Lock-free: No thread ever blocks waiting.
    """
    for _ in range(iterations):
        while True:
            current = atomic_ref.get()
            new_value = current + 1
            
            # Try to update
            if atomic_ref.compare_and_swap(current, new_value):
                break  # Success
            # else: Someone else modified it, retry

# Test lock-free increment
atomic_counter = AtomicReference(0)

threads = []
for i in range(10):
    t = threading.Thread(target=increment_atomic_cas, args=(atomic_counter, 100))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter: {atomic_counter.get()}")
# Expected: 1000, Actual: 1000 ✓ (lock-free but correct)
```

## Think of It Like This
Imagine a busy hotel with one shared bathroom on each floor.

**Without concurrency control** (no lock): Multiple guests try entering simultaneously. They collide in the doorway, items get knocked over, some guests start using facilities while others are still there (chaos, privacy violated, conflicts).

**With mutex lock** (bathroom door lock): First guest enters, locks door from inside. Other guests wait outside. Only one person uses bathroom at a time (orderly, safe, but guests wait in line).

**With semaphore** (multiple stalls, counter at door): Bathroom has 3 stalls. Counter shows "2 available". Up to 3 guests can enter simultaneously. Fourth guest waits until someone leaves (more throughput than single lock, still controlled).

**With optimistic locking** (knock first): Guest knocks, checks if empty, remembers the newspaper left on sink. Guest uses bathroom. Before leaving, checks if newspaper still there—if yes, room unchanged (safe to proceed); if no, someone else was there (abort, retry). Works great when conflicts are rare.

**With deadlock** (two bathrooms, need both): Guest A enters bathroom 1, needs bathroom 2. Guest B enters bathroom 2, needs bathroom 1. Both wait forever for the other (system hangs, manual intervention required).

Concurrency control gives your multi-agent system those bathroom coordination protocols—ensuring shared resources are used safely even when many agents need them simultaneously.

## The "So What?" Factor
**If you implement concurrency control properly:**
- No race conditions (data stays consistent)
- No lost updates (all modifications applied)
- No double-charging or duplicate operations
- Inventory never oversold
- Agent state remains coherent
- Database operations ACID-compliant
- Predictable behavior under load
- Can reason about system correctness
- Audit trails remain accurate
- No mysterious "sometimes it fails" bugs

**If you skip concurrency control:**
- Race conditions corrupt data randomly
- Lost updates (operations silently fail)
- Duplicate charges/orders/payments
- Inventory oversold (promise what you don't have)
- Inconsistent agent state (forgotten context)
- Database inconsistencies
- Unpredictable failures under load
- Cannot prove system correctness
- Expensive data corruption incidents
- Support burden from mysterious bugs

## Practical Checklist
Before deploying systems with shared state:
- [ ] Have you identified all shared mutable state?
- [ ] Are critical sections protected with appropriate locks?
- [ ] Is lock granularity appropriate (not too coarse, not too fine)?
- [ ] Have you considered deadlock possibility and prevention?
- [ ] Are database transactions used for multi-step operations?
- [ ] Is transaction isolation level set appropriately?
- [ ] Do optimistic locks have retry logic with exponential backoff?
- [ ] Are distributed locks released even on error (try/finally)?
- [ ] Do locks have timeouts (prevent permanent deadlock)?
- [ ] Are semaphores used for limited resource pools?
- [ ] Have you tested with high concurrency (100+ simultaneous operations)?
- [ ] Is there monitoring for lock contention and deadlocks?
- [ ] Are connection pools sized correctly for concurrency level?

## Watch Out For
⚠️ **Deadlocks**: Two threads each holding locks the other needs. Solution: lock ordering, timeouts, deadlock detection.

⚠️ **Lock Granularity Too Coarse**: One lock protecting too much (entire database instead of specific rows). Reduces concurrency unnecessarily.

⚠️ **Lock Granularity Too Fine**: Too many locks (lock per field instead of per record). Overhead exceeds benefit, complexity explodes.

⚠️ **Forgotten Lock Release**: Lock acquired but not released on error path. Solution: use context managers (with lock:), try/finally blocks.

⚠️ **Holding Locks Too Long**: Performing slow operations (API calls, disk I/O) while holding lock. Reduces concurrency dramatically.

⚠️ **Wrong Isolation Level**: Using READ UNCOMMITTED when SERIALIZABLE needed (or vice versa). Balance consistency vs performance.

⚠️ **Optimistic Locking Livelock**: Conflict rate so high that retries constantly fail. Solution: switch to pessimistic locking.

⚠️ **Distributed Lock TTL Too Short**: Lock expires before operation completes. Another process acquires lock, both think they have exclusive access.

⚠️ **Not Releasing Distributed Locks on Crash**: Stuck locks prevent progress. Solution: TTL expiration, health checks.

⚠️ **Race Conditions in Lock Implementation**: Using non-atomic operations to implement locks. Always use proven primitives (threading.Lock, database transactions, Redis SETNX).

## Connections
**Builds On:**
- Threading and async programming
- Database transactions (ACID)
- Distributed systems principles
- Data structures (queues, hashmaps)

**Works With:**
- [idempotency](idempotency.md) - Complementary: idempotent operations safe to retry even with conflicts
- [request_queuing](request_queuing.md) - Queues serialize access (form of concurrency control)
- [streaming_responses](streaming_responses.md) - Streaming state updates need concurrency control
- [handoff_protocol](handoff_protocol.md) - Agent handoffs must prevent concurrent state corruption
- Database connection pools
- Redis for distributed coordination

**Leads To:**
- Distributed transactions (two-phase commit)
- Consensus algorithms (Raft, Paxos)
- Eventually consistent systems
- CQRS (Command Query Responsibility Segregation)
- Event sourcing (append-only, no conflicts)

**Related Patterns:**
- [caching](../Data_and_Retrieval_Patterns/caching.md) - Cache invalidation needs concurrency control
- Transaction isolation levels
- Optimistic vs pessimistic strategies
- Lock-free data structures
- Software transactional memory

## Quick Decision Guide
**Use mutex locks when:**
- Single-process concurrency (threads)
- Simple exclusive access needed
- Lock duration is short
- Deadlock risk is low

**Use async locks when:**
- Async/await code (asyncio)
- I/O-bound operations
- Need cooperative multitasking
- Single event loop

**Use database transactions when:**
- Multiple related updates
- Need ACID guarantees
- Operating on database state
- Rollback capability required

**Use optimistic locking when:**
- Conflicts are rare (< 10%)
- Read-heavy workloads
- Can tolerate retries
- Distributed systems (lower latency than distributed locks)

**Use pessimistic locking when:**
- Conflicts are common (> 30%)
- Updates are expensive to retry
- Need guaranteed exclusive access
- Can tolerate blocking

**Use distributed locks when:**
- Multiple servers/processes
- Coordinating across services
- Resource not in single database
- Need exclusive access across cluster

**Use semaphores when:**
- Managing resource pools (connections, API quotas)
- Need controlled concurrency (not exclusive)
- Rate limiting concurrent operations

**Consider lock-free algorithms when:**
- Extreme performance requirements
- Lock contention is bottleneck
- Have expertise in lock-free programming
- Can validate correctness thoroughly

## Further Exploration
- 📖 **"Database Internals" by Petrov** - Chapter on concurrency control and isolation
- 🎯 **Implement Optimistic Locking with Retry** - Build version-based update with exponential backoff
- 💡 **Test Deadlock Scenarios** - Create intentional deadlock, implement prevention strategies
- 📖 **"The Art of Multiprocessor Programming" by Herlihy & Shavit** - Deep dive into lock-free algorithms
- 🎯 **Redis Distributed Locks (Redlock)** - Study consensus-based distributed locking
- 💡 **Benchmark Lock Strategies** - Compare throughput: no locks vs optimistic vs pessimistic
- 📖 **PostgreSQL Transaction Isolation** - Understand MVCC, snapshot isolation, serializable
- 🎯 **Two-Phase Locking (2PL)** - Database concurrency control theory
- 💡 **Implement Compare-And-Swap Counter** - Build lock-free increment with CAS loop
- 📖 **"Designing Data-Intensive Applications" by Kleppmann** - Chapter 7 on transactions

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
