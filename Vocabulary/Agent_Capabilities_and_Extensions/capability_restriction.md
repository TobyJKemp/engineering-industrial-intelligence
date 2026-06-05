# Capability Restriction

## At a Glance
| | |
|---|---|
| **Category** | Security / Policy / Governance |
| **Complexity** | Intermediate |
| **Time to Learn** | 1–2 hours for basics; more for advanced policy design |
| **Prerequisites** | Understanding of agents, permissions, and compliance requirements |

## One-Sentence Summary
Capability restriction is the practice of limiting what actions, tools, or resources an agent or system can access, based on policies, permissions, or context, to ensure safety, compliance, and control.

## Why This Matters to You
If you want your agents to operate safely, comply with regulations, or avoid unintended consequences, you need capability restriction. Without it, agents may access sensitive data, perform unauthorized actions, or violate policies—leading to security breaches, compliance failures, or loss of trust. Restricting capabilities ensures agents act within defined boundaries and only perform allowed operations.

## The Core Idea
### What It Is
Capability restriction involves defining and enforcing limits on what agents or tools can do. This can include:
- Allow/deny lists for tools, APIs, or actions
- Context-aware restrictions (e.g., only in certain workflows or user roles)
- Dynamic policy enforcement based on risk or compliance needs

Restrictions are implemented via configuration, code, or external policy engines. They are essential for multi-agent systems, regulated environments, and any scenario where safety and control are priorities.

### What It Isn't
Capability restriction is not a substitute for authentication or auditing; it complements them. It is not a one-time setup—policies must evolve as systems and requirements change. It is not about disabling all features; it is about enabling only what is necessary and safe.

## How It Works
1. **Define Policies**: Specify what actions, tools, or resources are allowed or denied.
2. **Enforce at Runtime**: Apply restrictions dynamically based on context, user, or workflow.
3. **Monitor and Update**: Audit usage, monitor for violations, and update policies as needed.

## Think of It Like This
Capability restriction is like setting parental controls on a device: you decide what apps or features are available, ensuring safe and appropriate use.

## The "So What?" Factor
**If you use this:**
- Agents operate safely and within defined boundaries
- Compliance and security requirements are met
- Risk of unintended actions or breaches is reduced

**If you don't:**
- Agents may perform unauthorized or unsafe actions
- Compliance failures and security incidents are more likely
- Trust in the system is diminished

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are all capabilities and actions reviewed for risk and necessity?
- [ ] Are restrictions documented, enforced, and auditable?
- [ ] Are policies updated as requirements change?

## Watch Out For
⚠️ Overly broad or outdated restrictions that block needed functionality
⚠️ Gaps in enforcement or auditing

## Connections
**Builds On:** [capability_model.md](capability_model.md), [security_policy.md](security_policy.md)
**Works With:** [capability_exposure.md](capability_exposure.md), [compliance_check.md](compliance_check.md)
**Leads To:** [multi-agent_system.md](../Agent_and_Orchestration/multi-agent_system.md), [zero_trust.md](../Security/zero_trust.md)

## Quick Decision Guide
**Use this when you need to:** Limit agent actions for safety, compliance, or control
**Skip this when:** All actions are safe, trivial, or already tightly controlled

## Further Exploration
- 📖 [Microsoft: Security Policy Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/security-policy)
- 🎯 [OpenAI Cookbook: Agent Safety and Restriction](https://github.com/openai/openai-cookbook#agent-safety)
- 💡 [OWASP: Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
