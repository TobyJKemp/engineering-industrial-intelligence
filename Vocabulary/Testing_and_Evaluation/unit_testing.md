# Unit Testing

## At a Glance
| | |
|---|---|
| **Category** | Technique / Quality Assurance Practice |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for basics, ongoing practice for mastery |
| **Prerequisites** | Basic programming concepts, understanding of functions and modules |

## One-Sentence Summary
Unit testing is the practice of writing automated tests that verify individual components of your system work correctly in isolation, catching bugs early and giving you confidence that each piece functions as intended before integrating them together.

## Why This Matters to You
When building AI agent systems, you're orchestrating complex interactions between [LLMs](../Foundational_AI%20&%20ML/large_language_model.md), [tools](../Agent_and_Orchestration/tool_and_function_calling.md), databases, APIs, and business logic. While the LLM itself may be non-deterministic, the infrastructure around it—prompt templates, output parsers, tool functions, validation logic, error handlers—absolutely must work reliably. Unit tests are your safety net, verifying that these critical components behave correctly before you connect them to expensive LLM calls or deploy them to production. Without unit tests, you'll discover bugs in production through user complaints or data corruption. With them, you catch problems in seconds on your laptop, fix them confidently, and build complex systems knowing each piece is solid. Unit testing transforms AI development from "hope it works" to "know it works."

## The Core Idea
### What It Is
Unit testing is the practice of writing small, focused test functions that verify individual components—usually a single function, method, or class—behave correctly under various conditions. Each unit test sets up a specific scenario, executes the component being tested with controlled inputs, and verifies the output matches expectations. These tests run automatically in seconds and tell you immediately when something breaks.

In the context of AI agent systems, unit tests typically target the deterministic parts of your codebase: the functions that format prompts from templates, parse LLM outputs into structured data, validate inputs before sending to APIs, implement [tool and function calling](../Agent_and_Orchestration/tool_and_function_calling.md) logic, handle errors and retries, manage [state](../../Agent_Operations/agent_state.md), and integrate with external systems. While you can't easily unit test the LLM's creative generation (that requires different [evaluation metrics](evaluation_metrics.md)), you can absolutely test everything that wraps around it.

A typical unit test has three phases: **Arrange** (set up test data and conditions), **Act** (call the function being tested), and **Assert** (verify the output is correct). For example, testing a prompt template function: arrange by creating test data, act by calling the template function with that data, assert the resulting prompt contains the expected text in the right format. Modern testing frameworks make this pattern simple and fast to write.

Unit tests accumulate into a test suite—potentially hundreds or thousands of small tests—that you run frequently, often on every code change. When a test fails, it pinpoints exactly which component broke and under what conditions, dramatically accelerating debugging. When all tests pass, you have confidence that your changes didn't break existing functionality. This fast feedback loop is essential for maintaining quality as systems grow complex.

### What It Isn't
Unit testing is not the same as testing the AI model itself. You don't unit test whether GPT-4 generates good responses—that's model evaluation. Unit tests focus on your code, not the model's capabilities. The distinction is crucial: unit tests verify your infrastructure works correctly; model evaluation verifies the AI produces quality outputs for your use case.

Unit testing is not [integration testing](integration_testing.md) or [end-to-end testing](end_to_end_testing.md). Unit tests verify components in isolation, often using mocks or stubs to replace dependencies. You wouldn't make real API calls to external services or databases in a unit test—those are integration concerns. A unit test might verify your API wrapper function correctly formats requests, but it wouldn't actually send those requests to the live API.

Unit tests are also not a substitute for manual testing or production monitoring. They catch logic errors, edge cases, and regressions in your code, but they can't catch everything. If your test data doesn't represent real-world scenarios, if your assumptions about behavior are wrong, or if production has unique characteristics your tests don't model, problems can still slip through. Unit tests are one layer of a comprehensive testing strategy, not the only layer.

Finally, unit testing is not about achieving 100% code coverage just to hit a metric. Coverage measures what code your tests execute, but high coverage doesn't guarantee good tests. You can have 100% coverage with tests that don't actually verify correct behavior. The goal is meaningful tests that catch real bugs, not just tests that exercise every line of code.

## How It Works
The unit testing workflow for AI agent systems:

1. **Identify Testable Units**: Look for deterministic functions in your codebase. Prime candidates include prompt template builders, output parsers (converting LLM text to JSON or structured data), validation functions, data transformation logic, API wrappers, [tool and function calling](../Agent_and_Orchestration/tool_and_function_calling.md) implementations, and error handling code.

2. **Choose a Testing Framework**: Select a framework appropriate for your language (pytest for Python, Jest for JavaScript, JUnit for Java, etc.). These frameworks provide test runners, assertion libraries, and utilities for organizing tests.

3. **Write Test Cases**: For each function, write multiple test cases covering normal operation, edge cases, error conditions, and boundary values. For example, testing a prompt formatter:
   - Normal case: valid inputs produce expected prompt
   - Edge case: empty inputs handled gracefully
   - Boundary: maximum length inputs don't break formatting
   - Error: invalid input types raise appropriate exceptions

4. **Use Mocking for Dependencies**: When testing a component that depends on external services (APIs, databases, LLM calls), use mocks or stubs to simulate those dependencies. This keeps tests fast, deterministic, and independent of external factors. For example, mock the LLM API to return predefined responses so you can test your parsing logic without actual API calls.

5. **Run Tests Frequently**: Execute your test suite on every code change, ideally before committing. Most development environments can run tests automatically when files change. This immediate feedback catches bugs within seconds of introduction.

6. **Maintain Tests**: As your system evolves, keep tests updated. When you fix bugs, add tests that would have caught them. When you add features, add tests for the new functionality. Treat test code with the same care as production code—it's your safety net.

7. **Monitor Coverage**: Use coverage tools to identify untested code, but focus on testing important behavior rather than chasing coverage percentages. Critical paths, error handlers, and complex logic deserve thorough testing. Simple getters/setters may not.

## Think of It Like This
**The Component Inspection Analogy**: Imagine a car factory where every component—spark plugs, brake pads, sensors—is tested individually on specialized equipment before assembly. The spark plug tester verifies electrical resistance, threading, and heat range without needing to install it in an engine. This catches defective parts immediately, preventing expensive failures later when the car is assembled. Unit testing is the same: you verify each code component works correctly in isolation before connecting them into a complete system. Just as the factory doesn't test the entire car during component inspection (that's final assembly testing), you don't test the entire AI agent during unit testing—you verify individual functions.

**Railway Metaphor**: Think of unit testing as inspecting each piece of railway equipment at the maintenance depot before it goes into service. You test brake systems on a test rig, verify signal lights with controlled power sources, and check switch mechanisms in isolation. You don't need a train running on live tracks to verify a brake pad meets specifications—you test it on a dedicated bench. Similarly, you don't need a running AI agent making real LLM calls to test your prompt formatter—you test it with sample inputs and verify the output format. These isolated inspections catch defects quickly and safely, before they can cause derailments in production.

## The "So What?" Factor
**If you use unit testing:**
- You catch bugs in seconds on your laptop instead of discovering them in production through user reports
- You can refactor and improve code confidently, knowing tests will catch any functionality you accidentally break
- You document how components should behave through executable examples (tests are living documentation)
- You reduce debugging time dramatically because test failures pinpoint exactly what broke and under what conditions
- You enable rapid iteration—make changes, run tests, get immediate feedback on whether things still work
- You build complex AI systems with confidence that the infrastructure layer is solid
- You onboard new team members faster because tests show how components are meant to be used

**If you don't use unit testing:**
- You'll discover bugs in production when they cause failures, data corruption, or bad user experiences
- You'll be afraid to refactor or improve code because you can't be sure what might break
- Debugging becomes a slow, painful process of reproducing issues and hunting through logs
- Every change risks introducing regressions that you won't notice until much later
- You'll waste time and money on LLM API calls during debugging when the problem is in your infrastructure code
- Code reviews become less effective because reviewers can't easily verify that logic handles edge cases
- Technical debt accumulates as the codebase becomes too fragile to modify safely

## Practical Checklist
Before implementing unit tests for your AI system, ask yourself:
- [ ] **What are my deterministic components?** Identify prompt builders, parsers, validators, tool implementations, and business logic that should behave predictably.
- [ ] **What edge cases exist?** Consider empty inputs, maximum values, invalid data types, null values, and malformed inputs.
- [ ] **What dependencies need mocking?** Identify external services (LLM APIs, databases, web services) that tests should simulate rather than call.
- [ ] **What's my testing framework?** Choose pytest, Jest, JUnit, or another framework appropriate for your language and set up the test environment.
- [ ] **How will I run tests frequently?** Set up IDE integration, pre-commit hooks, or CI/CD pipelines to run tests automatically.
- [ ] **What's worth testing first?** Prioritize critical paths, complex logic, and error-prone areas over simple code.

## Watch Out For
⚠️ **Over-Mocking Creates False Confidence**: If your mocks don't accurately represent real behavior, passing unit tests can give false confidence. A unit test might pass with a mocked LLM response that returns perfect JSON, but the real LLM might return slightly malformed data. Balance unit tests with [integration tests](integration_testing.md) that use real dependencies.

⚠️ **Testing Implementation Details Instead of Behavior**: Tests should verify what a function does (its contract), not how it does it (implementation). If you refactor internal logic but keep the same inputs and outputs, tests shouldn't break. Testing implementation details makes tests brittle and discourages refactoring.

⚠️ **Slow Tests Discourage Running Them**: Unit tests should run in milliseconds. If tests take minutes because they make real API calls or database queries, developers stop running them frequently. Keep unit tests fast through mocking and isolation.

⚠️ **Ignoring Test Maintenance**: Tests are code—they require maintenance. As your system evolves, outdated tests will fail or become irrelevant. Treat test maintenance as seriously as production code maintenance, or your test suite will rot and become a burden rather than a help.

⚠️ **The "Works on My Machine" Problem**: Tests that depend on local file paths, environment variables, or specific system configurations will fail on other machines or CI/CD pipelines. Make tests self-contained and portable.

⚠️ **Coverage Theater**: Achieving 90% code coverage with shallow tests that don't actually verify correct behavior is worse than 50% coverage with meaningful tests. Focus on testing important behavior, not maximizing coverage metrics.

## Connections
**Builds On:** Basic programming concepts, functions and modularity, test-driven development principles  
**Works With:** [Harness](harness.md) (infrastructure for running tests), [Integration Testing](integration_testing.md) (testing component interactions), [Evaluation Metrics](evaluation_metrics.md) (measuring test effectiveness)  
**Leads To:** [Test Suite](test_suite.md) (collection of unit tests), [Regression Testing](regression_testing.md) (preventing old bugs), [End-to-End Testing](end_to_end_testing.md) (complete system validation), continuous integration practices

## Quick Decision Guide
**Write unit tests for:**
- Prompt template builders and formatters
- Output parsers that convert LLM text to structured data
- Input validation and sanitization functions
- [Tool and function calling](../Agent_and_Orchestration/tool_and_function_calling.md) implementations
- Business logic and data transformations
- Error handling and retry logic
- State management functions
- API wrapper functions (with mocked external calls)
- Complex conditional logic and algorithms

**Don't bother unit testing:**
- Simple getters/setters with no logic
- Generated code or third-party libraries (trust their tests)
- The LLM model itself (use [evaluation metrics](evaluation_metrics.md) instead)
- Configuration files or static data
- One-off scripts that won't be maintained

**Prioritize unit tests when:**
- Building production systems that need reliability
- Working in teams where multiple people modify the codebase
- Creating reusable libraries or frameworks
- Dealing with complex logic that's hard to reason about
- Facing frequent regressions or bugs

**Skip unit tests if:**
- You're doing rapid prototyping to test concepts (add tests later when proven)
- The code is truly throwaway with no production future
- You're under extreme time pressure (but plan to add them immediately after)

## Further Exploration
- 📖 **"Test-Driven Development" by Kent Beck**: The foundational book on writing tests first, then code to pass them
- 🎯 **Pytest Documentation** (Python) or **Jest Documentation** (JavaScript): Practical guides for popular testing frameworks
- 💡 **Testing Pyramid Concept**: Understand how unit tests fit into a broader testing strategy (many unit tests, fewer integration tests, minimal E2E tests)
- 📖 **"Working Effectively with Legacy Code" by Michael Feathers**: Techniques for adding tests to existing codebases
- 🎯 **AI-Specific Testing Patterns**: Explore patterns like testing prompt templates, mocking LLM responses, and validating structured outputs
- 💡 **Property-Based Testing**: Advanced technique that generates test cases automatically to find edge cases you didn't think of

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*