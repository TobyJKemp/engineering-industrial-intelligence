# API Versioning

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Practice |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for concepts, ongoing practice for mastery |
| **Prerequisites** | [REST API](rest_api.md), basic software design principles, understanding of backward compatibility |

## One-Sentence Summary
API versioning is the practice of managing and communicating changes to an API over time by assigning version identifiers, allowing providers to evolve functionality while maintaining backward compatibility for existing clients—critical for AI agent systems that depend on stable, predictable API contracts.

## Why This Matters to You
Your [AI agent](../Agent_and_Orchestration/ai_agent.md) relies on external APIs to function—fetching data, triggering actions, integrating with services. When those APIs change (and they will), your agent needs to keep working without constant maintenance. API versioning is how providers signal what's changed, what's deprecated, and what's safe to use. Without versioning, you're in a nightmare scenario where APIs change unpredictably, breaking your agents in production. With good versioning, you can upgrade on your timeline, test new versions in staging, maintain multiple agent versions using different API versions, and plan migrations methodically. For teams building AI services, versioning is how you evolve your APIs without breaking every client that depends on you. It's the social contract that makes the API ecosystem functional instead of chaotic.

## The Core Idea
### What It Is
API versioning is a strategy for managing the lifecycle of an API as it evolves over time. When an API provider needs to add features, change behavior, remove deprecated functionality, or fix design flaws, they can't just modify the API and break all existing clients. Instead, they release a new version of the API alongside the old version, allowing clients to migrate gradually. Each version has an identifier (v1, v2, 2024-05-13) that clients use to specify which version they're calling.

Versioning exists on a spectrum from fine-grained (every endpoint can have different versions) to coarse-grained (entire API has one version). Most systems use coarse-grained versioning where the whole API advances together (v1 → v2 → v3), though individual endpoints within a version can be deprecated or added. The versioning scheme communicates meaning: semantic versioning (v2.3.1) signals the type of changes, date-based versioning (2026-05-13) indicates when the version was released.

API versioning encompasses several practices: **Version Identification** (how clients specify which version they want), **Compatibility Guarantees** (what changes are allowed within a version), **Deprecation Policies** (how long old versions remain supported), **Migration Paths** (how to upgrade from old to new versions), **Documentation** (clearly explaining differences between versions), and **Monitoring** (tracking which clients use which versions to inform sunset decisions).

For AI agent systems, versioning matters in two directions. As consumers, your agents need to handle versioned external APIs, specifying versions explicitly and planning upgrades. As providers, if you're building AI services (LLM APIs, agent orchestration platforms, tool services), you need versioning strategies so you can evolve without breaking customers' agents.

### What It Isn't
API versioning is **not** a license to break backward compatibility frequently. Good API design minimizes breaking changes through careful initial design, extensibility patterns, and additive evolution. Versioning is insurance for when breaking changes are unavoidable, not an excuse for careless API design. If you're releasing major versions every few months, the problem is your design process, not lack of versioning.

API versioning is **not** the same as software versioning. Your application might be at v5.2.1 with dozens of internal changes, but your API might stay at v2 for years if the contract hasn't changed. API versions are about external contracts, software versions are about internal implementation. They can evolve independently.

It's **not** sufficient to just slap version numbers on endpoints. Effective versioning requires comprehensive documentation explaining what changed between versions, migration guides showing how to upgrade, clear deprecation policies stating when old versions sunset, and active communication with API consumers about upcoming changes. Version numbers without context are useless.

API versioning is **not** free. Maintaining multiple API versions simultaneously means supporting multiple codebases, testing multiple versions, fixing bugs in multiple versions, and handling the operational complexity of routing requests to correct versions. Every version you support has maintenance cost. Eventually, old versions must be retired, which requires customer communication and migration support.

Finally, versioning **doesn't** solve all API evolution problems. Some changes (like removing entire core functionality) are so breaking that no versioning strategy makes them smooth. And version sprawl—supporting 10 different versions because customers won't upgrade—creates its own problems.

## How It Works
API versioning typically follows this lifecycle:

1. **Initial API Design (v1)**
   - Design API with forward compatibility in mind (extensible data structures, optional fields)
   - Publish comprehensive documentation and examples
   - Establish versioning strategy and deprecation policy upfront
   - Deploy v1 and begin onboarding clients

2. **Evolution Requirements Emerge**
   - Need to add new functionality (new endpoints, new fields)
   - Need to change behavior (different algorithm, different defaults)
   - Need to fix design mistakes (poor naming, inconsistent patterns)
   - Need to remove functionality (unused features, security risks)

3. **Assess Compatibility Impact**
   - **Non-breaking changes** (additive, backward compatible): Add new optional fields, add new endpoints, expand enum values with opt-in behavior
   - **Breaking changes** (require new version): Remove fields, change field types, change endpoint behavior, change required fields, rename endpoints
   - Decision: Can this change fit in current version, or does it require new version?

4. **Version Increment Decision**
   - **Patch increment** (v1.0.0 → v1.0.1): Bug fixes, security patches, no behavior changes
   - **Minor increment** (v1.0.0 → v1.1.0): Additive changes, new features, fully backward compatible
   - **Major increment** (v1.0.0 → v2.0.0): Breaking changes, redesigned APIs, compatibility broken
   - Communicate decision and timeline to API consumers

5. **Implementation of New Version**
   - Implement new version alongside old version (both run simultaneously)
   - Configure routing to direct requests to correct version based on identifier
   - Update [API Gateway](api_gateway.md) routing rules if using gateway pattern
   - Ensure monitoring differentiates between versions

6. **Version Identification Strategy** (how clients specify version):
   - **URI Path Versioning**: `/v1/customers` vs. `/v2/customers` (most common, explicit, cacheable)
   - **Query Parameter Versioning**: `/customers?version=2` (less common, more flexible)
   - **Header Versioning**: `Accept: application/vnd.myapi.v2+json` (cleaner URLs, less visible)
   - **Content Negotiation**: `Accept: application/json; version=2` (HTTP-native, complex)
   - Choose one strategy and use consistently across entire API

7. **Documentation and Communication**
   - Publish detailed changelog explaining differences between versions
   - Create migration guides with code examples showing how to upgrade
   - Annotate old version documentation with deprecation warnings
   - Communicate through developer newsletters, blog posts, dashboard notifications
   - Provide sandbox environments for testing new versions

8. **Deprecation Process**
   - Announce deprecation of old version with specific sunset date (6-12 months notice typical)
   - Mark deprecated endpoints with warnings in responses (headers, response metadata)
   - Monitor usage metrics to identify which clients still use old versions
   - Reach out directly to high-volume clients using deprecated versions
   - Provide migration support and incentives to upgrade

9. **Monitoring and Metrics**
   - Track API calls by version (volume, error rates, latency)
   - Identify clients still using old versions (user agents, API keys)
   - Monitor error rates when new versions launch (catch breaking changes quickly)
   - Dashboard showing version adoption over time
   - Alerts when old versions approach sunset but still have significant traffic

10. **Version Sunset**
    - Final warnings to remaining clients using old version
    - Disable old version endpoints (return 410 Gone or 404 Not Found)
    - Remove old version code from production
    - Archive old version documentation with historical reference
    - Reduce operational overhead by supporting fewer versions

## Think of It Like This
Think of API versioning like building codes and housing standards. When construction codes change—new electrical requirements, updated fire safety standards, different insulation rules—the city doesn't force everyone to immediately tear down and rebuild their homes. Instead, existing homes are "grandfathered in" under old codes (backward compatibility), but new construction must follow new codes. Over decades, as old buildings are renovated or demolished, the housing stock gradually transitions to newer standards. Homeowners can choose when to upgrade based on their needs and timeline. The building department maintains documentation for multiple code versions, provides transition guides, and eventually (after decades) stops supporting very old codes entirely.

Similarly, when you version an API, you're not forcing immediate upgrades. Clients using v1 continue working while new clients adopt v2. Over time, as clients migrate, v1 usage declines. Eventually, you "sunset" v1 (like retiring old building codes), but only after providing ample notice and migration support.

In our railway metaphor, API versioning is like operating different train gauges (track widths) on the same network. When the railway decides to standardize on a new gauge, they can't immediately tear up all old tracks—that would halt the entire system. Instead, they build new gauge tracks alongside existing ones, run trains on both simultaneously, gradually transition routes to the new gauge, and only retire old gauge tracks once all trains have migrated. During the transition, stations support both gauges (like an [API Gateway](api_gateway.md) routing to multiple API versions), timetables clearly indicate which gauge each route uses (like API documentation), and railway companies provide conversion equipment or replacement trains to help customers migrate (like migration guides and support).

## The "So What?" Factor
**If you version APIs properly:**
- You can evolve functionality without breaking existing clients
- Clients upgrade on their own schedules, reducing friction and resistance
- You maintain backward compatibility guarantees that build trust
- You can deprecate technical debt and design mistakes gradually
- You communicate changes clearly through version identifiers
- You maintain operational stability during transitions
- You collect metrics on version adoption to inform decisions

**If you don't version APIs (or version poorly):**
- Every API change risks breaking production systems for all clients simultaneously
- Clients fear updates and resist adopting new features
- You're stuck with design mistakes forever because fixing them breaks everyone
- Rapid changes create "integration hell" where nothing stays stable
- You have no visibility into which clients use which features
- Emergency breaking changes cause cascading failures across ecosystem
- Clients hard-code workarounds instead of trusting official APIs

## Practical Checklist
Before implementing API versioning, ask yourself:
- [ ] **What's my versioning scheme?** (Semantic versioning? Date-based? Simple v1/v2/v3? Choose one and document it)
- [ ] **How do clients specify versions?** (URI path? Header? Query param? Pick one method and use consistently)
- [ ] **What constitutes a breaking change in my API?** (Define clearly so you know when to increment major versions)
- [ ] **What's my deprecation policy?** (How long do I support old versions? 6 months? 12 months? Define before you need it)
- [ ] **How will I communicate changes?** (Changelog? Developer blog? Email notifications? Dashboard alerts?)
- [ ] **Can I make this change backward-compatible instead?** (Additive changes are better than breaking changes—explore alternatives first)
- [ ] **How will I monitor version adoption?** (Track which clients use which versions to inform sunset decisions)
- [ ] **Do I have migration guides ready?** (Code examples showing exactly how to upgrade from v1 to v2)

## Watch Out For
⚠️ **Version Sprawl:** Supporting too many versions simultaneously creates exponential maintenance burden. Each version needs testing, bug fixes, security patches, and monitoring. Establish sunset policies upfront and enforce them, or you'll end up supporting 10 versions indefinitely.

⚠️ **Inconsistent Versioning Across Endpoints:** If some endpoints are at v2 while others are still v1 within the same "version," clients get confused. Version the entire API cohesively, even if internally some modules haven't changed.

⚠️ **Surprise Breaking Changes:** Clients expect minor versions (v1.0 → v1.1) to be backward compatible. If you sneak breaking changes into minor releases, you destroy trust. Be disciplined about what changes go into which version increments.

⚠️ **Insufficient Deprecation Notice:** Announcing that v1 shuts down next month isn't enough time for clients to migrate, test, and deploy. Provide 6-12 months notice for major deprecations. Enterprise clients have slow release cycles.

⚠️ **Documentation Lag:** When v2 launches but documentation still shows v1 examples, clients can't migrate effectively. Keep documentation synchronized with version releases, showing examples for each supported version.

⚠️ **Ignoring Version Metrics:** If you don't track which clients use which versions, you're flying blind. You might sunset v1 thinking it's unused, then discover a critical client still depends on it. Monitor version adoption actively.

⚠️ **Over-Versioning:** Creating new major versions for trivial changes trains clients to ignore version numbers. Reserve major versions for genuinely significant changes. Use minor versions and additive evolution for routine improvements.

⚠️ **No Migration Path:** Saying "v1 is deprecated, use v2" without explaining how to migrate is unhelpful. Provide concrete migration guides with before/after code examples for common patterns.

## Connections
**Builds On:** 
- [REST API](rest_api.md) - The API contracts being versioned
- Software design principles - Backward compatibility, interface contracts, semantic meaning

**Works With:** 
- [API Gateway](api_gateway.md) - Gateways route requests to appropriate API versions
- [Monitoring](../Agent_Operations/monitoring.md) - Track version usage and adoption metrics
- [Integration Testing](../Testing_and_Evaluation/integration_testing.md) - Test multiple API versions for compatibility
- [Audit Trail](../Agent_Operations/audit_trail.md) - Record which versions clients used for historical analysis

**Leads To:** 
- API governance and standards
- Deprecation management
- Change management processes
- Client relationship management (communicating changes)
- Technical debt reduction (retiring old versions)

## Quick Decision Guide
**Use explicit API versioning when:**
- Your API is consumed by external clients you don't control
- Breaking changes are inevitable as your system evolves
- Multiple clients need different versions simultaneously
- You're building [AI agent services](../Agent_and_Orchestration/ai_agent.md) that others depend on
- You need to deprecate functionality gradually
- Your API has reached production maturity (v1.0+)

**Keep versioning simple when:**
- You have small number of known clients and can coordinate upgrades
- Your API is internal-only with tight version coupling between services
- You're in early development and expect rapid iteration
- The overhead of supporting multiple versions exceeds the benefit

**Versioning strategies by use case:**
- **High-stability enterprise APIs**: Semantic versioning (v2.1.0), long support windows (12+ months), comprehensive migration guides
- **Rapid-iteration startup APIs**: Simple v1/v2, shorter support windows (3-6 months), focus on additive changes
- **Third-party platform APIs** (AI model APIs, cloud services): Date-based versioning (2026-05-13), clear deprecation policies
- **Internal microservices**: Often skip versioning in favor of backward-compatible evolution and tight deployment coupling

## Further Exploration
- 📖 **"REST API Design Rulebook" by Mark Massé** - Chapter on API versioning strategies and tradeoffs
- 🎯 **Stripe API Versioning** - Exemplary case study of date-based versioning with excellent documentation
- 💡 **Semantic Versioning Specification (semver.org)** - Standard for version numbering and meaning
- 📖 **"Building Microservices" by Sam Newman** - Section on versioning in distributed systems
- 🎯 **Microsoft API Versioning Guidelines** - Enterprise patterns for REST API versioning
- 💡 **GitHub API Evolution** - How GitHub versions APIs and communicates deprecations
- 📖 **"API Design Patterns" by JJ Geewax** - Comprehensive patterns including versioning strategies

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*