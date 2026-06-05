# High Cohesion

## At a Glance
| | |
|---|---|
| **Category** | Software Design Principle |
| **Complexity** | Beginner |
| **Time to Learn** | 1-2 hours for concept, ongoing practice to master |
| **Prerequisites** | Basic understanding of functions, classes, and modules |

## One-Sentence Summary
High cohesion is the principle that a module, class, or function should have a single, well-focused purpose where all its elements work together toward that purpose, rather than doing many unrelated things.

## Why This Matters to You
When you build AI agent systems, you're creating complex architectures with many moving parts: agents that orchestrate tasks, tools that interact with APIs, prompt builders that construct context, memory managers that store conversation history, and evaluation functions that score outputs. If you create an `AgentHelper` class that handles prompt construction, logs to databases, makes API calls, validates outputs, manages memory, and sends monitoring metrics, you've created a maintenance nightmare—a tangled mess where fixing one thing breaks three others, testing requires mocking ten dependencies, and nobody understands what the class actually does. High cohesion guides you to create focused components: a `PromptBuilder` that only builds prompts, a `MemoryStore` that only manages memory, a `MetricsCollector` that only tracks metrics. Each component is easy to understand, test, modify, and reuse because it does one thing well. In 2026's complex AI systems with dozens of interacting components, high cohesion is the difference between maintainable architecture and spaghetti code.

## The Core Idea
### What It Is
High cohesion is a qualitative measure of how strongly related and focused the responsibilities within a single software module are. A highly cohesive module contains code that all serves a unified purpose—the functions, methods, and data all work together toward a single, well-defined goal.

Think of cohesion as **internal relatedness**. Within a class or module:
- Do all the methods operate on the same data?
- Do all the functions support the same overarching purpose?
- Could you describe what the module does in a single, clear sentence?
- Would changes to one part naturally involve changes to other parts?

**High cohesion** means the answer to these questions is "yes"—the module is focused and unified. A `VectorStore` class that provides methods for storing embeddings, retrieving similar vectors, and managing the embedding index has high cohesion. All methods work with embeddings and support the single purpose of vector storage and retrieval.

**Low cohesion** means the module does many unrelated things. An `AgentUtilities` class with methods for logging, sending emails, parsing JSON, retrying API calls, and validating schemas has low cohesion—these are unrelated responsibilities forced into one container.

Cohesion exists on a spectrum from lowest to highest:

1. **Coincidental Cohesion** (worst): Random, unrelated functions grouped together (`Utils`, `Helpers`)
2. **Logical Cohesion**: Functions that perform similar operations but on different data (a class with `format_json()`, `format_xml()`, `format_yaml()`)
3. **Temporal Cohesion**: Functions executed at the same time but for different reasons (`initialize()` that sets up database, loads config, and starts logging)
4. **Procedural Cohesion**: Functions that follow a sequence but serve different purposes (steps in a pipeline)
5. **Communicational Cohesion**: Functions that operate on the same data but for different purposes
6. **Sequential Cohesion**: Output of one function is input to another, forming a processing chain
7. **Functional Cohesion** (best): All elements contribute to a single, well-defined task

In 2026's AI agent development, high cohesion means:
- **Agent roles**: Each agent has a focused specialty (research agent, coding agent, analysis agent) rather than a general "do everything" agent
- **Tool design**: Tools do one thing well—a `WebSearchTool` searches the web, not searches, parses, summarizes, and caches
- **Prompt modules**: Prompt builders construct prompts, they don't also make API calls and parse responses
- **Memory components**: Memory stores manage conversation history, not also handle embeddings, retrieve documents, and run queries
- **Evaluation functions**: Metrics calculate specific scores (accuracy, relevance, toxicity), not also log results, update dashboards, and alert teams

### What It Isn't
High cohesion is not the same as **small size**. A module can be small and have low cohesion (a 50-line `Utils` class with ten unrelated functions), or large and have high cohesion (a 500-line `PromptTemplateEngine` that comprehensively handles template parsing, variable substitution, conditional logic, and rendering—all cohesively supporting prompt generation).

It's not about **single method classes**. Taking cohesion to an extreme where every class has one method creates unnecessary fragmentation. A `VectorStore` with `add_vector()`, `search_similar()`, `delete_vector()`, and `update_index()` has high cohesion despite having multiple methods because they all support the unified purpose of vector storage.

High cohesion doesn't mean **no dependencies**. A highly cohesive class can depend on many other classes. A `ConversationAgent` that depends on `PromptBuilder`, `LLMClient`, `MemoryStore`, and `ToolExecutor` can still have high cohesion if all its methods focus on conducting conversations by orchestrating these dependencies.

It's not the same as [**loose coupling**](loose_coupling.md), though they're related. Cohesion is about **internal** focus (what a module contains), while coupling is about **external** dependencies (what a module depends on). Ideal design has high cohesion (focused modules) and loose coupling (minimal dependencies). They're complementary principles.

Finally, high cohesion is not about **never mixing concerns**. Sometimes related concerns naturally coexist. A `CachingVectorStore` that combines caching logic with vector storage might be acceptable if caching is integral to how the vector store works. The key is whether the concerns truly support a unified purpose.

## How It Works

### Identifying Cohesion Levels

**High Cohesion Example (AI Agent Tool):**
```python
class WebSearchTool:
    """Performs web searches and returns results."""
    
    def __init__(self, api_key: str, max_results: int = 10):
        self.client = SearchAPIClient(api_key)
        self.max_results = max_results
    
    def search(self, query: str) -> List[SearchResult]:
        """Execute web search and return results."""
        return self.client.search(query, limit=self.max_results)
    
    def search_with_context(self, query: str, context: str) -> List[SearchResult]:
        """Execute web search with additional context."""
        enhanced_query = f"{query} {context}"
        return self.search(enhanced_query)
```
**Why it's cohesive**: Every method serves the single purpose of web searching. All data and methods are focused on that goal.

**Low Cohesion Example:**
```python
class AgentHelper:
    """Utility functions for agents."""  # Red flag: vague purpose
    
    def search_web(self, query: str) -> List[SearchResult]:
        """Search the web."""
        # ...
    
    def log_to_database(self, message: str):
        """Log message to database."""
        # ...
    
    def validate_json(self, data: str) -> bool:
        """Check if string is valid JSON."""
        # ...
    
    def send_slack_alert(self, text: str):
        """Send alert to Slack."""
        # ...
    
    def calculate_token_count(self, text: str) -> int:
        """Count tokens in text."""
        # ...
```
**Why it's not cohesive**: These are unrelated functions thrown together. They don't support a unified purpose. This should be split into separate modules: `WebSearchTool`, `DatabaseLogger`, `JsonValidator`, `SlackNotifier`, `TokenCounter`.

### Achieving High Cohesion

**1. Single Responsibility Focus**
Start by articulating the module's purpose in one sentence. If you need "and" or "or" to describe it, you likely have low cohesion.
- Good: "This class manages conversation memory"
- Bad: "This class manages memory and logs to databases and sends alerts"

**2. Group Related Functions**
Functions that operate on the same data or support the same purpose belong together.

**3. Split Unrelated Concerns**
When you find a class doing multiple unrelated things, extract them into separate modules:
- Extract utility functions into their own modules
- Move logging to a dedicated logger
- Separate validation logic from business logic

**4. The "Would I Change These Together?" Test**
If requirements change, would you modify all the methods in this class together, or just some? If just some, the class may have low cohesion.

## Think of It Like This
Imagine you're organizing a toolbox.

**High Cohesion** is like having specialized compartments: one section for screwdrivers (flathead, Phillips, Torx—all tools for driving screws), one for wrenches (all tools for tightening bolts), one for measuring tools (rulers, tape measures, levels). When you need to drive a screw, you know exactly where to look. When you buy a new screwdriver, you know where it goes.

**Low Cohesion** is throwing everything into one drawer: screwdrivers mixed with tape measures, wrenches tangled with extension cords, sandpaper scattered among drill bits. Finding the right tool takes forever. Adding a new tool means cramming it wherever there's space. You can't remember what's in there or whether you already have what you need.

In software, high cohesion is organizing your code into focused "compartments" where related functionality lives together. When you need to work on prompt generation, you go to `PromptBuilder`. When you need to add a new prompt feature, you know exactly which module to extend. Low cohesion is the "junk drawer" approach where related functionality is scattered and unrelated functionality is jumbled together.

## The "So What?" Factor
**If you design for high cohesion:**
- You can understand what a module does by reading its name and a few lines of code
- Testing is straightforward because each module has a clear, focused responsibility with minimal dependencies
- Changes are localized—modifying prompt logic doesn't risk breaking memory management or logging
- Reusing code is easy because modules do one thing well and don't drag in unrelated dependencies
- New team members onboard faster because modules have clear, understandable purposes
- Debugging is easier because you know which module handles which responsibility
- Parallel development works better because different team members can work on different cohesive modules without conflicts

**If you don't:**
- Module purposes are unclear—"What does `AgentManager` actually manage?"
- Testing requires mocking dozens of unrelated dependencies
- Changes ripple unpredictably—fixing a bug in logging breaks prompt generation
- Reusing code is impossible because every module drags along unrelated baggage
- New developers are confused by sprawling classes that do ten different things
- Debugging is painful because responsible code is scattered across many modules or buried in multi-purpose classes
- Merge conflicts and coordination overhead increase because everyone touches the same low-cohesion modules

## Practical Checklist
When designing or reviewing a module, ask yourself:
- [ ] Can I describe this module's purpose in one clear sentence without using "and" or "or"?
- [ ] Do all the methods/functions in this module serve that single purpose?
- [ ] If requirements change, would I likely modify all methods together, or just some?
- [ ] Could I extract a subset of methods into a separate module without the remaining methods depending on them?
- [ ] Are there methods that operate on completely different data or serve unrelated goals?
- [ ] Would a new developer immediately understand what this module is for from its name and interface?
- [ ] If I needed to reuse part of this module's functionality, would I be forced to bring along unrelated baggage?

## Watch Out For
⚠️ **The "Utils" trap**: Classes named `Utils`, `Helpers`, `Common`, or `Shared` are red flags for low cohesion. They become dumping grounds for unrelated functions. Instead of `AgentUtils`, create focused modules like `PromptFormatter`, `TokenCounter`, `RetryHandler`.

⚠️ **Over-fragmentation**: Taking cohesion to an extreme where every tiny function gets its own module creates excessive fragmentation and maintenance burden. Balance cohesion with pragmatism. Related helper functions can coexist if they truly support the same purpose.

⚠️ **Temporal cohesion disguised as high cohesion**: Functions that execute together (like initialization functions) but serve different purposes (setting up database, loading config, starting monitoring) have temporal cohesion, which is weaker than functional cohesion. Consider whether they really belong together.

⚠️ **Feature envy**: If a method in one class spends most of its time manipulating data from another class, it might belong in that other class. This is a sign the method doesn't cohere with its current class.

⚠️ **God objects**: Classes that try to do everything ("AgentOrchestrator that also handles logging, caching, monitoring, validation, and authentication") have low cohesion and violate [single_responsibility](single_responsibility.md). Break them apart into focused components.

⚠️ **Shotgun surgery**: If making a simple change requires modifying many unrelated modules, it might indicate responsibilities are split in ways that don't reflect actual cohesion of the problem domain. Sometimes related functionality that changes together should be in the same module.

## Connections
**Builds On:**
- [single_responsibility](single_responsibility.md) - High cohesion is closely related to SRP; a class with single responsibility naturally has high cohesion
- [separation_of_concerns](separation_of_concerns.md) - Separating concerns creates cohesive modules
- Basic software modularity - Understanding functions, classes, and modules

**Works With:**
- [loose_coupling](loose_coupling.md) - Ideal design has both high cohesion (focused modules) and loose coupling (minimal dependencies)
- [clean_code](clean_code.md) - Cohesive code is cleaner and more readable
- [solid_principles](solid_principles.md) - SRP (Single Responsibility Principle) directly promotes high cohesion
- [refactoring](refactoring.md) - Improving cohesion is a common refactoring goal
- [dependency_injection](dependency_injection.md) - DI helps achieve both high cohesion and loose coupling

**Leads To:**
- [solid_principles](solid_principles.md) - High cohesion is fundamental to several SOLID principles
- Domain-Driven Design - Cohesive bounded contexts and aggregates
- Microservices architecture - Services with high cohesion and loose coupling
- Component-based architecture - Building systems from cohesive, reusable components

**Related Patterns:**
- [factory_pattern](factory_pattern.md) - Factories have high cohesion around object creation
- [strategy_pattern](strategy_pattern.md) - Each strategy has high cohesion around one algorithm
- [adapter_pattern](adapter_pattern.md) - Adapters have cohesive purpose of interface translation
- [task_decomposition](../Agent_and_Orchestration/task_decomposition.md) - Breaking tasks into cohesive subtasks
- [multi-agent_system](../Agent_and_Orchestration/multi-agent_system.md) - Each agent should have cohesive, focused responsibilities

## Quick Decision Guide
**Aim for high cohesion when:**
- Designing new classes, modules, or components
- Building agents with specialized roles in multi-agent systems
- Creating reusable tools and utilities
- Refactoring sprawling "god objects"
- Establishing clear architectural boundaries
- Designing APIs and interfaces that are easy to understand and use

**Accept lower cohesion temporarily when:**
- Rapidly prototyping and learning the problem domain
- Building throw-away proof-of-concepts
- Working with legacy code where large-scale refactoring isn't feasible yet
- The cost of splitting components exceeds the benefit (pragmatism over purity)

## Further Exploration
- 📖 "Code Complete" by Steve McConnell - Chapter on high-quality routines covers cohesion extensively
- 🎯 "Clean Code" by Robert C. Martin - Chapters on classes and functions demonstrate cohesive design
- 💡 "Object-Oriented Software Construction" by Bertrand Meyer - Deep dive into cohesion and coupling metrics
- 📖 "Refactoring" by Martin Fowler - Techniques for improving cohesion (Extract Class, Move Method)
- 🎯 "Growing Object-Oriented Software, Guided by Tests" - Test-driven design naturally leads to high cohesion
- 💡 "Domain-Driven Design" by Eric Evans - Cohesive bounded contexts and aggregates
- 📖 "Software Engineering: A Practitioner's Approach" by Pressman & Maxim - Formal discussion of cohesion types and metrics
- 🎯 LangChain architecture - Examples of cohesive tool and chain implementations
- 💡 "Working Effectively with Legacy Code" by Michael Feathers - Introducing cohesion into low-cohesion codebases

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
