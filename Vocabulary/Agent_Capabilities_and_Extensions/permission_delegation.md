# Permission Delegation

## At a Glance
| | |
|---|---|
| **Category** | Security Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Identity, authorization, and least-privilege concepts |

## One-Sentence Summary
Permission delegation is granting a process, agent, or service limited authority to act on behalf of a user or system within defined boundaries.

## Why This Matters to You
Agents need permissions to do useful work, but broad permanent access is dangerous. Delegation lets you grant only what is needed for a specific task and time window. This improves safety while preserving automation speed. It also creates clearer accountability for who authorized what.

## The Core Idea
### What It Is
Permission delegation transfers scoped rights from one principal to another, often via tokens, roles, or policy grants. Delegated rights usually include constraints such as allowed actions, target resources, and expiration.

In agent environments, delegation is common when a user authorizes an assistant to run selected tools or perform bounded operations. Strong delegation models are explicit, revocable, and auditable.

### What It Isn't
Delegation is not identity impersonation without controls. The delegated actor should remain distinguishable for auditing.

It is also not a substitute for proper permission modeling. Delegation builds on, not replaces, underlying authorization design.

## How It Works
1. Define what authority can be delegated, to whom, and under what constraints.
2. Issue scoped credentials or policy grants for the delegated action window.
3. Enforce, monitor, and revoke delegated rights when no longer needed.

## Think of It Like This
Think of a station manager issuing a temporary movement permit to a certified operator for one route and one shift.

## The "So What?" Factor
**If you use this:**
- You enable automation with controlled risk.
- You keep access time-bound and purpose-bound.
- You improve auditability of privileged operations.

**If you don't:**
- Teams overuse static high-privilege credentials.
- Incidents become harder to contain and investigate.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are delegated permissions scoped to minimal required actions?
- [ ] Is there a clear expiration and revocation path?
- [ ] Can logs attribute delegated actions to original approvers?

## Watch Out For
⚠️ Delegating broad wildcard permissions for convenience.
⚠️ Missing revocation workflows when assignments change.

## Connections
**Builds On:** [permission_model.md](permission_model.md), [privilege_separation.md](privilege_separation.md)
**Works With:** [approval_workflow.md](approval_workflow.md), [tool_permission.md](tool_permission.md)
**Leads To:** [secure_execution.md](secure_execution.md), [audit_logging.md](audit_logging.md)

## Quick Decision Guide
**Use this when you need to:** Let agents act for users within strict, temporary boundaries.
**Skip this when:** The actor should have no access or requires permanent ownership-level privileges.

## Further Exploration
- [OAuth 2.0 delegated authorization](https://www.rfc-editor.org/rfc/rfc6749)
- [Least privilege implementation guidance](https://csrc.nist.gov/)
- [Zero trust identity principles](https://learn.microsoft.com/security/zero-trust/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
