# Factory Pattern

## At a Glance
| | |
|---|---|
| **Category** | Design Pattern / Creational Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-4 hours for basic understanding, weeks for mastery in complex scenarios |
| **Prerequisites** | Object-oriented programming, interfaces/abstract classes, [dependency_injection](dependency_injection.md) basics |

## One-Sentence Summary
The Factory Pattern is a creational design pattern that provides a centralized interface for creating objects without specifying their exact classes, allowing your code to request "an agent" or "a tool" without needing to know whether it's getting a GPT-4 agent, a specialized coding agent, or a fallback local model.

## Why This Matters to You
When you build AI agent systems in 2026, you're constantly creating objects whose specific type depends on runtime conditions: which LLM provider to use (OpenAI, Anthropic, Azure, local Llama), which type of agent to instantiate (research agent, coding agent, analysis agent), which tool implementation to provide (production database vs. mock for testing), or which prompt strategy to apply (chain-of-thought for complex reasoning, simple prompt for straightforward tasks). Hardcoding these decisions with direct class instantiation (`new GPT4Agent()`, `new AnthropicAgent()`) creates rigid, tightly-coupled code that breaks every time you need to support a new provider or switch implementations. The Factory Pattern centralizes object creation logic, allowing you to write code that says "give me an agent appropriate for this task" and let the factory decide whether that's a GPT-4 agent, a fine-tuned local model, or a mock agent for testing—all without changing your business logic code.

## The Core Idea
### What It Is
The Factory Pattern is a design pattern that delegates object creation to a specialized factory class or method rather than using direct instantiation (the `new` keyword). Instead of your code knowing about and directly creating concrete classes, it asks a factory for objects through an abstract interface.

There are several variants:

**Simple Factory** (not technically a pattern, but commonly used): A single class with a method that takes parameters and returns instances of different classes based on those parameters. `AgentFactory.create(task_type="research")` might return a `ResearchAgent`, while `task_type="code"` returns a `CodingAgent`.

**Factory Method Pattern**: Defines an interface for creating objects, but lets subclasses decide which class to instantiate. An abstract `AgentCreator` class has a `create_agent()` method, and concrete subclasses like `OpenAIAgentCreator` and `AnthropicAgentCreator` override this method to create their specific agent types.

**Abstract Factory Pattern**: Provides an interface for creating families of related objects without specifying their concrete classes. A `CloudProviderFactory` might create coordinated sets of resources—an `AzureProviderFactory` creates Azure-specific implementations of vector stores, compute resources, and monitoring tools, while `AWSProviderFactory` creates AWS equivalents.

The core benefit is **decoupling**. Your business logic (the code that uses agents) depends only on abstract interfaces (the `Agent` interface), not concrete implementations (`GPT4Agent`, `ClaudeAgent`). The factory handles the messy details of instantiation, configuration, and dependency injection.

In 2026's AI agent landscape, factories are particularly useful because:
- **Provider abstraction**: Switch between LLM providers (OpenAI, Anthropic, Cohere, local models) without changing application code
- **Environment-aware creation**: Use expensive GPT-4 in production but fast local models in development/testing
- **Configuration-driven systems**: Load which agent types to use from config files rather than hardcoding
- **Dynamic tool selection**: Choose tool implementations based on user permissions, rate limits, or A/B tests
- **Complex initialization**: Agents often require elaborate setup (API keys, system prompts, memory initialization, tool registration)—factories encapsulate this complexity

### What It Isn't
The Factory Pattern is not about **every object creation**. You don't need a factory for simple, unchanging objects like data transfer objects, configuration classes, or utility instances. Factories add abstraction overhead—use them when you need flexibility, not for every `new` keyword in your codebase.

It's not a substitute for **dependency injection containers**. While factories create objects, DI containers manage object lifecycles, dependencies, and configuration. Often you'll use both: the DI container provides the factory, which creates the specific objects. They're complementary tools.

The Factory Pattern is not the same as the **Builder Pattern**, though they're both creational patterns. Builders focus on constructing complex objects step-by-step (`.with_system_prompt()`, `.with_tools()`, `.with_memory()`, `.build()`), while factories focus on choosing which type of object to create. You might use a factory to select an agent type, then use a builder to configure it.

Finally, factories aren't about **hiding complexity** at all costs. If you have two agent types that differ in trivial ways, a factory might be over-engineering. Use factories when the creation logic is complex, varies by context, or needs to be centralized for consistency—not just to avoid writing `new`.

## How It Works

### Simple Factory Example (AI Agent Context):
```python
class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str, config: dict) -> Agent:
        if agent_type == "research":
            return ResearchAgent(
                model="gpt-4",
                tools=[WebSearchTool(), DocumentReaderTool()],
                system_prompt=config["research_prompt"]
            )
        elif agent_type == "coding":
            return CodingAgent(
                model="claude-3.5-sonnet",
                tools=[FileSystemTool(), GitTool()],
                system_prompt=config["coding_prompt"]
            )
        elif agent_type == "analysis":
            return AnalysisAgent(
                model="gpt-4o-mini",
                tools=[DataAnalysisTool()],
                system_prompt=config["analysis_prompt"]
            )
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

# Usage in your application
agent = AgentFactory.create_agent("research", config)
result = agent.run(user_query)
```

### Factory Method Example:
```python
from abc import ABC, abstractmethod

class LLMProviderFactory(ABC):
    @abstractmethod
    def create_client(self) -> LLMClient:
        pass
    
    @abstractmethod
    def create_embeddings(self) -> EmbeddingsModel:
        pass

class OpenAIFactory(LLMProviderFactory):
    def create_client(self) -> LLMClient:
        return OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    
    def create_embeddings(self) -> EmbeddingsModel:
        return OpenAIEmbeddings(model="text-embedding-3-large")

class AnthropicFactory(LLMProviderFactory):
    def create_client(self) -> LLMClient:
        return AnthropicClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def create_embeddings(self) -> EmbeddingsModel:
        # Anthropic doesn't provide embeddings, use OpenAI
        return OpenAIEmbeddings(model="text-embedding-3-small")

# Usage
factory = OpenAIFactory() if config["provider"] == "openai" else AnthropicFactory()
llm = factory.create_client()
embeddings = factory.create_embeddings()
```

### Key Components:
1. **Product Interface**: The abstract type returned by the factory (`Agent`, `LLMClient`, `Tool`)
2. **Concrete Products**: The actual implementations (`GPT4Agent`, `ClaudeAgent`, `WebSearchTool`)
3. **Factory Interface/Class**: The entity responsible for creating products
4. **Client Code**: Your business logic that uses the factory without knowing concrete types

### Typical Flow:
1. Client code needs an object but doesn't know which specific type
2. Client calls factory with parameters (agent type, provider name, config)
3. Factory examines parameters and instantiates the appropriate concrete class
4. Factory performs any complex initialization (API keys, configuration, dependency injection)
5. Factory returns the object through the abstract interface
6. Client uses the object through the interface, never seeing the concrete type

## Think of It Like This
Imagine you run a restaurant and need kitchen staff, but you don't want to interview and hire every cook, dishwasher, and prep chef yourself.

**Without a Factory Pattern**, you directly recruit each position: "I need a French pastry chef who trained at Le Cordon Bleu, speaks English and Japanese, has 10 years experience..." You handle all the specifics every time you need help.

**With a Factory Pattern**, you hire a staffing agency. You tell them: "I need a pastry chef for a high-end restaurant." The agency (factory) knows all the details—where to find qualified chefs, what certifications matter, how to vet candidates, what the going rate is. They handle the complexity and send you someone who fits the `PastryChef` role. You don't care if they trained in Paris or Tokyo, as long as they can execute your menu.

Even better, if your restaurant pivots from French to Italian cuisine, you tell the agency "now I need an Italian pastry chef" and they handle finding someone appropriate. Your restaurant operations (the client code) don't change—you still work with a pastry chef—but the factory swaps in the right specialist.

In AI systems, the factory is your "agent staffing agency"—you request "an agent for research tasks" and it delivers an appropriately configured agent without you managing all the initialization details.

## The "So What?" Factor
**If you use the Factory Pattern:**
- Your application code doesn't depend on specific LLM providers, making it easy to switch from OpenAI to Anthropic or add local model support
- You can choose implementations at runtime based on configuration, environment variables, or user preferences
- Testing becomes simpler—inject a factory that creates mock agents instead of real ones requiring API keys and network calls
- Complex initialization logic is centralized in one place rather than scattered across your codebase
- Adding new agent types or tool implementations requires minimal changes to existing code (Open/Closed Principle)
- You can implement environment-specific behavior (expensive models in prod, cheap ones in dev) without littering code with conditionals
- Configuration changes don't require code modifications—just update config files or environment variables

**If you don't:**
- Direct class instantiation creates tight coupling between business logic and concrete implementations
- Switching LLM providers requires find-and-replace across your entire codebase
- Testing requires elaborate mocking or actual API credentials even for unit tests
- Complex initialization logic is duplicated wherever you create agents, leading to inconsistencies
- Adding support for a new provider means modifying every file that creates agents
- Environment-specific logic clutters business code with `if ENV == "production"` conditionals everywhere
- Configuration changes require code changes and redeployment

## Practical Checklist
Before implementing a Factory Pattern, ask yourself:
- [ ] Do I need to create multiple variants of similar objects (different agent types, LLM providers, tool implementations)?
- [ ] Does object creation involve complex logic, configuration, or dependencies that would clutter client code?
- [ ] Do I need to choose which concrete class to instantiate at runtime based on configuration or user input?
- [ ] Am I switching between different implementations for testing vs. production?
- [ ] Would centralizing creation logic improve consistency and maintainability?
- [ ] Do I want to add new implementations without modifying existing client code?
- [ ] Is the abstraction valuable, or am I over-engineering a simple problem?

## Watch Out For
⚠️ **Over-engineering simple cases**: If you have two agent types that are unlikely to grow, a simple `if-else` might suffice. Don't create elaborate factory hierarchies for problems that don't warrant them. The pattern adds abstraction layers—make sure the flexibility is worth the complexity.

⚠️ **Factory bloat**: As you add more product types, factory methods can become long chains of `if-elif-else` or `switch` statements. This violates the Open/Closed Principle you're trying to achieve. Consider using a registry pattern (map of type strings to constructor functions) or dependency injection containers for complex scenarios.

⚠️ **God objects**: Factories that create too many unrelated types become "god objects" that know too much. An `AgentFactory` that also creates database connections, UI components, and logging systems has lost focus. Keep factories cohesive—one factory per domain or abstraction level.

⚠️ **Parallel class hierarchies**: Factory Method Pattern can lead to parallel hierarchies where every new product type requires both a new concrete product class and a new factory subclass. This doubles your maintenance burden. Simple Factory or Abstract Factory might be more appropriate.

⚠️ **Hidden dependencies**: When factories hide complex initialization, it becomes unclear what dependencies your code really has. If `AgentFactory.create()` secretly requires database connections, API keys, and configuration files, developers using the factory won't know until runtime. Document factory requirements clearly.

⚠️ **Testing challenges**: While factories improve testability of client code, the factory itself can be hard to test if it has complex conditional logic. Consider separating factory logic into testable strategy functions or using configuration-driven approaches.

⚠️ **Premature abstraction**: Don't create factories "just in case" you might need flexibility later (YAGNI). Build factories when you actually have multiple implementations or anticipate them based on concrete requirements, not speculation.

## Connections
**Builds On:**
- [solid_principles](solid_principles.md) - Particularly Open/Closed Principle (open for extension, closed for modification)
- [dependency_injection](dependency_injection.md) - Factories often work with DI containers
- [loose_coupling](loose_coupling.md) - Factories reduce coupling between client code and concrete classes
- [separation_of_concerns](separation_of_concerns.md) - Separates object creation from business logic
- Object-oriented programming fundamentals - Interfaces, inheritance, polymorphism

**Works With:**
- [strategy_pattern](strategy_pattern.md) - Factories can create strategies; strategies can use factories
- [adapter_pattern](adapter_pattern.md) - Factories often create adapters to wrap third-party implementations
- [singleton_pattern](singleton_pattern.md) - Factories can ensure single instances are returned
- [dependency_injection](dependency_injection.md) - DI containers often use factory patterns internally
- [clean_code](clean_code.md) - Factories promote cleaner, more maintainable code
- [decorator_pattern](decorator_pattern.md) - Factories can wrap created objects with decorators

**Leads To:**
- Abstract Factory Pattern - Families of related objects
- Builder Pattern - Complex object construction
- Dependency Injection Containers - Advanced object lifecycle management
- Plugin architectures - Dynamic loading of implementations
- [inversion_of_control](inversion_of_control.md) - Higher-level architectural pattern

**Related Patterns:**
- [agent_framework](../Agent_and_Orchestration/agent_framework.md) - Frameworks often use factories to create agents
- [tool_and_function_calling](../Agent_and_Orchestration/tool_and_function_calling.md) - Tool factories select implementations
- [multi-agent_system](../Agent_and_Orchestration/multi-agent_system.md) - Creating specialized agents dynamically
- Service Locator Pattern - Alternative to factories (though generally less preferred)
- Prototype Pattern - Creating objects by cloning prototypes

## Quick Decision Guide
**Use Factory Pattern when:**
- You have multiple implementations of an interface and need to choose at runtime
- Object creation is complex and should be centralized
- You want to support testing with mock implementations
- You need environment-specific implementations (dev vs. prod)
- You're abstracting across multiple LLM providers or agent types
- Configuration should drive which implementations are used
- You anticipate adding new implementations without modifying existing code

**Skip Factory Pattern when:**
- You have a single, unchanging implementation
- Object creation is trivial (simple constructor calls)
- The added abstraction doesn't provide value
- You're building a prototype where flexibility isn't needed yet
- Direct instantiation is clearer and you don't expect multiple implementations

## Further Exploration
- 📖 "Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of Four) - The canonical source for Factory Method and Abstract Factory patterns
- 🎯 "Head First Design Patterns" - Accessible introduction with practical examples
- 💡 "Refactoring to Patterns" by Joshua Kerievsky - When and how to introduce Factory Pattern into existing code
- 📖 "Clean Architecture" by Robert C. Martin - How factories fit into layered architectures
- 🎯 LangChain source code - Real-world examples of factories for creating LLM clients, embeddings, and vector stores
- 💡 Spring Framework documentation - Comprehensive dependency injection and factory patterns in enterprise context
- 📖 "Patterns of Enterprise Application Architecture" by Martin Fowler - Registry and Mapper patterns that extend factory concepts
- 🎯 Autogen framework - Multi-agent systems using factory patterns for agent creation
- 💡 "Dependency Injection Principles, Practices, and Patterns" - How factories integrate with modern DI

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
