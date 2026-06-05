# Observer Pattern

## At a Glance
| | |
|---|---|
| **Category** | Behavioral Design Pattern |
| **Complexity** | Beginner to Intermediate (concept is intuitive, implementation requires care) |
| **Time to Learn** | 1-2 days to understand, a week to apply effectively |
| **Prerequisites** | Basic OOP, interfaces, understanding of event-driven concepts |

## One-Sentence Summary
The Observer Pattern defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependent objects (observers) are automatically notified and updated—enabling loose coupling between event producers and event consumers.

## Why This Matters to You
When you're building AI agents and ML systems, you're constantly dealing with events that multiple parts of your system need to react to: an agent completes a task, a model finishes inference, a tool returns results, an error occurs, or a user sends a message. The naive approach is tight coupling—your agent code directly calls the logger, then calls the metrics collector, then calls the audit system, then calls the UI updater. Now your core agent logic is tangled with every system that needs to know about its actions. Adding a new monitoring system means modifying agent code. Testing the agent requires mocking all these dependencies. The Observer Pattern flips this relationship: your agent announces events ("I completed a task," "I called a tool," "I got an error"), and interested parties observe these events without the agent knowing they exist. Want to add performance monitoring? Create an observer and register it—no agent code changes. Want to test the agent without logging? Don't register the logger—no code modifications. Want to build a real-time dashboard showing agent activity? Add a UI observer—agent logic stays untouched. This pattern is everywhere in 2026 AI systems: frameworks like LangChain use observers for callbacks at every agent step, training pipelines use observers for progress monitoring, multi-agent systems use observers for inter-agent communication, and production systems use observers for observability without coupling instrumentation to business logic.

## The Core Idea
### What It Is
The Observer Pattern, documented in the Gang of Four's 1994 Design Patterns book, solves a fundamental problem: how do you let multiple objects react to changes in another object without creating tight coupling between them? The pattern establishes a one-to-many dependency where one object (the subject or observable) maintains a list of dependents (observers) and notifies them automatically of state changes, typically by calling one of their methods.

The key insight is separation: the subject knows only that observers exist and implement a specific interface—it doesn't know what they do with notifications or even what they are. Observers know they're interested in the subject's state changes, but the subject doesn't depend on observers' implementations. This creates loose coupling where observers can be added, removed, or changed without modifying the subject.

The pattern has two main participants:

**Subject (Observable)**: The object being observed. It maintains:
- A list of observers
- Methods to attach observers (`subscribe`, `add_observer`)
- Methods to detach observers (`unsubscribe`, `remove_observer`)  
- A notification method that calls each observer when state changes

**Observer**: Objects interested in the subject. They implement:
- An update method that the subject calls when notifying observers
- Logic to handle notifications appropriately

When the subject's state changes (or any event occurs that observers care about), the subject iterates through its observer list and calls each observer's update method, often passing relevant data about what changed.

For AI agents in 2026, this pattern is fundamental for building observable, extensible systems. Consider an agent executing tasks:

```python
class Agent:
    def __init__(self):
        self._observers = []
    
    def subscribe(self, observer):
        self._observers.append(observer)
    
    def _notify(self, event_type, data):
        for observer in self._observers:
            observer.update(event_type, data)
    
    def execute_task(self, task):
        self._notify("task_started", {"task": task})
        try:
            result = self._process_task(task)
            self._notify("task_completed", {"task": task, "result": result})
            return result
        except Exception as e:
            self._notify("task_failed", {"task": task, "error": e})
            raise

# Observers
class Logger:
    def update(self, event_type, data):
        if event_type == "task_started":
            log(f"Task started: {data['task']}")
        elif event_type == "task_completed":
            log(f"Task completed: {data['task']}")

class MetricsCollector:
    def update(self, event_type, data):
        if event_type == "task_completed":
            metrics.increment("tasks_completed")
        elif event_type == "task_failed":
            metrics.increment("tasks_failed")

class UIUpdater:
    def update(self, event_type, data):
        if event_type in ["task_started", "task_completed", "task_failed"]:
            ui.refresh_agent_status(data)

# Wire observers to subject
agent = Agent()
agent.subscribe(Logger())
agent.subscribe(MetricsCollector())
agent.subscribe(UIUpdater())
```

The agent doesn't know about Logger, MetricsCollector, or UIUpdater. It just notifies observers. Each observer handles notifications independently. Adding new observers (performance monitoring, audit logging, distributed tracing) doesn't require agent modifications. This decoupling is the Observer Pattern's power.

Modern variations include push vs. pull models (subject pushes data to observers vs. observers pull data from subject), event channels (centralized event buses rather than per-subject observer lists), and reactive programming (observables as first-class async streams). Frameworks like RxJS, Python's asyncio observers, and agent frameworks' callback systems all implement observer patterns, sometimes under names like pub-sub, event emitters, or signals.

### What It Isn't
Observer Pattern is not the same as polling. In polling, observers repeatedly check the subject to see if something changed—active, wasteful checking. Observer Pattern inverts this: the subject notifies observers when changes occur—passive, efficient notification. The difference: observers wait to be called rather than constantly asking "anything new?"

It's also not identical to the Pub-Sub (Publish-Subscribe) pattern, though they're very similar. Classic Observer Pattern has observers directly registered with the subject—they know each other. Pub-Sub introduces an intermediary (message broker, event bus) where publishers and subscribers don't know each other at all—fully decoupled through the broker. In practice, the terms are often used interchangeably, but technically pub-sub is more decoupled. For AI agents, both patterns apply: direct observers for component-level events, pub-sub for system-level events.

Don't confuse Observer Pattern with callbacks, though callbacks can implement the pattern. A callback is a function passed to be invoked later. Observer Pattern is a specific structure where subjects maintain observer lists and notify them systematically. You can implement observers using callbacks, but not all callbacks are observer patterns (one-off callbacks aren't observing ongoing state).

The pattern also isn't the same as event-driven architecture, though it's foundational to it. Event-driven architecture is an architectural style where systems react to events. Observer Pattern is a design pattern that enables event-driven systems at the object/component level. EDA is the macro view, Observer is the micro implementation.

Finally, Observer Pattern doesn't mean observers are passive recipients with no agency. Observers can take any action they want in response to notifications—update UI, trigger other processes, make decisions, modify their own state. The "observation" doesn't imply passivity; it means reacting to notifications from the subject.

## How It Works

**1. Define the Observer Interface:**
Create an interface or protocol that all observers must implement, typically with an update method:

```python
from typing import Protocol

class Observer(Protocol):
    def update(self, event_type: str, data: dict) -> None:
        """Called when subject notifies observers of events."""
        ...
```

This contract ensures the subject can notify any observer uniformly.

**2. Implement the Subject:**
The subject maintains a list of observers and provides methods to manage them:

```python
class AgentSubject:
    def __init__(self):
        self._observers: list[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Register an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Unregister an observer."""
        self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict) -> None:
        """Notify all observers of an event."""
        for observer in self._observers:
            observer.update(event_type, data)
```

The subject controls when notifications occur but doesn't control what observers do with them.

**3. Create Concrete Observers:**
Implement specific observers that react to notifications:

```python
class PerformanceMonitor:
    def __init__(self):
        self.start_times = {}
    
    def update(self, event_type: str, data: dict) -> None:
        if event_type == "llm_call_started":
            self.start_times[data['call_id']] = time.time()
        elif event_type == "llm_call_completed":
            duration = time.time() - self.start_times.pop(data['call_id'])
            metrics.histogram("llm_call_duration", duration)

class CostTracker:
    def __init__(self):
        self.total_cost = 0.0
    
    def update(self, event_type: str, data: dict) -> None:
        if event_type == "llm_call_completed":
            tokens = data.get('tokens', 0)
            cost = tokens * 0.00002  # Example pricing
            self.total_cost += cost
            metrics.gauge("total_llm_cost", self.total_cost)

class ConversationLogger:
    def update(self, event_type: str, data: dict) -> None:
        if event_type in ["user_message", "agent_response"]:
            log_to_database(event_type, data)
```

Each observer has different concerns and handles notifications differently. They're independent—one observer's logic doesn't affect others.

**4. Notify Observers at Key Points:**
In the subject's methods, call notify when events occur that observers should know about:

```python
class Agent(AgentSubject):
    def process_message(self, message: str):
        self.notify("user_message", {"message": message, "timestamp": time.time()})
        
        # Retrieve context
        context = self.retriever.retrieve(message)
        self.notify("context_retrieved", {"query": message, "context": context})
        
        # Call LLM
        call_id = generate_id()
        self.notify("llm_call_started", {"call_id": call_id, "prompt": message})
        response = self.llm.complete(message, context)
        self.notify("llm_call_completed", {"call_id": call_id, "response": response, "tokens": response.tokens})
        
        # Return response
        self.notify("agent_response", {"response": response.text})
        return response.text
```

The agent announces key events at appropriate moments. Observers react independently.

**5. Register Observers:**
Wire observers to subjects at initialization or configuration time:

```python
agent = Agent()
agent.attach(PerformanceMonitor())
agent.attach(CostTracker())
agent.attach(ConversationLogger())

# Later, add more observers without modifying agent
agent.attach(SecurityAuditor())
agent.attach(UIUpdater())
```

This registration is external to both subject and observers, enabling flexible configuration.

**6. Handle Observer Failures:**
Consider what happens if an observer raises an exception. Should it stop other observers from being notified? Typically no:

```python
def notify(self, event_type: str, data: dict) -> None:
    """Notify all observers, handling failures gracefully."""
    for observer in self._observers:
        try:
            observer.update(event_type, data)
        except Exception as e:
            log_error(f"Observer {observer} failed: {e}")
            # Continue notifying other observers
```

Isolate observer failures to prevent one broken observer from breaking the system.

**7. Optimize Notification (When Needed):**
For high-frequency events or many observers, consider optimizations:
- **Async notifications**: Use async/await or threading to notify observers concurrently
- **Filtering**: Let observers specify which event types they care about, only notify relevant observers
- **Batching**: Collect events and notify in batches rather than individually
- **Priority**: Notify critical observers first (though this adds complexity)

## Think of It Like This
Imagine you're a news publisher (the subject) and you have subscribers (observers) interested in your news. In the old days, each subscriber would call you every morning asking "Got any news?" (polling). Inefficient and annoying for both parties.

With the Observer Pattern, subscribers sign up for your mailing list. You don't know who they are or what they do with your news—maybe they're individuals reading over coffee, maybe they're businesses analyzing trends, maybe they're researchers archiving content. You just know they're on your list. When you publish news (state change), you send it to everyone on the list automatically. Subscribers receive notifications and handle them however they want.

Subscribers can join anytime (attach observer), leave anytime (detach observer), and you can keep publishing regardless of who's subscribed. If you want to add a new feature like breaking news alerts, you just send those notifications too—existing subscribers automatically receive them if they're still on the list.

This is the Observer Pattern: the publisher (subject) maintains a subscriber list and sends notifications, subscribers (observers) react to notifications independently, and neither is tightly coupled to the other. The publisher doesn't control what subscribers do, and subscribers don't control when publications happen—clean separation of concerns.

## The "So What?" Factor
**If you use this:**
- Your core logic stays clean—agent code focuses on agent behavior without tangling in logging, metrics, UI updates, or monitoring concerns
- Adding new functionality is safe—new observers (audit logging, performance monitoring, cost tracking) don't require modifying tested code
- Testing becomes practical—test the agent without observers, test observers without the agent, or mix-and-match for different test scenarios
- System observability improves—every component can observe relevant events without intrusive instrumentation in business logic
- Parallel development works—different developers build different observers simultaneously without conflicts
- Configuration flexibility emerges—enable/disable observers through configuration, support different observer sets for dev/staging/prod
- Real-time systems become feasible—UI components observe agent state and update instantly without polling or tight coupling

**If you don't:**
- Your core logic becomes tangled—agent code directly calls logger, metrics, UI, auditing, making it complex and hard to understand
- Adding functionality requires modification—every new monitoring or integration capability means editing and re-testing agent code
- Testing requires everything—you can't test the agent without all its dependencies or extensive mocking
- Observability suffers—instrumentation is scattered, inconsistent, and tightly coupled to business logic
- Development serializes—adding new observers means coordinating with agent code owners, creating bottlenecks
- Configuration becomes rigid—observers are hardcoded, requiring code changes to enable/disable monitoring or adjust instrumentation
- Real-time systems use polling—wasteful, high-latency checking rather than efficient event notifications

## Practical Checklist
Before implementing, ask yourself:
- [ ] **Is there a one-to-many relationship?** Do multiple components need to react to one component's events or state changes?
- [ ] **Is the subject unaware of observer details?** Can the subject notify observers without knowing what they do with notifications?
- [ ] **Are observers independent?** Can observers be added, removed, or changed without affecting the subject or each other?
- [ ] **Are notifications event-driven?** Does the subject know when to notify, or do you need observers to poll?
- [ ] **Is the observer interface clear?** Have I defined what information observers receive and when they're notified?
- [ ] **How do I handle observer failures?** If an observer throws an exception, does that stop other observers from being notified?
- [ ] **Is performance acceptable?** For high-frequency events or many observers, have I considered async notifications or filtering?
- [ ] **How do observers register?** Is there a clear mechanism for attaching/detaching observers, or is it hardcoded?

## Watch Out For
⚠️ **Memory Leaks from Undetached Observers**: When observers register with subjects, the subject holds references to them. If observers aren't explicitly detached when no longer needed, they remain in memory even if your code no longer references them. This causes memory leaks—observers accumulate but never get garbage collected. Always provide and use detach/unsubscribe mechanisms. Consider weak references for observers that should be automatically released when no longer in use elsewhere.

⚠️ **Notification Order Dependencies**: If observers depend on other observers having already processed notifications, you've created hidden coupling. Observer A might expect Observer B to have updated shared state before A runs. This violates the pattern's independence principle. Observers should be order-independent. If ordering matters, you might need a different pattern (mediator, coordinator) or explicit orchestration rather than simple observation.

⚠️ **Cascading Updates**: An observer receiving a notification might trigger another event, which notifies observers, which trigger more events—cascading notifications that are hard to understand and debug. If Observer A reacts to event X by causing event Y, and Observer B reacts to Y by causing Z, you've created implicit chains that are difficult to reason about. Keep observer reactions simple and avoid deep cascades. Consider using event queues or explicit workflow patterns for complex chains.

⚠️ **Performance Bottlenecks**: Notifying many observers synchronously can be slow, especially if observers do expensive work (database writes, API calls, computations). This blocks the subject until all observers finish. For performance-critical paths, use async notifications, threading, or background processing. Don't let slow observers impact subject performance. Consider filtering mechanisms so only relevant observers are notified for specific events.

⚠️ **Observer Explosion**: It's easy to overuse the pattern, creating dozens of granular observers for every tiny event. This fragments logic across many small observers that are hard to understand collectively. Balance observer granularity—don't create an observer for every single line of code that might be interesting. Group related observations into cohesive observers. Too many observers becomes its own maintenance burden.

⚠️ **Implicit Dependencies on Notification Content**: Observers that assume specific data structures or fields in notifications become brittle. If the subject changes what data it includes in notifications, observers break. Define clear event schemas or use typed event objects rather than generic dictionaries. Version events if breaking changes are needed. Treat notification contracts as stable APIs.

⚠️ **Lack of Error Isolation**: If one observer raises an exception and you don't catch it, subsequent observers might not be notified. Always wrap observer calls in try-catch blocks so one failing observer doesn't break others. Log observer failures but continue notifying. Decide whether observer failures should affect the subject's behavior (usually they shouldn't—observations are side effects, not core logic).

⚠️ **Testing Challenges**: While observers enable testing subjects without observers, they can make integration testing harder—you must ensure all necessary observers are registered in tests. Test environments might have different observer configurations than production, leading to "works in test, fails in prod" scenarios. Use consistent observer registration patterns and consider test-specific observer configurations that verify expected notifications.

## Connections
**Builds On:** 
- [Design Pattern](design_pattern.md) - Observer is one of the classic Gang of Four behavioral patterns
- [Loose Coupling](loose_coupling.md) - Observer Pattern achieves loose coupling between subjects and observers
- [Separation of Concerns](separation_of_concerns.md) - Separates core business logic (subject) from cross-cutting concerns (observers)

**Works With:** 
- [Inversion of Control](inversion_of_control.md) - Observer Pattern is a form of IoC where the subject calls observer code
- [Event-Driven Architecture](../System_Architecture/event_driven_architecture.md) - Observer Pattern is fundamental to event-driven systems
- [Pub-Sub Pattern](../System_Architecture/pub_sub.md) - More decoupled variation using message brokers
- [Strategy Pattern](strategy_pattern.md) - Both patterns use polymorphism; Observer for notifications, Strategy for algorithms
- [Decorator Pattern](decorator_pattern.md) - Can combine—observers can wrap subjects to add observation capabilities
- [Singleton Pattern](singleton_pattern.md) - Often used together for global event buses or notification managers

**Leads To:** 
- [Event-Driven Architecture](../System_Architecture/event_driven_architecture.md) - Architectural pattern built on observer concepts at system scale
- [Reactive Programming](../System_Architecture/event_driven_architecture.md) - Modern evolution treating event streams as first-class async sequences
- [Message Queue](../System_Architecture/message_queue.md) - Persistent, distributed implementation of observer pattern for reliable event delivery
- [CQRS Pattern](../System_Architecture/cqrs_pattern.md) - Uses observer-like concepts for event sourcing and read model updates

**Related Patterns:**
- [Mediator Pattern](../Agent_and_Orchestration/orchestration.md) - Alternative to Observer when you need centralized coordination rather than direct observation
- [Agent Framework](../Agent_and_Orchestration/agent_framework.md) - Modern frameworks use Observer Pattern extensively for callbacks and monitoring
- [Multi-Agent System](../Agent_and_Orchestration/multi-agent_system.md) - Agents often observe each other's actions through observer patterns

## Quick Decision Guide
**Use this when you need to:** 
- Enable multiple components to react to events without tight coupling (logging, metrics, UI, auditing all observe agent actions)
- Build observable systems where instrumentation doesn't invade business logic
- Support dynamic behaviors where observers can be added/removed at runtime
- Implement event-driven agent systems where components react to state changes
- Create plugin architectures where plugins observe and react to host application events
- Build real-time monitoring and dashboards that update as systems execute
- Enable cross-cutting concerns (logging, monitoring, auditing) without scattering them through core logic

**Skip this when:** 
- You have a one-to-one relationship (one observer for one subject)—just call the dependency directly; Observer Pattern is overkill
- Observers need complex coordination or ordering—use orchestration patterns (workflow engines, mediators) instead
- The subject has only a couple of events and they're simple—direct method calls might be clearer than observer infrastructure
- You're building simple systems where observer overhead exceeds its benefits
- Observers are tightly coupled to the subject anyway—if observers depend on intimate subject knowledge, you haven't gained loose coupling
- You need guaranteed delivery and persistence—use message queues, not in-memory observer lists

## Further Exploration
- 📖 **Design Patterns: Elements of Reusable Object-Oriented Software** (1994) - Original Gang of Four documentation of Observer Pattern
- 📖 **Reactive Programming with RxJS** (2020) by Sergi Mansilla - Modern reactive observer patterns for async event streams
- 🎯 **"Observer Pattern in AI Agent Systems"** (2025) - LangChain callbacks, agent monitoring, and event-driven agent architectures
- 💡 **"Event-Driven Architecture Patterns"** - Observer Pattern as foundation for event-driven systems
- 📖 **Head First Design Patterns** (2004) by Freeman & Freeman - Accessible explanation of Observer with practical examples
- 🎯 **"Avoiding Observer Pattern Pitfalls"** - Memory leaks, cascading updates, and performance considerations
- 💡 **"Push vs. Pull Observer Models"** - Trade-offs between pushing data to observers vs. observers pulling from subjects
- 📖 **Pattern-Oriented Software Architecture, Vol. 2** (2000) - Observer Pattern variations for distributed and concurrent systems

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*