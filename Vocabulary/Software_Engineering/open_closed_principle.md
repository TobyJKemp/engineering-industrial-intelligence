# Open-Closed Principle

## At a Glance
| | |
|---|---|
| **Category** | Design Principle / SOLID Principle |
| **Complexity** | Intermediate (concept is clear, application requires design skill) |
| **Time to Learn** | 3-5 days to understand, weeks to months to apply effectively |
| **Prerequisites** | Object-oriented programming, interfaces/abstractions, basic design patterns |

## One-Sentence Summary
The Open-Closed Principle states that software entities (classes, modules, functions) should be open for extension but closed for modification—meaning you should be able to add new functionality without changing existing, tested code.

## Why This Matters to You
When you're building AI agents and ML systems, requirements change constantly: new LLM providers emerge, retrieval strategies evolve, tool integrations multiply, and user needs shift. If every new requirement forces you to edit existing code, you're playing a dangerous game—each change risks breaking working functionality, requires re-testing everything, and creates merge conflicts in team environments. The Open-Closed Principle gives you a design strategy for change: structure your system so that adding capabilities means writing new code that plugs into existing abstractions, not modifying battle-tested implementations. Want to add support for Anthropic's Claude alongside your existing OpenAI integration? With Open-Closed design, you create a new `ClaudeClient` class implementing your `LLMProvider` interface—no changes to agent logic. Need a new retrieval strategy that combines vector search with knowledge graphs? Implement a new `HybridRetriever` class—no modifications to your RAG pipeline. This isn't just about code elegance; it's about velocity and safety. Teams that follow Open-Closed principles ship features faster because they're adding, not editing. They have fewer bugs because they're not touching working code. And they scale better because multiple developers can work simultaneously without conflicts.

## The Core Idea
### What It Is
The Open-Closed Principle (OCP), articulated by Bertrand Meyer in 1988 and later refined by Robert Martin as part of SOLID principles, captures a fundamental tension in software development: systems must accommodate change (openness), yet change itself is risky (we want closure/stability). OCP resolves this by distinguishing between two types of change: extending behavior (adding new cases, new options, new paths) versus modifying behavior (changing existing implementations).

The principle says: design your modules so that you can extend what they do without modifying their source code. This sounds paradoxical at first—how do you add functionality without changing code? The answer is abstraction and polymorphism. You create abstract interfaces that define contracts (what operations are available), then provide concrete implementations of those interfaces. When you need new behavior, you implement the interface in a new class rather than editing existing classes.

In practical AI agent development, OCP manifests constantly. Your agent might work with an `LLMProvider` interface defining methods like `complete(prompt) -> response`. Initially, you implement `OpenAIProvider` and `AnthropicProvider`. Later, you need Azure OpenAI support. Instead of modifying the existing providers or adding conditional logic throughout your agent, you simply implement a new `AzureOpenAIProvider` class. The agent code—which depends only on the `LLMProvider` interface—works unchanged. The system is "closed" (agent code doesn't change) yet "open" (it now supports a new provider).

This design approach has profound implications for 2026 AI systems where the landscape shifts rapidly. LLM APIs evolve, new embedding models emerge, retrieval techniques improve, and tool ecosystems expand. Systems built with OCP adapt by adding new implementations, not by editing core logic. Your retrieval pipeline supports vector search, keyword search, and graph traversal through a `Retriever` interface. When semantic hybrid retrieval becomes state-of-the-art, you add it by implementing the interface—your RAG system instantly supports it without code changes, only configuration changes that specify which retriever to use.

The principle trades upfront design investment for long-term flexibility. Creating good abstractions takes thought—you must identify what varies (LLM providers, retrieval strategies, tool implementations) and extract that variation behind interfaces. But once you've made that investment, extensions become additive rather than invasive, dramatically reducing risk and increasing velocity.

### What It Isn't
Open-Closed Principle is not about making everything pluggable or abstract "just in case." That leads to over-engineering—complex abstraction layers for problems you might never face. OCP applies when you have genuine variation or anticipate it based on domain knowledge. If your agent will only ever use one LLM provider with no plans to change, don't create elaborate provider abstractions. Follow YAGNI (You Aren't Gonna Need It) until you actually need it.

It's also not the same as plugin architecture, though plugin systems exemplify OCP. Plugin architecture is one implementation strategy; OCP is the broader principle. You can follow OCP without plugins (through inheritance, composition, strategy patterns) and you can have plugin systems that violate OCP (if plugins require modifying core system code to integrate).

OCP doesn't mean you never modify existing code. "Closed for modification" is an ideal, not an absolute. Bug fixes require changing code. Poor abstractions need refactoring. New requirements sometimes reveal that your original design didn't capture the right variation points. What OCP means is: when adding genuinely new functionality (not fixing bugs or improving existing features), you should be able to do it through extension rather than modification. If you must modify, that's feedback that your abstractions might need improvement.

Don't confuse OCP with making everything inheritable or using inheritance heavily. Modern OCP practice favors composition over inheritance. Rather than extending classes through subclassing, you compose behaviors using interfaces and dependency injection. A `RetrieverPipeline` that accepts a list of `Retriever` implementations and orchestrates them follows OCP through composition, not inheritance.

Finally, OCP isn't about preventing all changes to existing files. If you add a new `Retriever` implementation to your retrievers module, you've modified that module's file (added code). That's fine. "Closed for modification" means closed to changes in existing, working behavior—not closed to adding new classes, functions, or exports to a module. The key is that existing functionality remains untouched while new functionality is added.

## How It Works

**1. Identify Variation Points:**
Analyze where your system is likely to vary or evolve. In AI agents, common variation points include:
- LLM providers (OpenAI, Anthropic, Azure, local models)
- Retrieval strategies (vector, keyword, graph, hybrid)
- Tool implementations (different APIs, different protocols)
- Prompt templates (different formats, different strategies)
- Result parsers (JSON, XML, structured extraction)
- Caching strategies (memory, Redis, distributed)
- Error handling approaches (retry, fallback, fail-fast)

These are your extension points—places where you'll want to add new options without changing existing code.

**2. Create Abstractions:**
Define interfaces or abstract base classes that capture the essential contract of what these variations do, without specifying how they do it. For example:

```python
# Python example with Protocol
from typing import Protocol

class LLMProvider(Protocol):
    def complete(self, prompt: str, **kwargs) -> str:
        """Generate completion for prompt."""
        ...
    
    def stream_complete(self, prompt: str, **kwargs) -> Iterator[str]:
        """Stream completion tokens."""
        ...
```

The abstraction defines what all providers must do (complete prompts) without dictating implementation details (API endpoints, authentication, token handling).

**3. Implement Concrete Variants:**
Create concrete classes that implement your abstractions, each providing specific behavior:

```python
class OpenAIProvider:
    def complete(self, prompt: str, **kwargs) -> str:
        # OpenAI-specific implementation
        response = openai.Completion.create(
            model=kwargs.get('model', 'gpt-4'),
            prompt=prompt
        )
        return response.choices[0].text

class AnthropicProvider:
    def complete(self, prompt: str, **kwargs) -> str:
        # Anthropic-specific implementation
        response = anthropic.Completion.create(
            model=kwargs.get('model', 'claude-3'),
            prompt=prompt
        )
        return response.completion
```

Each implementation is self-contained—all the provider-specific logic lives in one place.

**4. Depend on Abstractions:**
Your high-level code (agent logic, orchestration) depends on the abstract interface, not concrete implementations:

```python
class Agent:
    def __init__(self, llm: LLMProvider, retriever: Retriever):
        self.llm = llm  # Depends on interface, not concrete class
        self.retriever = retriever
    
    def answer_question(self, question: str) -> str:
        context = self.retriever.retrieve(question)
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        return self.llm.complete(prompt)
```

`Agent` doesn't know or care which specific LLM or retriever is provided. It works through the contracts defined by interfaces.

**5. Extend Through New Implementations:**
When you need new functionality, implement the interface in a new class:

```python
class AzureOpenAIProvider:
    def complete(self, prompt: str, **kwargs) -> str:
        # Azure-specific implementation
        response = azure_openai.Completion.create(
            deployment=kwargs.get('deployment'),
            prompt=prompt
        )
        return response.choices[0].text
```

No changes to `Agent`, `OpenAIProvider`, or `AnthropicProvider`. You've extended the system's capabilities without modifying existing code. The agent automatically works with the new provider because it adheres to the `LLMProvider` contract.

**6. Configure Extension Selection:**
Use configuration, dependency injection, or factory patterns to select which implementations to use:

```python
# Configuration-driven selection
config = load_config()
if config['llm_provider'] == 'openai':
    llm = OpenAIProvider()
elif config['llm_provider'] == 'anthropic':
    llm = AnthropicProvider()
elif config['llm_provider'] == 'azure':
    llm = AzureOpenAIProvider()

agent = Agent(llm=llm, retriever=selected_retriever)
```

Extension selection happens at system initialization through configuration, not through conditional logic scattered throughout the codebase.

**7. Refactor When Abstractions Fail:**
When you add a new implementation and find that the existing interface doesn't accommodate it, that's feedback. You might need to:
- Refine the interface (add optional methods, parameters)
- Split the interface (maybe you've identified two distinct concerns)
- Reconsider your abstraction (perhaps the variation point is different than you thought)

OCP doesn't mean your first abstractions are perfect. It means you design for extension, then refine abstractions based on real extension needs.

## Think of It Like This
Imagine you're designing a power outlet system for a building. You could hardwire every appliance directly to the building's wiring—but then adding a new appliance means opening walls and modifying the electrical system (dangerous, expensive, invasive). Instead, you install standard outlets (abstractions) that define a contract: "provide 120V AC at 60Hz through these prongs."

Now appliances (implementations) are designed to that contract. Want to add a new lamp? Plug it in—no modifications to the building's wiring. Want to upgrade your phone charger? Swap it out—the outlet doesn't care. The building's electrical system is "closed for modification" (you're not rewiring) yet "open for extension" (it accepts any compliant device).

The Open-Closed Principle creates software "outlets"—interface contracts that new implementations can plug into. Your agent has a "retrieval outlet" (the `Retriever` interface). Any retrieval strategy that implements the contract can plug in. Vector search, keyword search, graph traversal, hybrid approaches—all plug into the same outlet. Your agent code (the building's wiring) stays unchanged while the retrievers you plug in (the appliances) vary freely.

Just as you wouldn't create outlets for hypothetical future appliances you might never use, you don't create abstractions for every possible variation. But for areas where you know extension will happen (like LLM providers or retrieval strategies in AI systems), establishing the "outlet" pattern pays off enormously.

## The "So What?" Factor
**If you use this:**
- Adding features becomes safe—you write new code instead of modifying tested code, dramatically reducing regression risk
- Development velocity increases—multiple developers can add extensions in parallel without merge conflicts in core logic
- Testing stays focused—new implementations get new tests; existing functionality doesn't need re-testing when you add extensions
- Experimentation becomes low-risk—want to try a new LLM provider or retrieval strategy? Implement it and compare—if it fails, remove the new class, no core code was touched
- System evolution is smooth—as the AI landscape changes (new models, new techniques), you adapt by adding implementations, not rewriting core systems
- Deployment becomes flexible—different environments or customers can use different implementations through configuration, not code branches
- Code review is easier—reviewers focus on the new implementation, not whether modifications broke existing functionality

**If you don't:**
- Every new feature requires editing existing code, creating risks of introducing bugs into working functionality
- Development slows because changes conflict—everyone's modifying the same core files, creating merge nightmares
- Testing becomes comprehensive every time—you can't trust existing functionality unchanged, so every addition requires full regression testing
- The codebase fills with conditional logic checking which variant to use (`if provider == 'openai': ... elif provider == 'anthropic': ...`), making code harder to understand and maintain
- Experimentation is risky—trying new approaches means touching production code paths, not isolating experiments
- Technical debt accumulates—each new variant adds another conditional branch, another special case, compounding complexity
- Onboarding slows—new developers must understand the entire conditional maze rather than examining one implementation at a time

## Practical Checklist
Before implementing, ask yourself:
- [ ] **Have I identified genuine variation points?** Am I abstracting areas that actually vary or will vary based on domain knowledge, not hypothetical "what-ifs"?
- [ ] **Is my abstraction stable?** Does the interface capture the essential contract without leaking implementation details of specific variants?
- [ ] **Can I add a new implementation without modifying existing ones?** If adding a new LLM provider requires changes to OpenAIProvider, something's wrong with the abstraction
- [ ] **Does high-level code depend only on abstractions?** Is my agent logic referencing interfaces/protocols, not concrete classes?
- [ ] **Have I avoided premature abstraction?** Am I creating this abstraction because I have real variants or strong domain-driven anticipation, not speculative "might need someday"?
- [ ] **Is the interface cohesive?** Does it represent one coherent concept (like "LLM provider" or "retriever"), not a grab-bag of unrelated operations?
- [ ] **How do I select implementations?** Have I designed a configuration or dependency injection approach for choosing which implementation to use?
- [ ] **Can I test extensions independently?** Can new implementations have their own test suites without requiring changes to existing test infrastructure?

## Watch Out For
⚠️ **Premature Abstraction and YAGNI Violation**: The most common mistake is creating elaborate abstractions for variations that never materialize. Don't abstract until you have at least two implementations or strong domain-driven certainty that variations are coming. The cost of abstraction (complexity, indirection, cognitive load) should be justified by actual variation, not hypothetical flexibility. Wait until you feel pain from not having abstraction, then refactor.

⚠️ **Leaky Abstractions**: Interfaces sometimes expose implementation details, defeating the purpose. If your `LLMProvider` interface includes methods like `get_openai_client()` or parameters like `anthropic_api_version`, it's leaking specific provider details. Good abstractions capture what all implementations share (completing prompts) while hiding what differs (API details, authentication mechanisms). Design interfaces around capabilities, not implementations.

⚠️ **Interface Bloat**: As you add implementations, you might be tempted to add methods to the interface to support new capabilities. This violates OCP—you're modifying the interface, which means modifying all existing implementations. Instead, consider optional methods, separate interfaces for additional capabilities (Interface Segregation), or parameters that enable extensions without interface changes. Balance stable interfaces against evolving needs.

⚠️ **Inheritance Overuse**: Classic OCP teaching emphasized inheritance (extend by subclassing). Modern practice favors composition (implement interfaces, inject dependencies). Inheritance creates tight coupling between parent and child; composition maintains loose coupling. For AI agents, composition through dependency injection is usually preferable—your agent composes with an LLM provider interface, not subclasses from an agent base class.

⚠️ **Configuration Complexity**: When you have many extension points (LLM provider, retriever, tools, parsers, caching), configuration becomes complex. You need 20 configuration parameters to wire everything together, and invalid combinations become possible. Consider using factory patterns, builder patterns, or configuration validation to manage this complexity. Don't let flexibility create unusable systems.

⚠️ **Testing Neglect**: Just because you haven't modified existing code doesn't mean you can skip testing. New implementations need thorough testing—unit tests for the implementation, integration tests confirming it works with the system, and potentially contract tests verifying it meets the interface contract. Extensions can still break systems through unexpected edge cases or behavior differences.

⚠️ **Abstraction Mismatch**: Sometimes you abstract the wrong thing. You create an `LLMProvider` abstraction but later realize different providers have fundamentally different capabilities (one supports function calling, another doesn't; one streams, another batches). When your abstraction doesn't fit reality, extensions become awkward workarounds. This is feedback—refactor the abstraction. Perhaps you need a richer interface with optional capabilities, or multiple interfaces for different provider tiers.

⚠️ **False Closure**: You think you've achieved closure (no modifications needed), but then a new requirement forces you to change the interface or core logic anyway. This isn't failure—it's learning. OCP is a guideline, not a law. Sometimes requirements genuinely change in ways your abstraction can't accommodate. The value was in making most extensions safe and easy; occasional core changes are acceptable and better informed by real needs than premature speculation.

## Connections
**Builds On:** 
- [Design Pattern](design_pattern.md) - OCP underlies many design patterns that enable extension without modification
- [SOLID Principles](solid_principles.md) - OCP is the "O" in SOLID, working synergistically with other principles
- [Separation of Concerns](separation_of_concerns.md) - OCP applies separation by isolating variation points behind abstractions

**Works With:** 
- [Single Responsibility](single_responsibility.md) - Classes with single responsibilities are easier to keep closed for modification
- [Dependency Injection](dependency_injection.md) - Primary mechanism for injecting extension implementations at runtime
- [Loose Coupling](loose_coupling.md) - Depending on abstractions creates loose coupling, enabling OCP
- [Strategy Pattern](strategy_pattern.md) - Classic implementation of OCP—interchangeable strategies extend behavior without modifying context
- [Decorator Pattern](decorator_pattern.md) - Extends behavior by wrapping objects, not modifying them—pure OCP
- [Adapter Pattern](adapter_pattern.md) - Adapts existing implementations to new interfaces, enabling extension
- [Factory Pattern](factory_pattern.md) - Centralizes creation of extension implementations, keeping selection logic isolated
- [Observer Pattern](observer_pattern.md) - Extends system with new observers without modifying the subject

**Leads To:** 
- [Hexagonal Architecture](../System_Architecture/hexagonal_architecture.md) - Ports and adapters architecture built on OCP for external integrations
- [Plugin Architecture](../System_Architecture/hexagonal_architecture.md) - Natural evolution of OCP applied to external extensibility
- [Microservices](../System_Architecture/microservices.md) - OCP at service level—add services without modifying existing ones
- [Refactoring](refactoring.md) - When you can't extend without modifying, that's a refactoring trigger toward OCP-compliant design

**Related Patterns:**
- [Inversion of Control](inversion_of_control.md) - Framework-level OCP where frameworks are extended through injection, not modification
- [Clean Code](clean_code.md) - OCP is one pillar of clean, maintainable code
- [Technical Debt](technical_debt.md) - Violating OCP (modification instead of extension) accumulates debt; following it pays it down

## Quick Decision Guide
**Use this when you need to:** 
- Support multiple implementations of a concept (multiple LLM providers, multiple retrieval strategies, multiple data stores)
- Enable plugin or extension ecosystems where third parties add functionality
- Experiment safely with alternatives—you want to try new approaches without risking existing functionality
- Build systems where variation is inherent to the domain (AI agents that will support many different tools, models, data sources)
- Support different deployment configurations through implementation selection, not code branches
- Enable parallel development where multiple developers add different implementations simultaneously
- Follow clean architecture principles that separate stable business logic from volatile implementation details

**Skip this when:** 
- You have a single implementation and no reasonable expectation of alternatives—don't abstract prematurely for hypothetical needs
- The "variation" is actually configuration (different parameter values) not different algorithms—parameterize, don't abstract
- You're prototyping and exploring—premature abstraction slows learning; get working code first, refactor to OCP when you understand variation
- The abstraction cost exceeds its benefit—for simple systems with limited scope, straightforward conditional logic might be clearer than elaborate abstractions
- Your team lacks familiarity with interfaces and polymorphism—forcing advanced patterns creates confusion if the team doesn't understand them
- The implementation details genuinely can't be abstracted cleanly—sometimes variations are so different that forcing them behind one interface creates a leaky, awkward abstraction

## Further Exploration
- 📖 **Agile Software Development, Principles, Patterns, and Practices** (2002) by Robert C. Martin - Comprehensive treatment of OCP with examples
- 📖 **Clean Architecture** (2017) by Robert C. Martin - OCP applied at architectural level for system boundaries and dependencies
- 🎯 **"Open-Closed Principle in AI Agent Systems"** (2025) - Modern examples showing OCP for LLM providers, retrieval strategies, and tool integrations
- 💡 **"Refactoring to Patterns: Open-Closed"** - Practical guide to identifying OCP violations and refactoring toward extensibility
- 📖 **Design Patterns: Elements of Reusable Object-Oriented Software** (1994) - Many patterns implement OCP (Strategy, Decorator, Observer, etc.)
- 🎯 **"Interface Design for Extensibility"** - Deep dive into creating stable abstractions that support extension without modification
- 💡 **"OCP in Dynamic Languages"** (Python, JavaScript) - How to apply OCP in duck-typed languages without explicit interfaces
- 📖 **Object-Oriented Software Construction** (1988) by Bertrand Meyer - Original articulation of the Open-Closed Principle

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*