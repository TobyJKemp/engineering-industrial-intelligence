# Multi-Factor Authentication

## At a Glance
| | |
|---|---|
| **Category** | Security |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts |
| **Prerequisites** | Authentication, security basics |

## One-Sentence Summary
Multi-Factor Authentication (MFA) requires users to provide multiple forms of verification (something you know, something you have, something you are) before gaining access—significantly reducing unauthorized access even if one factor is compromised.

## The Core Idea
- **Multiple factors:** Requires more than one type of verification
- **Types combined:** Password + code/biometric/device
- **Security improvement:** Much harder to compromise multiple factors
- **Trade-off:** Security vs. convenience
- **Standard practice:** MFA now industry best practice

## How It Works
1. **First factor:** User provides password
2. **Second factor:** System requires additional verification (code, biometric, device)
3. **Types of factors:**
   - Something you know: Password, PIN, security question
   - Something you have: Phone, hardware token, app
   - Something you are: Fingerprint, face recognition
4. **Verification:** Both factors verified before access granted

## Think of It Like This
MFA is like **bank security**: Password alone isn't enough (something you know). Also need physical card/ID (something you have) or fingerprint (something you are).

## The "So What?" Factor
- **Security:** Much harder for attackers to compromise
- **Compliance:** Required by many regulations
- **Peace of mind:** Better protection for sensitive accounts
- **Friction:** Extra steps slow down legitimate access

## Watch Out For
⚠️ **User experience:** Can be frustrating/slow.
⚠️ **Backup factors:** Backup access methods can be weak point.

## Practical Checklist
- [ ] Is MFA enabled for all sensitive accounts?
- [ ] Have you tested MFA across all access methods?
- [ ] Are backup/recovery methods secure?
- [ ] Is MFA enforced consistently?
- [ ] Have you documented supported MFA methods?
- [ ] Is user support process documented for MFA issues?
- [ ] Are MFA events logged and monitored?
- [ ] Have you tested MFA during account recovery?
- [ ] Is MFA integrated with your authentication system?
- [ ] Have you communicated MFA requirements to users?

## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

## Connections
**Builds On:** [Authentication](..\Integration_and_APIs\authentication.md)
**Works With:** [Access Control](..\Safety_and_Control\access_control.md)
**Leads To:** [Zero Trust](../Security/zero_trust.md)

---
*Added: June 2, 2026 | Updated: June 2, 2026 | Confidence: High*

