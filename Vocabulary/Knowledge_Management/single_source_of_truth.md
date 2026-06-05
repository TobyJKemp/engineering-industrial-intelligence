# Single Source of Truth

## At a Glance
| | |
|---|---|
| **Category** | Data Architecture Principle |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours to understand, weeks to implement correctly |
| **Prerequisites** | data_consistency, information_architecture, version_control |

## One-Sentence Summary
Single Source of Truth (SSOT) is the practice of structuring information models and data architecture so that every piece of data is stored, edited, and maintained in exactly one authoritative location—eliminating conflicting duplicates and ensuring all systems reference the same accurate information.

## Why This Matters to You
When your AI agent makes a decision based on customer data, and your reporting system shows different customer data, and your billing system has yet another version—which one is correct? Without a Single Source of Truth, you're building on quicksand. SSOT means every system queries the same authoritative data source, so your autonomous agents, dashboards, and business logic all operate from identical facts. When debugging goes wrong, you're not chasing down which of five databases has the "real" answer. When your agent updates a record, every system sees that update immediately. SSOT transforms data chaos into data confidence—the foundation for reliable AI systems.

## The Core Idea
### What It Is
Single Source of Truth is an architectural principle that mandates each piece of information exists in exactly one authoritative, master location. All other references to that data are either direct queries to the source or calculated derivations with explicit provenance. When you need to know a customer's email address, there's one database table, one field, one record that holds the authoritative answer. Everything else points back to that source.

In AI agent systems and intelligent applications, SSOT becomes critical for consistency and reliability. Your RAG system retrieves documents from the knowledge base—that's the SSOT for domain knowledge. Your agents execute actions based on user profiles stored in a central identity system—that's the SSOT for user data. Your model configuration lives in a single configuration service—that's the SSOT for behavior parameters. When multiple agents, services, and humans all reference the same source, decisions remain consistent and auditable.

The implementation of SSOT involves careful data architecture decisions: identifying authoritative systems for each domain (customers in CRM, products in inventory, configurations in config service), establishing clear ownership and update protocols, providing universal access patterns (APIs, queries, event streams), and actively preventing unauthorized duplication. SSOT doesn't mean all data lives in one giant database—it means clear ownership and authoritative sources for each data domain.

In the context of knowledge management and repositories like Engineered Intelligence, SSOT means each concept, definition, or procedure is documented in exactly one canonical location. Other documents link to that canonical source rather than duplicating content. When you update the canonical definition of "vector database," that update propagates everywhere through links—you don't hunt down twenty documents that copied the definition.

### What It Isn't
SSOT is not the elimination of all copies or caches. Performance and availability often require replicas, caches, and derived datasets. The key is that these are explicitly recognized as copies—they're read-only, eventually consistent, and everyone knows which system is authoritative. Your Redis cache might hold customer data for speed, but everyone knows PostgreSQL is the SSOT. When conflicts arise, PostgreSQL wins.

It's also not centralization of all data into one system. SSOT is about logical authority, not physical location. You can have customer data in one service, product data in another, and order data in a third—each is the SSOT for its domain. The anti-pattern is having customer email addresses in five different systems with no clear authority about which is correct.

Finally, SSOT doesn't mean real-time global consistency across all systems. In distributed systems, you often have eventual consistency—replicas and caches catch up over time. SSOT means there's a clear authoritative source and a defined propagation mechanism. When your AI agent queries three seconds after an update, it might hit a stale cache, but the system knows the cache is stale and can refresh from the SSOT if required.

## How It Works
Implementing SSOT follows a systematic approach:

1. **Identify Data Domains**: Map out distinct types of information in your system—users, products, orders, configurations, documents, model parameters. Each domain needs a clear SSOT designation.

2. **Designate Authoritative Sources**: For each domain, explicitly choose the authoritative system. Customer profiles live in the identity service. Product catalog lives in the inventory system. Documentation lives in the knowledge repository. Make these designations explicit and documented.

3. **Establish Update Protocols**: Define who can update the SSOT and how. The identity service API is the only way to update user profiles. Pull requests are the only way to update canonical documentation. Configuration changes go through the config service. Block all backdoor updates.

4. **Provide Universal Access**: Make the SSOT accessible to all authorized systems. Expose APIs, publish event streams, provide query interfaces. Your AI agents, human users, and other services all access the same source through standard interfaces.

5. **Handle Derivations Explicitly**: When you create derived data (aggregations, summaries, embeddings), mark it clearly as derived and maintain traceability to the source. Your vector database holds embeddings derived from the document SSOT—and you know which document version was embedded.

6. **Prevent Unauthorized Duplication**: Actively discourage and prevent copying authoritative data into local stores. Use references, links, and queries instead of copies. When caching is necessary for performance, mark caches as non-authoritative and implement refresh mechanisms.

7. **Resolve Conflicts Automatically**: When conflicts arise (shouldn't happen in true SSOT, but distributed reality is messy), have explicit rules: SSOT always wins, timestamps determine freshness, or manual conflict resolution with clear escalation.

## Think of It Like This
Imagine a train dispatch center where the master schedule board shows which trains are where. Every station, conductor, and signal box references this master board to make decisions. When a train is delayed, the master board updates, and everyone sees the same information. Now imagine if each station kept its own separate schedule board, updating independently. Station A thinks Train 47 arrives at noon. Station B thinks 12:15. The train itself thinks 12:30. Chaos ensues—missed connections, conflicting signals, accidents.

The master dispatch board is your SSOT. Individual stations might have local displays (caches) that show the schedule, but everyone knows the dispatch center is authoritative. When displays conflict, you check the master board. That's SSOT in action—one truth, many views.

## The "So What?" Factor
**If you implement SSOT:**
- AI agents make decisions from consistent facts, eliminating contradictory behaviors
- Debugging is straightforward—you check the authoritative source, not hunt through duplicates
- Data quality improves because updates happen in one place with clear ownership
- Audit trails are clean—you can trace every decision back to the data it referenced
- System complexity reduces as you eliminate synchronization logic between duplicates
- Compliance is easier—you know exactly where sensitive data lives and who can access it

**If you don't:**
- Agents behave inconsistently because they're reading different versions of "truth"
- Data conflicts are constant—which system has the "real" customer email?
- Updates are unreliable—changing data in one place doesn't propagate everywhere
- Debugging is impossible—you can't reproduce issues because data differs between systems
- Data quality degrades as different copies drift out of sync
- Security vulnerabilities multiply as sensitive data spreads to unauthorized locations

## Practical Checklist
Before claiming you have SSOT, ask yourself:
- [ ] Can you identify the authoritative source for every critical data type? (no "it depends" answers)
- [ ] Do all systems query the authoritative source rather than maintaining local copies? (except explicit caches)
- [ ] Is there exactly one way to update each piece of authoritative data? (no backdoors)
- [ ] When data conflicts arise, is there automatic resolution that respects SSOT? (no manual reconciliation)
- [ ] Can you trace any derived data back to its authoritative source? (full provenance)
- [ ] Are SSOT designations documented and known to all developers and operators? (explicit knowledge)
- [ ] Do your AI agents have clear, consistent access to authoritative data sources? (no agent-specific data silos)

## Watch Out For
⚠️ **SSOT Theater**: Declaring one system as SSOT while still allowing updates through backdoor channels. If five different APIs can update customer data independently, you don't have SSOT—you have distributed chaos with better marketing.

⚠️ **Overly Rigid Centralization**: Forcing all data into one physical system for "SSOT compliance." SSOT is about logical authority, not physical consolidation. You can have domain-appropriate authoritative systems as long as ownership is clear.

⚠️ **Ignoring Caching Reality**: Pretending caches don't exist or treating them as SSOT violations. Modern systems need caches for performance. The key is marking caches as non-authoritative and implementing refresh mechanisms.

⚠️ **Version Confusion**: Treating the latest version as always correct. SSOT applies to specific versions—your AI agent needs to know which version of a document it retrieved. SSOT + version control = truth at a point in time.

⚠️ **Distributed System Denial**: Expecting instant global consistency in distributed systems. SSOT with eventual consistency is valid—you know the authoritative source and accept brief lag in propagation.

## Connections
**Builds On:** data_consistency, information_architecture, version_control, data_governance, schema_design

**Works With:** api_design, event_driven_architecture, caching_strategies, database_design, master_data_management, data_lineage, audit_trail, immutable_data

**Leads To:** data_mesh, domain_driven_design, microservices_architecture, eventual_consistency, distributed_systems, temporal_database

## Quick Decision Guide
**Use SSOT when you need to:** Ensure consistent data across multiple systems, support reliable AI agent decision-making, simplify debugging and auditing, maintain data quality, comply with regulations requiring data control, eliminate conflict resolution logic

**Skip SSOT when:** You're building a completely isolated system with no external references (rare), data is inherently subjective with multiple valid perspectives (opinions, preferences), you're prototyping and consistency doesn't matter yet (but fix before production)

## Further Exploration
- 📖 "Designing Data-Intensive Applications" by Martin Kleppmann - deep dive into consistency patterns
- 🎯 Study Master Data Management (MDM) practices for enterprise SSOT implementation
- 💡 Research Event Sourcing and CQRS as patterns that support SSOT with different read/write models
- 🔍 Explore Data Lineage tools that trace data from SSOT through transformations
- 🤖 Implement SSOT principles in your knowledge repository so AI agents access canonical definitions
- 📊 Study CAP theorem to understand trade-offs between consistency, availability, and partition tolerance in distributed SSOT

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*