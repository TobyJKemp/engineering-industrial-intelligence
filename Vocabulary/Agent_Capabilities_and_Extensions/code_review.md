# Code Review

## At a Glance
| | |
|---|---|
| **Category** | Quality & Collaboration |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts |
| **Prerequisites** | Software development, version control |

## One-Sentence Summary
Code Review is a systematic process where developers examine changes made by peers before they're merged into the main codebase—catching bugs, ensuring quality, sharing knowledge, and maintaining standards.

## Why This Matters to You
Code review is the highest-leverage quality practice available: it catches bugs before they run, spreads knowledge across teams, enforces architectural standards, and prevents technical debt from compounding. No automated tool catches design-level problems, unclear intent, or missing edge case handling—only human review does. For AI agent systems, this matters even more: reviewing agent instruction files, tool definitions, system prompts, and capability configurations is as critical as reviewing code. A poorly designed agent policy can have outsized consequences compared to a typical software bug.

## The Core Idea
- **Peer review:** Other developers review code
- **Approval required:** Code doesn't merge until approved
- **Quality focus:** Look for bugs, style, performance
- **Learning:** Share knowledge across team
- **Standards enforcement:** Enforce coding standards

## How It Works
1. **Developer submits:** Developer proposes code changes
2. **Reviewers examine:** Other developers review
3. **Provide feedback:** Suggest improvements
4. **Address feedback:** Developer addresses comments
5. **Approve/merge:** Approver merges if acceptable

## Think of It Like This
Code review is like **academic paper review**: Author writes paper → reviewers examine → provide feedback → author addresses → paper accepted if satisfactory.

## The "So What?" Factor
- **Quality:** Catches bugs before production
- **Learning:** Team learns from each other
- **Standards:** Enforces coding standards
- **Knowledge sharing:** Reduces knowledge silos

## Practical Checklist
- [ ] **Scope clear** - PR description explains what changed, why, and what reviewers should focus on
- [ ] **Size managed** - PR small enough to review meaningfully (<400 lines); large changes split or pre-discussed
- [ ] **Tests included** - New behavior covered by tests; reviewer checks test quality, not just presence
- [ ] **Reviewer assigned** - Specific reviewers assigned who have domain context, not random selection
- [ ] **Criteria established** - Team has shared standards for what merits approval; not up to individual preference
- [ ] **Feedback actionable** - Reviewer comments are specific and actionable; not vague or personal
- [ ] **Author responsive** - Author responds to all comments before merge; unresolved threads documented
- [ ] **Time-bounded** - SLA for review response defined; reviews not left waiting indefinitely
- [ ] **Security checked** - Sensitive patterns (auth logic, external calls, data handling) explicitly reviewed
- [ ] **Documentation updated** - Code changes reflected in documentation; reviewer validates docs match code

## Watch Out For
⚠️ **Too strict/nitpicky:** Reviews focus on style over substance, slowing delivery without improving quality. Separate style (automate via linting) from logic review.
⚠️ **Rubber-stamping:** Reviews approve quickly without genuine inspection, especially on PRs from senior engineers. Psychological safety for reviewers is essential.
⚠️ **PR too large:** PRs over 500 lines are rarely reviewed thoroughly. Large PRs get rubber-stamped or stuck. Enforce size limits.
⚠️ **Knowledge hoarding:** Only one person capable of reviewing a module. Single point of failure. Rotate reviewers to spread knowledge.

## Connections

### Builds On
- [Acceptance Criteria](acceptance_criteria.md) - Review validates that code satisfies acceptance criteria
- [Static Analysis](static_analysis.md) - Static analysis handles mechanical checks so reviewers focus on logic

### Works With
- [Code Quality Gate](code_quality_gate.md) - Gates enforce automated criteria; review enforces judgment criteria
- [Test Coverage](test_coverage.md) - Reviewers verify that new behavior is tested, not just present code
- [Approval Workflow](approval_workflow.md) - Code review is the primary approval workflow for code changes

### Leads To
- [Compliance Check](compliance_check.md) - Security and compliance review is a specialized form of code review

## Quick Decision Guide

**Use Code Review When:**
- Code will run in production or shared environments
- Changes affect security, data handling, or critical business logic
- Team has multiple contributors who need to stay aligned
- Knowledge sharing and mentoring are organizational priorities
- Defects are costly to fix after deployment

**Don't Use Code Review When:**
- Exploratory prototypes that will be discarded
- Hotfixes in active incidents where speed is critical (review post-hoc)
- Automated code generation with comprehensive test coverage and validation

## Further Exploration

📖 **Foundational Readings**
- Google Engineering Practices: Code Review - Authoritative guide from Google's engineering culture
- The Code Review Pyramid - Framework for prioritizing review focus (correctness > design > style)

📚 **Applied Resources**
- GitHub pull request review features - Inline comments, suggestions, and review workflows
- Gerrit code review system - Used at Google and Android; fine-grained code review control

🎯 **Implementation Goals**
- Establish team code review standards: what always requires review, what constitutes approval, SLA expectations
- Implement PR size limits and automated reminders for stale reviews
- Create a review checklist for security-sensitive code paths

💡 **Strategic Insights**
- The best code reviews catch design issues before implementation is complete, not after
- Review culture depends on psychological safety: reviewers must be able to push back on senior engineers
- In AI agent systems, review of agent instructions, tool definitions, and behavior policies is as critical as code review

🔍 **Research Frontiers**
- AI-assisted code review (automated first-pass review highlighting potential issues)
- Review analytics (tracking which review patterns correlate with production defects)
- Asynchronous vs. synchronous review effectiveness across team sizes

## Metadata
- **Author:** Copilot
- **Added:** June 2, 2026
- **Last Updated:** June 2, 2026
- **Confidence:** High
- **Status:** Research Complete
- **Related Category:** Quality & Collaboration, Agent_Capabilities_and_Extensions
