# Hook Composition

## At a Glance
| | |
|---|---|
| **Category** | Advanced Operational Pattern / Extension Architecture |
| **Complexity** | Advanced |
| **Time to Learn** | 6-10 hours for concepts; 3-4 weeks for robust implementation; months to master at scale |
| **Prerequisites** | Agent hooks, lifecycle hooks, function composition, functional programming patterns, complex workflow orchestration |

## One-Sentence Summary
Hook composition is the practice of combining multiple hooks and handlers into coordinated workflows—where handlers for one hook trigger other hooks, handlers share state, and complex multi-hook sequences execute as coherent operations—enabling sophisticated agent behaviors without hardcoding logic into agent core.

## Why This Matters to You
Single hooks are powerful; composed hooks are transformative. In engineered intelligence systems, decisions often require multi-step workflows: validation hook → logging hook → policy enforcement hook → metrics collection hook → downstream notification hook. Without composition, you implement these sequences by hand in each handler (coupling handlers, duplicating logic). With composition, you define workflows declaratively: "when this hook fires, run this sequence of handlers in this order, sharing this context, and notify these systems." Hook composition enables: **workflow abstraction** (define complex behaviors as named sequences), **handler reuse** (one handler serving multiple workflows), **dependency management** (handlers that depend on each other's outputs), **conditional logic** (run handler A if condition, else handler B), and **dynamic behavior** (compose hooks at runtime based on policy/configuration). For railway operations: arrival of equipment triggers 5-hook sequence (validate specs, check availability, assign location, notify operators, log event). Hook composition means this sequence defined once, reused across all equipment types.

## The Core Idea

### What It Is
Hook composition is a structured approach to combining multiple hooks and handlers. The core concepts are:

**Sequential Composition** - Multiple hooks execute in sequence: hook A fires, its handlers complete, then hook B fires. Example: `before_action` hook validates action, then `after_action_complete` hook logs outcome. Sequential composition is the most common pattern.

**Parallel Composition** - Multiple hooks or handlers execute concurrently. Example: `on_decision_made` hook fires 3 independent handlers: (1) log decision to audit system, (2) update metrics, (3) notify monitoring. Parallel composition requires: thread safety, result aggregation, and timeout management.

**Conditional Composition** - Hook execution depends on conditions. Example: `on_error` hook fires different handlers based on error type: transient error → retry handler, permanent error → escalation handler, rate limit error → backoff handler. Conditional composition requires explicit decision logic.

**Nested Composition** - Handlers themselves register other handlers, creating composite behavior. Example: `on_initialization_start` handler registers handlers for `on_dependency_check`, `on_config_loaded`, etc. Nested composition enables: progressive behavior definition, dynamic handler registration, and complex workflows.

**Stateful Composition** - Handlers in composed sequences share state (context object passed through sequence). Example: `before_action` handler populates context with action metadata, `on_action_complete` handler uses that metadata to compute metrics, `after_action_complete` handler uses metrics for reporting. Stateful composition requires: clear state contract (what fields handlers can read/write?) and conflict resolution (what if two handlers modify same field?).

**Transactional Composition** - Composed sequences must maintain consistency: either all handlers succeed or all rollback. Example: creating new equipment in railway system: validate specs (success), allocate resource (success), update inventory (fails) → rollback all previous changes. Transactional composition is complex but critical for data consistency.

### What It Isn't
Hook composition is not simply chaining method calls (handler1() then handler2()). That's implementation detail. Composition is architectural pattern describing how hooks relate.

Hook composition is not middleware stacking. While both involve sequential processing, middleware typically operates on request/response objects flowing through. Hooks are more fine-grained, tied to specific agent events.

Hook composition is not just event publishing. Pub/sub systems broadcast events to subscribers without explicit composition. Hook composition defines structured workflows with explicit coordination.

Hook composition is not orchestration frameworks (like Airflow, Temporal). While orchestration tools can implement composed hooks, composition happens at hook level, not external workflow engine level.

## How It Works
A production hook composition system operates through these design phases:

1. **Identify Workflows** - System architect identifies recurring multi-step processes that span multiple hooks. Example workflows for railway system:
   - Equipment arrival: validate specs → check availability → assign location → notify operators → log event
   - Agent error recovery: detect error → classify error → attempt recovery → if success notify monitoring else escalate → log outcome
   - Configuration deployment: validate new config → dry-run test → backup current config → apply new config → smoke test → notify services
   These are workflows: multi-hook sequences with defined input, output, and success criteria.

2. **Define Workflow Specification** - Each workflow formally specifies: hooks involved (in order), handlers at each hook, data flow (how context flows between handlers), error handling (if handler fails, what happens?), and completion criteria (how do we know workflow succeeded?). Example specification for equipment arrival:
   ```
   Workflow: equipment_arrival
   Hooks: [on_equipment_arrived, on_validate_specs, on_check_availability, 
           on_assign_location, on_notify_operators, on_log_complete]
   Handlers:
     on_equipment_arrived: extract_equipment_id, record_arrival_time
     on_validate_specs: validate_against_schema, populate_context['specs_valid']
     on_check_availability: check_resource_pool, populate_context['location']
     on_assign_location: reserve_location, populate_context['location_reserved']
     on_notify_operators: send_notification, populate_context['notification_sent']
     on_log_complete: log_workflow_completion
   Data Flow: context object carries equipment_id, arrival_time, specs, availability, location
   Error Handling: if any handler fails, fire on_equipment_arrival_failed hook, log error
   Success Criteria: all handlers complete without exception
   ```

3. **Context Management** - Define context object that flows through workflow. Context carries:
   - **Input data** (what triggered workflow)
   - **Intermediate results** (outputs from handlers that later handlers need)
   - **Metadata** (timestamps, request IDs, user context)
   - **State** (current progress through workflow)
   Context must be: immutable where possible (avoid accidental mutations), versioned (can evolve without breaking handlers), documented (handlers know what fields available), and scoped (handlers only access fields they need).

4. **Handler Registration for Composition** - Register handlers as part of workflow. Rather than registering handlers individually, register workflow: `register_workflow('equipment_arrival', equipment_arrival_spec)`. System automatically registers all handlers in correct order. Alternatively: handlers register themselves as members of workflow: `@handler_for('equipment_arrival', phase='validate') def validate_specs():`

5. **Sequential Execution** - Workflow engine fires hooks in sequence. For each hook:
   - Collect all handlers registered for this hook AND part of this workflow
   - Execute handlers in order (deterministic ordering: handlers themselves define dependencies or system defines order)
   - Aggregate results into context object
   - If any handler fails: decide on error strategy (fail fast, skip handler, apply default, or execute alternative handlers)
   - Proceed to next hook if no failure (or if failure recoverable)

6. **Parallel Execution** - For hooks that have independent handlers, execute in parallel:
   ```
   on_decision_made handlers:
     handler_1: update_metrics (independent)
     handler_2: log_audit (independent)
     handler_3: notify_monitoring (independent)
   → execute all 3 concurrently, wait for all to complete before proceeding
   ```
   Parallel execution requires: thread safety (handlers don't interfere), timeout management (don't wait forever), and result aggregation (collect results from all handlers).

7. **Conditional Branching** - Workflows support conditional logic: `if context['specs_valid'] then on_check_availability else on_equipment_rejected`. Conditions evaluated at runtime based on workflow context. Handlers can populate context fields that drive branching decisions.

8. **Error Handling and Recovery** - Workflow defines error handling: 
   - **Fail-fast** - First handler exception stops workflow, triggers error handler
   - **Continue-on-error** - Handler exception logged but workflow continues (useful for non-critical steps)
   - **Retry** - Failed handler retried (with exponential backoff, max retries)
   - **Alternative** - If primary handler fails, execute fallback handler
   - **Rollback** - If later handler fails, execute compensating handlers to undo earlier steps (transactional)

9. **Compensation (Rollback)** - For workflows requiring transactional guarantees: each handler registers compensating action (rollback handler). If workflow fails mid-sequence:
   - Execute compensating handlers in reverse order of original execution
   - Restore system to state before workflow started
   - Log rollback for audit trail
   Example: config deployment workflow - if final smoke test fails, rollback handlers restore original configuration, restart services with original config.

10. **Workflow Execution and Monitoring** - Workflow engine tracks execution:
    - Records which handlers executed, when, with what results
    - Tracks workflow progress (which phase executing)
    - Collects performance metrics (latency per handler, total workflow time)
    - Logs all decisions, branches taken, errors encountered
    - Generates workflow execution trace (complete audit trail)
    This tracing is essential for debugging complex workflows.

## Think of It Like This
Think of hook composition like an assembly line in a factory. Individual machines (hooks) perform specific operations. A car's assembly involves sequential operations: welding station → paint booth → tire assembly → electronics → final inspection → shipping. Each station is a hook. The car carries context (growing more complete through each station). Some stations operate in parallel (painting and tire assembly independent). If inspection fails, compensating actions (rework) apply. Some decisions branch logic (luxury model takes different paint booth than standard). The assembly line is the composed workflow: sequence of hooks coordinated into a production process. Just as factory can adjust assembly line without changing individual machines, you can adjust composed hooks without changing individual handlers.

## The "So What?" Factor

**Benefits:**
- ✅ **Behavior Abstraction** - Complex multi-step behaviors defined once as workflows, reused everywhere. Reduces code duplication by 60-80%.
- ✅ **Handler Reuse** - Individual handlers solve specific problems (validate specs, check availability). Composed into many workflows. One handler used by 5+ workflows.
- ✅ **Maintainability** - Changes to workflow specification automatically apply to all instances. No scattered handler logic to update.
- ✅ **Testability** - Test workflows in isolation from agent core. Mock handlers, test error paths, test parallel execution.
- ✅ **Debuggability** - Workflows generate complete execution traces. When workflow fails, trace shows exactly: what succeeded, what failed, when, why.
- ✅ **Dynamic Behavior** - Compose workflows at runtime based on policy/context. Same agent supports different workflows for different customers.
- ✅ **Observability** - Workflow engine provides built-in metrics: workflow success rates, handler latencies, error patterns.
- ✅ **Consistency** - Transactional workflows guarantee: either entire workflow succeeds or all changes rolled back. No partial failures leaving system inconsistent.

**Risks and Challenges:**
- ⚠️ **Workflow Complexity** - Complex workflows become hard to understand: many hooks, branching logic, error paths. Visualization and documentation critical.
- ⚠️ **Handler Dependency Management** - When handlers depend on each other (handler B reads output of handler A), ordering becomes critical. Hidden dependencies cause bugs.
- ⚠️ **Execution Order Non-Determinism** - Parallel handlers execute in unpredictable order. If handlers have undocumented dependencies, results become non-deterministic.
- ⚠️ **Context Object Evolution** - Context fields accumulate over time. Handlers assume fields exist. Adding/removing fields breaks handlers. Requires versioning strategy.
- ⚠️ **Debugging Difficulty** - Composed workflows spanning many handlers with complex error paths are hard to debug. Requires comprehensive logging and tracing.
- ⚠️ **Performance Unpredictability** - Workflow latency depends on slowest handler in sequence (bottleneck). Parallel composition reduces latency but creates concurrency complexity.
- ⚠️ **Testing Combinatorial Explosion** - With N handlers and M hooks, testing all combinations becomes impractical. Requires smart testing strategy (mock handlers, test critical paths).
- ⚠️ **Compensation Complexity** - Implementing correct compensation logic is hard. Forgetting to implement rollback handler for one step can break transactional guarantees.

## Practical Checklist
- [ ] **Workflows Identified** - List multi-step processes in system that span multiple hooks
- [ ] **Workflow Specifications Documented** - For each workflow: hooks, handlers, data flow, error handling, success criteria formally documented
- [ ] **Context Contract Defined** - Context object structure documented: what fields handlers read, what they write, format of each field
- [ ] **Handler Dependencies Explicit** - If handlers depend on each other's outputs, documented and enforced (ordering, context field contracts)
- [ ] **Error Handling Strategy** - Defined for each workflow: fail-fast vs. continue-on-error, retry strategy, error handling handlers
- [ ] **Compensation Handlers** - For transactional workflows, implemented compensation handlers for each modification handler
- [ ] **Workflow Visualization** - Created diagrams showing workflow structure: hooks, handlers, data flow, branching logic
- [ ] **Workflow Execution Tracing** - Implemented logging: which handlers executed, in order, with results, latencies
- [ ] **Performance Testing** - Tested workflow latency: in sequence, in parallel, with different error scenarios
- [ ] **Testing Strategy** - Defined how to test workflow: mock handlers, test individual paths, test error scenarios, test handler combinations
- [ ] **Documentation** - Created workflow documentation for operators: what does workflow do? When does it run? What can go wrong?
- [ ] **Monitoring** - Set up metrics for each workflow: success rate, latency, error rate, handler latencies

## Watch Out For

⚠️ **Hidden Handler Dependencies** - Handler B assumes Handler A already ran and populated certain context fields. But ordering not enforced. If handlers execute in different order (parallel execution), Handler B fails with cryptic error. Solution: make dependencies explicit (document, enforce ordering, add assertions at handler start).

⚠️ **Context Mutation Bugs** - Multiple handlers modify same context field. Last one wins, intermediate values lost. Solution: make context immutable where possible, use explicit state management (handler returns modified context, previous handler's changes preserved), document which handlers modify which fields.

⚠️ **Unintended Compensation Cascades** - Compensation handler for step 5 triggers workflow that itself has compensation handlers. Cascading failures cause system to thrash rolling back/forward. Solution: keep compensation simple (ideally idempotent, not triggering new workflows), test compensation paths thoroughly, use compensation budgets (don't compensate more than N levels deep).

⚠️ **Workflow Deadlock** - Workflow A waiting for hook that Workflow B should fire, but Workflow B waiting for different hook. System deadlocks. Solution: design workflows to avoid circular dependencies, add timeouts (workflows that hang too long fail), monitor for stuck workflows.

⚠️ **Silent Workflow Failures** - Workflow fails mid-execution, handlers stop running, but failure not reported. Agent silently operates with incomplete workflow. Solution: wrap all workflows in try-catch, always fire completion hook (success or failure), monitor for workflows that never complete, test error paths.

⚠️ **Parallel Handler Race Conditions** - Two parallel handlers modify shared state simultaneously. Corrupted state results. Solution: handlers that modify shared state must coordinate (locks, compare-and-swap), or handlers shouldn't modify shared state (share context, not global state), or use eventual consistency patterns.

## Connections

### Builds On
- [Agent Hook](agent_hook.md) - Hook composition composes multiple hooks
- [Lifecycle Hooks](lifecycle_hooks.md) - Lifecycle hooks often compose into workflows
- [Skill Orchestration](../Agent_Capabilities_and_Extensions/skill_orchestration.md) - Similar composition patterns at skill level

### Works With
- [Async Hook Execution](async_hook_execution.md) - Asynchronous composed workflows
- [Error Handling](error_handling.md) - Error handling within composed workflows
- [State Management](state_management.md) - Context state flowing through composition
- [Audit Trail](audit_trail.md) - Audit trails of composed workflows

### Leads To
- [Workflow Orchestration](../Dispatching/Orchestration/) - Large-scale workflow systems
- [Skill Composition](../Agent_Capabilities_and_Extensions/skill_composition.md) - Similar composition at skill level
- [Multi-Agent Workflows](../Dispatching/Agent_Coordination/) - Coordinating composed workflows across agents

## Quick Decision Guide

**Use Hook Composition When:**
- You have multi-step processes repeating across codebase
- You need to coordinate multiple handlers into coherent workflow
- Different customers/scenarios require different hook sequences
- You need workflow observability (tracing, debugging)
- You want transactional semantics (all-or-nothing)
- You're building complex coordination logic

**Don't Use Hook Composition When:**
- Workflow is trivially simple (2 hooks, 1 handler each)
- Performance is critical and hook overhead unacceptable
- You have only one workflow (composition overhead not justified)
- System is one-off/not expected to evolve

## Further Exploration

📖 **Foundational Readings**
- Saga pattern (distributed transactions) - Composition pattern for multi-service workflows
- Business Process Model and Notation (BPMN) - Standardized workflow specification language
- Functional composition (fp-ts, Ramda) - Programming patterns for composing functions

📚 **Applied Resources**
- Apache Airflow - Production workflow orchestration engine
- Temporal.io - Distributed workflow engine with compensation patterns
- Spring Cloud Stream - Event-driven composition patterns
- Kubernetes Operator pattern - Composing hooks and webhooks

🎯 **Implementation Goals**
- Design 3-5 core workflows for your system
- Implement workflow engine supporting sequential, parallel, conditional execution
- Create workflow visualization and debugging tools
- Build comprehensive workflow test suite

💡 **Strategic Insights**
- Hook composition is where system complexity moves from code to configuration
- Invest in workflow visualization; complex workflows invisible in code
- Compensation logic is often forgotten and causes production issues
- Observable, traceable workflows pay dividends in operational debugging

🔍 **Research Frontiers**
- Automated workflow optimization (identify critical paths, optimize bottlenecks)
- Distributed workflow composition (workflows spanning multiple agents/services)
- Workflow versioning and migration (evolving workflows without breaking running instances)
- Self-healing workflows (detecting and recovering from failures automatically)

## Metadata
- **Author:** Copilot
- **Added:** June 2, 2026
- **Last Updated:** June 2, 2026
- **Confidence:** High
- **Status:** Research Complete
- **Related Category:** Agent_Operations, Advanced Orchestration
