# Test Coverage

## At a Glance
| | |
|---|---|
| **Category** | Testing Methodology / Quality Metric |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 1-2 hours for fundamentals, ongoing practice for effective use |
| **Prerequisites** | Understanding of [unit_testing](unit_testing.md), basic programming concepts |

## One-Sentence Summary
Test coverage measures the percentage of your code that is executed when tests run, answering "how much of my code is actually tested?"—like discovering that your agent's error handling paths have never been tested because all your tests use happy-path scenarios.

## Why This Matters to You
When you write tests for AI agent systems in 2026, you face a hidden risk: you think you've tested your code thoroughly, but entire sections—error handlers, edge cases, fallback logic, timeout handling—might never execute during tests. Your agent's retry logic looks solid in code review, but no test actually exercises it. Your fallback to cheaper models exists but is never validated. Your context truncation code has a subtle bug that only surfaces when context exceeds limits. Test coverage reveals these blind spots by measuring which lines, branches, and functions your tests actually execute. It transforms "I wrote a lot of tests" into concrete data: "87% of code is covered, but our error handling is only 45% tested." This tells you where to focus testing effort, where regressions might hide, and which code paths are validated versus assumed to work. Without coverage tracking, you're flying blind—you don't know what's tested and what's a production incident waiting to happen.

## The Core Idea
### What It Is
Test coverage is a quantitative measurement of how much of your codebase is executed when your test suite runs. Coverage tools instrument your code, track which lines/branches/functions execute during testing, and report percentages showing tested versus untested code.

**Types of Coverage:**

**1. Line Coverage (Statement Coverage)**:
What percentage of code lines were executed?
```python
def process_query(query: str, max_retries: int = 3) -> Response:
    if not query:                              # Line 1 ✓ Covered
        raise ValueError("Empty query")        # Line 2 ✗ NOT covered (no test with empty query)
    
    for attempt in range(max_retries):         # Line 3 ✓ Covered
        try:                                   # Line 4 ✓ Covered
            response = llm.complete(query)      # Line 5 ✓ Covered
            return response                    # Line 6 ✓ Covered
        except TimeoutError:                   # Line 7 ✗ NOT covered (no timeout test)
            if attempt == max_retries - 1:     # Line 8 ✗ NOT covered
                raise                          # Line 9 ✗ NOT covered
            time.sleep(2 ** attempt)           # Line 10 ✗ NOT covered (retry path untested)

# Line coverage: 5/10 = 50%
```

**2. Branch Coverage**:
What percentage of decision branches (if/else, try/except) were taken?
```python
def validate_confidence(confidence: float) -> bool:
    if confidence < 0:          # Branch: True path ✓ Covered
        return False            # Branch: False path ✗ NOT covered
    elif confidence > 1:        # Branch: True path ✗ NOT covered
        return False            # Branch: False path ✓ Covered
    else:
        return True             # ✓ Covered

# Branch coverage: 3/4 = 75%
# (Both if-true and elif-true branches not tested)
```

**3. Function Coverage**:
What percentage of functions/methods were called?
```python
class AgentOrchestrator:
    def handle_query(self, query):           # ✓ Covered (called in tests)
        return self.process(query)
    
    def process(self, query):                # ✓ Covered (called by handle_query)
        return self.execute(query)
    
    def execute(self, query):                # ✓ Covered
        return {"response": "ok"}
    
    def handle_batch(self, queries):         # ✗ NOT covered (never tested)
        return [self.process(q) for q in queries]
    
    def handle_streaming(self, query):       # ✗ NOT covered (never tested)
        for chunk in self.stream(query):
            yield chunk
    
    def cleanup(self):                       # ✗ NOT covered (never tested)
        self.close_connections()

# Function coverage: 3/6 = 50%
```

**4. Condition Coverage (Expression Coverage)**:
For complex boolean expressions, were all sub-conditions evaluated to both true and false?
```python
def should_escalate(confidence: float, attempts: int, is_critical: bool) -> bool:
    # Complex condition with three parts
    if confidence < 0.8 and attempts > 2 and is_critical:
        return True
    return False

# Need tests covering all combinations:
# - confidence < 0.8: True and False
# - attempts > 2: True and False  
# - is_critical: True and False
# Full condition coverage requires testing all 2^3 = 8 combinations
```

**In AI Agent Systems (2026):**

**RAG Pipeline Coverage**:
```python
class RAGAgent:
    def query(self, question: str) -> Answer:
        # Retrieval phase
        docs = self.retrieve(question)              # ✓ Covered
        
        # Check if enough context
        if not docs:                                # ✗ NOT covered (no test with zero results)
            return self.fallback_response(question) # ✗ NOT covered
        
        # Rerank if many results
        if len(docs) > 10:                          # ✗ NOT covered (tests use 3-5 docs)
            docs = self.rerank(docs)                # ✗ NOT covered
        
        # Generate with context
        context = self.format_context(docs)         # ✓ Covered
        answer = self.generate(question, context)   # ✓ Covered
        
        # Validate answer quality
        if answer.confidence < 0.6:                 # ✗ NOT covered (all test answers high confidence)
            answer = self.improve_with_cot(question, context)  # ✗ NOT covered
        
        return answer                               # ✓ Covered

# Coverage reveals: Core path tested, edge cases (no results, many results, low confidence) untested
```

**Tool Execution Coverage**:
```python
def execute_tool(tool_name: str, params: dict) -> ToolResult:
    # Validation
    if tool_name not in AVAILABLE_TOOLS:           # ✓ Covered (test invalid tool)
        raise ToolNotFoundError(tool_name)          # ✓ Covered
    
    # Parameter validation
    required_params = TOOL_SCHEMAS[tool_name]["required"]
    if not all(p in params for p in required_params):  # ✗ NOT covered (no missing param test)
        raise MissingParameterError(required_params)    # ✗ NOT covered
    
    # Execute with timeout
    try:                                            # ✓ Covered
        result = TOOLS[tool_name](**params)         # ✓ Covered
        return ToolResult(success=True, data=result)  # ✓ Covered
    except TimeoutError:                            # ✗ NOT covered (no timeout test)
        return ToolResult(success=False, error="timeout")  # ✗ NOT covered
    except Exception as e:                          # ✗ NOT covered (no general error test)
        logger.error(f"Tool execution failed: {e}") # ✗ NOT covered
        return ToolResult(success=False, error=str(e))  # ✗ NOT covered

# Coverage reveals: Happy path + explicit invalid tool tested, but parameter validation and error paths untested
```

### What It Isn't
Test coverage is not **a quality metric**. 100% coverage doesn't mean your tests are good—it means every line was executed, not that every behavior was validated. You can have 100% coverage with trivial tests that don't check outputs, edge cases, or correctness.

```python
# 100% coverage, terrible test
def test_process_query():
    process_query("test")  # Line executes, but we don't assert anything!
    # This achieves coverage but validates nothing
```

It's not **a goal in itself**. Chasing 100% coverage leads to diminishing returns—testing getters/setters, impossible error conditions, or trivial code. Focus on meaningful coverage of critical paths, complex logic, and error handling. 80-90% coverage with thoughtful tests beats 100% coverage with mechanical tests.

Test coverage is not **exhaustive testing**. 100% branch coverage doesn't test all possible input combinations, timing conditions, race conditions, or integration scenarios. A function with 100% coverage might still fail with unexpected inputs, extreme values, or concurrent access.

It's not **stable**. Adding new code reduces coverage percentage even if existing tests remain unchanged. Don't obsess over exact percentages—focus on trends (coverage increasing/decreasing) and covering critical/complex code.

Coverage is not **free**. Instrumentation adds overhead—tests run 10-30% slower with coverage enabled. Generating coverage reports takes time. In CI/CD, balance coverage collection (valuable for identifying gaps) with test execution speed (fast feedback).

Finally, coverage is not **the same across languages**. Python's coverage.py measures statements; JavaScript's Istanbul measures lines, branches, functions; Go's cover tool measures statements. Coverage semantics and tools differ—understand your language's coverage model.

## How It Works

### Measuring Coverage

**Step 1: Install Coverage Tool**
```bash
# Python
pip install pytest-cov

# JavaScript/TypeScript
npm install --save-dev nyc

# Go
# Built into go test

# Java
# Add JaCoCo plugin to Maven/Gradle
```

**Step 2: Run Tests with Coverage**
```bash
# Python with pytest
pytest --cov=src --cov-report=html --cov-report=term

# JavaScript with nyc
nyc --reporter=html --reporter=text npm test

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Output shows coverage percentages and generates HTML report
```

**Step 3: Analyze Coverage Report**
```python
# Coverage report output:
"""
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/agent.py               45      8    82%   23-25, 67-71
src/tools.py               67     22    67%   34-38, 89-102, 145
src/retrieval.py           89      5    94%   234-238
src/orchestration.py      123     45    63%   45-67, 123-145, 201-209
------------------------------------------------------
TOTAL                     324     80    75%
"""

# Analysis:
# - Overall 75% coverage (decent starting point)
# - retrieval.py well-tested (94%)
# - orchestration.py needs attention (63%, many untested lines)
# - Missing line numbers show exactly what's untested
```

**Step 4: Identify Gaps**
Open HTML coverage report to see annotated source:
```python
# Green (covered)
def handle_query(query: str) -> str:
    if query:                        # ✓ Green
        return process(query)        # ✓ Green
    
    # Red (not covered)
    else:                            # ✗ Red
        raise ValueError("Empty")    # ✗ Red
```

**Step 5: Write Tests for Gaps**
```python
# Original test (incomplete coverage)
def test_handle_query():
    result = handle_query("test question")
    assert result is not None

# Add test for uncovered branch
def test_handle_query_empty():
    with pytest.raises(ValueError, match="Empty"):
        handle_query("")

# Coverage increases from 66% to 100% for this function
```

**Step 6: Set Coverage Thresholds**
Prevent coverage regressions:
```python
# pytest.ini or pyproject.toml
[tool:pytest]
addopts = --cov=src --cov-fail-under=80

# CI/CD will fail if coverage drops below 80%
```

### Coverage in CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Tests with Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=xml --cov-report=term
      
      - name: Check coverage threshold
        run: |
          coverage report --fail-under=75
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
      
      # Fail if coverage decreased significantly
      - name: Coverage diff check
        run: |
          python scripts/check_coverage_diff.py --threshold=-2
          # Fails if coverage dropped by more than 2 percentage points
```

### Practical Coverage Strategies for AI Agents

**Strategy 1: Focus on Critical Paths**
```python
# Prioritize testing high-risk, complex code
critical_modules = [
    "src/agent_core.py",       # Core agent logic
    "src/tool_execution.py",   # Tool calling (external dependencies)
    "src/error_handling.py",   # Error recovery
    "src/context_management.py",  # Context truncation, memory
]

# Target 90%+ coverage for critical modules
# Accept 70%+ for utilities, config loading, simple helpers
```

**Strategy 2: Test Error Paths**
```python
def test_llm_timeout_handling():
    """Test coverage for timeout error path."""
    with patch('llm_client.complete', side_effect=TimeoutError):
        result = agent.query("test")
        # Ensures timeout handling code is covered
        assert result.status == "timeout"
        assert result.retry_count > 0

def test_tool_execution_failure():
    """Test coverage for tool failure path."""
    with patch('tools.execute', side_effect=Exception("Tool failed")):
        result = agent.execute_tool("search", {"query": "test"})
        # Ensures error handling code is covered
        assert result.success is False
        assert "Tool failed" in result.error
```

**Strategy 3: Use Coverage to Guide Testing**
```python
# 1. Run tests: pytest --cov=src --cov-report=html
# 2. Open htmlcov/index.html
# 3. Find module with low coverage (e.g., orchestration.py 63%)
# 4. Click to see uncovered lines
# 5. Write tests specifically for red (uncovered) lines
# 6. Re-run tests and verify coverage increased

# Example: Coverage reveals untested batch processing
def test_batch_processing():
    """Tests added after coverage analysis showed gap."""
    queries = ["q1", "q2", "q3"]
    results = orchestrator.process_batch(queries)
    assert len(results) == 3
    assert all(r.success for r in results)
```

## Think of It Like This
Imagine you're a safety inspector testing fire evacuation routes in a building.

**Without coverage tracking**, you run a fire drill and everyone exits safely. You declare the evacuation plan "tested." But actually, everyone used the front door. The side exits, emergency stairs, and roof access—all part of the plan—were never used. If fire blocks the front door, those untested routes might be locked, blocked, or confusing.

**With coverage tracking**, you instrument the building with sensors that record which routes people use. After the drill, you discover:
- Main entrance: ✓ Used (tested)
- Main stairs: ✓ Used (tested)
- Side exit A: ✗ Not used (untested)
- Side exit B: ✗ Not used (untested)
- Emergency stairs: ✗ Not used (untested)
- Roof access: ✗ Not used (untested)

Now you know where testing gaps exist. You run additional drills specifically using those untested routes and discover side exit B is locked and emergency stairs are unclear. Coverage revealed the blind spots.

In code, test coverage is your sensor system showing which paths through your code have been exercised by tests and which remain untested—helping you identify where bugs might hide.

## The "So What?" Factor
**If you track test coverage:**
- You identify untested code paths—error handlers, edge cases, fallback logic
- You make informed decisions about where to invest testing effort
- You prevent coverage regressions by setting minimum thresholds in CI/CD
- You gain confidence that critical paths are validated, not just assumed to work
- You discover dead code (0% coverage might mean unused, removable code)
- You can demonstrate testing thoroughness to stakeholders with quantitative data
- You spot patterns (all retry logic is untested, all error paths are untested)
- You focus code reviews on uncovered changes (new code with 0% coverage needs tests)
- You reduce the risk of production incidents in untested code paths
- You create accountability—PRs must maintain or improve coverage

**If you don't:**
- Entire code paths (error handling, edge cases) remain untested without your knowledge
- Testing effort is unfocused—you might over-test simple code, under-test complex code
- Coverage can regress silently—new features added without tests
- Stakeholders have no quantitative evidence of testing rigor
- Dead code accumulates because you don't know it's unused
- Code reviews miss untested changes—"looks good" doesn't mean "is tested"
- Production incidents occur in code paths you thought were tested but weren't
- Team has no shared understanding of what's validated versus assumed
- Regressions hide in untested branches that never executed in test suite
- Testing feels arbitrary rather than systematic

## Practical Checklist
Before implementing test coverage tracking, ask yourself:
- [ ] Have I installed a coverage tool appropriate for my language/framework?
- [ ] Can I run tests with coverage enabled locally and in CI/CD?
- [ ] Do I understand what coverage percentage I currently have (baseline)?
- [ ] Have I set realistic coverage goals (75-85% is often good, not 100%)?
- [ ] Am I using coverage to identify gaps rather than chasing arbitrary percentages?
- [ ] Have I prioritized high-coverage for critical/complex modules over simple utilities?
- [ ] Do I have CI/CD checks preventing significant coverage regressions?
- [ ] Am I reviewing coverage reports, not just collecting them?
- [ ] Have I focused on branch/condition coverage, not just line coverage?
- [ ] Do I understand that 100% coverage ≠ perfect tests?
- [ ] Am I writing meaningful tests for uncovered code, not just executing it?
- [ ] Have I configured coverage to ignore generated code, vendor dependencies?

## Watch Out For
⚠️ **Coverage theater**: Writing tests that execute code without validating behavior just to increase coverage percentage. Tests should assert correctness, not just call functions. 100% coverage with no assertions is worthless.

```python
# Bad: Coverage without validation
def test_process_query():
    process_query("test")  # Coverage ✓, but no assertions!

# Good: Coverage with validation
def test_process_query():
    result = process_query("test")
    assert result.success
    assert len(result.answer) > 0
    assert result.confidence > 0.5
```

⚠️ **Diminishing returns**: Pursuing 100% coverage means testing trivial code (getters, property assignments), impossible error conditions, and edge cases with minimal risk. 80-90% coverage with thoughtful tests is often the sweet spot. The last 10-20% is often low-value.

⚠️ **Misleading metrics**: High line coverage with low branch coverage means you're executing code but not testing decision paths. 90% line coverage but 50% branch coverage indicates many if/else branches untested. Look at multiple coverage dimensions.

⚠️ **False confidence**: Coverage shows what was executed, not what was tested properly. A function can have 100% coverage but still fail with unexpected inputs, race conditions, or integration issues. Coverage is necessary but not sufficient.

⚠️ **Coverage decay**: As codebase grows, coverage percentage naturally drops unless testing keeps pace. New features without tests reduce overall coverage. Track coverage trends, not just absolute numbers. A drop from 85% to 78% signals testing isn't keeping up with development.

⚠️ **Tool overhead**: Coverage instrumentation slows test execution by 10-30%. In large test suites, this adds minutes to CI/CD. Consider running full coverage checks nightly and lighter checks on every PR. Balance thoroughness with speed.

⚠️ **Configuration complexity**: Coverage tools need configuration—what to include/exclude, which paths to ignore (vendor dependencies, generated code, test files themselves). Poor configuration leads to misleading coverage reports (e.g., 95% coverage because half the codebase is excluded).

⚠️ **Coverage debt**: Low coverage is often a symptom, not the root problem. Legacy code with 30% coverage might be hard to test due to poor design, tight coupling, or lack of [dependency injection](../Software_Engineering/dependency_injection.md). Improving coverage requires [refactoring](../Software_Engineering/refactoring.md), not just adding tests.

## Connections
**Builds On:**
- [unit_testing](unit_testing.md) - Coverage measures how much code unit tests exercise
- [integration_testing](integration_testing.md) - Coverage applies to integration test suites too
- Test execution infrastructure

**Works With:**
- [assertion](assertion.md) - Coverage shows code was executed; assertions validate it's correct
- [regression_testing](regression_testing.md) - Coverage helps ensure regression tests cover changed code
- [end_to_end_testing](end_to_end_testing.md) - Coverage reveals which code paths E2E tests exercise
- [benchmark](benchmark.md) - Coverage ensures benchmarks test relevant code paths
- [refactoring](../Software_Engineering/refactoring.md) - Coverage provides safety net during refactoring
- [technical_debt](../Software_Engineering/technical_debt.md) - Low coverage is a form of technical debt
- Continuous integration - Coverage checks in CI/CD pipelines

**Leads To:**
- Test-driven development (TDD) - Writing tests first ensures coverage by design
- Mutation testing - Next-level validation beyond coverage (testing the tests)
- Code quality metrics - Coverage as one dimension of quality assessment

**Related Patterns:**
- [harness](harness.md) - Test infrastructure includes coverage collection
- Code review practices - Reviewing coverage changes in PRs
- [clean_code](../Software_Engineering/clean_code.md) - Testable code tends to have better coverage
- [monitoring](../Agent_Operations/monitoring.md) - Runtime code path tracking in production
- Static analysis - Complementary code quality measurement

## Quick Decision Guide
**Invest in coverage tracking when:**
- Building production systems where untested code poses risks
- Working on team projects where coverage provides shared visibility
- Refactoring complex code and need safety net
- Onboarding new team members who need guidance on what's tested
- CI/CD pipeline can enforce coverage thresholds
- You want to identify dead code or ensure new features are tested
- Stakeholders require quantitative evidence of testing rigor

**Use lightly or skip when:**
- Building quick prototypes where comprehensive testing isn't justified
- Working solo on experimental projects
- Code is so simple that gaps are obvious (trivial utilities)
- Test execution speed matters more than coverage metrics
- Coverage tools don't support your language/framework well
- Team is already test-disciplined and coverage doesn't add value

## Further Exploration
- 📖 "Test-Driven Development" (Kent Beck) - Writing tests that ensure coverage by design
- 🎯 coverage.py documentation - Python coverage tool
- 💡 Istanbul/nyc documentation - JavaScript coverage tools
- 📖 "Working Effectively with Legacy Code" (Michael Feathers) - Testing and covering legacy systems
- 🎯 JaCoCo documentation - Java coverage tool
- 💡 Go testing documentation - Built-in coverage support
- 📖 "The Art of Software Testing" (Myers et al.) - Testing thoroughness and coverage
- 🎯 Codecov/Coveralls - Coverage tracking services for CI/CD
- 💡 pytest-cov plugin documentation - Coverage integration for pytest
- 📖 "Growing Object-Oriented Software, Guided by Tests" (Freeman & Pryce) - Test coverage in practice

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
