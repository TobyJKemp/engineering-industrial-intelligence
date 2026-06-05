# Principle of Least Privilege

## At a Glance
| | |
|---|---|
| **Category** | Security & Governance |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts |
| **Prerequisites** | Security, access control, governance |

## One-Sentence Summary
The Principle of Least Privilege dictates that users, applications, and systems should have only the minimum access and permissions necessary to perform their required functions—reducing damage from compromises.

## The Core Idea
- **Minimal access:** Give only what's needed
- **No excess:** Don't grant "just in case" permissions
- **Containment:** Compromised account/system limited to its permissions
- **Regular review:** Remove permissions no longer needed
- **Foundation:** Core security principle

## How It Works
1. **Identify needed access:** What permissions are required?
2. **Grant minimum:** Grant only those permissions
3. **Document:** Document why each permission granted
4. **Review regularly:** Audit permissions periodically
5. **Remove unused:** Revoke permissions no longer needed

## Think of It Like This
Principle of least privilege is like **need-to-know basis in espionage**: Agent only told information they need for their mission. If captured, enemy only learns limited info.

## The "So What?" Factor
- **Risk reduction:** Compromised account causes limited damage
- **Compliance:** Required by most security standards
- **Insider threat:** Reduces damage from malicious insiders
- **Simplicity:** Simpler security model

## Watch Out For
⚠️ **Over-restriction:** Can prevent legitimate work.
⚠️ **Permission creep:** Permissions accumulate over time.

## Practical Checklist
- [ ] Have you mapped all roles and their required permissions?
- [ ] Are permissions reviewed regularly (at least annually)?
- [ ] Is access provisioning automated and auditable?
- [ ] Are inactive accounts automatically disabled?
- [ ] Is privilege escalation logged and monitored?
- [ ] Are permissions revoked promptly on role change?
- [ ] Is exception handling process documented?
- [ ] Are service accounts using minimal required permissions?
- [ ] Have you implemented approval workflows for elevated access?
- [ ] Are audit logs reviewed for permission violations?

## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

## Connections
**Builds On:** [Access Control](..\Safety_and_Control\access_control.md), Security
**Works With:** [Role-Based Access Control](..\Safety_and_Control\access_control.md)
**Leads To:** Privilege Management

---
*Added: June 2, 2026 | Updated: June 2, 2026 | Confidence: High*

