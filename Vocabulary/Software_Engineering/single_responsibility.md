# Single Responsibility Principle

## At a Glance
| | |
|---|---|
| **Category** | Design Principle / SOLID Principle |
| **Complexity** | Beginner to Intermediate (concept is intuitive, boundaries require judgment) |
| **Time to Learn** | 2-3 days to understand, weeks to months to apply consistently |
| **Prerequisites** | Basic OOP, understanding of classes and modules, awareness of cohesion |

## One-Sentence Summary
The Single Responsibility Principle (SRP) states that a class, module, or function should have only one reason to change—meaning it should have only one responsibility or job, focused on a single aspect of the system's functionality.

## Why This Matters to You
When you're building AI agents and ML systems, you're juggling multiple distinct concerns: prompt engineering, LLM API communication, response parsing, tool orchestration, state management, error handling, logging, caching, and business logic. The temptation is to create components that do multiple things: an `Agent` class that handles prompts, calls the LLM, parses responses, manages tools, stores conversation history, and implements business rules all in one place. This creates a tangled mess where changing how you format prompts requires understanding tool orchestration, fixing response parsing risks breaking state management, and adding new business logic means navigating through hundreds of lines mixing concerns. The Single Responsibility Principle gives you a clear criterion for organizing code: each component should do exactly one thing. Your `PromptBuilder` builds prompts, your `LLMClient` calls the LLM, your `ResponseParser` extracts structured data, your `ToolOrchestrator` manages tool execution, and your `ConversationStore` maintains state. When you need to change how prompts work, you modify one focused component that only knows about prompts. When parsing breaks, you fix one parser without touching LLM communication or tool logic. This isn't just organizational aesthetics—it's about maintainability and velocity. Components with single responsibilities are easy to understand (they do one thing), easy to test (one thing to test), easy to modify (changes localize), and easy to reuse (focused components fit many contexts). Teams that follow SRP ship features faster because changes are surgical, not systemic. Debugging is faster because problems localize. Onboarding is faster because each component is simple enough to grasp individually.

## The Core Idea
### What It Is
The Single Responsibility Principle, articulated by Robert C. Martin (Uncle Bob) in the early 2000s as the first of the SOLID principles, captures a fundamental insight about how to organize code. The principle states: "A class should have only one reason to change." This is sometimes reformulated as "a class should have only one responsibility" or "a class should do one thing."

The key word is "responsibility"—not "task" or "method," but responsibility in the sense of "an area of concern" or "an axis of change." Different parts of your system change for different reasons: UI changes because users want different interfaces, data access changes because you switch databases, business logic changes because requirements evolve, logging changes because you need different observability. When a component mixes multiple responsibilities, changes in one area require touching code that handles other areas, increasing the risk of breaking unrelated functionality.

Martin's formulation focuses on reasons to change because that's the practical symptom of violating SRP. If your `Agent` class needs to be modified when:
- You change prompt formatting (prompt responsibility)
- You switch LLM providers (API communication responsibility)  
- You adjust response parsing (parsing responsibility)
- You add new tools (tool management responsibility)
- You change how conversation history is stored (state management responsibility)

...then it has at least five responsibilities and five reasons to change. Each change risks breaking the others because they're tangled in one component. This is the maintenance nightmare SRP prevents.

The principle operates at multiple levels:
- **Function level**: Each function should do one thing (calculate a result, format a string, call an API)
- **Class level**: Each class should have one cohesive responsibility (manage prompts, handle LLM calls, orchestrate tools)
- **Module level**: Each module should address one area of concern (prompt engineering, tool implementations, state management)

For AI agent development in 2026, SRP is particularly valuable because agent systems naturally decompose into distinct responsibilities:

**Prompt Engineering**: Building effective prompts from templates, context, and user input—a specialized concern requiring iteration and testing. Separate prompt construction from other concerns so you can evolve prompting strategies independently.

**LLM Communication**: Handling API calls, authentication, rate limiting, retries, streaming responses—infrastructure concerns that change when providers change or APIs evolve. Isolate this so switching from OpenAI to Anthropic means changing one component, not hunting through scattered API calls.

**Response Parsing**: Extracting structured data from LLM outputs, handling malformed responses, validating extracted information—a distinct concern with its own complexity. Separate parsing so you can improve extraction logic without touching business logic.

**Tool Orchestration**: Deciding which tools to invoke, passing parameters, handling tool errors—the coordination logic. Keep this separate from tool implementations and agent reasoning.

**Business Logic**: The domain-specific reasoning, decision-making, and rules that make your agent valuable. This should be isolated from infrastructure concerns so domain changes don't require understanding LLM APIs or parsing strategies.

**State Management**: Maintaining conversation history, user context, and agent memory—a persistence and retrieval concern. Separate this so switching from in-memory to Redis doesn't affect business logic.

When each responsibility lives in its own focused component, changes localize. Adding caching to LLM calls? Modify the `LLMClient` component that handles calls. Improving prompt templates? Change the `PromptBuilder` that constructs prompts. Fixing a parsing bug? Update the `ResponseParser`. No other components need changes because they depend on stable interfaces, not implementation details.

### What It Isn't
Single Responsibility Principle is not "a class should only have one method" or "do only one small thing." A class with a single responsibility might have many methods, as long as they all serve that one responsibility. A `PromptBuilder` class might have methods like `build_system_prompt()`, `add_context()`, `format_conversation()`, and `build_final_prompt()`—multiple methods, but one responsibility: constructing prompts.

It's also not the same as making everything tiny and granular. You can violate SRP by making components too small—if you have `PromptHeaderBuilder`, `PromptBodyBuilder`, `PromptFooterBuilder`, and `PromptCombiner`, you might have split one cohesive responsibility into artificial fragments. The responsibility should be a meaningful, cohesive concern, not arbitrarily small pieces.

Don't confuse SRP with Separation of Concerns (SoC), though they're closely related. Separation of Concerns is about organizing entire systems around distinct aspects (presentation, business logic, data access). Single Responsibility is about individual components within those concerns—it's SoC applied at the class/module level. SoC is macro; SRP is micro.

SRP also doesn't mean components can't interact or depend on each other. A `PromptBuilder` and `LLMClient` and `ResponseParser` all need to work together. The point isn't independence; it's that each handles one clear responsibility and depends on others through stable interfaces.

Finally, SRP isn't about perfect boundaries or eliminating all ambiguity. Sometimes determining whether something is "one responsibility" or "two responsibilities" requires judgment. Is error handling a separate responsibility, or part of every component's responsibility? Is logging separate, or integrated? These are design decisions without absolute answers. SRP provides a guiding principle: prefer focused, cohesive responsibilities and resist mixing unrelated concerns. The exact boundaries emerge from experience and context.

## How It Works

**1. Identify Distinct Responsibilities:**
Look at your component and list what it does. For an `Agent` class, you might find:
- Constructs prompts from templates
- Calls LLM API with prompts
- Parses LLM responses for structured data
- Determines which tools to call
- Executes tool calls
- Maintains conversation history
- Implements business logic and decision-making
- Handles errors and retries
- Logs operations

That's at least 9 distinct responsibilities. Each represents a different reason the component might change and a different area of concern.

**2. Extract Each Responsibility to Its Own Component:**
Create focused components, each handling one responsibility:

```python
class PromptBuilder:
    """Responsible for: Constructing prompts from templates and context"""
    def build_system_prompt(self, persona: str) -> str: ...
    def add_conversation_context(self, history: list) -> str: ...
    def build_user_prompt(self, query: str, context: str) -> str: ...

class LLMClient:
    """Responsible for: Communicating with LLM APIs"""
    def complete(self, prompt: str, **params) -> LLMResponse: ...
    def stream_complete(self, prompt: str, **params) -> Iterator[str]: ...

class ResponseParser:
    """Responsible for: Extracting structured data from LLM outputs"""
    def parse_json(self, response: str) -> dict: ...
    def extract_tool_calls(self, response: str) -> list[ToolCall]: ...
    def validate_response(self, response: str, schema: Schema) -> bool: ...

class ToolOrchestrator:
    """Responsible for: Managing tool execution"""
    def select_tool(self, tool_calls: list[ToolCall]) -> list[Tool]: ...
    def execute_tools(self, tools: list[Tool]) -> list[ToolResult]: ...
    def handle_tool_errors(self, error: ToolError) -> ToolResult: ...

class ConversationStore:
    """Responsible for: Managing conversation state and history"""
    def add_message(self, message: Message) -> None: ...
    def get_history(self, limit: int = 10) -> list[Message]: ...
    def clear_history(self) -> None: ...
```

Each component has one clear responsibility. Changes to one don't affect others.

**3. Compose Components in Coordinator/Orchestrator:**
With responsibilities separated, you need something to coordinate them. This might be a higher-level `Agent` class that composes the focused components:

```python
class Agent:
    """Responsible for: Orchestrating agent workflow by delegating to specialized components"""
    def __init__(self, 
                 prompt_builder: PromptBuilder,
                 llm_client: LLMClient,
                 parser: ResponseParser,
                 tool_orchestrator: ToolOrchestrator,
                 conversation_store: ConversationStore):
        self.prompt_builder = prompt_builder
        self.llm = llm_client
        self.parser = parser
        self.tools = tool_orchestrator
        self.conversation = conversation_store
    
    def process_query(self, query: str) -> str:
        # Build prompt using PromptBuilder
        history = self.conversation.get_history()
        prompt = self.prompt_builder.build_user_prompt(query, history)
        
        # Call LLM using LLMClient
        response = self.llm.complete(prompt)
        
        # Parse response using ResponseParser
        tool_calls = self.parser.extract_tool_calls(response.text)
        
        # Execute tools using ToolOrchestrator
        if tool_calls:
            results = self.tools.execute_tools(tool_calls)
            # Incorporate results and continue...
        
        # Store in ConversationStore
        self.conversation.add_message(Message(query, response.text))
        
        return response.text
```

The `Agent` now has one responsibility: orchestrate the workflow by delegating to specialized components. Each concrete concern lives in a focused component.

**4. Test Components Independently:**
With single responsibilities, testing becomes straightforward:

```python
def test_response_parser():
    parser = ResponseParser()
    
    # Test one responsibility: parsing JSON from LLM responses
    response = '{"action": "search", "query": "AI agents"}'
    result = parser.parse_json(response)
    
    assert result["action"] == "search"
    assert result["query"] == "AI agents"
```

You're testing the parser without needing an LLM, prompt builder, or orchestrator. Each component tests its single responsibility in isolation.

**5. Modify Components Independently:**
When requirements change, modifications localize:

**Change prompt strategy**:
```python
class PromptBuilder:
    def build_user_prompt(self, query: str, context: str) -> str:
        # NEW: Using chain-of-thought prompting
        return f"""Context: {context}

Query: {query}

Think through this step-by-step:
1. What information is relevant?
2. What tools might help?
3. What's the best answer?

Answer:"""
```

Only `PromptBuilder` changes. LLMClient, ResponseParser, ToolOrchestrator, ConversationStore unchanged.

**Switch LLM provider**:
```python
class AnthropicLLMClient:
    def complete(self, prompt: str, **params) -> LLMResponse:
        # NEW: Anthropic API instead of OpenAI
        response = anthropic.Completion.create(prompt=prompt, model="claude-3")
        return LLMResponse(text=response.completion)
```

Create new LLMClient implementation. PromptBuilder, ResponseParser, etc. unchanged.

**6. Recognize When Responsibilities Mix:**
Watch for signs that a component has multiple responsibilities:
- Long classes (hundreds of lines) doing many things
- Method names from different domains (`format_prompt()`, `call_api()`, `parse_json()`, `store_history()` in one class)
- Changes in one area requiring changes throughout the class
- Difficulty naming the class without "and" or "or" (`PromptBuilderAndLLMCaller`)
- Tests that require mocking unrelated concerns

These are code smells indicating mixed responsibilities. Refactor by extracting responsibilities into focused components.

## Think of It Like This
Imagine running a restaurant. You could have one person responsible for:
- Taking orders from customers
- Cooking all the food
- Washing dishes
- Managing inventory
- Handling payments
- Cleaning the dining room
- Marketing the restaurant

This violates Single Responsibility—that person has seven distinct jobs. When you need to change how orders are taken (add online ordering), you must coordinate with the same person who cooks and cleans, risking disruption to unrelated tasks. When they're sick, the entire restaurant shuts down. They're overwhelmed, mediocre at everything, and changes are slow because every change affects their complex role.

With Single Responsibility:
- **Server**: Takes orders, serves customers (one responsibility: customer interaction)
- **Chef**: Cooks food (one responsibility: food preparation)
- **Dishwasher**: Cleans dishes and kitchen (one responsibility: cleaning)
- **Manager**: Handles inventory, finances, marketing (one responsibility: operations management)

Now when you need online ordering, only the server role changes—doesn't affect the chef, dishwasher, or manager. If the dishwasher is sick, cooking and serving continue unaffected. Each person specializes and excels at their focused responsibility. Changes localize, problems isolate, and the restaurant operates efficiently.

This is SRP: give each component one clear job, let it specialize and excel, and coordinate through defined interactions. When responsibilities are singular, changes are localized and the system remains maintainable.

## The "So What?" Factor
**If you use this:**
- Changes localize—modifying how prompts work doesn't risk breaking LLM communication, parsing, or tool orchestration
- Testing is practical—test each responsibility independently without complex setup or mocking unrelated concerns
- Understanding is fast—each component is small and focused, understandable in minutes rather than hours
- Debugging is straightforward—problems localize to specific responsibilities; if parsing fails, check the parser, not the entire agent
- Reusability emerges—focused components (like `LLMClient` or `ResponseParser`) can be reused across projects
- Parallel development works—multiple developers work on different responsibilities simultaneously without conflicts
- Maintenance is cheap—each component is simple enough that changes are fast and safe
- Onboarding accelerates—new developers grasp one responsibility at a time rather than monolithic complexity

**If you don't:**
- Changes cascade—modifying one concern requires understanding and potentially changing unrelated code mixed in the same component
- Testing requires everything—you can't test prompt logic without LLM APIs, or parsing without business logic, because everything is tangled
- Understanding takes days—components mix concerns, requiring you to untangle prompt logic from API handling from parsing from business rules
- Debugging is archaeological—when something fails, the problem could be anywhere in the tangled component; isolating the issue is detective work
- Reusability is impossible—components doing multiple things can't be reused because they drag unrelated concerns along
- Parallel development stalls—developers working on different concerns modify the same multi-responsibility component, creating conflicts
- Maintenance is expensive—simple changes require navigating complex, multi-concern components with unclear responsibilities
- Onboarding takes weeks—new developers must understand monolithic components mixing many concerns before contributing

## Practical Checklist
Before implementing, ask yourself:
- [ ] **Can I state this component's responsibility in one sentence?** If the description uses "and" or requires multiple clauses, it might have multiple responsibilities
- [ ] **How many reasons could this component change?** List them. If there are multiple unrelated reasons (prompt format changes, API changes, parsing logic changes), you have multiple responsibilities
- [ ] **Can I name this component clearly?** Names with "Manager," "Handler," "Controller," or "Service" often hide multiple responsibilities. Specific names like `PromptBuilder`, `ResponseParser` indicate focused responsibilities
- [ ] **Can I test this component independently?** If testing requires mocking many unrelated concerns, the component likely mixes responsibilities
- [ ] **Are all methods related to the same concern?** If some methods handle prompts, others call APIs, and others parse responses, you have mixed responsibilities
- [ ] **Would changes in one area of concern require modifying this component?** If prompt strategies, API providers, parsing logic, and business rules all trigger changes here, it has too many responsibilities
- [ ] **Is this component cohesive?** Do all parts relate to one aspect of the system, or are there unrelated pieces doing different things?

## Watch Out For
⚠️ **Over-Splitting Into Tiny Fragments**: The pursuit of single responsibility can lead to excessive fragmentation—dozens of tiny classes, each doing almost nothing, creating complexity through proliferation rather than simplification. A class that has one method calling another class with one method calling another is over-split. Balance focus with cohesion—ensure each component represents a meaningful, cohesive responsibility, not an arbitrary sliver of functionality.

⚠️ **Ambiguous Responsibility Boundaries**: Sometimes it's unclear whether something is one responsibility or two. Is error handling a separate responsibility or part of every component's responsibility? Is validation separate or integrated into parsing? These gray areas require judgment. Don't get paralyzed seeking perfect boundaries—make reasonable choices and refactor if they prove problematic. Experience improves boundary judgment.

⚠️ **Coordinator Becomes God Object**: When you extract responsibilities to focused components, you need coordination. The coordinator can become a "god object" that knows about everything and orchestrates everyone—effectively just moving complexity rather than reducing it. Keep coordinators thin—they should delegate to focused components, not implement complex logic themselves. If your orchestrator grows large, you likely haven't extracted all responsibilities.

⚠️ **Testing Each Component Doesn't Test Integration**: With separated responsibilities, you must test both individual components and their integration. A `PromptBuilder` might work perfectly in isolation, and an `LLMClient` might work perfectly, but they might not work together correctly. Integration tests ensure components collaborate properly. Don't rely solely on unit tests of individual responsibilities.

⚠️ **Premature Extraction**: Sometimes you don't understand the responsibility boundaries until you've built something. Starting by extracting every possible responsibility prematurely can create awkward, unstable boundaries. It's often better to build a working system first, identify actual responsibilities that emerge, then refactor to separate them. "Make it work, then make it right" is a valid approach.

⚠️ **Responsibility Creep**: Over time, focused components accumulate additional responsibilities. A `PromptBuilder` starts handling prompt formatting, then someone adds caching logic, then prompt validation, then template versioning. Gradually it violates SRP. Guard against this creep—regularly review components to ensure they maintain single responsibilities. Refactor when responsibilities drift.

⚠️ **Ignoring Cross-Cutting Concerns**: Some concerns (logging, monitoring, authentication, error handling) cut across all components. Trying to isolate these completely leads to either duplication (every component logs separately) or awkward designs (passing loggers everywhere). Use framework features, decorators, or aspect-oriented techniques for cross-cutting concerns. They're an exception to strict SRP.

⚠️ **Confusing Layers with Responsibilities**: A component can be in the "data access layer" and still violate SRP if it handles database operations, caching, and data validation. Layers organize system architecture; responsibilities organize component design. Both matter, but they're different concerns. A layer can contain multiple components, each with single responsibilities.

## Connections
**Builds On:** 
- [Clean Code](clean_code.md) - Single responsibility is fundamental to clean, maintainable code
- [High Cohesion](high_cohesion.md) - SRP is essentially high cohesion at the component level
- [Separation of Concerns](separation_of_concerns.md) - SRP applies separation of concerns at class/module level

**Works With:** 
- [SOLID Principles](solid_principles.md) - SRP is the "S" in SOLID, working synergistically with other principles
- [Open-Closed Principle](open_closed_principle.md) - Focused responsibilities make components easier to extend without modifying
- [Dependency Injection](dependency_injection.md) - Separated responsibilities compose through dependency injection
- [Loose Coupling](loose_coupling.md) - Single-responsibility components couple loosely because they depend on minimal interfaces
- [Refactoring](refactoring.md) - Mixed responsibilities are a refactoring trigger; extract classes/methods to separate them
- [KISS Principle](kiss_principle.md) - Single-responsibility components are simpler, more understandable components

**Leads To:** 
- [Adapter Pattern](adapter_pattern.md) - Focused components with clear interfaces work well with adapters
- [Strategy Pattern](strategy_pattern.md) - Single-responsibility algorithms become interchangeable strategies
- [Decorator Pattern](decorator_pattern.md) - Single-responsibility components can be decorated to add behavior
- [Factory Pattern](factory_pattern.md) - Object creation as a separate responsibility from usage

**Related Patterns:**
- [Technical Debt](technical_debt.md) - Mixed responsibilities accumulate debt; SRP prevents it
- [Code Smell](code_smell.md) - Long classes, methods from different domains, and difficult naming are smells indicating SRP violations
- [Agent Framework](../Agent_and_Orchestration/agent_framework.md) - Agent frameworks benefit from SRP separation of concerns

## Quick Decision Guide
**Use this when you need to:** 
- Design any class, module, or function—SRP applies universally to component design
- Organize complex systems like AI agents with many concerns (prompts, LLM calls, parsing, tools, state, business logic)
- Make code maintainable—separating responsibilities enables localized changes
- Enable parallel development—different developers work on different responsibilities without conflicts
- Create testable components—single responsibilities test independently
- Build reusable components—focused components fit multiple contexts
- Reduce debugging difficulty—single responsibilities make problems localize

**Skip this when:** 
- Never. SRP always applies. The question is identifying the right responsibility boundaries for your context, not whether to have focused responsibilities. Even simple systems benefit from clear responsibilities. There's no scenario where mixing unrelated concerns into one component is better than having focused, single-responsibility components.

## Further Exploration
- 📖 **Agile Software Development, Principles, Patterns, and Practices** (2002) by Robert C. Martin - Original detailed explanation of SRP
- 📖 **Clean Architecture** (2017) by Robert C. Martin - SRP applied at architectural level
- 🎯 **"Single Responsibility Principle in AI Agent Systems"** (2025) - Modern examples of separating agent responsibilities
- 💡 **"SRP: The Most Violated Principle"** - Why SRP is hard and how to improve at identifying responsibilities
- 📖 **The Pragmatic Programmer** (2019) by Thomas and Hunt - Practical advice on cohesion and responsibility
- 🎯 **"Refactoring to SRP"** - Techniques for identifying and extracting mixed responsibilities
- 💡 **"Responsibility-Driven Design"** - Design methodology centered on identifying and assigning clear responsibilities
- 📖 **Growing Object-Oriented Software, Guided by Tests** (2009) - TDD approach that naturally leads to single-responsibility components

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*