# Agent Delegation

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Architectural Mechanism |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 hours for concept, 1-2 weeks for production implementation |
| **Prerequisites** | AI agent basics, task decomposition, tool calling, orchestration concepts |

## One-Sentence Summary
Agent delegation is the pattern where one AI agent assigns a discrete unit of work to another agent (or to itself in a specialized mode), transferring responsibility for that subtask's execution while retaining accountability for the overall outcome—enabling complex tasks to be decomposed across agents with different capabilities, contexts, or authority levels.

## Why This Matters to You
You're building a system where a single agent handles customer onboarding: it needs to verify identity documents, check compliance databases, generate account configurations, and send welcome communications. One agent doing all of this requires an enormous context window, every possible tool loaded simultaneously, and permissions spanning security-sensitive identity systems through to marketing email APIs. Agent delegation lets you decompose this into focused handoffs—the orchestrating agent delegates identity verification to a specialized agent with access to only document analysis tools and compliance databases, delegates account setup to another agent with infrastructure permissions, and delegates communications to a third with email/SMS access. Each delegated agent operates within tight boundaries, carries only the context it needs, and returns a structured result. The orchestrating agent never needs credentials for identity systems, the identity agent never sees email infrastructure. You get separation of concerns, reduced blast radius, and agents that are individually simpler to test, audit, and trust.

## The Core Idea
### What It Is
Agent delegation is the mechanism by which one agent (the **delegator**) identifies that a portion of its current task is better handled by another agent (the **delegate**) and transfers that work along with the necessary context, constraints, and success criteria. The delegator formulates a clear request—"verify this document is a valid government-issued ID and return the extracted name, date of birth, and document number"—sends it to the delegate agent, and waits for (or asynchronously monitors) the result. When the delegate completes its work, it returns a structured response to the delegator, which incorporates that result into its ongoing task.

This is fundamentally different from a single agent using a tool. When an agent calls a tool (like a database query function), the tool executes deterministically and returns data—there's no reasoning, no judgment, no autonomous decision-making in the tool itself. When an agent delegates to another agent, the delegate brings its own reasoning capabilities, its own context understanding, its own tool set, and its own judgment about how to accomplish the subtask. The delegate might call multiple tools, reason through ambiguous situations, handle errors, and make decisions—all autonomously within the scope of the delegated task.

Delegation operates across several dimensions:

**Vertical delegation** — An orchestrator agent delegates downward to specialist agents with narrower capabilities. The orchestrator sees the big picture (onboard this customer), specialists handle focused tasks (verify this document, configure this account). This is hierarchical: orchestrator retains authority, specialists execute within constraints.

**Horizontal delegation** — Peer agents delegate to each other based on capability matching. A coding agent encounters a database schema question and delegates to a data modeling agent. Neither is "above" the other—they're peers with different expertise. The original agent recognizes it's not the best-equipped for this subtask and routes accordingly.

**Self-delegation** — An agent delegates to itself in a different mode or with a different context window. An agent processing a large codebase might spawn a focused sub-instance of itself with only the relevant files loaded, avoiding context window pollution. Same underlying model, but a fresh reasoning context focused on the subtask.

The delegation contract typically includes: (1) a clear task description with success criteria, (2) the minimum context the delegate needs (not the delegator's full context), (3) constraints on what the delegate may and may not do, (4) the expected output format, and (5) a timeout or resource budget. Well-designed delegation contracts are the difference between effective multi-agent systems and chaotic ones.

### What It Isn't
Agent delegation is not **tool calling** or **function invocation**. When an agent calls a tool, it's invoking a deterministic function—`search_database(query="customer 12345")` always returns the same result for the same database state. There's no reasoning in the tool, no judgment, no autonomy. Delegation involves transferring work to an entity that reasons about how to accomplish it. A delegate agent might call several tools, try different approaches, handle ambiguous inputs, and make judgment calls. The delegator says "figure this out and tell me the answer"—not "execute this exact operation."

Agent delegation is not **prompt chaining** or **sequential processing**. In prompt chaining, a single agent processes outputs from one prompt as inputs to the next—same agent, same context, different steps. Delegation involves a distinct agent with its own context, its own tool access, and its own reasoning process. The delegate doesn't share the delegator's conversation history, doesn't see the delegator's full context, and operates independently within its scope.

It's not **load balancing** or **parallel execution** of identical work. Load balancing distributes identical tasks across identical workers for throughput. Delegation routes specific tasks to specific agents because those agents have different capabilities, permissions, or expertise. You don't delegate to whichever agent is least busy—you delegate to the agent best equipped for this particular subtask.

Agent delegation is also not **human-in-the-loop approval**. When an agent pauses to ask a human for approval, that's escalation or gating—not delegation. The human isn't doing the agent's work; they're authorizing the agent to proceed. Delegation transfers actual work execution to the delegate, not just approval authority. (Though delegation can include escalation paths: "if you can't resolve this, escalate to a human rather than guessing.")

## How It Works
Agent delegation follows a consistent lifecycle regardless of implementation framework:

**1. Task Recognition — "I shouldn't do this myself"**

The delegator agent, while processing its assigned task, identifies a subtask that is better handled by another agent. This recognition happens through several mechanisms:
- **Capability mismatch**: "I need to analyze an image but I'm a text-only agent"
- **Permission boundary**: "This requires database write access I don't have"
- **Context isolation**: "Processing this 50,000-line codebase will overwhelm my context; a fresh agent with just the relevant files will reason better"
- **Expertise matching**: "This is a legal compliance question and there's a compliance-specialized agent available"
- **Risk containment**: "This action is irreversible; delegating to an agent with stricter guardrails is safer"

**2. Contract Formation — "Here's exactly what I need"**

The delegator constructs a delegation request containing:
- **Task specification**: Clear description of what needs to be accomplished ("Verify that the attached document is a valid US passport or driver's license, extract the full name and date of birth, and assess whether the photo matches the selfie image")
- **Context transfer**: Minimum necessary context, not full conversational history ("Here is the document image, here is the selfie image, here is the customer's claimed name for comparison")
- **Constraints**: What the delegate may and may not do ("Do not store the images after processing. Do not call external APIs. Return results in structured JSON format. If confidence is below 80%, return 'inconclusive' rather than guessing")
- **Success criteria**: How the delegator will evaluate the result ("Response must include: document_type, full_name, date_of_birth, photo_match_confidence, overall_validity_assessment")
- **Resource budget**: Limits on execution ("Complete within 30 seconds. Maximum 5 tool invocations. Do not request additional information—work with what's provided")

**3. Handoff Execution — "Go"**

The delegation request is transmitted to the delegate agent through the system's orchestration layer. Depending on architecture, this might be:
- A direct API call to a running agent instance
- A message placed on a task queue for the next available agent of that type
- A subagent spawn (new agent instance created specifically for this task)
- A mode switch within a multi-modal agent framework

The delegator then either waits synchronously (blocking until result returns) or continues other work asynchronously (checking back for the result when needed).

**4. Autonomous Execution — The delegate works independently**

The delegate agent receives the task, operates within its own context, uses its own tools, and reasons autonomously about how to accomplish the work. It might:
- Call multiple tools in sequence (OCR the document, extract fields, compare against validation rules)
- Handle errors and retry (OCR failed on first attempt, try different preprocessing)
- Make judgment calls within its constraints (document is slightly damaged but readable—proceed rather than fail)
- Produce intermediate reasoning that stays within its context (not shared back to delegator unless requested)

**5. Result Return — "Here's what I found"**

The delegate returns a structured result conforming to the delegation contract:
- The actual output (extracted data, analysis result, generated artifact)
- Confidence/quality signals (how certain the delegate is about its answer)
- Metadata (execution time, tools used, any warnings or caveats)
- Error information if task could not be completed (what went wrong, what was tried, whether retry might help)

**6. Integration — Delegator incorporates the result**

The delegator receives the delegate's response, validates it against success criteria, and incorporates it into its ongoing work. If the result is insufficient (low confidence, missing fields, error), the delegator may retry (re-delegate with additional context), try a different delegate, or escalate.

## Think of It Like This
Agent delegation works like a general contractor building a house. The general contractor (delegator) understands the full project—the blueprint, timeline, budget, and how everything fits together. But the GC doesn't personally wire the electrical, plumb the pipes, and pour the foundation. Instead, the GC delegates to specialized subcontractors: "Here's the electrical plan, here are the code requirements, here's where the panel goes—wire this house and pass inspection." The electrician (delegate) brings their own expertise, tools, and judgment about routing, wire gauge, and junction box placement. They work autonomously within the spec, make professional decisions about details the GC didn't specify, and return a completed result ("electrical done, passed inspection, here's the as-built diagram"). The GC doesn't need to know how to wire a house—they need to know what to ask for, who to ask, and how to verify the result. That's delegation: decompose complex work across specialists who each bring focused expertise, operate within clear constraints, and return verified results to the coordinator who assembles them into the complete outcome.

## The "So What?" Factor
**If you use this:**
- Complex tasks decompose naturally across agents with focused capabilities, contexts, and permissions
- Each agent operates with minimal blast radius—compromise of one delegate doesn't expose the entire system
- Individual agents become simpler to build, test, audit, and improve (narrow scope, clear contracts)
- Context windows stay focused—delegates only see what they need, avoiding distraction and confusion from irrelevant information
- You can scale specific capabilities independently (add more document verification agents during onboarding spikes without scaling the orchestrator)

**If you don't:**
- Single monolithic agents accumulate every tool, every permission, and every piece of context—becoming unwieldy and unpredictable
- Testing becomes combinatorially explosive (one agent with 50 tools has thousands of possible interaction paths)
- Security boundaries collapse (one agent with all permissions has catastrophic breach potential)
- Context windows overflow or degrade on complex tasks (agent loses track of what it's doing in a sea of irrelevant context)
- Failure is all-or-nothing (single agent fails = entire task fails; delegated subtask fails = orchestrator can retry or route around)

## Practical Checklist
Before implementing agent delegation, ask yourself:
- [ ] Is the subtask genuinely better handled by a different agent, or am I over-engineering? (Simple tool calls don't need delegation)
- [ ] Can I define a clear, complete delegation contract? (Vague delegation produces vague results)
- [ ] Does the delegate have exactly the tools and permissions it needs—no more? (Principle of least privilege)
- [ ] What happens if the delegate fails, times out, or returns garbage? (Error handling is mandatory, not optional)
- [ ] Is the context transfer minimal and sufficient? (Too little = delegate can't succeed; too much = security risk and context pollution)
- [ ] How will I validate the delegate's result before incorporating it? (Trust but verify—delegates can hallucinate too)
- [ ] Is the delegation boundary a natural seam in the task, or am I splitting something that should stay together? (Artificial boundaries create coordination overhead that exceeds the benefit)

## Watch Out For
⚠️ **Delegation ping-pong**: Agent A delegates to Agent B, which decides it needs Agent A's help, which delegates back to B. Without cycle detection or depth limits, delegation chains can loop indefinitely. Always implement maximum delegation depth and cycle detection.

⚠️ **Context loss at boundaries**: Every delegation boundary is a potential information loss point. The delegator must decide what context to transfer—too little and the delegate fails; too much and you leak sensitive information or overwhelm the delegate's context. Getting this right requires iteration and testing.

⚠️ **Accountability diffusion**: When a delegated task produces a wrong answer, who's responsible? The delegator (for choosing the wrong delegate or providing insufficient context)? The delegate (for reasoning incorrectly)? The system (for insufficient guardrails)? Establish clear accountability chains before deploying.

⚠️ **Latency multiplication**: Each delegation hop adds latency (context transfer, agent initialization, reasoning time, result return). A task delegated through 4 levels of agents may take 10x longer than a single agent with all capabilities. Optimize for the right level of decomposition—not maximum decomposition.

⚠️ **Over-delegation of simple tasks**: Not every subtask needs a separate agent. If the task is "look up a value in a database," a tool call suffices—you don't need to spin up a "database specialist agent" for a SELECT query. Delegate when there's genuine reasoning, judgment, or capability difference; use tools for deterministic operations.

## Connections
**Builds On:** [task_decomposition](../Agent_and_Orchestration/task_decomposition.md), [tool_invocation](tool_invocation.md), [permission_model](permission_model.md), [execution_context](execution_context.md)
**Works With:** [subagent_spawning](subagent_spawning.md), [specialized_agent](specialized_agent.md), [handoff_protocol](../Agent_Operations/handoff_protocol.md), [orchestration](../Agent_and_Orchestration/orchestration.md), [access_boundary](access_boundary.md)
**Leads To:** [multi-agent_system](../Agent_and_Orchestration/multi-agent_system.md), [skill_orchestration](skill_orchestration.md), [capability_negotiation](capability_negotiation.md), [permission_delegation](permission_delegation.md)

## Quick Decision Guide
**Use this when you need to:** Route a subtask to an agent with different capabilities, permissions, or context requirements than the current agent—especially when the subtask involves autonomous reasoning (not just data retrieval).
**Skip this when:** The subtask is a deterministic operation (use a tool call), the task is simple enough for one agent to handle in its current context, or the coordination overhead of delegation would exceed the benefit of specialization.

## Further Exploration
- 📖 Microsoft AutoGen documentation — multi-agent conversation patterns and delegation frameworks
- 📖 LangGraph agent orchestration — stateful delegation with checkpointing and error recovery
- 🎯 CrewAI framework — role-based agent delegation with explicit task assignment
- 💡 "Voyager: An Open-Ended Embodied Agent" (2023) — self-delegation patterns where an agent decomposes and delegates to specialized sub-routines it builds for itself

---
*Added: May 20, 2026 | Updated: May 20, 2026 | Confidence: High*