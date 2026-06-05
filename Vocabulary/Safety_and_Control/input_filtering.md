# Input Filtering

## At a Glance
| | |
|---|---|
| **Category** | Technique |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 hours |
| **Prerequisites** | Basic understanding of AI agents, prompt engineering, security concepts |

## One-Sentence Summary
Input filtering is the practice of validating, sanitizing, and screening user inputs before they reach an AI system, acting as a protective barrier against malicious prompts, injection attacks, inappropriate content, and inputs that could cause the AI to behave unsafely or unexpectedly.

## Why This Matters to You
Your AI agent accepts text from users, and some of those users will try to break it—intentionally or accidentally. Without input filtering, attackers can inject malicious instructions that override your system prompts, extract sensitive information, generate harmful content, or cause your agent to take unintended actions. Even well-meaning users might paste in problematic content that confuses your agent or triggers expensive API calls. Input filtering is your first line of defense, the bouncer at the door who checks everyone before they enter. Skip it, and you're inviting chaos into your carefully engineered system.

## The Core Idea
### What It Is
Input filtering is a security and safety mechanism that examines every piece of user-supplied data before it's processed by your AI system. Think of it as a screening checkpoint that evaluates inputs against a set of rules, patterns, and policies to determine whether they're safe, appropriate, and properly formatted. The filtering process can reject inputs entirely, modify them to remove problematic elements, or flag them for additional scrutiny.

Input filtering operates at multiple levels. At the most basic level, it performs syntax validation—checking that inputs conform to expected formats, lengths, and character sets. At a more sophisticated level, it looks for semantic patterns associated with attacks, such as prompt injection attempts, jailbreak techniques, or requests for prohibited content. Advanced filtering systems use machine learning models to detect adversarial inputs that might slip past rule-based filters.

The goal isn't to block all unexpected inputs—that would make your system unusably rigid—but rather to intercept inputs that pose genuine risks while allowing legitimate, creative use. Good input filtering strikes a balance between security and usability, catching attacks without creating frustrating false positives that block normal users.

### What It Isn't
Input filtering is **not** a complete security solution by itself. It's one layer in a defense-in-depth strategy, working alongside output filtering, guardrails, rate limiting, and monitoring. Attackers constantly develop new techniques to bypass filters, so relying solely on input filtering is like having a great front door lock but no walls—eventually, someone finds a way around it.

Input filtering is **not** censorship or content moderation, though they're related. Filtering focuses on preventing the AI system from being exploited or behaving dangerously, not on enforcing editorial policies about acceptable speech. While you might use similar techniques for both, they serve different purposes: filtering protects system integrity, while moderation enforces community standards.

It's also **not** infallible. No filter catches 100% of malicious inputs while allowing 100% of legitimate ones. Attackers use encoding tricks, linguistic obfuscation, and adversarial techniques specifically designed to evade detection. Input filtering makes attacks harder and catches unsophisticated attempts, but determined adversaries may still find ways through—which is why layered defenses matter.

## How It Works
Input filtering typically operates in stages, creating multiple checkpoints that inputs must pass:

1. **Basic Validation**
   - Length checks: Reject inputs that are too long (token limits, DoS prevention) or suspiciously short
   - Character set validation: Ensure inputs use expected encoding (UTF-8, ASCII)
   - Format validation: Check that structured inputs (JSON, XML) are well-formed
   - Type checking: Verify data types match expectations (numbers are numeric, dates are valid)

2. **Pattern-Based Filtering**
   - Blocklist matching: Scan for known malicious patterns, phrases, or injection signatures
   - Regular expression filters: Detect suspicious structures (repeated instructions, role-playing attempts)
   - Keyword detection: Flag inputs containing prohibited terms or commands
   - Syntax analysis: Identify attempts to break out of intended context (special characters, delimiters)

3. **Semantic Analysis**
   - Intent classification: Determine what the user is trying to accomplish
   - Prompt injection detection: Identify attempts to override system instructions ("Ignore previous instructions...")
   - Jailbreak detection: Recognize role-play scenarios designed to bypass safety guardrails
   - Adversarial input detection: ML models trained to spot adversarially crafted inputs

4. **Policy Enforcement**
   - Content policy checks: Ensure inputs don't request prohibited content (violence, illegal activities, private data)
   - Rate limiting integration: Track per-user input patterns for abuse detection
   - Allowlist verification: For high-security contexts, only permit explicitly approved input types
   - Risk scoring: Assign risk levels and route high-risk inputs to human review

5. **Sanitization and Transformation**
   - Escaping special characters: Neutralize characters that have special meaning
   - Normalization: Convert to standard formats (Unicode normalization, case folding)
   - Stripping: Remove potentially dangerous elements while preserving safe content
   - Encoding: Transform inputs to prevent interpretation as code or commands

## Think of It Like This
Imagine your AI system is a high-security building, and user inputs are visitors arriving at the front entrance. Input filtering is the security checkpoint in the lobby. Every visitor must pass through metal detectors, show ID, and have their bags screened. Most people pass through smoothly—the security team isn't there to hassle legitimate visitors. But someone trying to sneak in weapons, fake credentials, or prohibited materials gets stopped at the door, long before they can access the building's sensitive areas.

The security guards (your filtering logic) have a checklist: Does this person match expected visitor profiles? Are they carrying anything suspicious? Have they been flagged before? Some decisions are automatic (metal detector goes off = no entry). Others require judgment (this person's behavior is unusual, let's watch them closely). The goal isn't to make the building a fortress that no one can enter—it's to keep out the troublemakers while welcoming everyone else.

In our railway metaphor, input filtering is the track inspection team that examines the condition of incoming rail cars before they're coupled into the train. They check for structural defects, hazardous materials not properly secured, or tampered cargo that could derail the train or damage other cars. Most cargo passes inspection and continues smoothly, but anything unsafe is rejected at the yard entrance before it endangers the entire operation.

## The "So What?" Factor
**If you use this:**
- **Attack prevention:** Block prompt injection, jailbreak attempts, and adversarial inputs before they compromise your AI
- **Cost control:** Reject malformed or excessively long inputs that would waste API tokens and computational resources
- **Compliance assurance:** Enforce policies about prohibited content and use cases before processing begins
- **Reduced downstream issues:** Catch problems early rather than dealing with consequences after the AI processes bad inputs
- **Audit trail:** Log filtered inputs to understand attack patterns and improve defenses over time

**If you don't:**
- **Prompt injection succeeds:** Attackers override your system instructions and make your AI do things you never intended
- **Data exfiltration:** Users trick your AI into revealing training data, system prompts, or sensitive information
- **Harmful outputs:** Your AI generates dangerous, illegal, or reputationally damaging content because it processed a malicious prompt
- **Resource exhaustion:** Malformed inputs cause crashes, infinite loops, or expensive processing that drains your budget
- **Regulatory violations:** Unfiltered inputs lead to outputs that violate laws or compliance requirements
- **Loss of user trust:** When your AI behaves erratically or unsafely due to unchecked inputs, users lose confidence in the system

## Practical Checklist
Before implementing input filtering, ask yourself:
- [ ] **What are the most critical threats to my system?** (Prioritize filters for your biggest risks: prompt injection, data exfiltration, harmful content generation)
- [ ] **What defines a "valid" input for my use case?** (Be specific about expected formats, lengths, and content so you can filter deviations)
- [ ] **How will I handle false positives?** (When legitimate users get blocked, do they get helpful error messages? A way to appeal?)
- [ ] **Am I filtering at the right layer?** (Client-side, API gateway, or within the AI application? Defense in depth uses multiple layers)
- [ ] **How will I keep filters updated?** (New attack techniques emerge constantly—plan for ongoing filter maintenance)
- [ ] **What gets logged when inputs are filtered?** (Capture enough detail to understand attacks without logging sensitive user data)
- [ ] **Have I tested against known attack patterns?** (Use public jailbreak and injection datasets to validate filter effectiveness)

## Watch Out For
⚠️ **Over-Filtering (False Positives):** If your filters are too aggressive, you'll block legitimate users and create frustration. A filter that blocks 100% of attacks but also 20% of normal users is worse than one that blocks 90% of attacks with 1% false positives. Test extensively with real user inputs.

⚠️ **Under-Filtering (False Negatives):** Attackers constantly develop new evasion techniques—Unicode tricks, Base64 encoding, linguistic obfuscation, token smuggling. Your filters need to evolve. What works today might be obsolete in three months.

⚠️ **Performance Impact:** Complex filtering logic (especially ML-based semantic analysis) adds latency to every request. If filtering takes 500ms and your users expect sub-second responses, you've got a problem. Profile your filters and optimize hot paths.

⚠️ **Attacker Adaptation:** Once attackers learn what your filters catch, they'll craft inputs specifically to evade them. Security through obscurity doesn't work—assume attackers will probe your filters systematically to find gaps.

⚠️ **Context Loss:** Aggressive sanitization might strip away important context or nuance from user inputs, causing the AI to misunderstand legitimate requests. Balance safety with preserving user intent.

⚠️ **Maintenance Burden:** Filter rules multiply over time as you patch each discovered vulnerability. Without regular refactoring, you'll end up with thousands of brittle rules that are hard to maintain and create unexpected interactions.

⚠️ **Compliance vs. Usability:** Legal and regulatory requirements might demand strict filtering that reduces usability. Document these tradeoffs explicitly so stakeholders understand why certain restrictions exist.

## Connections
**Builds On:** 
- [Prompt Engineering](../Foundational_AI%20&%20ML/prompt_engineering.md) - Understanding prompts helps you recognize malicious prompt patterns
- [Token](../Foundational_AI%20&%20ML/token.md) - Input length and structure validation relates to tokenization

**Works With:** 
- [Guardrails](../Safety_and_Control/guardrails.md) - Input filtering is one type of guardrail operating at the entry point
- [Human-in-the-Loop](../Safety_and_Control/human-in-the-loop.md) - High-risk filtered inputs can be routed to human review instead of auto-rejection
- [Audit Trail](../Agent_Operations/audit_trail.md) - Filtered inputs should be logged for security monitoring and analysis
- [Observability](../System_Patterns/observability.md) - Monitoring filter performance and attack patterns over time

**Leads To:** 
- Output Filtering - Screening AI-generated content before delivery to users
- Adversarial ML - Techniques for detecting and defending against adversarial inputs
- Security Monitoring - Aggregating filter logs to detect systematic attacks or abuse patterns
- Red Teaming - Testing your filters against sophisticated attack techniques

## Quick Decision Guide
**Use this when you need to:**
- Accept user-generated inputs in any AI system (this is basically always—filtering is a baseline security practice)
- Protect against prompt injection, jailbreak attempts, and adversarial inputs
- Enforce content policies or regulatory compliance requirements
- Control costs by rejecting malformed or excessively resource-intensive inputs
- Build trust by demonstrating that your system has security controls in place

**Skip this when:**
- Your AI system processes only trusted, pre-validated inputs from controlled sources (rare—and even then, defense in depth suggests light filtering)
- The cost of implementing filtering exceeds the risk of unfiltered inputs (extremely low-stakes, experimental systems)
- You're in early prototyping phase and need to move fast (but add it before any production deployment)

## Further Exploration
- 📖 OWASP Top 10 for LLMs - Industry-standard framework for AI security risks, with extensive coverage of input attacks
- 🎯 PromptArmor and similar libraries - Open-source tools for prompt injection detection
- 💡 "Adversarial Robustness in ML" (Goodfellow et al.) - Academic foundations of detecting adversarial inputs
- 🔬 Jailbreak chat datasets - Public collections of jailbreak attempts to test your filters against
- 🏛️ Azure AI Content Safety - Commercial API demonstrating enterprise-grade input filtering
- 📊 Lakera's prompt injection research - Ongoing research into new attack vectors and detection techniques

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*