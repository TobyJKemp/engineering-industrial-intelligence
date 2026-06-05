# Authorization

## At a Glance
| | |
|---|---|
| **Category** | Security Mechanism |
| **Complexity** | Intermediate to Advanced |
| **Time to Learn** | 4-6 hours for fundamentals, ongoing for complex policies |
| **Prerequisites** | [Authentication](authentication.md), basic security concepts, understanding of access control |

## One-Sentence Summary
Authorization is the security process that determines what actions an authenticated user, system, or [AI agent](../Agent_and_Orchestration/ai_agent.md) is permitted to perform on specific resources—answering "what can you do?" after identity has been verified—essential for enforcing access policies, protecting sensitive operations, and implementing least-privilege security in AI systems.

## Why This Matters to You
Your [AI agent](../Agent_and_Orchestration/ai_agent.md) might successfully authenticate (prove who it is), but that doesn't mean it should be able to do everything. Should your customer service agent access financial records? Should your data analysis agent delete production databases? Should your content generation agent modify user accounts? Authorization is the security layer that enforces these boundaries. Without proper authorization, authenticated agents can access data they shouldn't see, perform operations beyond their intended scope, and cause damage through privilege escalation. For AI systems you build, authorization ensures users can only invoke capabilities appropriate to their role, prevents agents from exceeding their defined permissions, creates accountability by linking actions to specific permission grants, and meets compliance requirements that mandate access controls. Poor authorization means data breaches, unauthorized transactions, compliance violations, and agents doing things you never intended them to do—even though they're "legitimate" authenticated entities.

## The Core Idea
### What It Is
Authorization is the security mechanism that controls access to resources and operations based on permissions, roles, policies, or attributes associated with an authenticated identity. After [authentication](authentication.md) verifies "who you are," authorization determines "what you're allowed to do." It evaluates whether the authenticated entity (user, [AI agent](../Agent_and_Orchestration/ai_agent.md), service) has permission to perform the requested action (read customer data, delete records, invoke expensive operations) on the specific resource (customer ID 12345, production database, GPT-4 API).

Authorization operates through policies—rules that map identities to permissions. These policies can be simple (user Alice can read documents) or complex (agents in the data-science role can query analytics databases during business hours when the request originates from the corporate network and involves anonymized data only). The authorization system evaluates these policies on every request, making allow/deny decisions before operations execute.

In AI agent architectures, authorization appears at multiple levels: **User-to-Agent** (which users can access which agent capabilities?), **Agent-to-Resource** (which APIs, databases, or services can this agent access?), **Agent-to-Agent** (in [multi-agent systems](../Agent_and_Orchestration/multi-agent_system.md), which agents can invoke other agents?), and **Operation-Level** (even authorized agents might be restricted from high-risk operations like data deletion or expensive API calls).

Authorization models include several approaches:

**Role-Based Access Control (RBAC)**: Permissions are assigned to roles (admin, editor, viewer), and users/agents are assigned to roles. Simple to understand and manage at scale. Example: "Data Analyst" role can query databases but not modify them.

**Attribute-Based Access Control (ABAC)**: Access decisions based on attributes of the user, resource, action, and environment. More flexible and context-aware than RBAC. Example: Allow access if (user.department == resource.owner_department AND time.hour >= 9 AND time.hour <= 17).

**Access Control Lists (ACLs)**: Resources explicitly list which identities can access them and what they can do. Fine-grained but hard to manage at scale. Example: Document-123 specifies [Alice: read/write, Bob: read, Agent-X: read].

**Policy-Based Access Control**: Centralized policy engine evaluates rules written in policy language (like OPA's Rego or AWS IAM policies). Most powerful and flexible, but most complex to implement correctly.

### What It Isn't
Authorization is **not authentication**. This confusion is the source of countless security vulnerabilities. Authentication proves identity ("you are Alice"), while authorization determines permissions ("Alice can read this file but not delete it"). They always work together—you must authenticate before you can authorize—but they're separate concerns. Many systems correctly authenticate but fail to properly authorize, allowing authenticated users to access resources they shouldn't.

Authorization is **not simply checking if someone is "logged in"**. Being authenticated doesn't grant universal access. Even after successful authentication, each request must be authorized—checking not just "is this user logged in?" but "does this user have permission to perform this specific action on this specific resource?"

Authorization is **not a one-time check at login**. It's an ongoing evaluation process. Just because a user was authorized to access System-A when they logged in doesn't mean they're authorized to delete data in System-B five minutes later. Authorization decisions are made per-request, per-resource, per-action.

Authorization is **not the same as rate limiting or quotas**, though they're related. Authorization asks "are you allowed to do this?"; rate limiting asks "have you done this too many times?"; quotas ask "have you exhausted your allocation?" All are access controls, but they serve different purposes and use different decision criteria.

Finally, coarse-grained authorization ("this user can access the API") is **not sufficient** for production AI systems. You need fine-grained authorization that considers the specific operation, specific data, and context. The difference between "Agent-X can call the database" and "Agent-X can query customer table where user_id matches authenticated user and only return anonymized data" is the difference between security theater and actual security.

## How It Works
Authorization evaluation in an AI agent system follows this decision flow:

1. **Request Context Assembly** (after successful authentication)
   - Extract authenticated identity from request (user ID, agent ID, service principal)
   - Identify requested resource (customer record, database table, API endpoint)
   - Determine requested action (read, write, delete, execute)
   - Collect contextual attributes (time, location, resource sensitivity, request metadata)
   - Example: Agent-42 (identity) wants to DELETE (action) customer record ID-789 (resource) at 2AM (context)

2. **Permission Lookup**
   - Query authorization system for applicable permissions
   - In RBAC: Retrieve roles assigned to identity, then permissions for those roles
   - In ABAC: Retrieve attributes for identity, resource, action, and environment
   - In ACL: Check resource's access control list for identity's permissions
   - In Policy-Based: Pass context to policy engine for evaluation

3. **Policy Evaluation**
   - Authorization engine evaluates policies against request context:
     - **Direct Permission**: User explicitly granted permission for this action
     - **Role Permission**: User's role includes this permission
     - **Attribute Match**: User's attributes satisfy policy conditions (department matches, time is within hours, etc.)
     - **Hierarchical Permission**: Permission inherited from parent resource or broader scope
     - **Deny Rules**: Explicit denials that override allow rules (important for least-privilege)

4. **Context-Aware Checks** (for advanced systems)
   - Evaluate dynamic conditions:
     - **Time-based**: Only allow access during business hours
     - **Location-based**: Only allow from corporate network
     - **Resource-state**: Only allow if resource is in "draft" status
     - **Rate-limited**: Only allow if quota not exceeded
     - **Risk-based**: Require additional verification for high-risk operations
   - These checks supplement basic permissions with environmental context

5. **Authorization Decision**
   - **Allow**: All applicable policies permit the action, no denials present
   - **Deny**: At least one policy explicitly denies, or no policy permits
   - **Conditional Allow**: Allowed but with constraints (read-only, redacted fields, limited scope)
   - Default-deny principle: If no explicit allow policy matches, deny the request
   - Log the decision with full context for audit trail

6. **Enforcement**
   - If denied: Return 403 Forbidden error with minimal details (don't leak authorization structure)
   - If allowed: Proceed with request processing
   - If conditional: Apply constraints (filter data, limit operations, add safeguards)
   - Record authorization decision in [audit trail](../Agent_Operations/audit_trail.md)

7. **Dynamic Scope Filtering** (data-level authorization)
   - Even with operation permission, filter data based on authorization:
     - User can query customer table, but only see their own records
     - Agent can read documents, but only non-confidential ones
     - Service can access logs, but with PII redacted
   - Authorization affects both "can you do this?" and "what subset of data can you access?"

8. **Permission Inheritance and Hierarchies**
   - Permissions can be hierarchical:
     - Permission to read /documents implies permission to read /documents/public
     - Admin role inherits all permissions from editor role
     - Organization-level permissions propagate to projects and resources
   - Simplifies management but requires careful design to avoid unintended access

9. **Delegation and Impersonation**
   - In [multi-agent systems](../Agent_and_Orchestration/multi-agent_system.md), Agent-A might act on behalf of User-X:
     - Agent-A's permissions + User-X's permissions (intersection or union?)
     - Typically: Agent can only perform actions User is authorized for (delegation)
     - Audit trail shows both Agent-A (actor) and User-X (principal)
   - Prevents agents from privilege escalation beyond their users' permissions

10. **Permission Caching and Performance**
    - Authorization checks on every request can be expensive
    - Cache authorization decisions (but carefully—invalidate when permissions change)
    - Use short cache TTLs (seconds to minutes) to balance performance with security
    - For high-security operations, always check fresh (no cache)

## Think of It Like This
Authorization is like a building with different security clearance levels. You've already passed through the lobby security checkpoint where you proved your identity (authentication). Now you're standing in front of various doors throughout the building. Your ID badge has permissions encoded on it: you can enter the cafeteria (everyone can), the second-floor offices (employees only), and the engineering lab (engineering staff only), but not the executive suite (executives only) or the server room (IT admins only). When you tap your badge on a door reader, it checks: "Does this badge have permission for this specific door?" Each door makes an independent authorization decision based on your permissions. Having valid building access doesn't grant you access to every room—each protected resource enforces its own authorization rules.

Similarly, your authenticated [AI agent](../Agent_and_Orchestration/ai_agent.md) might have broad system access, but each API endpoint, database table, or operation checks: "Is this agent authorized for this specific action?" The agent can query customer data (permission granted) but cannot delete it (permission denied), even though both operations exist on the same authenticated connection.

In our railway metaphor, authorization is the track access control system that determines which trains can use which tracks. A freight train has authenticated its identity to the central dispatcher (proven it's Train-247), but authorization determines its permitted routes. Train-247 can use freight lines (authorized) but not passenger express lines (unauthorized). Even though it's a legitimate, authenticated train, track authorization restricts where it can travel based on its type, cargo, schedule, and operational clearances. The railway network maintains complex authorization rules: freight trains during off-peak hours on specific routes, passenger trains on dedicated lines, maintenance vehicles only on closed sections. Each junction point validates authorization before allowing the train to proceed, preventing unauthorized access to tracks regardless of successful authentication.

## The "So What?" Factor
**If you implement authorization properly:**
- You enforce least-privilege principle (agents access only what they need)
- You prevent privilege escalation attacks (authenticated but unauthorized users can't access sensitive resources)
- You meet compliance requirements (GDPR, HIPAA, SOC 2 mandate access controls)
- You create accountability (audit trail shows who was authorized to do what)
- You enable safe multi-tenancy (customers can't access each other's data)
- You can delegate safely (users can grant limited permissions to agents without full access)
- You reduce blast radius of compromised credentials (stolen token can only access what it's authorized for)

**If you skip authorization or implement it poorly:**
- Authenticated users and agents can access anything (authentication without authorization)
- You face privilege escalation attacks (users discover they can access resources beyond their scope)
- You violate compliance regulations (lack of access controls = fines, legal liability)
- You can't support multi-tenancy safely (no isolation between customers)
- You have no fine-grained control (all-or-nothing access)
- Your [audit trails](../Agent_Operations/audit_trail.md) can't distinguish between authorized and unauthorized but successful requests
- Data breaches happen even without credential theft (existing users access data they shouldn't)
- [AI agents](../Agent_and_Orchestration/ai_agent.md) exceed intended scope and cause unintended damage

## Practical Checklist
Before implementing authorization for your AI agent system, ask yourself:
- [ ] **What authorization model fits my needs?** (RBAC for simplicity, ABAC for flexibility, policy-based for complex rules)
- [ ] **What resources need protection?** (APIs, databases, operations, data fields—identify your authorization boundaries)
- [ ] **What roles or permissions should exist?** (Start with least-privilege—what's the minimum access each agent/user needs?)
- [ ] **How granular should authorization be?** (Operation-level? Data-level? Field-level? Balance security with complexity)
- [ ] **How will I handle delegation?** (When agents act on behalf of users, whose permissions apply?)
- [ ] **What's my default policy?** (Default-deny is security best practice—explicit allows only)
- [ ] **How will I test authorization?** (Negative testing is critical—verify unauthorized requests are blocked)
- [ ] **Am I logging authorization decisions?** (For audit, debugging, and security monitoring)
- [ ] **How will permissions evolve?** (Plan for role changes, permission updates, and revocation)

## Watch Out For
⚠️ **Confusing Authentication with Authorization:** The most common mistake. Just because a request is authenticated doesn't mean it's authorized. Always implement both layers, and never skip authorization checks because "they already logged in." Attackers exploit this by using legitimate credentials to access unauthorized resources.

⚠️ **Client-Side Authorization Checks:** Never rely on the client (browser, mobile app, [AI agent](../Agent_and_Orchestration/ai_agent.md)) to enforce authorization. Clients can be modified, bypassed, or impersonated. Always enforce authorization server-side, even if you also check client-side for UX reasons.

⚠️ **Overly Permissive Default Permissions:** Starting with "everyone can access everything" and restricting later is backwards. Start with default-deny (no one can access anything) and explicitly grant permissions. Many security breaches happen because someone forgot to restrict access to a new resource.

⚠️ **Role Explosion:** RBAC systems tend to accumulate roles over time—CustomerServiceBasic, CustomerServiceAdvanced, CustomerServiceSupervisor, CustomerServiceManager. Soon you have 100 roles with unclear distinctions. Regularly audit and consolidate roles, or consider ABAC for more flexible policy expression.

⚠️ **Inconsistent Authorization Logic:** Having different authorization logic in different parts of your system (one service uses RBAC, another uses ACLs, a third has custom checks) creates security gaps. Standardize on one authorization approach and centralize policy enforcement.

⚠️ **Missing Data-Level Authorization:** Checking if a user can "access customer records" (operation-level) without checking "which specific customer records" (data-level) is insufficient. Users should only access their own data, their organization's data, or data they're explicitly granted access to. Authorization must filter data, not just operations.

⚠️ **No Permission Revocation:** When users leave, roles change, or agents are decommissioned, their permissions must be revoked immediately. Stale permissions are a major security risk. Implement automated revocation processes and regular permission audits.

⚠️ **Permission Caching Without Invalidation:** Caching authorization decisions improves performance but creates security risks if not invalidated properly. When permissions change, cached decisions become stale. Use short cache TTLs and implement cache invalidation on permission updates.

## Connections
**Builds On:** 
- [Authentication](authentication.md) - Must authenticate identity before authorizing actions
- Security principles - Least privilege, defense in depth, fail-safe defaults

**Works With:** 
- [API Gateway](api_gateway.md) - Centralizes authorization enforcement for multiple services
- [Audit Trail](../Agent_Operations/audit_trail.md) - Logs authorization decisions for compliance and forensics
- [Human-in-the-Loop](../Safety_and_Control/human-in-the-loop.md) - Routes high-risk operations to human approval (authorization with human decision)
- [Guardrails](../Safety_and_Control/guardrails.md) - Policy enforcement mechanisms that include authorization rules
- [Monitoring](../Agent_Operations/monitoring.md) - Tracks authorization failures and patterns

**Leads To:** 
- Identity and Access Management (IAM) - Comprehensive identity, authentication, and authorization systems
- Zero Trust Architecture - "Never trust, always verify" requires authorization on every request
- Policy-as-Code - Treating authorization policies as versioned, tested, deployable code
- Attribute-Based Access Control (ABAC) - Advanced authorization using rich contextual attributes

## Quick Decision Guide
**Choose authorization model based on complexity:**

**RBAC (Role-Based)** when:
- Relatively simple permission structure
- Clear role hierarchies (admin, editor, viewer)
- Most users fit into predefined categories
- Example: Content management system with author/editor/admin roles

**ABAC (Attribute-Based)** when:
- Context-aware authorization needed (time, location, resource state)
- Complex policies that RBAC can't express
- Dynamic access requirements
- Example: [AI agent](../Agent_and_Orchestration/ai_agent.md) can access customer data only if customer.region == agent.authorized_region

**ACL (Access Control Lists)** when:
- Fine-grained per-resource permissions
- Small scale or specific use cases (file systems, documents)
- Users need custom permissions per resource
- Example: Document collaboration where each document has specific user permissions

**Policy-Based (OPA, AWS IAM)** when:
- Highly complex authorization requirements
- Need centralized policy management
- Multiple services requiring consistent authorization
- Example: [Multi-agent system](../Agent_and_Orchestration/multi-agent_system.md) with complex cross-service authorization rules

**Granularity levels:**
- **Service-level**: Can user access this API? (coarse, minimal protection)
- **Operation-level**: Can user perform this action (read/write/delete)? (common, reasonable)
- **Resource-level**: Can user access this specific record? (fine-grained, more secure)
- **Field-level**: Can user see this specific field? (very fine-grained, maximum security)

Choose granularity based on security requirements vs. complexity tradeoffs.

## Further Exploration
- 📖 **NIST RBAC Model (RBAC-2000)** - Standard reference for role-based access control
- 🎯 **XACML (eXtensible Access Control Markup Language)** - Standard for expressing authorization policies
- 💡 **Open Policy Agent (OPA)** - Modern policy engine for cloud-native authorization
- 📖 **AWS IAM Documentation** - Comprehensive example of policy-based authorization at scale
- 🎯 **OWASP Authorization Cheat Sheet** - Security best practices for authorization
- 💡 **Zanzibar Paper (Google)** - Describes Google's global authorization system handling trillions of checks
- 📖 **"Authorization in the Wild" (Stripe)** - Real-world authorization challenges at scale

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*