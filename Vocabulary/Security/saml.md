# SAML

## At a Glance
| | |
|---|---|
| **Category** | Security & Identity |
| **Complexity** | Intermediate-Advanced |
| **Time to Learn** | 3-4 hours for concepts |
| **Prerequisites** | Web security, XML, Single Sign-On concepts |

## One-Sentence Summary
Security Assertion Markup Language (SAML) is an XML-based standard for exchanging authentication and authorization information between identity providers and service providers—enabling Single Sign-On (SSO) across enterprise systems.

## The Core Idea
- **Authentication exchange:** Securely exchange authentication info
- **SSO enablement:** Users authenticate once, access multiple services
- **Enterprise focus:** Designed for enterprise SSO
- **Standards-based:** Interoperable across systems
- **Federated identity:** Supports multiple identity providers

## How It Works
1. **User requests access:** User requests access to service
2. **Redirect to IdP:** Service redirects to identity provider
3. **Authentication:** User authenticates with IdP
4. **SAML assertion:** IdP creates SAML assertion (signed XML)
5. **Redirect to service:** IdP redirects user back with assertion
6. **Verify assertion:** Service verifies signature and grants access

## Think of It Like This
SAML is like **diplomatic passport**: Issued by one country (identity provider), trusted by other countries (service providers). One passport enables access to multiple borders.

## The "So What?" Factor
- **SSO:** Users authenticate once, access multiple systems
- **Enterprise standard:** Widely used in enterprises
- **Interoperability:** Works across different vendors
- **Security:** Uses XML signatures and encryption

## Watch Out For
⚠️ **Complexity:** SAML can be complex to implement.
⚠️ **Performance:** XML processing can be slower than alternatives.

## Practical Checklist
- [ ] Is SAML 2.0 implementation current?
- [ ] Have you validated signed assertions are verified?
- [ ] Is encryption enabled for sensitive data?
- [ ] Are assertion time windows configured appropriately?
- [ ] Is metadata shared securely with service providers?
- [ ] Have you tested SSO flow end-to-end?
- [ ] Are SAML failures logged and monitored?
- [ ] Have you tested attribute mapping for all applications?
- [ ] Is user provisioning/de-provisioning automated?
- [ ] Have you planned for federated identity recovery?

## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

## Connections
**Builds On:** [Authentication](..\Integration_and_APIs\authentication.md), Single Sign-On
**Works With:** [OAuth Flow](oauth_flow.md)
**Leads To:** Federated Identity

---
*Added: June 2, 2026 | Updated: June 2, 2026 | Confidence: High*

