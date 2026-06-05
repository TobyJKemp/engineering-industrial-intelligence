# Adapter Pattern

## At a Glance
| | |
|---|---|
| **Category** | Software Design Pattern |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours to understand, practiced through implementation |
| **Prerequisites** | Object-oriented programming, interfaces/protocols, basic software design |

## One-Sentence Summary
The Adapter Pattern is a structural design pattern that converts the interface of one class or system into another interface that clients expect—acting as a translator or bridge that allows incompatible interfaces to work together without modifying their original code.

## Why This Matters to You
You're building an AI agent that needs to call different LLM providers—OpenAI's GPT, Anthropic's Claude, Google's Gemini, and a local Llama model. Each has a completely different API: different method names, parameter structures, authentication approaches, response formats, and error handling. You could write conditional logic everywhere: "if OpenAI do this, if Claude do that, if Gemini do something else." Your code becomes a tangled mess of provider-specific branches that's impossible to maintain, test, or extend. The Adapter Pattern solves this elegantly: create a common interface `LLMProvider` with standard methods `generateText()`, `streamResponse()`, `countTokens()`. Then write adapters—`OpenAIAdapter`, `ClaudeAdapter`, `GeminiAdapter`—that implement this interface by translating to each provider's specific API. Now your agent code depends only on the `LLMProvider` interface, not specific implementations. Switching providers is trivial (swap adapters). Testing is clean (mock the interface). Adding new providers doesn't touch existing code (just add new adapters). The Adapter Pattern is how you integrate heterogeneous systems, abstract vendor-specific details, future-proof against API changes, and maintain clean architecture in AI systems where you constantly integrate diverse services, models, and data sources. In 2026, with AI systems composed of multiple models, APIs, and tools, the Adapter Pattern isn't optional—it's foundational architecture.

## The Core Idea
### What It Is
The Adapter Pattern is one of the classic Gang of Four structural design patterns that solves the problem of incompatible interfaces. When you need to use an existing class or system (the "adaptee") but its interface doesn't match what your code expects (the "target interface"), the adapter acts as a wrapper that translates calls from the target interface to the adaptee's actual interface. The client code interacts with the adapter through the target interface, completely unaware of the adaptee's actual implementation.

The pattern has three key participants:

**Target Interface** - The interface that the client code expects and depends on. This defines the contract that clients interact with—the methods, parameters, and return types that client code is written against. In AI systems, this might be an `LLMProvider` interface with methods like `generateText(prompt, config)`, `embedText(text)`, and `countTokens(text)`.

**Adaptee** - The existing class or system with an incompatible interface that needs to be integrated. This is what you're trying to adapt—it might be a third-party library, external API, legacy system, or any code you can't or won't modify. The adaptee works perfectly well on its own; it just doesn't match the interface your code expects. In AI systems, this might be OpenAI's API with its specific `chat.completions.create()` method structure.

**Adapter** - The class that implements the target interface while internally delegating to the adaptee. The adapter translates between interfaces: it receives calls via the target interface, transforms parameters as needed, calls the adaptee's actual methods, transforms responses back, and returns results matching the target interface contract. The adapter contains the integration logic—the "glue code" that makes incompatible systems work together.

There are two implementation approaches:

**Object Adapter** - Uses composition. The adapter holds a reference to the adaptee as a member variable and delegates calls to it. This is more flexible because the adapter can work with any class implementing the adaptee's interface (including subclasses), and a single adapter can adapt multiple adaptees if needed. Most modern implementations use object adapters.

**Class Adapter** - Uses multiple inheritance. The adapter inherits from both the target interface and the adaptee class, directly accessing the adaptee's methods. This is less flexible (requires languages supporting multiple inheritance, can't adapt sealed classes) but slightly more efficient (no delegation overhead). Less commonly used in practice.

The power of the Adapter Pattern lies in **separation of concerns**: integration complexity is isolated in adapters, client code remains clean and depends only on stable interfaces, adaptees remain unchanged (you don't need to modify third-party code), and new adaptees can be integrated by adding new adapters without touching existing code. This follows the Open-Closed Principle: open for extension (new adapters), closed for modification (existing code unchanged).

For AI systems in 2026, adapters are everywhere:

**LLM Provider Abstraction** - Different LLM APIs (OpenAI, Anthropic, Cohere, Azure OpenAI, local models) all provide similar capabilities but with different interfaces. Adapters create a unified interface, allowing code to be provider-agnostic. Switching from GPT-4 to Claude becomes a configuration change, not a code rewrite.

**Tool Integration** - AI agents need to call tools—databases, APIs, file systems, calculators, web searches. Each tool has its own interface. Tool adapters present a standard `Tool` interface with `execute(parameters)`, enabling agents to work with heterogeneous tools uniformly.

**Data Format Translation** - AI systems process data from various sources: JSON APIs, XML feeds, CSV files, Parquet datasets, protobuf messages. Format adapters convert everything to internal representations, letting processing code ignore source formats.

**Model Abstraction** - Classification models, embedding models, generation models, fine-tuned models—all with different input/output formats. Model adapters standardize interfaces: `predict(input)` returns standardized output regardless of whether the underlying model is scikit-learn, PyTorch, TensorFlow, or ONNX.

**Legacy System Integration** - When integrating modern AI capabilities with legacy systems (SOAP services, mainframe protocols, proprietary APIs), adapters bridge old and new without modifying legacy code that might be fragile or inaccessible.

### What It Isn't
The Adapter Pattern is not the same as the Facade Pattern, though they're often confused. A facade provides a simplified interface to a complex subsystem (making complexity easier to use). An adapter provides a different interface to an existing system (making incompatible interfaces compatible). Facades simplify; adapters translate. Though in practice, you might combine both: a facade that uses adapters internally.

It's also not the same as a Wrapper or Decorator, though the implementation looks similar. Decorators add responsibilities to objects (enhancing behavior) while maintaining the same interface. Adapters change the interface without necessarily changing behavior. If you're adding caching, logging, or validation, that's decoration. If you're making an incompatible interface compatible, that's adaptation.

The Adapter Pattern doesn't mean creating "God objects" that do everything. Each adapter should have a single, clear purpose: adapting one specific adaptee to one specific target interface. If your adapter is handling multiple unrelated concerns or adapting multiple adaptees to multiple interfaces, you've over-complicated it. Keep adapters focused and simple.

Finally, adapters are not performance-free. There's overhead in translation—method calls, parameter transformations, response conversions. For most use cases, this overhead is negligible compared to benefits (maintainability, flexibility, testability). But for ultra-high-performance inner loops, direct calls might be necessary. Know when to use adapters (most places) and when not to (performance-critical paths where nanoseconds matter).

## How It Works
Implementing the Adapter Pattern follows a clear structure:

1. **Define Target Interface**: Start by defining the interface your client code expects. This should be stable, well-designed, and match your domain's needs—not shaped by any specific adaptee. Example: Define an `LLMProvider` interface with methods `generate(prompt, options)`, `stream(prompt, options)`, `embed(text)`. Make this interface provider-agnostic.

2. **Identify Adaptee**: Understand the existing class or system you need to integrate—its methods, parameters, return types, error handling, and behavior. Document how it differs from your target interface. Example: OpenAI's API uses `client.chat.completions.create(messages=[...], model="gpt-4")` with specific message format and streaming via iterators.

3. **Create Adapter Class**: Implement a class that implements the target interface while internally using the adaptee. The adapter's constructor typically receives or creates the adaptee instance. Example: `OpenAIAdapter implements LLMProvider` with a private `openai_client` member.

4. **Implement Translation Logic**: For each method in the target interface, implement the translation: transform input parameters from target format to adaptee format, call the appropriate adaptee method(s), handle any errors or edge cases, transform the response from adaptee format to target format, and return results matching the target interface. Example: `OpenAIAdapter.generate(prompt, options)` converts `prompt` to OpenAI's message format, calls `openai_client.chat.completions.create()`, extracts text from response, and returns in standard format.

5. **Handle Error Translation**: Adapt exceptions and error conditions from the adaptee to standard exceptions expected by the target interface. Don't let adaptee-specific errors leak through—wrap them in domain-appropriate exceptions. Example: Catch OpenAI's `APIError` and raise a standard `LLMProviderError` with normalized error information.

6. **Add Configuration Flexibility**: Allow adapters to be configured for different scenarios. Constructor parameters, configuration objects, or builder patterns enable adapters to work with variations of adaptees. Example: `OpenAIAdapter(api_key, base_url, timeout)` supports both OpenAI's hosted API and Azure OpenAI with different endpoints.

7. **Test Adapters Independently**: Write unit tests for adapters that verify translation logic without requiring the real adaptee. Mock the adaptee to test that adapter correctly translates calls and responses. Example: Mock OpenAI client to verify `OpenAIAdapter` correctly formats messages and parses responses.

8. **Use Dependency Injection**: Don't hard-code which adapter to use. Let client code depend on the target interface, and inject specific adapters via dependency injection, configuration, or factory patterns. This enables runtime provider switching, A/B testing, and fallback strategies. Example: Agent constructor receives `llm_provider: LLMProvider` parameter, injected with specific adapter.

9. **Document Adapter Limitations**: Some adaptee features may not map cleanly to the target interface. Document any limitations, unsupported features, or behavioral differences. Example: If your `LLMProvider` interface supports streaming but a particular provider doesn't, document how the adapter handles this (buffers entire response, raises exception, etc.).

10. **Consider Bidirectional Adaptation**: Sometimes you need to adapt in both directions—external system to your interface AND your interface to external system. This might require pairs of adapters or bidirectional translation logic. Example: Webhook handlers that receive data in external format, process using internal format, and return responses in external format.

## Think of It Like This
Imagine you travel to a country with different electrical outlets. Your laptop charger has a US plug (two flat prongs), but the wall outlets are European (two round pins). The charger works perfectly; the outlet works perfectly. They're just incompatible. You don't redesign the charger, and you can't rewire the building. Instead, you use a travel adapter—a small device with European pins on one side and US socket on the other. The adapter doesn't generate electricity or transform voltage (that's what converters do); it simply makes compatible interfaces that would otherwise be incompatible.

Software adapters work identically: they don't change what systems do (that's business logic); they make incompatible interfaces compatible. Your code expects the "US plug" interface; the external system provides a "European outlet" interface. The adapter bridges them.

## The "So What?" Factor
**If you use the Adapter Pattern:**
- Client code depends on stable interfaces, not volatile implementations—changes in external systems don't cascade through your codebase
- Integration is localized—complexity lives in adapters, keeping client code clean
- Systems are composable—swap implementations by changing which adapter is injected
- Testing is easier—mock the target interface, test client code without real external dependencies
- Maintenance is bounded—when external APIs change, update the adapter, not everywhere
- Future-proofing is built-in—new integrations are new adapters, not modifications to existing code
- Architectural boundaries are clear—adapters mark integration points between your code and external systems

**If you don't:**
- Client code couples to specific implementations—vendor lock-in and brittle dependencies
- Integration logic scatters—conditional branches handling different systems everywhere
- Systems are rigid—switching implementations requires widespread code changes
- Testing is difficult—can't test business logic without real external dependencies
- Maintenance is unbounded—API changes require finding and fixing every reference
- Adding integrations breaks existing code—no isolation means changes ripple everywhere
- Architectural boundaries blur—integration concerns mix with business logic

## Practical Checklist
Before considering adapter implementation complete, ask yourself:
- [ ] Does the adapter fully implement the target interface without leaking adaptee details? (complete abstraction)
- [ ] Is error handling translated to target interface exceptions? (error abstraction)
- [ ] Can client code work with any adapter implementing the target interface? (interface dependency)
- [ ] Are adapters testable in isolation from real adaptees? (unit testability)
- [ ] Is adapter configuration flexible for different scenarios? (configurability)
- [ ] Are limitations and unsupported features documented? (transparency)
- [ ] Does client code receive adapters via dependency injection? (decoupling)

## Watch Out For
⚠️ **Leaky Abstractions**: Allowing adaptee-specific details to leak into the target interface. If your target interface has methods like `getOpenAICompletionConfig()`, you've failed—the interface is contaminated by adaptee details. Keep interfaces generic and adaptee-agnostic. If you need provider-specific features, consider alternative patterns or extension points.

⚠️ **Adapter Explosion**: Creating too many single-purpose adapters when a configurable adapter would suffice. If you have `OpenAIGPT4Adapter`, `OpenAIGPT35Adapter`, `OpenAIChatAdapter`, `OpenAICompletionAdapter` all doing nearly identical work, consolidate. One `OpenAIAdapter` with configuration handles variations better.

⚠️ **Complex Translation Logic**: Putting excessive business logic inside adapters. Adapters should translate, not implement business rules. If your adapter is making complex decisions about how to transform data beyond format conversion, you've given it too much responsibility. Keep adapters thin—they're translators, not decision-makers.

⚠️ **Incomplete Adaptation**: Implementing only part of the target interface or handling only the happy path. Incomplete adapters fail in production when edge cases, error conditions, or less-common features are used. Implement the full interface or explicitly document unsupported operations (throwing `NotImplementedError` with clear messages).

⚠️ **Testing Against Real Adaptees**: Only testing with live external systems rather than mocking adaptees. This makes tests slow, fragile (depends on external availability), and difficult (requires credentials, network, etc.). Test adapter translation logic with mocked adaptees; integration tests can verify against real systems separately.

⚠️ **Ignoring Performance**: Assuming adapter overhead is always negligible. For high-throughput or low-latency paths, measure the cost. If profiling reveals adapter calls as bottlenecks, optimize translation logic or consider whether adaptation is necessary in that specific path.

## Connections
**Builds On:** object_oriented_design, interface_segregation, dependency_inversion, separation_of_concerns, composition

**Works With:** dependency_injection, factory_pattern, strategy_pattern, facade_pattern, interface_contracts, software_architecture_culture

**Leads To:** loosely_coupled_systems, testable_code, vendor_independence, maintainable_integrations, composable_architectures, plugin_systems

## Quick Decision Guide
**Use Adapter Pattern when:** Integrating third-party libraries or APIs with different interfaces, abstracting vendor-specific implementations (database drivers, cloud providers, LLM services), working with legacy code you can't modify, creating plugin systems where implementations vary, building systems that must support multiple similar but incompatible providers

**Use alternative patterns when:** You control both interfaces and can make them compatible directly, the translation is extremely complex requiring substantial business logic (consider dedicated integration layer), performance overhead is unacceptable for the specific use case (measure first!), the interface mismatch is trivial and localized (simple wrapper function might suffice)

## Further Exploration
- 📖 "Design Patterns: Elements of Reusable Object-Oriented Software" by Gang of Four - original adapter pattern definition
- 🎯 Implement LLM provider adapters: OpenAI, Anthropic, Cohere, Azure OpenAI unified behind common interface
- 💡 Study real-world adapters: database drivers (SQLAlchemy adapters), cloud SDKs (boto3 for AWS, Azure SDK), logging frameworks (different handlers)
- 🔍 Explore adapter variations: two-way adapters, cached adapters, composable adapters, adapter chains
- 🤖 Build AI tool adapters: standard tool interface for heterogeneous capabilities (APIs, databases, calculators, web search)
- 📊 Research framework-agnostic ML: adapters abstracting PyTorch, TensorFlow, scikit-learn, ONNX behind unified interface
- 🏛️ Study protocol adaptation: REST to GraphQL, SOAP to REST, protocol buffers to JSON
- 🔬 Investigate aspect-oriented programming: cross-cutting concerns (logging, metrics) applied to adapters

---
*Added: May 14, 2026 | Updated: May 14, 2026 | Confidence: High*