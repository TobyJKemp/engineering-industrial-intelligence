# Compliance Check

## At a Glance
| | |
|---|---|
| **Category** | Quality & Governance |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts |
| **Prerequisites** | Compliance, regulations, policy |

## One-Sentence Summary
A Compliance Check is an automated or manual verification that code, configurations, or processes meet regulatory requirements, organizational policies, or security standards—preventing non-compliant code from advancing.

## Why This Matters to You
Compliance failures aren't just legal risk—they're operational risk that materializes suddenly and expensively. Automated compliance checks turn compliance from a manual bottleneck (periodic audits, manual reviews) into a continuous safety net. For engineered intelligence systems, compliance checks enforce that agents operating within regulated domains (railway safety, equipment standards, personnel certification) adhere to the governance frameworks the organization is accountable to. Without automated compliance checks, you're relying on developers to independently know and apply all applicable requirements—an unreliable approach at scale.

## The Core Idea
- **Policy verification:** Verify compliance with policies
- **Automated:** Many checks can be automated
- **Standards:** Check against known standards
- **Documentation:** Document compliance status
- **Prevention:** Prevent non-compliant code deployment

## How It Works
1. **Define policies:** What compliance requirements?
2. **Identify checks:** What checks verify compliance?
3. **Automate:** Where possible, automate checks
4. **Run checks:** Execute checks on code/config
5. **Document:** Document compliance status

## Think of It Like This
Compliance check is like **airport security screening**: Passenger goes through multiple checks (ID verification, baggage screening, etc.) before boarding. Non-compliant passengers don't board.

## The "So What?" Factor
- **Risk prevention:** Prevents regulatory violations
- **Consistency:** Same standards applied everywhere
- **Automation:** Many checks can be automated
- **Audit trail:** Documents compliance verification

## Practical Checklist
- [ ] **Requirements mapped** - Relevant regulations and policies inventoried; each mapped to specific checks
- [ ] **Checks automated** - Automatable checks are automated; manual checks documented with clear evaluation criteria
- [ ] **Coverage complete** - All components in scope have at least one compliance check
- [ ] **Evidence captured** - Each check produces evidence of compliance; evidence stored and retrievable for audits
- [ ] **Frequency defined** - Continuous (on every change), periodic (weekly/monthly), or event-triggered (before release)
- [ ] **Exceptions documented** - When checks produce exceptions, exceptions are documented with owner and resolution plan
- [ ] **False positive process** - Clear escalation for legitimate code that fails compliance checks
- [ ] **Audit-ready** - Check results formatted for auditors; demonstrates which requirements are satisfied how
- [ ] **Team trained** - Engineers understand which compliance requirements apply to their work and why
- [ ] **Drift monitoring** - System monitors for configuration drift from compliant baseline between scheduled checks

## Watch Out For
⚠️ **Over-compliance:** Applying requirements that don't actually apply to your context. Creates friction without reducing risk. Map requirements to scope carefully.
⚠️ **False compliance:** Checks pass because they test proxies (policy document exists) not outcomes (policy is followed). Design checks that verify actual behavior.
⚠️ **Point-in-time compliance:** System compliant at audit time but non-compliant between audits. Continuous compliance monitoring prevents this.
⚠️ **Compliance without understanding:** Teams implement checks mechanically without knowing why. When requirements change, teams can't adapt intelligently.

## Connections

### Builds On
- [Acceptance Criteria](acceptance_criteria.md) - Compliance requirements expressed as measurable acceptance criteria
- [Audit Logging](audit_logging.md) - Compliance checks rely on audit trails as evidence

### Works With
- [Code Quality Gate](code_quality_gate.md) - Compliance checks implemented as quality gate policies
- [Approval Workflow](approval_workflow.md) - Compliance status feeds into approval decisions
- [Static Analysis](static_analysis.md) - Static analysis tools enforce code-level compliance requirements
- [Execution Policy](execution_policy.md) - Runtime policies enforce behavioral compliance requirements

### Leads To
- [Governance](../../Signal_Logic/Governance/) - Compliance checks operationalize governance frameworks

## Quick Decision Guide

**Use Compliance Checks When:**
- Operating in regulated environments (GDPR, HIPAA, SOC 2, ISO 27001)
- Organizational policies mandate verification before deployment
- Auditors require evidence of compliance at defined intervals
- Automated systems take consequential actions that must be governed

**Don't Use Compliance Checks When:**
- Requirements don't apply to your domain or context
- Check overhead exceeds value for the risk level involved
- Early prototypes with no production data or user impact

## Further Exploration

📖 **Foundational Readings**
- Policy as Code (PaC) - Expressing compliance requirements as executable code rather than documents
- Compliance-as-Code with OPA (Open Policy Agent) - Industry-standard tool for automated compliance

📚 **Applied Resources**
- AWS Config Rules, Azure Policy - Cloud-native compliance checking at infrastructure level
- SonarQube security rules - Code-level compliance enforcement for OWASP and other standards

🎯 **Implementation Goals**
- Inventory your applicable regulations; map each to specific automated checks
- Implement continuous compliance monitoring rather than point-in-time audits
- Build compliance evidence collection into your CI/CD pipeline

💡 **Strategic Insights**
- Compliance automation shifts compliance from burden to competitive advantage
- Checks are only valuable if they test actual behavior, not proxy indicators
- In AI agent systems, compliance checks must include behavioral validation, not just code-level checks

🔍 **Research Frontiers**
- Adaptive compliance (requirements interpreted in context, not applied uniformly)
- AI-assisted compliance mapping (automatically identify applicable requirements from system description)
- Continuous compliance attestation without periodic audit cycles

## Metadata
- **Author:** Copilot
- **Added:** June 2, 2026
- **Last Updated:** June 2, 2026
- **Confidence:** High
- **Status:** Research Complete
- **Related Category:** Quality & Governance, Agent_Capabilities_and_Extensions
