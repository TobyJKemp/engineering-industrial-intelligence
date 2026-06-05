# Dependency Injection

## At a Glance

| Aspect | Detail |
|--------|--------|
| **What It Is** | A design pattern where objects receive their dependencies from external sources rather than creating them internally—enabling components to declare what they need without knowing how to obtain it |
| **Primary Function** | Decouples component implementation from dependency acquisition, allowing external configuration of how components are wired together at runtime |
| **Core Challenge** | Balancing flexibility and configurability against complexity and indirection—making systems more testable and modular without making them harder to understand |
| **Key Trade-Off** | Explicit dependencies and easy testing versus additional abstraction layers and potential over-engineering |
| **Success Indicator** | Components can be instantiated with different implementations of their dependencies for testing, configuration, or deployment scenarios without code changes |

## One-Sentence Summary

**Dependency injection** is a design pattern where objects receive their dependencies (services, configuration, resources they need to function) from external sources rather than creating or locating them internally—enabling loose coupling, testability, and flexible configuration by separating component logic from dependency acquisition and lifecycle management.

## Why This Matters to You

If you're building AI agents, ML systems, or intelligent applications in 2026, **dependency injection determines whether your system is flexible or brittle**.

You've experienced the pain without it: You build an AI agent that creates its own LLM client, database connection, and retrieval system internally. Now you need to test it—but can't mock the expensive LLM calls. You want to swap from OpenAI to Azure OpenAI—requires code changes throughout. You need to run different configurations for development vs. production—hard-coded values everywhere. Your "simple" agent became a tangled mess of hard-coded dependencies.

**This affects your AI development constantly:**

- **Your AI agent** hard-codes which LLM it uses (`client = OpenAI(api_key=...)`). Now you can't test without expensive API calls, can't A/B test different models, can't let users choose their preferred provider—every change requires modifying agent code.

- **Your RAG pipeline** creates its own embedding model, vector database, and chunking strategy. You want to experiment with different approaches—but they're tightly coupled. Testing requires spinning up real infrastructure. Configuration changes mean code edits.

- **Your multi-agent system** has agents that instantiate their own tools. Agent A creates a DatabaseTool, Agent B creates another instance—no shared connection pooling, no centralized configuration, no way to inject mock tools for testing.

- **Your ML training pipeline** hard-codes data loaders, model architectures, training strategies. Running experiments means editing code, not just changing configuration. Testing components in isolation is nearly impossible.

**The 2026 AI impact:** Modern AI systems are *inherently compositional*—agents with swappable tools, RAG with configurable retrievers, multi-model systems with fallback strategies, orchestrators with pluggable components. Dependency injection is how you make composition practical rather than brittle.

**The career consequence:** Engineers who use dependency injection build AI systems that are testable (mock expensive dependencies), configurable (swap models/tools/strategies without code changes), modular (components work independently), and evolvable (add new capabilities by configuration). Those who don't create systems that seem simple initially but become unmaintainable as requirements change.

Understanding dependency injection transforms how you structure AI agents (inject tools and models), design ML pipelines (inject data sources and strategies), build RAG systems (inject retrievers and embedders), and test AI components (inject mocks and stubs). It's the difference between "change the code" and "change the configuration."

## The Core Idea

### What It Is

**Dependency injection (DI)** is a design pattern and architectural technique where objects receive their dependencies—services, configuration, resources, collaborators they need to function—from external sources through constructors, methods, or properties, rather than creating those dependencies internally through direct instantiation or global access.

**The fundamental principle:** A component declares *what* it needs (interfaces, abstract dependencies) but doesn't know *how* to obtain it. An external entity (DI container, composition root, manual wiring) provides concrete implementations.

**Three primary injection patterns:**

1. **Constructor Injection** — Dependencies passed through constructor parameters (preferred for required dependencies):
```python
class RAGAgent:
    def __init__(self, llm: LLMClient, retriever: VectorRetriever, 
                 prompt_template: PromptTemplate):
        self.llm = llm
        self.retriever = retriever
        self.prompt_template = prompt_template
    
    def query(self, question: str) -> str:
        context = self.retriever.retrieve(question)
        prompt = self.prompt_template.format(question, context)
        return self.llm.generate(prompt)

# External configuration provides dependencies:
agent = RAGAgent(
    llm=AzureOpenAIClient(endpoint=config.azure_endpoint),
    retriever=PineconeRetriever(index=config.vector_index),
    prompt_template=load_template("rag_prompt.txt")
)
```

2. **Setter/Property Injection** — Dependencies set through methods or properties (for optional dependencies):
```python
class MLPipeline:
    def __init__(self, model: Model):
        self.model = model
        self._logger = default_logger  # Default
        self._monitor = None  # Optional
    
    def set_logger(self, logger: Logger):
        self._logger = logger
    
    def set_monitor(self, monitor: MetricsMonitor):
        self._monitor = monitor
```

3. **Interface/Method Injection** — Dependencies passed to methods that need them:
```python
class AgentExecutor:
    def execute(self, task: Task, tools: List[Tool], 
                context: ExecutionContext):
        # Dependencies provided per execution
        pass
```

**Key characteristics:**

- **Explicit dependencies:** Component signatures declare what they need—no hidden dependencies
- **Dependency inversion:** Components depend on abstractions (interfaces), not concrete implementations
- **External configuration:** Wiring happens outside components, often in a "composition root"
- **Lifecycle management:** External entity controls dependency creation, sharing, disposal
- **Testability:** Easy to inject mocks, stubs, or alternative implementations

**Dependency Injection Containers (DI Frameworks):**

Modern applications often use DI containers that automate dependency resolution:

```python
# Registration (composition root):
container = Container()
container.register(LLMClient, AzureOpenAIClient, singleton=True)
container.register(VectorRetriever, PineconeRetriever)
container.register(PromptTemplate, lambda: load_template("rag_prompt.txt"))
container.register(RAGAgent, RAGAgent)  # Auto-resolves dependencies

# Resolution (automatic):
agent = container.resolve(RAGAgent)  # Container builds entire dependency graph
```

**For 2026 AI systems, dependency injection enables:**

- **Model swapping:** Inject different LLM implementations (OpenAI, Anthropic, Azure, local) without agent code changes
- **Tool registration:** Agents receive tools through injection, enabling dynamic tool sets
- **Retriever configuration:** RAG systems work with any retriever implementing the interface
- **Environment-specific behavior:** Inject production vs. development dependencies based on configuration
- **Testing isolation:** Inject mocks for expensive external dependencies (LLM calls, vector databases)
- **A/B testing:** Different users get different model implementations transparently
- **Fallback strategies:** Inject retry wrappers, circuit breakers, fallback implementations
- **Observability:** Inject telemetry, logging, monitoring without modifying core logic

### What It Isn't

**Dependency injection is NOT:**

❌ **Service Locator pattern** — Components actively requesting dependencies from a registry/container (DI *provides* dependencies; service locator requires components to *request* them)

❌ **Just passing parameters** — DI specifically refers to providing *dependencies* (collaborating objects that provide services) rather than configuration data or request parameters

❌ **Only about frameworks** — DI is a pattern; frameworks (Spring, .NET DI, dependency_injector) automate it, but you can do manual "poor man's DI" without frameworks

❌ **Dependency creation** — DI separates *using* dependencies from *creating* them; the pattern is about *injection*, not construction

❌ **Always better** — Simple systems with few dependencies may be clearer with direct instantiation; DI adds valuable indirection for complex systems

❌ **Automatic** — Someone must configure how dependencies wire together (composition root); DI doesn't eliminate configuration, it centralizes it

❌ **Only for testing** — Testing benefits are significant, but DI primarily enables flexible, modular architecture; testability is a bonus

❌ **Just IoC (Inversion of Control)** — IoC is broader principle (framework calls your code); DI is specific technique for achieving IoC for dependencies

❌ **Removing all coupling** — Components still depend on interfaces/abstractions; DI removes *implementation* coupling, not all coupling

❌ **A silver bullet** — Over-using DI creates unnecessary indirection; use where flexibility and testability matter

## How It Works

**Dependency injection follows a systematic pattern for separating component logic from dependency management:**

### 1. **Dependency Declaration**

Components explicitly declare dependencies through constructor parameters, properties, or method signatures:

```python
# Agent declares what it needs via constructor:
class ResearchAgent:
    def __init__(self, 
                 llm: LLMClient,              # Required dependency
                 search_tool: SearchTool,      # Required dependency
                 memory: ConversationMemory,   # Required dependency
                 max_iterations: int = 10):    # Configuration (not a dependency)
        self.llm = llm
        self.search_tool = search_tool
        self.memory = memory
        self.max_iterations = max_iterations
```

**Key principle:** Dependencies are *declared* in signatures, making them explicit and discoverable.

### 2. **Dependency Abstraction**

Components depend on interfaces or abstract base classes, not concrete implementations:

```python
# Abstract interface:
class LLMClient(Protocol):
    def generate(self, prompt: str, **kwargs) -> str:
        ...
    
    def stream(self, prompt: str) -> Iterator[str]:
        ...

# Multiple implementations:
class OpenAIClient(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        return openai.ChatCompletion.create(...)

class AnthropicClient(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        return anthropic.messages.create(...)

class MockLLMClient(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        return "Mock response for testing"
```

**Key principle:** Components depend on *what* services do (interface), not *how* they do it (implementation).

### 3. **Composition Root**

Application startup code (composition root) configures and wires dependencies:

```python
# Application entry point:
def create_production_agent() -> ResearchAgent:
    # Create dependencies:
    llm = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    search = BingSearchTool(api_key=os.getenv("BING_KEY"))
    memory = RedisMemory(connection=os.getenv("REDIS_URL"))
    
    # Inject into agent:
    return ResearchAgent(
        llm=llm,
        search_tool=search,
        memory=memory,
        max_iterations=20
    )

def create_test_agent() -> ResearchAgent:
    # Inject test doubles:
    return ResearchAgent(
        llm=MockLLMClient(),
        search_tool=MockSearchTool(),
        memory=InMemoryMemory(),
        max_iterations=5
    )
```

**Key principle:** Wiring configuration centralized at application root, separated from business logic.

### 4. **Dependency Lifetime Management**

External entity controls when dependencies are created, shared, and disposed:

```python
class Container:
    def __init__(self):
        self._singletons = {}
        self._factories = {}
    
    def register_singleton(self, interface, implementation):
        """Single instance shared across all consumers"""
        if interface not in self._singletons:
            self._singletons[interface] = implementation()
    
    def register_transient(self, interface, factory):
        """New instance per request"""
        self._factories[interface] = factory
    
    def resolve(self, interface):
        if interface in self._singletons:
            return self._singletons[interface]
        if interface in self._factories:
            return self._factories[interface]()
        raise ValueError(f"No registration for {interface}")
```

**Common lifetimes:**
- **Singleton:** One instance for entire application (LLM clients, database connections)
- **Transient:** New instance per request (agents, request handlers)
- **Scoped:** One instance per scope/session (conversation memory per session)

### 5. **Dependency Resolution**

Container automatically builds complex dependency graphs:

```python
# Complex dependency graph:
class RAGAgent:
    def __init__(self, llm: LLMClient, retriever: VectorRetriever):
        ...

class VectorRetriever:
    def __init__(self, embedder: Embedder, vector_db: VectorDatabase):
        ...

class Embedder:
    def __init__(self, model_client: ModelClient):
        ...

# Container resolves entire graph:
container = Container()
container.register_singleton(ModelClient, OpenAIEmbeddings)
container.register_singleton(VectorDatabase, PineconeDB)
container.register_transient(Embedder, Embedder)
container.register_transient(VectorRetriever, VectorRetriever)
container.register_transient(RAGAgent, RAGAgent)

# Single call resolves: RAGAgent → VectorRetriever → Embedder → ModelClient
agent = container.resolve(RAGAgent)
```

**Key principle:** Container recursively resolves dependencies, building object graphs automatically.

### 6. **Configuration-Driven Wiring**

Dependency wiring can be driven by configuration files:

```yaml
# config.yaml
dependencies:
  llm:
    implementation: AzureOpenAIClient
    config:
      endpoint: ${AZURE_OPENAI_ENDPOINT}
      model: gpt-4
  
  retriever:
    implementation: PineconeRetriever
    config:
      index: production-embeddings
  
  agent:
    implementation: RAGAgent
    dependencies:
      - llm
      - retriever
```

**Key principle:** Wiring changes through configuration, not code changes.

## Think of It Like This

**Dependency injection is like hiring specialists versus doing everything yourself.**

**Without DI (doing it yourself):**

You're building a house. You:
- Learn plumbing yourself and install pipes
- Learn electrical work yourself and wire outlets
- Learn HVAC yourself and install heating
- Learn carpentry yourself and build cabinets

You control everything, but you're not an expert at any of it. Changing approaches means relearning everything. Testing is impossible (you can't test plumbing without real water).

**With DI (hiring specialists):**

You're the general contractor. You:
- Define what you need: "I need plumbing that provides water to these locations"
- Hire specialists who implement interfaces: PlumberInterface, ElectricianInterface
- Don't care *how* they do their work, only that they fulfill the contract
- Can swap specialists if needed (different plumber for different approach)
- Can use "mock" specialists for testing (simulate water flow without real pipes)

**In code:**

```python
# Without DI (doing everything yourself):
class Agent:
    def __init__(self):
        # Agent creates its own dependencies:
        self.llm = OpenAI(api_key="...")  # Hard-coded implementation
        self.db = Database("connection_string")  # Hard-coded
        self.retriever = VectorRetriever(self.db)  # Tightly coupled
    
    def query(self, question: str):
        # Can't test without real OpenAI, real database
        # Can't swap implementations without changing this code
        # Hard to reuse agent with different dependencies
        ...

# With DI (hiring specialists):
class Agent:
    def __init__(self, llm: LLMClient, retriever: Retriever):
        # Agent declares what it needs, external code provides it:
        self.llm = llm  # Any LLMClient implementation
        self.retriever = retriever  # Any Retriever implementation
    
    def query(self, question: str):
        # Same code works with production OpenAI or test mocks
        # Same code works with any LLM provider
        # Agent focuses on logic, not dependency creation
        ...

# External code configures:
agent = Agent(
    llm=OpenAIClient(api_key=config.key),
    retriever=PineconeRetriever(config.index)
)
# Or:
test_agent = Agent(
    llm=MockLLM(),
    retriever=MockRetriever()
)
```

**The key insight:** You're not eliminating dependencies (the house still needs plumbing). You're separating *using* dependencies from *creating* them, enabling flexibility, testability, and modularity.

## The "So What?" Factor

**Why dependency injection is critical for modern AI systems:**

### For AI Agent Systems (Where Flexibility Determines Adaptability)

AI agents in 2026 need unprecedented flexibility:

- **Multi-model strategies:** Production agents use GPT-4 for complex reasoning, GPT-3.5-turbo for simple tasks, local models for sensitive data. Without DI, switching models means code changes. With DI, inject different `LLMClient` implementations based on context.

- **Dynamic tool sets:** Different users or scenarios need different tools. Without DI, tools are hard-coded. With DI, inject appropriate tool collections: `Agent(llm, tools=[SearchTool(), CalculatorTool()])` vs `Agent(llm, tools=[DatabaseTool(), AnalyticsTool()])`.

- **Testing AI behavior:** Testing agents with real LLMs is expensive, slow, non-deterministic. With DI, inject `MockLLMClient` that returns predefined responses: `agent = Agent(llm=MockLLM(responses=["test response"]))`.

- **Environment-specific configuration:** Development uses cheaper models, production uses premium models. With DI, same agent code, different dependencies: `agent = Agent(llm=dev_llm)` vs `agent = Agent(llm=prod_llm)`.

**Example impact:** Team building multi-agent customer support system. Without DI: Each agent hard-codes OpenAI client, testing requires $50/day in API costs, switching to Azure OpenAI requires editing 15+ agent files. With DI: Agents receive LLM through constructor, testing uses mocks (zero API cost), switching to Azure means changing composition root only, A/B testing different models is configuration change.

### For RAG Systems (Where Component Swapping Enables Experimentation)

RAG systems have multiple configurable components:

```python
# RAG components as injected dependencies:
class RAGPipeline:
    def __init__(self,
                 embedder: Embedder,
                 vector_store: VectorStore,
                 retriever: Retriever,
                 reranker: Optional[Reranker],
                 llm: LLMClient):
        self.embedder = embedder
        self.vector_store = vector_store
        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm

# Experimentation through dependency injection:
# Experiment 1: OpenAI embeddings + Pinecone + GPT-4
pipeline_v1 = RAGPipeline(
    embedder=OpenAIEmbedder(model="text-embedding-3-large"),
    vector_store=PineconeStore(index="v1"),
    retriever=DenseRetriever(top_k=5),
    reranker=None,
    llm=OpenAIClient(model="gpt-4")
)

# Experiment 2: Local embeddings + ChromaDB + reranking + local LLM
pipeline_v2 = RAGPipeline(
    embedder=SentenceTransformerEmbedder(model="all-MiniLM-L6-v2"),
    vector_store=ChromaStore(path="./db"),
    retriever=HybridRetriever(top_k=10),
    reranker=CrossEncoderReranker(top_n=3),
    llm=OllamaClient(model="llama2")
)
```

**The impact:** Same RAG pipeline code runs dozens of experimental configurations by injecting different components. Testing evaluates each configuration systematically. Production deployment is choosing the winning configuration and injecting production-grade dependencies.

### For Testing AI Systems (Where Mocking Enables Fast, Deterministic Tests)

AI systems have expensive, non-deterministic external dependencies:

```python
# Agent with injected dependencies:
class ResearchAgent:
    def __init__(self, llm: LLMClient, search: SearchTool):
        self.llm = llm
        self.search = search
    
    def research(self, topic: str) -> str:
        results = self.search.search(topic)
        prompt = f"Summarize: {results}"
        return self.llm.generate(prompt)

# Production (real dependencies):
prod_agent = ResearchAgent(
    llm=OpenAIClient(api_key=key),
    search=BingSearchTool(api_key=bing_key)
)

# Testing (mock dependencies):
def test_research_agent():
    mock_llm = MockLLMClient(response="Test summary")
    mock_search = MockSearchTool(results=["Result 1", "Result 2"])
    
    agent = ResearchAgent(llm=mock_llm, search=mock_search)
    result = agent.research("AI safety")
    
    assert result == "Test summary"
    assert mock_search.was_called_with("AI safety")
```

**The impact:** Tests run in milliseconds (no API calls), deterministically (predefined mock responses), cheaply (no API costs), in isolation (no external dependencies). Teams test AI systems comprehensively without infrastructure dependencies.

### For Multi-Tenant AI Systems (Where Configuration Varies Per Tenant)

SaaS AI platforms need per-tenant configuration:

```python
# Different tenants get different dependencies:
def create_agent_for_tenant(tenant_id: str) -> Agent:
    tenant_config = load_tenant_config(tenant_id)
    
    # Inject tenant-specific LLM:
    if tenant_config.llm_provider == "openai":
        llm = OpenAIClient(api_key=tenant_config.openai_key)
    elif tenant_config.llm_provider == "azure":
        llm = AzureOpenAIClient(endpoint=tenant_config.azure_endpoint)
    elif tenant_config.llm_provider == "anthropic":
        llm = AnthropicClient(api_key=tenant_config.anthropic_key)
    
    # Inject tenant-specific vector store:
    vector_store = create_tenant_vector_store(tenant_id)
    
    # Inject tenant-specific tools:
    tools = load_tenant_tools(tenant_config.enabled_tools)
    
    return Agent(llm=llm, vector_store=vector_store, tools=tools)
```

**The impact:** Same agent code serves all tenants with different LLM providers, storage backends, tool configurations. New tenant onboarding is configuration, not code changes.

## Practical Checklist

**When designing new components:**

✅ **Identify dependencies**
   - What services, resources, or collaborators does this component need?
   - Which are required vs. optional?
   - Which might vary between environments or configurations?

✅ **Depend on abstractions**
   - Define interfaces or abstract base classes for dependencies
   - Component depends on interface, not concrete implementation
   - Enables multiple implementations (production, testing, alternatives)

✅ **Use constructor injection for required dependencies**
   - Pass dependencies through constructor parameters
   - Makes dependencies explicit and obvious
   - Ensures component is never in invalid state (missing required dependencies)

✅ **Use setter injection for optional dependencies**
   - Optional dependencies via properties/setters
   - Provide sensible defaults
   - Allow customization without forcing configuration

✅ **Avoid service locator pattern**
   - Don't have components request dependencies from container/registry
   - Have dependencies provided to components
   - Makes dependencies explicit, not hidden

✅ **Keep constructors simple**
   - Constructor should store dependencies, not do work
   - Avoid complex logic in constructors
   - Enables easy instantiation for testing

**When creating composition roots:**

✅ **Centralize wiring configuration**
   - Single location for dependency configuration
   - Easier to understand application structure
   - Simpler to change wiring for different environments

✅ **Configure lifetimes appropriately**
   - Singleton: Expensive resources (database connections, LLM clients)
   - Transient: Stateful components (agents, request handlers)
   - Scoped: Per-session resources (conversation memory)

✅ **Use configuration files**
   - Externalize wiring to configuration when practical
   - Enables deployment-time changes without recompilation
   - Supports different configurations for different environments

✅ **Handle dependency chains**
   - Resolve complex dependency graphs automatically
   - Avoid manual wiring of deep dependency trees
   - Use DI container for automatic resolution

**For AI-specific components:**

✅ **Inject LLM clients**
   - Never instantiate LLM clients inside agents
   - Inject through constructor: `Agent(llm: LLMClient)`
   - Enables model swapping, testing, A/B testing

✅ **Inject tool collections**
   - Agents receive tools as dependencies: `Agent(tools: List[Tool])`
   - Enables dynamic tool sets per agent instance
   - Testing with mock tools

✅ **Inject retrieval components**
   - RAG systems inject embedders, vector stores, retrievers
   - Experiment with different components through injection
   - Test with in-memory implementations

✅ **Inject observability**
   - Inject loggers, metrics collectors, tracers
   - Add observability without modifying core logic
   - Different observability strategies per environment

**For testing:**

✅ **Create test doubles**
   - Build mock implementations of dependencies
   - Return predefined responses for deterministic testing
   - Verify interactions with dependencies

✅ **Inject mocks through same interface**
   - Test code uses same injection mechanism as production
   - `agent = Agent(llm=MockLLM())` vs `agent = Agent(llm=OpenAIClient())`
   - No special test scaffolding

✅ **Test component in isolation**
   - Inject mocks for all external dependencies
   - Test component logic independently
   - Fast, deterministic, isolated tests

## Watch Out For

**Over-Injection (Dependency Explosion)** — Components with 8, 10, 15+ constructor parameters become unmanageable. Each dependency adds complexity. Often indicates component is doing too much or dependencies are too granular. *Mitigation:* Group related dependencies into higher-level abstractions, apply Single Responsibility Principle, consider facade pattern for complex dependency groups.

**Hidden Complexity** — DI moves complexity from component internals to composition root and container configuration. While component code becomes simpler, wiring configuration can become complex and opaque—especially with deeply nested dependency graphs and conditional wiring. *Mitigation:* Keep composition roots organized, document wiring decisions, use configuration files for clarity, avoid overly clever container tricks.

**Runtime Errors for Configuration Problems** — With direct instantiation, missing dependencies cause compile-time errors. With DI containers, misconfiguration often discovered at runtime when container tries to resolve dependencies. *Mitigation:* Use DI containers with compile-time validation when possible, write container configuration tests, validate container at startup before handling requests.

**Lifetime Mismatches** — Injecting transient dependency into singleton creates unintended sharing. Injecting singleton into scoped breaks isolation. Short-lived component capturing long-lived dependency causes memory leaks. *Mitigation:* Understand and document lifetime requirements, avoid singleton dependencies in transient components, use scoped lifetimes carefully.

**Testing Becomes Too Easy** — Easy mocking can lead to testing only the easy paths—mocking away all complexity. Tests become "green" but don't validate real system behavior. Integration gaps emerge between mocked unit tests and production. *Mitigation:* Balance unit tests (mocked dependencies) with integration tests (real dependencies), test critical paths with real implementations, use contract tests to verify mocks match reality.

**Abstraction Overhead** — Every dependency requires an interface. Simple systems become over-engineered with interfaces, factories, containers for components that never change. *Mitigation:* Use DI where flexibility and testability matter, direct instantiation for simple, stable dependencies. Prefer "poor man's DI" (manual wiring) over frameworks for small systems.

**Container Magic and Indirection** — Advanced DI containers use reflection, decorators, conventions, auto-wiring—making dependency resolution opaque. Debugging becomes difficult when you can't see how components are wired. *Mitigation:* Prefer explicit configuration over convention when possible, document complex container behavior, consider simpler manual DI for critical paths.

**Circular Dependencies** — Component A depends on B, B depends on A. DI containers detect and fail, but fixing requires redesign. *Mitigation:* Design to avoid circular dependencies (usually indicates design smell), use events/mediator pattern to break cycles, introduce interfaces to invert dependencies.

**Interface Proliferation** — Creating interfaces for everything "because DI" leads to interface explosion. One-to-one interface-to-implementation relationships add ceremony without value. *Mitigation:* Create interfaces when multiple implementations exist or are likely, use concrete classes when appropriate (Python duck typing), focus on abstractions that matter.

**Configuration Drift** — Different environments (dev, test, staging, production) have different dependency configurations. Keeping configurations synchronized and correct becomes operational burden. *Mitigation:* Use environment-specific configuration files, validate configurations at startup, automate configuration management, maintain configuration documentation.

**Premature Abstraction** — Creating abstract interfaces for dependencies "just in case" before knowing requirements. YAGNI (You Aren't Gonna Need It) violation—abstractions add complexity without delivering value. *Mitigation:* Start concrete, refactor to abstract when second implementation needed, prefer simple code over "flexible" code until flexibility required.

## Connections

**Related Concepts in This Vocabulary:**

- **[inversion_of_control](inversion_of_control.md)** — Broader principle where framework controls flow; dependency injection is specific technique for achieving IoC for dependency management

- **[design_pattern](design_pattern.md)** — Reusable solutions to common problems; dependency injection is a structural design pattern for managing object dependencies

- **[interface_design](interface_design.md)** — Defining contracts between components; dependency injection relies on depending on interfaces rather than implementations

- **[separation_of_concerns](separation_of_concerns.md)** — Dividing program into distinct sections; DI separates component logic from dependency acquisition and lifecycle management

- **[modular_architecture](../System_Architecture/modular_architecture.md)** — Building systems from independent modules; dependency injection enables true modularity by decoupling components from their dependencies

- **[testability](../Testing_and_Evaluation/testability.md)** — Design for ease of testing; dependency injection is primary technique for making components testable by enabling mock injection

- **[configuration_management](../MLOps/configuration_management.md)** — Managing application settings; DI enables configuration-driven component wiring for different environments

- **[composition_over_inheritance](composition_over_inheritance.md)** — Favoring object composition; DI facilitates composition by making dependencies explicit and injectable

**Extended Exploration:**

- **DI containers and frameworks** (Spring, .NET Core DI, dependency_injector, Guice) and their trade-offs
- **Dependency injection in AI agent frameworks** (LangChain, AutoGen, CrewAI) and architectural patterns
- **Testing patterns with DI** (mocks, stubs, fakes, test doubles) for AI systems
- **Lifetime management strategies** for different dependency types in long-running AI systems
- **Factory pattern and DI** for creating objects with runtime-determined dependencies
- **Service mesh and DI** for distributed systems dependency management

## Quick Decision Guide

**When should you use dependency injection?**

✅ Component has dependencies that vary between environments (dev, test, production)
✅ You need to test component in isolation without real external dependencies
✅ Multiple implementations of dependency exist or are likely (different LLM providers, storage backends)
✅ Component will be reused in different contexts with different dependencies
✅ Dependencies are expensive or complex to create (database connections, LLM clients)
✅ You want configuration-driven behavior (swap implementations via configuration)

**When is direct instantiation acceptable?**

✅ Dependency is simple, stable, has single implementation unlikely to change
✅ Component and dependency are tightly coupled by nature (durable pair)
✅ System is small and complexity of DI outweighs benefits
✅ Dependency is pure data/value object, not a service
✅ You're in prototyping phase and flexibility isn't needed yet

**Which injection pattern should you use?**

- **Constructor injection:** Required dependencies, immutable after construction, clear dependency graph
- **Setter injection:** Optional dependencies, need to change after construction, defaults available
- **Method injection:** Dependency needed only for specific method, varies per method call
- **Property injection:** Framework conventions, late binding, optional dependencies

**Do you need a DI container/framework?**

✅ YES if: Complex dependency graphs, many components, need lifetime management, large team benefits from conventions
✅ NO if: Simple application, few dependencies, manual wiring is clear, prefer explicitness over magic

**For AI systems specifically:**

✅ **Always inject:** LLM clients, vector stores, embedding models, external APIs, expensive resources
✅ **Usually inject:** Tools, retrievers, prompt templates, parsing strategies, observability
✅ **Sometimes inject:** Configuration values, simple utilities, pure functions
✅ **Rarely inject:** Data objects, enums, primitive values, internal helpers

## Further Exploration

**Foundational Concepts:**
- "Dependency Injection Principles, Practices, and Patterns" (Seemann & van Deursen, 2019) — Comprehensive DI guide
- Martin Fowler's "Inversion of Control Containers and the Dependency Injection pattern" (2004) — Foundational article defining DI patterns
- Robert C. Martin's "SOLID Principles" — Dependency Inversion Principle as foundation for DI

**Framework Documentation:**
- Python: `dependency_injector`, `injector`, FastAPI dependencies
- .NET: Built-in Microsoft.Extensions.DependencyInjection
- Java: Spring Framework, Google Guice
- TypeScript/JavaScript: InversifyJS, TSyringe

**For AI-Specific Applications:**
- LangChain architecture — Dependency patterns in AI agent frameworks
- Ray Serve — Dependency injection for ML model serving
- Testing AI systems — Mock LLMs, embedders, retrievers for deterministic testing
- Multi-model systems — Injecting different models for different scenarios

**Advanced Topics:**
- Aspect-Oriented Programming (AOP) — Cross-cutting concerns through DI
- Factory patterns with DI — Creating objects with runtime-determined dependencies
- Service lifetime patterns — Singleton, transient, scoped in distributed systems
- DI in microservices — Service mesh and dependency management across services

**Practical Resources:**
- Design patterns in Python with type hints and protocols
- Testing strategies with pytest fixtures and dependency injection
- DI container performance and startup optimization
- Configuration-driven DI for cloud-native applications

---

*Entry completed: May 14, 2026*  
*Confidence: High — Dependency injection is well-established software engineering pattern, increasingly critical for flexible AI systems*  
*Needs refinement: Emerging patterns for DI in multi-agent systems and distributed AI architectures*