# Canonical Identifier

## At a Glance
| | |
|---|---|
| **Category** | Data Modeling Pattern |
| **Complexity** | Beginner |
| **Time to Learn** | 30 minutes |
| **Prerequisites** | Data modeling, unique keys |

## One-Sentence Summary
A canonical identifier is a unique, persistent reference assigned to an entity to ensure consistent identification across systems and contexts.

## Why This Matters to You
Canonical identifiers prevent confusion, duplication, and errors when integrating data from multiple sources. They make it possible to reliably link, merge, and track entities—critical for building robust knowledge graphs, ontologies, and distributed AI systems. Without them, data silos and mismatches are almost inevitable.

## The Core Idea
### What It Is
A canonical identifier is a single, authoritative ID (such as a URI, UUID, or database key) that represents an entity regardless of where or how it appears. It enables consistent referencing, deduplication, and integration across databases, APIs, and knowledge systems.

Canonical identifiers are foundational for interoperability, data lineage, and semantic integration.

### What It Isn't
A canonical identifier is not just any label or name—it must be unique, persistent, and agreed upon as the “source of truth.” It’s not a synonym or alias, and it’s not meant to change over time.

## How It Works
1. **Assign:** Designate a unique, persistent ID for each entity.
2. **Reference:** Use the canonical ID in all systems and integrations.
3. **Resolve:** Map alternative IDs or aliases to the canonical identifier as needed.

## Think of It Like This
Think of a passport number: no matter where you travel, it uniquely identifies you, even if your name is common or changes.

## The "So What?" Factor
**If you use this:**
- You avoid duplicate or conflicting records.
- You enable seamless data integration and linking.
- You support traceability and auditability.

**If you don't:**
- Data silos and mismatches proliferate.
- Integrations become error-prone and costly.
- Entity tracking and governance are weakened.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are identifiers globally unique and persistent?
- [ ] Is there a clear process for assigning and resolving IDs?
- [ ] Are alternative IDs mapped to the canonical form?

## Watch Out For
⚠️ Changing or reusing identifiers can break integrations.
⚠️ Lack of governance can lead to ID collisions or ambiguity.

## Connections
**Builds On:** [identity_resolution.md](identity_resolution.md), [uri_strategy.md](uri_strategy.md)
**Works With:** [entity_resolution.md](entity_resolution.md), [ontology_alignment.md](ontology_alignment.md)
**Leads To:** [data_lineage.md](data_lineage.md), [knowledge_graph_quality.md](knowledge_graph_quality.md)

## Quick Decision Guide
**Use this when you need to:** Integrate, link, or track entities across systems.
**Skip this when:** Data is isolated, simple, or not shared externally.


## Quick Decision Guide

Use this concept when:
- You need to model knowledge
- You're building semantic systems
- You need consistency and rigor

## Further Exploration

- 📖 **Best Practices** — domain-specific operating practices and decision rules
- 🎯 **Implementation Template** — sequence of implementation steps with ownership and checkpoints
- 💡 **Success Case Study** — a concrete scenario where this improved outcomes
- 💡 **Failure Case Study** — a concrete scenario where poor use caused issues
- 🔍 **Research** — key research directions and evidence to review

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*


