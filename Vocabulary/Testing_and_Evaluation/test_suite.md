# Test Suite

## At a Glance
| | |
|---|---|
| **Category** | Testing Infrastructure / Quality Assurance |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for fundamentals, ongoing practice for effective organization |
| **Prerequisites** | Understanding of [unit_testing](unit_testing.md), [integration_testing](integration_testing.md), basic testing concepts |

## One-Sentence Summary
A test suite is an organized collection of tests grouped by purpose, scope, or component, executed together to validate system behavior—like having separate folders for "agent core tests" (runs in 10 seconds), "RAG pipeline tests" (runs in 2 minutes), and "full E2E tests" (runs in 15 minutes) so you can run the right tests at the right time.

## Why This Matters to You
When you build AI agent systems in 2026, you accumulate hundreds or thousands of tests—unit tests for prompt builders, integration tests for tool execution, [end-to-end tests](end_to_end_testing.md) for complete workflows, [regression tests](regression_testing.md) for bug fixes, [benchmarks](benchmark.md) for quality validation. Running all tests every time you change one line takes too long. Running only one test provides insufficient confidence. You need organization: fast unit tests run on every save (5 seconds), integration tests run on every commit (30 seconds), E2E tests run on pull requests (5 minutes), comprehensive suites run nightly (30 minutes). Test suites provide this structure—logical groupings that let you run "just the RAG tests," "just the critical path tests," or "everything" depending on context. Without test suites, testing is chaotic: you don't know which tests to run, tests take forever, developers skip testing, and bugs slip through. With well-organized suites, testing is systematic: developers run fast feedback loops locally, CI/CD runs appropriate checks at each stage, and you maintain confidence without waiting hours for test results.

## The Core Idea
### What It Is
A test suite is a logical grouping of related tests that can be executed together. Instead of treating all tests as an undifferentiated pile, you organize them into meaningful collections based on scope, purpose, speed, or component.

**Common Test Suite Types:**

**1. Unit Test Suite**:
Fast, isolated tests for individual functions/classes.
```python
# tests/unit/test_prompt_builder.py
class TestPromptBuilder:
    def test_build_with_context(self):
        builder = PromptBuilder()
        prompt = builder.build(
            query="What is RAG?",
            context=["RAG stands for Retrieval-Augmented Generation..."]
        )
        assert "What is RAG?" in prompt
        assert "Retrieval-Augmented Generation" in prompt
    
    def test_build_without_context(self):
        builder = PromptBuilder()
        prompt = builder.build(query="What is RAG?", context=[])
        assert "What is RAG?" in prompt
        assert "context" not in prompt.lower()
    
    def test_truncate_long_context(self):
        builder = PromptBuilder(max_tokens=100)
        long_context = ["x" * 10000]  # Very long context
        prompt = builder.build(query="Test", context=long_context)
        assert len(prompt) < 1000  # Truncated

# Run: pytest tests/unit/test_prompt_builder.py
# Typical execution: <1 second
```

**2. Integration Test Suite**:
Tests verifying components work together.
```python
# tests/integration/test_rag_pipeline.py
class TestRAGPipeline:
    def setup_method(self):
        self.vector_store = VectorStore(in_memory=True)
        self.vector_store.index(TEST_DOCUMENTS)
        self.rag = RAGPipeline(vector_store=self.vector_store)
    
    def test_retrieval_and_generation(self):
        result = self.rag.query("What is machine learning?")
        assert result.answer is not None
        assert len(result.sources) > 0
        assert result.confidence > 0
    
    def test_handles_no_relevant_docs(self):
        result = self.rag.query("xyzabc123 nonsense query")
        assert result.fallback_used
        assert "I don't have information" in result.answer

# Run: pytest tests/integration/test_rag_pipeline.py
# Typical execution: 2-5 seconds (involves vector search, LLM call)
```

**3. End-to-End Test Suite**:
Complete workflow tests from user perspective.
```python
# tests/e2e/test_customer_support_agent.py
class TestCustomerSupportE2E:
    def setup_method(self):
        self.agent = CustomerSupportAgent(
            environment="test",
            mock_external_apis=True
        )
    
    def test_simple_question_workflow(self):
        response = self.agent.handle_conversation(
            user_message="What are your business hours?"
        )
        assert response.success
        assert "9" in response.text and "5" in response.text
        assert response.latency < 3.0
    
    def test_multi_turn_conversation(self):
        # Turn 1
        response1 = self.agent.handle_conversation("I need help with billing")
        assert "billing" in response1.text.lower()
        
        # Turn 2
        response2 = self.agent.handle_conversation("I was charged twice")
        assert response2.context_includes_previous_turn
        assert "refund" in response2.text.lower() or "duplicate" in response2.text.lower()

# Run: pytest tests/e2e/test_customer_support_agent.py
# Typical execution: 10-30 seconds (full agent pipeline)
```

**4. Smoke Test Suite**:
Minimal tests validating basic functionality after deployment.
```python
# tests/smoke/test_basic_health.py
class TestSmoke:
    def test_agent_responds(self):
        """Basic sanity check that agent returns a response."""
        response = agent.query("Hello")
        assert response is not None
        assert len(response.text) > 0
    
    def test_database_connection(self):
        """Verify database is accessible."""
        assert database.is_connected()
        result = database.query("SELECT 1")
        assert result is not None
    
    def test_llm_api_available(self):
        """Verify LLM API is reachable."""
        response = llm_client.complete("Test", max_tokens=5)
        assert response.success

# Run: pytest tests/smoke/ -v
# Typical execution: <5 seconds
# Run after every deployment to verify basic functionality
```

**5. Regression Test Suite**:
Tests for previously fixed bugs to prevent reintroduction.
```python
# tests/regression/test_bug_fixes.py
class TestRegressions:
    def test_bug_123_context_truncation(self):
        """Regression: Context exceeded max tokens, causing failures.
        Fixed in PR #456. This test ensures fix remains in place.
        """
        huge_context = ["x" * 100000]
        response = agent.query("Test", context=huge_context)
        assert response.success  # Should not crash
    
    def test_bug_234_tool_parameter_escaping(self):
        """Regression: Special characters in tool params caused JSON errors.
        Fixed in PR #567.
        """
        response = agent.execute_tool("search", {"query": 'test "quoted" term'})
        assert response.success  # Should handle quotes correctly

# Run: pytest tests/regression/ -v
# Typical execution: 5-15 seconds
```

**6. Performance/Benchmark Suite**:
Tests measuring quality and performance metrics.
```python
# tests/benchmarks/test_quality_benchmarks.py
class TestQualityBenchmarks:
    def test_accuracy_benchmark(self):
        """Run standard accuracy benchmark."""
        results = run_benchmark(
            agent=agent,
            dataset=ACCURACY_BENCHMARK_DATASET,
            metrics=["accuracy", "f1_score"]
        )
        assert results["accuracy"] >= 0.85  # Minimum threshold
        assert results["f1_score"] >= 0.80
    
    def test_latency_benchmark(self):
        """Verify P95 latency within acceptable range."""
        latencies = []
        for query in LATENCY_BENCHMARK_QUERIES:
            start = time.time()
            agent.query(query)
            latencies.append(time.time() - start)
        
        p95 = np.percentile(latencies, 95)
        assert p95 < 2.0  # P95 under 2 seconds

# Run: pytest tests/benchmarks/ -v
# Typical execution: 1-5 minutes (many queries)
```

### What It Isn't
A test suite is not **a single test**. One test validates one behavior; a suite groups many tests. A suite might contain 50 unit tests, 20 integration tests, or 10 E2E tests.

It's not **just a folder**. While tests are often organized in folders (tests/unit/, tests/integration/), a suite is a logical grouping—you might have a "critical path suite" that includes select tests from multiple folders. Organization supports suites but isn't the suite itself.

Test suites are not **independent**. Unit tests within a suite are independent (can run in any order), but suites often have dependencies: unit suite passes before integration suite runs, integration passes before E2E runs. This is the test pyramid in action.

They're not **static**. As your system evolves, test suites evolve. You add tests for new features, remove obsolete tests, reorganize slow tests, split large suites, and adjust what runs when. Suite organization is living structure.

A test suite is not the same as a **[test harness](harness.md)**. The harness is infrastructure for running tests (pytest, jest, Go's testing package). The suite is the logical collection of tests you run with the harness. You use pytest (harness) to run your unit test suite (collection).

Finally, test suites are not **all-or-nothing**. You don't run all tests all the time. Fast suites run frequently (on save, on commit), slow suites run less often (on PR, nightly). The goal is running the right tests at the right time for fast feedback and thorough validation.

## How It Works

### Organizing Test Suites

**Typical Directory Structure:**
```
tests/
├── unit/                          # Fast, isolated tests
│   ├── test_prompt_builder.py     # ~30 tests, <1s total
│   ├── test_context_manager.py    # ~25 tests, <1s total
│   ├── test_tool_schemas.py       # ~40 tests, <1s total
│   └── test_response_formatter.py # ~20 tests, <1s total
├── integration/                   # Component interaction tests
│   ├── test_rag_pipeline.py       # ~15 tests, 5s total
│   ├── test_tool_execution.py     # ~20 tests, 8s total
│   └── test_vector_store.py       # ~10 tests, 3s total
├── e2e/                           # Full workflow tests
│   ├── test_customer_support.py   # ~10 tests, 30s total
│   ├── test_code_generation.py    # ~8 tests, 45s total
│   └── test_multi_agent.py        # ~5 tests, 60s total
├── regression/                    # Previously fixed bugs
│   └── test_bug_fixes.py          # ~30 tests, 10s total
├── smoke/                         # Post-deployment checks
│   └── test_basic_health.py       # ~5 tests, 5s total
├── benchmarks/                    # Quality/performance validation
│   ├── test_accuracy.py           # ~3 benchmarks, 120s total
│   └── test_performance.py        # ~5 benchmarks, 180s total
└── conftest.py                    # Shared fixtures, configuration
```

**Running Different Suites:**
```bash
# Fast feedback: Unit tests only (~2 seconds)
pytest tests/unit/

# Moderate feedback: Unit + Integration (~15 seconds)
pytest tests/unit/ tests/integration/

# Pre-commit: Unit + Integration + Smoke (~20 seconds)
pytest tests/unit/ tests/integration/ tests/smoke/

# PR validation: Everything except benchmarks (~5 minutes)
pytest tests/ --ignore=tests/benchmarks/

# Comprehensive: Everything including benchmarks (~10 minutes)
pytest tests/

# Specific component: Just RAG-related tests
pytest tests/unit/test_rag*.py tests/integration/test_rag*.py tests/e2e/test_rag*.py

# Critical path only: Tagged tests
pytest -m critical

# Nightly: Comprehensive + slow tests
pytest tests/ --run-slow
```

### Test Suite Configuration

**Using pytest markers to organize suites:**
```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "unit: Fast unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow tests (>10s)")
    config.addinivalue_line("markers", "critical: Critical path tests")

# tests/unit/test_prompt_builder.py
import pytest

@pytest.mark.unit
@pytest.mark.critical
def test_build_prompt_with_context():
    # Critical functionality tested quickly
    pass

# tests/e2e/test_workflow.py
@pytest.mark.e2e
@pytest.mark.slow
def test_complete_workflow():
    # Comprehensive but slow test
    pass

# Run by marker:
# pytest -m unit              # Just unit tests
# pytest -m "critical"        # Critical path only
# pytest -m "not slow"        # Exclude slow tests
# pytest -m "unit or integration"  # Fast tests only
```

**Suite configuration in pyproject.toml:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

# Default: Run unit and integration, skip slow tests
addopts = "-v --strict-markers -m 'not slow'"

# Minimum test coverage threshold
addopts = "--cov=src --cov-fail-under=75"

# Parallel execution for faster suites
addopts = "-n auto"  # Use all CPU cores

markers = [
    "unit: Fast unit tests (<1s each)",
    "integration: Integration tests (1-10s each)",
    "e2e: End-to-end tests (10s+ each)",
    "slow: Slow tests (>10s each)",
    "critical: Critical path tests",
    "smoke: Post-deployment smoke tests"
]
```

### CI/CD Pipeline Integration

**Multi-stage testing strategy:**
```yaml
# .github/workflows/test.yml
name: Test Suites

on: [push, pull_request]

jobs:
  # Stage 1: Fast feedback on every commit
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
    # Typical duration: 5-10 seconds
  
  # Stage 2: Integration validation
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests  # Only if unit tests pass
    steps:
      - uses: actions/checkout@v3
      - name: Start test services (DB, Redis)
        run: docker-compose -f docker-compose.test.yml up -d
      - name: Run integration tests
        run: pytest tests/integration/ -v
    # Typical duration: 30-60 seconds
  
  # Stage 3: E2E validation (PR only)
  e2e-tests:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v3
      - name: Run E2E tests
        run: pytest tests/e2e/ -v --maxfail=3
    # Typical duration: 5-10 minutes
  
  # Stage 4: Nightly comprehensive suite
  nightly-tests:
    if: github.event.schedule == 'cron'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run comprehensive test suite
        run: pytest tests/ --run-slow -v
      - name: Run benchmarks
        run: pytest tests/benchmarks/ -v
      - name: Upload benchmark results
        run: python scripts/store_benchmark_results.py
    # Typical duration: 30-60 minutes
```

### AI Agent Test Suite Patterns (2026)

**RAG System Test Suite:**
```python
# tests/rag_suite/test_rag_comprehensive.py

class TestRAGEmbedding:
    """Unit tests for embedding component."""
    def test_embed_query(self): pass
    def test_batch_embed(self): pass
    def test_embedding_cache(self): pass

class TestRAGRetrieval:
    """Unit tests for retrieval component."""
    def test_vector_search(self): pass
    def test_reranking(self): pass
    def test_metadata_filtering(self): pass

class TestRAGGeneration:
    """Unit tests for generation component."""
    def test_prompt_construction(self): pass
    def test_citation_extraction(self): pass
    def test_answer_formatting(self): pass

class TestRAGIntegration:
    """Integration tests for combined pipeline."""
    def test_query_to_answer_pipeline(self): pass
    def test_handles_no_results(self): pass
    def test_handles_many_results(self): pass

class TestRAGEndToEnd:
    """E2E tests with real queries."""
    def test_factual_question(self): pass
    def test_complex_question(self): pass
    def test_multi_hop_reasoning(self): pass

# Run entire RAG suite: pytest tests/rag_suite/
# Run just retrieval: pytest tests/rag_suite/test_rag_comprehensive.py::TestRAGRetrieval
```

**Multi-Agent Orchestration Suite:**
```python
# tests/multi_agent_suite/

# tests/multi_agent_suite/test_agents_unit.py
class TestResearchAgent:
    """Unit tests for research agent."""
    pass

class TestAnalysisAgent:
    """Unit tests for analysis agent."""
    pass

# tests/multi_agent_suite/test_coordination.py
class TestAgentCoordination:
    """Integration tests for agent coordination."""
    def test_handoff_between_agents(self): pass
    def test_parallel_agent_execution(self): pass

# tests/multi_agent_suite/test_workflows_e2e.py
class TestMultiAgentWorkflows:
    """E2E tests for complete workflows."""
    def test_research_analysis_synthesis_workflow(self): pass
    def test_agent_failure_recovery(self): pass

# Run suite: pytest tests/multi_agent_suite/
```

## Think of It Like This
Imagine you're organizing a kitchen for a restaurant.

**Without test suite organization**, all your utensils, pots, pans, ingredients, and tools are in one giant pile. When you need to cook, you spend forever searching for the right items. You can't efficiently prep multiple dishes because everything is mixed together.

**With organized test suites**, you have logical organization:
- **Frequently used tools** (spatulas, knives) are at arm's reach—like unit tests you run constantly
- **Medium-use equipment** (specialty pans, mixers) is in nearby cabinets—like integration tests you run regularly
- **Rarely used items** (holiday platters, specialty molds) are in storage—like comprehensive E2E tests you run periodically
- **Essential basics** (salt, oil, water) are immediately accessible—like smoke tests verifying basics work

Each station has what it needs, chefs can work efficiently, and you can quickly grab "everything for desserts" or "everything for appetizers" without searching the entire kitchen. In testing, suites provide this same organization—run "just unit tests" for quick feedback, "integration tests" for moderate confidence, or "everything" for comprehensive validation.

## The "So What?" Factor
**If you organize test suites effectively:**
- You get fast feedback loops—run relevant tests in seconds, not minutes
- You match test scope to context—quick tests on save, comprehensive tests on PR
- You optimize CI/CD pipeline—parallel execution, staged validation, early failure detection
- You make testing sustainable—developers actually run tests because they're fast enough
- You identify issues efficiently—test failures point to specific components or layers
- You balance coverage and speed—comprehensive validation without waiting forever
- You maintain code quality—tests run frequently enough to catch regressions early
- You can debug failures faster—suite organization reveals where problems occur
- You scale testing as codebase grows—add tests to appropriate suites
- You communicate testing strategy—suite names convey what's tested and when

**If you don't organize test suites:**
- Developers run all tests or no tests—both extremes harm quality and productivity
- Feedback loops are too slow—waiting minutes for results on small changes
- CI/CD pipelines are inefficient—running unnecessary tests or skipping important ones
- Testing becomes unsustainable—slow tests get disabled or ignored
- Failures are hard to diagnose—everything mixed together provides no structure
- You can't optimize—don't know what's slow, what's critical, what's redundant
- Quality suffers—slow testing means less frequent testing means more bugs
- Debugging takes longer—no clear organization to narrow down issues
- Testing doesn't scale—adding tests makes everything slower indiscriminately
- Team lacks shared understanding of testing strategy

## Practical Checklist
Before organizing test suites, ask yourself:
- [ ] Have I separated unit, integration, and E2E tests into distinct suites?
- [ ] Can I run fast tests (unit + integration) in under 30 seconds locally?
- [ ] Do I have a smoke test suite for post-deployment validation?
- [ ] Are regression tests for bug fixes organized separately?
- [ ] Can I run specific component tests without running everything?
- [ ] Have I configured CI/CD to run appropriate suites at each stage?
- [ ] Are slow tests (E2E, benchmarks) marked and excluded from frequent runs?
- [ ] Do I use test markers/tags for flexible suite composition?
- [ ] Can developers easily discover and run relevant test suites?
- [ ] Have I documented what each suite tests and when to run it?
- [ ] Are test suites balanced—no single suite too large or slow?
- [ ] Do I periodically review and reorganize suites as codebase evolves?

## Watch Out For
⚠️ **Over-granular organization**: Creating 20 tiny suites with elaborate taxonomy makes testing confusing. Start simple (unit, integration, e2e, smoke) and add specialized suites only when clear need emerges. Over-organization is as bad as no organization.

⚠️ **Ignoring the test pyramid**: Having 5 unit tests, 50 integration tests, and 200 E2E tests inverts the pyramid—slow, brittle, expensive testing. Maintain pyramid proportions: many fast unit tests, fewer integration tests, fewest E2E tests. Suites should reflect this balance.

⚠️ **Suite dependency chains**: If your unit suite must complete before integration suite can start, and integration before E2E, you lose parallelization benefits. Design suites to run independently where possible (with appropriate setup/teardown).

⚠️ **Mixing test types**: Putting slow integration tests in the unit suite or unit tests in the E2E suite destroys the point of organization. Be disciplined about what belongs in each suite. When unsure, err toward slower suite classification.

⚠️ **Stale test organization**: As codebase evolves, test organization becomes outdated—new tests added to wrong suites, old suites no longer relevant, naming inconsistent. Schedule periodic test organization reviews (quarterly) to maintain structure.

⚠️ **No clear naming**: Vague suite names like "test_misc.py" or "test_other.py" defeat organization purpose. Use clear, descriptive names that communicate what's tested: test_rag_retrieval.py, test_tool_execution.py, test_customer_support_e2e.py.

⚠️ **Forgetting local development**: Optimizing for CI/CD but making local testing cumbersome frustrates developers. Ensure developers can easily run relevant suites locally with simple commands. If local testing is painful, it won't happen.

⚠️ **Static test selection**: Running the same suite every time regardless of what changed. Smart test selection (run tests affected by changes) can dramatically speed feedback. Modern tools can detect which tests are impacted by code changes and run only those.

## Connections
**Builds On:**
- [unit_testing](unit_testing.md) - Individual tests organized into suites
- [integration_testing](integration_testing.md) - Integration tests form integration suites
- [end_to_end_testing](end_to_end_testing.md) - E2E tests form comprehensive validation suites
- Testing strategy and test pyramid principles

**Works With:**
- [harness](harness.md) - Infrastructure that executes test suites
- [test_coverage](test_coverage.md) - Coverage measured per suite to identify gaps
- [regression_testing](regression_testing.md) - Regression tests organized into dedicated suites
- [benchmark](benchmark.md) - Benchmarks form performance validation suites
- [assertion](assertion.md) - Individual test assertions within suite tests
- Continuous integration/deployment - Suites integrated into CI/CD stages
- [monitoring](../Agent_Operations/monitoring.md) - Production monitoring validates what test suites check

**Leads To:**
- Test-driven development workflows
- Continuous testing practices
- Shift-left testing (testing earlier in development)
- Test impact analysis (smart test selection)

**Related Patterns:**
- Test pyramid - Principle guiding suite composition
- Test organization patterns - Suite structure and naming conventions
- [clean_code](../Software_Engineering/clean_code.md) - Clean test organization
- [refactoring](../Software_Engineering/refactoring.md) - Test suites enable safe refactoring
- Parallel test execution - Running suites concurrently

## Quick Decision Guide
**Invest in organized test suites when:**
- You have more than 20-30 tests and execution time becomes noticeable
- Working on team projects where multiple developers run tests
- CI/CD pipeline needs to balance speed and thoroughness
- Different test types have different speeds and purposes
- You want to optimize feedback loops for developer productivity
- Growing codebase makes testing slower and more complex
- Need to run different tests at different stages (commit, PR, deploy, nightly)

**Keep simple organization when:**
- Small projects with under 20 tests that all run in under 10 seconds
- Solo projects where sophisticated organization adds more overhead than value
- All tests are similar speed and scope
- Testing needs are simple and uniform
- Over-organization would be premature optimization

## Further Exploration
- 📖 "Test-Driven Development" (Kent Beck) - Test organization and design patterns
- 🎯 pytest documentation - Test organization, markers, and fixtures
- 💡 "Continuous Delivery" (Humble & Farley) - Test automation in deployment pipelines
- 📖 "Growing Object-Oriented Software, Guided by Tests" (Freeman & Pryce) - Test suite evolution
- 🎯 Jest documentation - JavaScript test organization and suite running
- 💡 Go testing documentation - Table-driven tests and benchmarks
- 📖 "The Art of Unit Testing" (Osherove) - Test organization patterns
- 🎯 GitHub Actions documentation - Multi-stage test workflows
- 💡 "Accelerate" (Forsgren et al.) - Research on testing practices and delivery performance
- 📖 Test pyramid pattern - Martin Fowler's testing strategy guide

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
