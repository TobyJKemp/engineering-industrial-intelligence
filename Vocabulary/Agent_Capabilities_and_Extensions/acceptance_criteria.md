# Acceptance Criteria

## At a Glance
| | |
|---|---|
| **Category** | Quality & Testing |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts |
| **Prerequisites** | Testing, requirements, quality assurance |

## One-Sentence Summary
Acceptance Criteria are explicit, measurable conditions that must be satisfied for a requirement or feature to be considered complete—providing objective standards for validating that code/features meet specifications.

## Why This Matters to You
Without acceptance criteria, "done" is subjective and contested. Developers ship what they thought was asked for, reviewers approve what they hope is complete, and stakeholders reject what they expected to be different. This dynamic causes costly rework and erodes trust. Acceptance criteria solve the most fundamental problem in delivery: aligning expectations before work starts. In AI agent and autonomous systems, the stakes are higher—agents act without constant human oversight, so behavioral expectations must be explicit and testable before deployment. If an agent doesn't have acceptance criteria for its actions (what constitutes a valid decision? a compliant response? a successful task completion?), it can't be validated and can't be trusted in production.

## The Core Idea
- **Objective definition:** Clear, testable criteria not subjective judgment
- **Completeness:** How do we know when work is done?
- **Testability:** Each criterion must be verifiable
- **Documentation:** Criteria documented before development
- **Validation:** Used to validate finished work

## How It Works
1. **Define requirements:** What needs to be built?
2. **Break into criteria:** What specific conditions must be met?
3. **Make measurable:** Each criterion must be testable
4. **Document:** Write criteria clearly
5. **Validate:** Test against criteria before calling complete

## Think of It Like This
Acceptance criteria are like **restaurant food inspection checklist**: Health inspector has specific criteria (temperature, cleanliness, storage); restaurant passes if all criteria met; no subjective judgment about whether "good enough."

## The "So What?" Factor
- **Clarity:** Everyone knows what "done" means
- **Quality:** Prevents "almost done" limbo
- **Testing:** Basis for automated/manual testing
- **Disputes:** Reduces "I thought we were done" conflicts

## Practical Checklist
- [ ] **Written before development** - Criteria defined and agreed before code is written, not after
- [ ] **Measurable** - Every criterion has a clear, testable condition; no subjective language like "works well"
- [ ] **Covers edge cases** - Criteria include happy path, validation failures, and boundary conditions
- [ ] **Stakeholder-aligned** - Product, engineering, and QA agree on criteria before sprint begins
- [ ] **Mapped to tests** - Each criterion has corresponding automated or manual test
- [ ] **Scope-bounded** - Criteria cover this feature only; scope additions captured separately
- [ ] **Documented** - Criteria stored with the ticket, spec, or PR they belong to
- [ ] **Reviewed** - At least one other person has verified criteria are clear and complete
- [ ] **Definition-of-done linked** - Criteria feed into team's official done checklist
- [ ] **Post-delivery validated** - After implementation, verified all criteria are actually satisfied

## Watch Out For
⚠️ **Ambiguous criteria:** Criteria that aren't measurable—"the system should respond quickly" is not a criterion.
⚠️ **Scope creep:** Criteria expand after development starts, invalidating work already done.
⚠️ **Written after the fact:** Criteria written post-implementation to match what was built—not acceptance criteria, just documentation.
⚠️ **Too many criteria:** 30+ conditions per feature create overhead and are rarely all tested. Target 5-15 focused conditions.

## Connections

### Builds On
- [Code Review](code_review.md) - Review verifies that work actually satisfies acceptance criteria
- [Precondition](precondition.md) - Preconditions at function level mirror acceptance criteria at feature level

### Works With
- [Test Coverage](test_coverage.md) - Tests map to acceptance criteria; gaps in criteria = gaps in coverage
- [Static Analysis](static_analysis.md) - Automated checks enforce measurable quality criteria
- [Code Quality Gate](code_quality_gate.md) - Gates can automatically enforce criteria as pipeline checks
- [Approval Workflow](approval_workflow.md) - All criteria must be met before approval is granted

### Leads To
- [Compliance Check](compliance_check.md) - Compliance requirements formalized as acceptance criteria for regulated features

## Quick Decision Guide

**Use Acceptance Criteria When:**
- Building features with multiple stakeholders or reviewers
- Work requires formal sign-off before shipping
- Teams need shared understanding of what "done" means
- Automated tests need a behavioral specification to map to
- Disputes about feature completeness are common

**Don't Use Acceptance Criteria When:**
- Exploratory prototypes with no defined outcomes
- Internal tools with a single owner and immediate feedback loop
- Work is so trivially small that completion is self-evident

## Further Exploration

📖 **Foundational Readings**
- Behavior-Driven Development (BDD) - Acceptance criteria expressed as executable Given/When/Then specifications
- User story acceptance criteria conventions - How Agile teams define done with measurable conditions

📚 **Applied Resources**
- Cucumber and Gherkin - Turning acceptance criteria into automated test scripts
- JIRA, Linear, Azure DevOps - Practical tooling for capturing and tracking criteria per ticket

🎯 **Implementation Goals**
- Define acceptance criteria for your next 3 features before development begins
- Map your existing test suite to acceptance criteria to identify untested assumptions
- Establish a team-agreed template for writing consistent, testable criteria

💡 **Strategic Insights**
- Criteria written before development reduce scope disputes and rework significantly
- If a criterion can't be tested, it's an aspiration, not an acceptance condition
- In AI agent systems, acceptance criteria must cover behavioral edge cases and safety boundaries

🔍 **Research Frontiers**
- AI-assisted acceptance criteria generation from user stories and historical tickets
- Automated traceability linking criteria to tests to deployments to production behavior

## Metadata
- **Author:** Copilot
- **Added:** June 2, 2026
- **Last Updated:** June 2, 2026
- **Confidence:** High
- **Status:** Research Complete
- **Related Category:** Quality & Testing, Agent_Capabilities_and_Extensions
