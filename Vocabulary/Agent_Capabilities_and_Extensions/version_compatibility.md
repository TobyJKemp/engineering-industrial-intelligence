# Version Compatibility

## At a Glance
| | |
|---|---|
| **Category** | Integration Constraint |
| **Complexity** | Intermediate |
| **Time to Learn** | 1 hour |
| **Prerequisites** | Versioning and API/schema evolution basics |

## One-Sentence Summary
Version compatibility is the ability of components using different versions to interoperate correctly within defined expectations.

## Why This Matters to You
Systems evolve continuously, but operations cannot stop for every upgrade. Compatibility planning lets you ship improvements without breaking existing workflows. It reduces outage risk and supports staged migrations. In tool ecosystems, it is a key factor in long-term stability.

## The Core Idea
### What It Is
Compatibility defines which version combinations are supported and what behavior is guaranteed. It may include backward compatibility, forward compatibility, or negotiated capability subsets.

Strong compatibility policy includes testing matrices, deprecation windows, and communication standards. This helps teams coordinate upgrades safely.

### What It Isn't
Compatibility is not assuming "newer always works." Breaking changes are common without explicit policy.

It is also not only a semantic version label. Actual behavior and contracts must be verified.

## How It Works
1. Define supported version relationships and breaking-change criteria.
2. Test critical version combinations in CI and staging.
3. Publish migration paths and deprecation timelines.

## Think of It Like This
Think of ensuring old and new signaling equipment can coexist on shared tracks during phased upgrades.

## The "So What?" Factor
**If you use this:**
- You reduce upgrade-related incidents.
- You allow incremental migration across teams.
- You improve confidence in release planning.

**If you don't:**
- Upgrades become risky and often delayed.
- Mixed-version environments produce hard-to-debug failures.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are supported version ranges documented and discoverable?
- [ ] Are compatibility tests automated for key combinations?
- [ ] Is there a clear fallback for incompatible clients?

## Watch Out For
⚠️ Treating undocumented behavior as compatibility guarantee.
⚠️ Retaining obsolete compatibility layers indefinitely.

## Connections
**Builds On:** [protocol_versioning.md](protocol_versioning.md), [tool_lifecycle.md](tool_lifecycle.md)
**Works With:** [migration_path.md](migration_path.md), [tool_schema.md](tool_schema.md)
**Leads To:** [skill_versioning.md](skill_versioning.md), [tool_validation.md](tool_validation.md)

## Quick Decision Guide
**Use this when you need to:** Run mixed-version components without service disruption.
**Skip this when:** The system is single-version and upgraded atomically.

## Further Exploration
- [Semantic Versioning](https://semver.org/)
- [Backward compatibility patterns](https://martinfowler.com/articles/consumerDrivenContracts.html)
- [Release engineering practices](https://sre.google/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
