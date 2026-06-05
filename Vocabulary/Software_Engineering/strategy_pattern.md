# Strategy Pattern

## At a Glance
| | |
|---|---|
| **Category** | Design Pattern / Behavioral Pattern |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 2-3 days to understand, 1-2 weeks to apply confidently |
| **Prerequisites** | Basic object-oriented programming, understanding of interfaces/protocols |

## One-Sentence Summary
The Strategy Pattern defines a family of interchangeable algorithms, encapsulates each one behind a common interface, and makes them swappable at runtime—so your code can choose different behaviors without changing its structure.

## Why This Matters to You
If you're building AI agents or intelligent systems, you constantly face situations where the "best" approach depends on context: which LLM to use for this query, which retrieval strategy fits this use case, which error handling approach works for this scenario. The Strategy Pattern lets you package these different approaches as plug-and-play components that your system selects at runtime. Instead of littering your codebase with if-else chains or switch statements checking which approach to use, you define each approach once, give it a consistent interface, and let your system swap between them cleanly. This becomes critical when you're experimenting with different AI techniques, A/B testing agent behaviors, or building systems that need to adapt their approach based on user preferences, data characteristics, or performance requirements. The Strategy Pattern is how professional systems achieve flexibility without chaos.

## The Core Idea
### What It Is
The Strategy Pattern solves a common problem: you need different ways to accomplish the same task, and you want to choose between them without rewriting your code every time. Imagine you're building an AI agent that answers questions. Sometimes it should use a fast, cached response. Sometimes it should query a knowledge graph. Sometimes it should invoke a heavyweight LLM. All three are "answering strategies," but they work differently.

The pattern structures this with three components. First, a **Strategy interface** defines the contract—what all strategies must be able to do. In our example, that might be an `AnswerStrategy` interface with a method `generate_answer(question)`. Second, **Concrete strategies** implement that interface, each one encapsulating a different algorithm or approach. You'd have `CachedAnswerStrategy`, `GraphQueryStrategy`, and `LLMAnswerStrategy`, each implementing `generate_answer` differently. Third, a **Context** class uses strategies without knowing which specific one it's using—it just knows it has something that can generate answers.

What makes this powerful is runtime flexibility. Your context doesn't hard-code which strategy to use. Instead, you inject the strategy when you create the context or swap it dynamically based on conditions. Your agent might start with the cached strategy for speed, fall back to the graph query strategy if there's no cache hit, and only invoke the expensive LLM strategy as a last resort. The calling code doesn't change—it just works with whatever strategy is active.

In 2026 AI systems, the Strategy Pattern appears everywhere because experimentation is continuous. You're constantly trying new prompting techniques, different embedding models, alternative retrieval algorithms. The Strategy Pattern lets you package each approach cleanly, compare them side-by-side, and switch between them without refactoring your entire codebase. Modern agent frameworks often provide strategy-based abstractions: you plug in your preferred LLM client, vector store, or tool execution handler, and the framework handles the rest.

### What It Isn't
The Strategy Pattern is not about inheritance hierarchies where subclasses override methods. That's the Template Method pattern—where the structure is fixed and subclasses fill in specific steps. Strategy Pattern is about composition, not inheritance: you compose your context with a strategy object rather than subclassing to change behavior. This gives you runtime flexibility that inheritance can't provide.

It's also not the same as the State Pattern, though they look similar. State Pattern models an object that changes its behavior because its internal state changed (a connection goes from "connecting" to "connected" to "disconnected"). Strategy Pattern models different algorithms for the same problem, chosen based on external factors or preferences. If your agent switches retrieval methods because the user changed a preference setting, that's Strategy. If it switches because its internal state machine moved from one state to another, that's State. The implementation might look similar, but the intent differs.

Don't confuse Strategy Pattern with just using function pointers or callbacks. Yes, in languages with first-class functions, you can pass functions around to achieve similar flexibility. Strategy Pattern formalizes this with a clear interface, makes strategies testable and composable, and works well in languages that emphasize objects and types. It's the "grown-up" version of passing functions around—with contracts, documentation, and structure.

## How It Works
1. **Define the Strategy Interface**: Create an interface or abstract class that declares the method(s) all strategies must implement. This is your contract—it says "any strategy can be used here as long as it provides these capabilities." For an AI agent that needs different reasoning approaches, you might define `ReasoningStrategy` with a method `reason(context, question) -> answer`.

2. **Implement Concrete Strategies**: Create classes that implement your strategy interface, each one encapsulating a different algorithm or approach. `ChainOfThoughtStrategy` might implement step-by-step logical reasoning. `RetrievalAugmentedStrategy` might pull context from a knowledge base first. `FastCachedStrategy` might check a lookup table. Each strategy is self-contained—all the logic for that approach lives in one place, making it easy to understand, test, and maintain.

3. **Create the Context**: Build a class that uses strategies without knowing their internal details. The context holds a reference to a strategy (often as an instance variable or property) and delegates work to it. Your `Agent` class might have a `reasoning_strategy` attribute and call `self.reasoning_strategy.reason(...)` when it needs to reason. The agent doesn't know or care which specific strategy is plugged in—it just knows the interface.

4. **Enable Strategy Selection**: Provide ways to set or change the strategy. This might happen at initialization (`Agent(strategy=ChainOfThoughtStrategy())`), through configuration (`agent.set_strategy(new_strategy)`), or dynamically based on runtime conditions (if query is simple, use fast strategy; if complex, use thorough strategy). The key is that the calling code chooses the strategy, not the context itself.

5. **Execute Through the Interface**: When your context needs to perform the strategy-dependent operation, it calls the method on the strategy interface. The actual implementation that runs depends on which concrete strategy is active, but the calling code looks the same regardless. This uniform interface is what makes strategies truly interchangeable.

6. **Optionally Share Context State**: If strategies need access to shared data or configuration, the context can pass itself as a parameter or provide accessor methods. For example, your reasoning strategy might need access to the agent's memory or tool inventory. Design this carefully—strategies should stay loosely coupled to the context, depending only on the data they truly need.

## Think of It Like This
Imagine you're traveling to work and you have three options: drive your car, take the bus, or bike. All three are "transportation strategies" that accomplish the same goal—getting you to work. Each has different characteristics: driving is fast but expensive, the bus is cheap but slower, biking is free but weather-dependent. Your decision of which to use depends on factors like weather, how much time you have, parking availability, or your fitness goals.

The Strategy Pattern is exactly this. Your commute planner (the context) doesn't need to contain all the logic for driving, busing, and biking mixed together with nested if-statements. Instead, it says "I need transportation" and uses whatever TransportationStrategy you've configured. Tomorrow, if you add "take the train" as a new option, you don't modify your planner code—you just implement a new TrainStrategy and plug it in. The planner works the same way regardless of how you're traveling, and you can switch strategies based on the day's conditions without rewriting anything.

## The "So What?" Factor
**If you use this:**
- Your AI systems become experimentation-friendly—you can test different LLM prompting strategies, retrieval algorithms, or reasoning approaches by swapping strategies, not by rewriting core logic
- Code stays clean and focused—each algorithm lives in its own class with a single responsibility, rather than sprawling across giant conditional blocks
- Adding new approaches is safe and non-invasive—you implement a new strategy class without touching existing code, reducing the risk of breaking working functionality
- A/B testing becomes architectural—you can route different users to different strategies, measure outcomes, and pick winners based on data rather than guessing
- Runtime adaptation becomes possible—your agent can switch strategies based on query complexity, user tier, time constraints, or available resources
- Testing becomes granular—you can unit test each strategy in isolation, mocking dependencies cleanly, then integration test the context with different strategies
- Documentation improves naturally—when each approach is a named class with clear responsibilities, new developers understand the system faster than when logic is scattered across conditional branches

**If you don't:**
- Your code fills with nested conditionals that check which approach to use, making the logic hard to follow and brittle to change
- Adding new algorithms means modifying existing code, risking regressions in already-working logic and violating the [Open-Closed Principle](open_closed_principle.md)
- Testing becomes painful—you can't easily test one algorithm in isolation because it's tangled with selection logic and other approaches
- Experimentation requires code changes rather than configuration changes—trying a new prompting technique means editing production code paths instead of plugging in a new strategy
- Runtime flexibility is lost—you can't change behavior based on context or user preferences without deploying new code
- Code duplication creeps in—similar logic appears in multiple places because there's no clean way to package and reuse algorithmic variations
- Your agent system becomes rigid—instead of adapting to different scenarios, it's locked into one-size-fits-all approaches that don't optimize for specific use cases

## Practical Checklist
Before implementing, ask yourself:
- [ ] **Do I have multiple algorithms for the same problem?** If you only have one way to do something and no plans for alternatives, the Strategy Pattern might be premature abstraction.
- [ ] **Do these algorithms truly need to be interchangeable?** If the "different approaches" require different inputs or produce incompatible outputs, they might not fit cleanly behind a common interface.
- [ ] **Will I need to switch strategies at runtime?** If the choice is made once at compile time or deployment time and never changes, simpler approaches (like configuration files or build flags) might suffice.
- [ ] **Are strategies genuinely independent?** If your algorithms need to share complex state or coordinate with each other, the Strategy Pattern's clean separation might not work well—consider whether you actually need a different pattern.
- [ ] **Have I defined a clear interface?** The strategy interface should capture the essence of what all strategies do, without leaking implementation details of specific strategies. Get this right before implementing concrete strategies.
- [ ] **How will strategies access necessary data?** Will you pass everything as method parameters, give strategies access to context, or use a hybrid approach? Design this carefully to balance flexibility and coupling.
- [ ] **What's my strategy selection mechanism?** Will you inject strategies at initialization, provide a factory to create them, let users configure them, or select them automatically based on heuristics? This decision affects your system's usability and testability.

## Watch Out For
⚠️ **Over-abstracting simple decisions**: If you have two similar if-statements that choose between approaches, you don't necessarily need Strategy Pattern. The pattern pays off when you have multiple complex algorithms or when runtime flexibility matters. Don't create elaborate strategy hierarchies for trivial decisions—sometimes a simple conditional is clearer.

⚠️ **Strategy explosion**: It's tempting to create a strategy for every tiny variation, leading to dozens of strategy classes that could have been handled with parameters or configuration. Balance granularity: create strategies for meaningfully different algorithms, not for every parameter combination. If your strategies differ only in constant values, consider parameterizing a single strategy instead.

⚠️ **Leaky abstractions**: The strategy interface should hide implementation details, but it needs to expose enough to be useful. If every new strategy forces you to modify the interface or add context-specific methods, your abstraction is leaking. Design interfaces carefully: they should be stable as you add new strategies, not constantly evolving to accommodate special cases.

⚠️ **Context-strategy coupling**: Strategies should depend on the context through well-defined interfaces, not by reaching into context internals. If your strategy needs access to ten different context properties, either you're passing too much responsibility to strategies, or your context is doing too much and needs refactoring. Keep strategies focused and minimize what they need from the context.

⚠️ **Forgetting about composition**: Sometimes you need to combine strategies rather than choose between them. The Strategy Pattern as classically defined assumes one strategy at a time, but real systems often need pipelines or fallback chains (try strategy A, if it fails try B). Consider whether you need strategy composition patterns like Chain of Responsibility or Decorator alongside your basic strategies.

⚠️ **Making strategy selection too complex**: If the logic for choosing which strategy to use becomes as complicated as the strategies themselves, you've just moved complexity around rather than managing it. Strategy selection should be straightforward—based on clear criteria like performance requirements, data characteristics, or explicit user choice. If selection logic is convoluted, you might need to rethink your strategy boundaries.

⚠️ **Ignoring strategy lifecycle**: Strategies might have initialization costs, maintain state, or need cleanup. Don't treat them as throwaway objects if they're expensive to create or hold resources. Consider pooling strategies, reusing instances, or explicitly managing their lifecycle if performance matters. For example, if your LLMStrategy holds a connection to an expensive model service, you don't want to create and destroy it on every request.

⚠️ **Not testing strategy combinations**: If your context can work with any strategy, test it with multiple strategies to ensure your interface is truly implementation-agnostic. Also test invalid cases: what happens if someone passes a null strategy or a strategy that throws exceptions? Defensive programming matters—the Strategy Pattern gives flexibility, but that flexibility shouldn't enable runtime errors.

## Connections
**Builds On:** 
- [Design Pattern](design_pattern.md) - Strategy Pattern is one of the classic Gang of Four behavioral patterns, part of the design pattern canon
- [Dependency Injection](dependency_injection.md) - Strategies are typically injected into contexts, exemplifying dependency injection principles
- [Open-Closed Principle](open_closed_principle.md) - Strategy Pattern lets you extend behavior (by adding new strategies) without modifying existing code

**Works With:** 
- [Factory Pattern](factory_pattern.md) - Often used together: a factory creates the appropriate strategy based on conditions, then injects it into the context
- [Adapter Pattern](adapter_pattern.md) - When integrating third-party libraries with different interfaces, wrap them in adapters that implement your strategy interface
- [Decorator Pattern](decorator_pattern.md) - Decorators can wrap strategies to add cross-cutting concerns (logging, caching, metrics) without modifying strategy code
- [Separation of Concerns](separation_of_concerns.md) - Strategy Pattern enforces separation by isolating each algorithm in its own class
- [Loose Coupling](loose_coupling.md) - Contexts depend on strategy interfaces, not concrete implementations, achieving loose coupling

**Leads To:** 
- [Plugin Architecture](../System_Architecture/hexagonal_architecture.md) - Strategy Pattern is foundational to plugin systems where external components provide different implementations
- [Agent Framework](../Agent_and_Orchestration/agent_framework.md) - Modern agent frameworks use strategy-like patterns for swappable LLM backends, tool handlers, and memory systems
- [Decision Making](../Agent_and_Orchestration/decision_making.md) - Complex decision systems often use strategies to encapsulate different decision algorithms
- [A/B Testing](../Testing_and_Evaluation/a_b_testing.md) - Strategy Pattern enables clean A/B testing by routing users to different strategy implementations

**Related Patterns:**
- [Observer Pattern](observer_pattern.md) - Another behavioral pattern, but focused on event notification rather than algorithm selection
- [Singleton Pattern](singleton_pattern.md) - Sometimes strategies are implemented as singletons if they're stateless and can be shared

## Quick Decision Guide
**Use this when you need to:** 
- Swap algorithms or behaviors at runtime based on conditions, user preferences, or external factors
- Avoid polluting your codebase with conditional logic that selects between different approaches
- Experiment with different techniques (LLM prompting strategies, retrieval methods, optimization algorithms) without rewriting core code
- Enable plugin architectures where third parties can provide alternative implementations
- A/B test different approaches by routing users to different strategy implementations
- Comply with the Open-Closed Principle: add new behaviors without modifying existing code
- Make each algorithm independently testable and maintainable in its own class

**Skip this when:** 
- You have only one algorithm and no realistic expectation of alternatives—don't over-engineer for hypothetical future needs
- The "different approaches" aren't truly interchangeable (different inputs, outputs, or contracts)—you might need separate abstractions rather than forcing them behind one interface
- Strategy selection happens once at compile time and never changes—simpler configuration mechanisms might be more appropriate
- The algorithms are trivial (a few lines of code)—the Strategy Pattern's structure would add more complexity than it removes
- Strategies would need extensive coupling to the context to function—if strategies require deep knowledge of context internals, the separation isn't clean enough for this pattern
- You're working in a functional programming paradigm where passing functions is more idiomatic than creating strategy objects—use the tools that fit your language and style

## Further Exploration
- 📖 **Design Patterns: Elements of Reusable Object-Oriented Software** (1994) by Gang of Four - The original canonical description of Strategy Pattern (still relevant in 2026)
- 🎯 **"Strategy Pattern in Python for AI Systems"** - Practical tutorial showing Strategy Pattern for swappable LLM backends, with code examples and anti-patterns
- 💡 **"Behavioral Design Patterns for Agent Architectures"** (2025) - Research paper exploring how classic patterns like Strategy adapt to autonomous agent development
- 📖 **Head First Design Patterns** (2020 edition) - Accessible, visual introduction to Strategy Pattern with memorable examples
- 🎯 **LangChain / LlamaIndex Source Code** - Real-world examples of Strategy-like patterns in production AI frameworks (swappable LLM clients, vector stores, retrievers)
- 💡 **"From If-Else to Strategy: Refactoring AI Systems"** - Case study of refactoring a production AI agent from conditional logic to Strategy Pattern, with performance and maintainability metrics
- 📖 **Refactoring: Improving the Design of Existing Code** (2019) by Martin Fowler - Includes "Replace Conditional with Polymorphism" refactoring that leads to Strategy Pattern

---
*Added: May 18, 2026 | Updated: May 18, 2026 | Confidence: High*