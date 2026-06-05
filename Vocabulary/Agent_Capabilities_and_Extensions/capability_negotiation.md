# Capability Negotiation

## At a Glance
| | |
|---|---|
| **Category** | Pattern / Interoperability / Collaboration |
| **Complexity** | Intermediate |
| **Time to Learn** | 1–2 hours for basics; more for advanced negotiation protocols |
| **Prerequisites** | Understanding of agents, protocols, and capability models |

## One-Sentence Summary
Capability negotiation is the process by which agents, tools, or systems communicate and agree on which features, actions, or protocols to use for a given interaction, enabling dynamic, context-aware collaboration.

## Why This Matters to You
If you want your agents to work flexibly with diverse partners, adapt to changing environments, or support new features without breaking compatibility, you need capability negotiation. Without it, integrations are brittle, and agents may fail when encountering unknown or unsupported features. Negotiation enables robust, future-proof collaboration and smooth upgrades.

## The Core Idea
### What It Is
Capability negotiation is a protocol or pattern where agents or systems:
- Advertise their available features or supported protocols
- Discover the capabilities of their peers
- Agree on a common set of features or actions for the current interaction

This process can be static (at connection time) or dynamic (per request or session). It is essential for multi-agent systems, evolving APIs, and environments where not all parties have the same capabilities.

### What It Isn't
Capability negotiation is not hardcoded feature selection or manual configuration. It is not a replacement for versioning or compatibility layers; it complements them by enabling runtime adaptation. It is not about granting all capabilities—negotiation may result in a minimal, safe subset.

## How It Works
1. **Advertise Capabilities**: Each agent or system shares its supported features or protocols.
2. **Discover and Compare**: Peers exchange information and identify overlaps or gaps.
3. **Agree and Operate**: Select a mutually supported set of capabilities for the interaction.

## Think of It Like This
Capability negotiation is like two travelers comparing what languages they speak and agreeing to converse in the one they both know best.

## The "So What?" Factor
**If you use this:**
- Agents and systems collaborate flexibly and robustly
- Upgrades and new features can be adopted without breaking compatibility
- Integration is more resilient to change and diversity

**If you don't:**
- Integrations break when capabilities differ
- Upgrades and new features are hard to roll out
- Collaboration is limited to the lowest common denominator

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are all capabilities clearly advertised and documented?
- [ ] Is negotiation protocol robust and secure?
- [ ] Are fallbacks or minimal sets defined for critical interactions?

## Watch Out For
⚠️ Incomplete or misleading capability advertisements
⚠️ Negotiation deadlocks or failures due to protocol mismatch

## Connections
**Builds On:** [capability_model.md](capability_model.md), [protocol.md](protocol.md)
**Works With:** [capability_exposure.md](capability_exposure.md), [version_compatibility.md](version_compatibility.md)
**Leads To:** [multi-agent_system.md](../Agent_and_Orchestration/multi-agent_system.md), [system_evolution.md](../System_Architecture/system_evolution.md)

## Quick Decision Guide
**Use this when you need to:** Enable dynamic, context-aware collaboration between agents or systems
**Skip this when:** All parties share a fixed, known set of capabilities

## Further Exploration
- 📖 [Microsoft: Protocol and Capability Negotiation Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/protocol-adapter)
- 🎯 [OpenAI Cookbook: Agent Collaboration](https://github.com/openai/openai-cookbook#agent-collaboration)
- 💡 [IETF: Capability Negotiation in Protocols](https://datatracker.ietf.org/doc/html/rfc5939)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*
