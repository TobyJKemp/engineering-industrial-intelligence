# Decorator Pattern

## At a Glance
| | |
|---|---|
| **Category** | Structural Design Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | Hours to understand, days to apply effectively |
| **Prerequisites** | Object-oriented programming, interfaces/abstract classes, composition vs inheritance |

## One-Sentence Summary
Decorator Pattern is a structural design pattern that allows you to dynamically add new behaviors or responsibilities to objects by wrapping them in decorator objects that implement the same interface—enabling flexible, composable functionality enhancement without modifying original code or creating complex inheritance hierarchies, making it ideal for layering cross-cutting concerns like logging, caching, retry logic, and validation onto AI system components.

## Why This Matters to You
You're building an AI agent that calls an LLM API. Initially, you just need to make the call and get a response—simple function. But then requirements evolve: you need to add retry logic for transient failures, then caching to reduce costs, then logging for debugging, then rate limiting to avoid quota exhaustion, then token counting for cost tracking, then input validation to catch malformed prompts, then response parsing to extract structured data. You could modify the original function to handle all this, creating a 300-line monster that's hard to test and maintain. Or you could create separate classes for each scenario: `LLMClient`, `RetryableLLMClient`, `CachedLLMClient`, `LoggedLLMClient`, etc.—but you need combinations (cached AND logged AND retried), leading to class explosion. **This is where Decorator Pattern shines**—it lets you compose behaviors dynamically: wrap the base LLM client in a retry decorator, wrap that in a cache decorator, wrap that in a logging decorator. Each decorator adds one responsibility, implements the same interface, and can be combined in any order. `LoggingDecorator(CacheDecorator(RetryDecorator(LLMClient())))` gives you all three behaviors without modifying `LLMClient` or creating specialized subclasses. For AI systems in 2026, decorators are essential infrastructure: AI operations are expensive (need caching), unreliable (need retry), non-deterministic (need logging), rate-limited (need throttling), and security-sensitive (need validation). Rather than building monolithic components with all concerns baked in, you build focused components and layer concerns via decorators. This creates composable, testable, maintainable systems. You test each decorator independently: retry logic without cache complexity, cache without logging overhead. You compose decorators based on needs: production gets full stack (validation + retry + cache + logging + rate limiting), development gets simpler stack (logging only), tests get minimal stack (no decorators, testing core logic). The pattern follows Open-Closed Principle: systems are open to extension (add new decorators) but closed to modification (don't touch core components). This matters because AI systems evolve rapidly—new observability requirements, new cost optimizations, new reliability patterns—and decorators let you add capabilities without destabilizing existing code.

## The Core Idea
### What It Is
Decorator Pattern is one of the classic Gang of Four design patterns, published in 1994 but highly relevant for modern AI systems. The pattern provides an alternative to inheritance for extending functionality. Instead of creating subclasses with additional behavior, you create decorator objects that wrap the original object and add behavior while maintaining the same interface.

The pattern has four key participants:

**Component Interface** - Defines the common interface that both concrete components and decorators must implement. For AI systems, this might be `LLMProvider` with method `generate(prompt: str) -> str` or `Tool` with method `execute(input: dict) -> dict`. The interface establishes the contract that all participants must honor.

**Concrete Component** - The original object being decorated. This is the core implementation without additional behaviors. Example: `OpenAIClient` that makes direct API calls to OpenAI, or `DatabaseTool` that executes SQL queries. Concrete components focus on their primary responsibility without cross-cutting concerns.

**Decorator Base** - An abstract decorator that implements the Component interface and holds a reference to a Component. This serves as the foundation for concrete decorators. The base decorator typically delegates all operations to the wrapped component, allowing concrete decorators to override specific methods.

**Concrete Decorators** - Specific decorator implementations that add particular behaviors. Examples: `RetryDecorator` adds retry logic, `CacheDecorator` adds caching, `LoggingDecorator` adds logging. Each decorator wraps a component, delegates to it, and adds its specific behavior before/after/around the delegation.

The key mechanism is **wrapping and delegation**: decorators wrap components (holding references to them), implement the same interface, delegate calls to wrapped components, and add behavior around the delegation. This creates layers of functionality like Russian nesting dolls—each layer adds something, then delegates to the next layer.

For AI systems in 2026, common decorators include:

**Retry Decorator** - Wraps AI operations (LLM calls, API requests) and automatically retries on transient failures. Implements exponential backoff, respects retry-after headers, distinguishes transient errors (503, timeout) from permanent errors (401, 404), and eventually gives up after max attempts. Critical for production AI systems where services have occasional hiccups.

**Cache Decorator** - Wraps expensive operations and caches results. For LLM calls with identical prompts and parameters, returns cached responses instead of making new calls. Manages cache keys (hash of prompt + parameters), TTL (time-to-live), invalidation strategies, and storage backends (memory, Redis, disk). Can reduce costs by 50-80% for systems with repeated queries.

**Logging Decorator** - Wraps operations and logs inputs, outputs, timing, and errors. For AI systems, logs prompts sent, responses received, token counts, latency, model used, and any errors. Essential for debugging non-deterministic AI behavior—when model gives wrong answer, logs show exactly what it was given. Implements structured logging for queryability.

**Rate Limiting Decorator** - Wraps operations and enforces rate limits to avoid quota exhaustion. Tracks requests per time window (per second, per minute, per hour), blocks when limit reached, implements token bucket or leaky bucket algorithms. Protects against runaway costs from bugs or attacks (infinite loop calling LLM would drain account without rate limiting).

**Validation Decorator** - Wraps operations and validates inputs/outputs. For LLM calls, validates prompt isn't empty, doesn't exceed token limits, doesn't contain injection attempts. Validates responses match expected schema (if expecting JSON, verify it's valid JSON). Catches errors early before expensive operations or downstream failures.

**Authentication Decorator** - Wraps operations and adds authentication credentials. Manages API keys, refreshes tokens, handles auth failures. Separates authentication concerns from business logic—core component doesn't know about auth; decorator handles it transparently.

**Metrics Decorator** - Wraps operations and emits metrics. Counts invocations, measures latency, tracks success/failure rates, records costs (tokens used). Feeds monitoring dashboards and alerts. Essential for production observability.

**Circuit Breaker Decorator** - Wraps operations and implements circuit breaker pattern. After N consecutive failures, stops calling the wrapped service (circuit "opens"), returns errors immediately for a timeout period, then tries again ("half-open"). Prevents cascading failures when downstream services are down.

**Tracing Decorator** - Wraps operations and adds distributed tracing spans. Integrates with OpenTelemetry or similar frameworks, creates spans for each operation, propagates trace context, enables end-to-end request tracking. Critical for debugging complex AI workflows with multiple service calls.

The power of decorators is **composability**: you can stack multiple decorators, each adding specific behavior, in any order. The order matters: `LoggingDecorator(CacheDecorator(client))` logs every call including cache hits, while `CacheDecorator(LoggingDecorator(client))` only logs cache misses (cache shortcuts logging). This flexibility enables tuning behavior per environment or use case.

In 2026, decorator frameworks for AI systems often provide:
- **Declarative decorator composition**: Use Python `@decorators` or configuration to specify decorator stack
- **Conditional decorators**: Apply decorators based on environment (prod vs dev) or configuration
- **Smart decorator ordering**: Frameworks automatically order decorators optimally (e.g., cache always outside retry, validation always outermost)

### What It Isn't
Decorator Pattern is not the same as Python's `@decorator` syntax, though they're related concepts. Python decorators are syntactic sugar for wrapping functions. The Decorator Pattern is an object-oriented design pattern about wrapping objects. Both involve wrapping, but Decorator Pattern is architectural—about composing object behaviors—while Python `@decorator` is syntactic—about transforming functions. They can be used together (Python `@decorator` implementing Decorator Pattern), but they're distinct concepts.

Decorator Pattern also isn't Proxy Pattern, though they look similar (both wrap objects, both implement same interface). The distinction is intent: Proxy controls access to an object (lazy initialization, access control, remote communication), while Decorator adds responsibilities to an object. In practice, they're closely related—a caching decorator could be called a caching proxy. The difference is philosophical more than technical.

Decorator Pattern isn't about modifying objects in-place. Decorators don't change the original object; they wrap it in a new object that adds behavior. The original remains unchanged and usable independently. This is composition, not mutation.

Finally, decorators aren't always the right choice. For static, class-wide behavior extensions, inheritance might be simpler. For single-responsibility enhancements, direct modification might be clearest. Decorators shine when you need: dynamic composition (behavior determined at runtime), multiple orthogonal concerns (logging + caching + retry), or flexible combinations (different decorator stacks for different use cases).

## How It Works
Implementing Decorator Pattern effectively requires systematic approach:

1. **Define Component Interface**: Start by defining the interface that both concrete components and decorators will implement. Make it focused: `LLMProvider` with `generate()`, `Tool` with `execute()`, `DataSource` with `query()`. The interface should represent core functionality without cross-cutting concerns. Use abstract base classes or protocols for type safety.

2. **Implement Concrete Component**: Build the core implementation that handles primary responsibility without decorations. Example: `OpenAIClient` that makes direct API calls, handling only the essential logic (construct request, make HTTP call, parse response). Keep it focused—no logging, no retry, no caching. Test it thoroughly in isolation.

3. **Create Decorator Base Class**: Build an abstract decorator that implements the component interface and holds a reference to another component (the wrapped object). The base typically delegates all calls to the wrapped component unchanged. This establishes the delegation pattern concrete decorators will follow.

4. **Implement Concrete Decorators**: Create specific decorators for each cross-cutting concern. Each decorator extends the base, adds its specific behavior, and delegates to wrapped component. Example: `RetryDecorator.__init__(wrapped_component, max_attempts, backoff)` stores wrapped component, then `RetryDecorator.generate(prompt)` implements retry logic around `self.wrapped.generate(prompt)`. Keep each decorator focused on one responsibility.

5. **Compose Decorators**: Build decorator stacks by wrapping components in multiple decorators. Order matters for some combinations: validation should be outermost (catch bad inputs before expensive operations), caching should be before retry (don't retry for cached results), metrics should be outermost (measure everything including decorator overhead). Document recommended ordering.

6. **Test Decorators Independently**: Write tests for each decorator in isolation, using mock wrapped components. Test retry logic with controlled failures, test cache with repeated calls, test validation with invalid inputs. Independent testing ensures each decorator works correctly before composition.

7. **Test Decorator Compositions**: Test common decorator stacks end-to-end. Verify caching + retry works correctly (cached results aren't retried), logging + validation captures both concerns, metrics + all others measures everything. Test order-dependent behaviors.

8. **Use Dependency Injection**: Don't hardcode decorator stacks in component code. Use dependency injection or factory patterns to construct decorator stacks based on configuration. This enables different stacks per environment: production uses full stack, tests use minimal stack, development uses custom stack.

9. **Document Decorator Behaviors**: Clearly document what each decorator does, any ordering constraints, configuration options, and performance implications. Example: "CacheDecorator: Caches results based on input hash. Configuration: TTL (default 3600s), max_size (default 1000 entries). Note: Should be placed outside RetryDecorator to avoid caching errors."

10. **Implement Transparent Pass-Through**: Ensure decorators implement the full interface correctly, including edge cases. If interface has multiple methods, all must be wrapped. If methods have keyword arguments, decorators must pass them through. Incomplete decorators break composition.

11. **Handle Errors Gracefully**: Decorators should fail gracefully. If logging decorator can't write logs, it shouldn't crash the operation—log the logging failure and continue. If cache decorator can't reach cache, fall through to wrapped component. Decorators are enhancements, not critical dependencies (usually).

12. **Monitor Decorator Performance**: Track overhead added by decorators. Measure latency impact: how much does each decorator add? Profile in production: is logging slowing things down? Is cache lookup overhead negating benefits? Optimize or remove decorators that don't justify their cost.

## Think of It Like This
Imagine you're wrapping a gift. You start with the gift itself (concrete component). You can add a layer of wrapping paper (first decorator), then a ribbon (second decorator), then a gift tag (third decorator), then place it in a gift bag (fourth decorator). Each layer adds something—protection, aesthetics, information, portability—but the gift inside remains unchanged. You can unwrap the layers in reverse order, and the gift is exactly as it was. The layers are independent: ribbon doesn't care what wrapping paper you used, gift tag doesn't care about the ribbon. You can mix and match: same gift, different wrapping papers; same wrapping, different ribbons.

Decorator Pattern works identically for software. You start with a core component (the "gift"). You wrap it in decorators—retry logic, caching, logging, metrics—each adding specific behavior. The core component is unchanged and usable independently. The decorators are independent: logging doesn't care about caching, metrics don't care about retry. You can mix and match: same core component with different decorator combinations for different use cases. Each layer wraps the previous one, adding its concern transparently.

## The "So What?" Factor
**If you use Decorator Pattern:**
- Flexibility increases—add/remove behaviors without modifying core components
- Composability is achieved—combine behaviors in any order and combination
- Testing is simplified—test each concern independently, not all combinations
- Code is maintainable—each decorator has single responsibility, easy to understand
- Open-Closed Principle is honored—extend functionality without modifying existing code
- Cross-cutting concerns are centralized—all retry logic in RetryDecorator, all caching in CacheDecorator
- Configuration is flexible—different decorator stacks per environment or use case
- Evolution is manageable—add new decorators without touching existing code
- Debugging is easier—can remove decorators to isolate core behavior
- Performance is tunable—measure decorator overhead, remove expensive decorators if needed

**If you don't:**
- Flexibility suffers—adding behaviors requires modifying core code or creating subclasses
- Composability is limited—combining behaviors requires explicit combinations (class explosion)
- Testing is complex—must test all feature combinations, exponential growth
- Code is unmaintainable—monolithic components mixing concerns become unmanageable
- Open-Closed Principle is violated—every new feature modifies existing code
- Cross-cutting concerns scatter—retry logic in multiple places, inconsistency emerges
- Configuration is rigid—can't easily change behavior per environment
- Evolution is risky—changes to add features risk breaking existing functionality
- Debugging is hard—can't disable individual concerns to isolate problems
- Performance is opaque—can't measure overhead of individual concerns

## Practical Checklist
Before implementing decorators, verify:
- [ ] Does the component interface represent core functionality cleanly? (good abstraction)
- [ ] Are decorators each focused on single cross-cutting concern? (single responsibility)
- [ ] Can decorators be composed in different orders safely? (order independence or documented constraints)
- [ ] Are decorators tested independently with mocked wrapped components? (isolated testing)
- [ ] Are common decorator stacks tested end-to-end? (integration testing)
- [ ] Is decorator composition configured via dependency injection? (flexibility)
- [ ] Are decorator ordering constraints documented? (clear guidance)
- [ ] Do decorators handle errors gracefully without breaking wrapped operations? (robustness)
- [ ] Is decorator performance overhead measured and acceptable? (performance)

## Watch Out For
⚠️ **Decorator Explosion**: Creating too many decorators for every minor concern leads to complexity managing composition. Not every cross-cutting concern needs a decorator—sometimes adding functionality to the base component is simpler. Use decorators for truly orthogonal concerns that need flexible composition, not for every small feature.

⚠️ **Order Dependency Confusion**: Some decorator combinations are order-sensitive (cache before retry vs retry before cache has different behavior), while others aren't. Without clear documentation, developers will compose decorators incorrectly. Document which decorators must be in specific order and why. Consider providing factory functions that build correctly-ordered stacks.

⚠️ **Interface Leakage**: Decorators adding methods or properties not in the component interface break composability. If `CacheDecorator` adds `cache.clear()` method, code depending on that method can't work with non-cached implementations. Keep decorators transparent—only implement interface methods. If new methods needed, extend the interface or use separate management objects.

⚠️ **Performance Death by Decorators**: Each decorator adds overhead. Stacking 10 decorators creates 10 layers of function calls, each potentially doing work. Measure cumulative overhead: are decorators adding 50ms to 10ms operation (bad) or 5ms to 500ms operation (acceptable)? Profile and optimize expensive decorators or combine them if overhead is unacceptable.

⚠️ **Incomplete Pass-Through**: Decorators that don't properly implement entire interface break in subtle ways. If interface has 5 methods but decorator only wraps 3, calling the other 2 fails. If methods accept keyword arguments but decorator doesn't forward them, calls break. Ensure decorators transparently wrap all interface methods with all parameters.

⚠️ **State Management Complexity**: Decorators with state (cache contents, retry counts, rate limit buckets) add complexity. Is state per decorator instance or shared? Is state thread-safe? Does state need persistence? Stateful decorators are powerful but require careful design. Consider whether stateless decorators or separate state management objects are cleaner.

⚠️ **Testing Overhead**: While decorators simplify testing individual concerns, they create testing complexity around composition. Do you test every possible decorator combination? That's exponential. Establish convention: test each decorator independently, test common production stacks end-to-end, don't test every theoretical combination. Focus testing on actual usage patterns.

## Connections
**Builds On:** object_oriented_programming, interfaces_and_contracts, composition_over_inheritance, single_responsibility_principle, open_closed_principle

**Works With:** dependency_injection, factory_pattern, adapter_pattern, proxy_pattern, chain_of_responsibility, software_architecture_culture, separation_of_concerns

**Leads To:** composable_systems, maintainable_code, flexible_architectures, testable_components, cross_cutting_concerns_management, aspect_oriented_programming

## Quick Decision Guide
**Use Decorator Pattern when:** You need to add responsibilities to objects dynamically, you have multiple orthogonal concerns (logging, caching, retry, validation), you need different combinations of behaviors in different contexts, you want to honor Open-Closed Principle, you need to compose behaviors at runtime based on configuration

**Skip Decorator Pattern when:** Behavior is static and class-wide (inheritance is simpler), you have single concern to add (direct modification might be clearer), the interface is unstable (decorator maintenance burden too high), performance overhead of layers is unacceptable, team finds pattern too abstract (pragmatism over purity)

**Decorators especially valuable for:** AI system infrastructure (retry, caching, logging, rate limiting for LLM calls), cross-cutting concerns (authentication, authorization, metrics, tracing), protocol adapters (HTTP retry, database connection pooling), I/O operations (buffering, compression, encryption)

## Further Exploration
- 📖 "Design Patterns: Elements of Reusable Object-Oriented Software" by Gang of Four - original decorator pattern definition
- 🎯 Implement decorator-based AI client: base LLM client + retry decorator + cache decorator + logging decorator
- 💡 "Head First Design Patterns" - accessible explanation with examples
- 🔍 Study decorator frameworks: Python `functools.wraps`, Java decorator annotations, middleware patterns in web frameworks
- 🤖 AI-specific decorator libraries: LangChain decorators, LlamaIndex decorators, custom observability decorators
- 📊 Performance profiling: measure decorator overhead in production AI systems
- 🏛️ Aspect-Oriented Programming: related paradigm for cross-cutting concerns using different mechanisms
- 🔬 Research decorator pattern variations: dynamic decorators, decorator chains, decorator composition strategies

---
*Added: May 14, 2026 | Updated: May 14, 2026 | Confidence: High*