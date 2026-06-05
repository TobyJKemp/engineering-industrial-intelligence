# Organizational Sense Making

## At a Glance
| | |
|---|---|
| **Category** | Cognitive/Social Process |
| **Complexity** | Advanced |
| **Time to Learn** | 6-10 hours for concepts; ongoing practice to master |
| **Prerequisites** | Understanding of organizational dynamics, communication patterns |

## One-Sentence Summary
Organizational sense making is the collective process by which groups of people interpret ambiguous situations, construct shared understanding, and decide on coordinated action—essential for AI system development where teams must collectively make sense of complex technical failures, interpret ambiguous model behaviors, align on architectural decisions, and build shared mental models of systems too complex for any individual to fully comprehend, with the quality of organizational sense making directly determining whether teams build coherent systems or fragmented pieces that fail to integrate.

## Why This Matters to You
When building AI systems, individual technical expertise isn't enough—teams must collectively make sense of complex, ambiguous situations where no single person has complete understanding. Your ML model fails in production: is it data drift, concept drift, infrastructure issues, or adversarial inputs? The team must collectively interpret symptoms, share observations, build hypotheses, and converge on diagnosis. Your RAG system retrieves wrong documents: is it embedding quality, chunking strategy, query formulation, or index configuration? The team debates, tests, and constructs shared understanding. Your agent behaves unexpectedly: is it prompt engineering, tool selection, reasoning chain, or context window management? Multiple perspectives must be synthesized into coherent explanation. Organizational sense making is how teams move from confusion to clarity, from individual interpretations to shared understanding, from scattered observations to coherent action. Poor sense making creates dysfunctional patterns: different team members operating on contradictory assumptions, debates that don't converge, repeated investigation of already-understood issues, and decisions made without incorporating all relevant perspectives. Good sense making creates high-performing teams: rapid convergence on problems, efficient knowledge sharing, collective learning from incidents, and decisions grounded in shared reality. In AI development where complexity exceeds individual cognitive capacity, organizational sense making is the mechanism that enables teams to be collectively smarter than any individual member. When your AI system has a production incident at 2 AM, sense making quality determines whether the team quickly identifies root cause and fixes it, or spends hours in confusion with different people pulling in contradictory directions. When architecting a new agent system, sense making determines whether the team converges on coherent design or builds components based on divergent mental models that fail to integrate. The technical challenges of AI are hard enough; teams that can't collectively make sense of those challenges multiply difficulty unnecessarily.

## The Core Idea
### What It Is
Organizational sense making, developed primarily by organizational theorist Karl Weick, is the collaborative process through which people in organizations notice, interpret, and construct meaning from ambiguous or unexpected events, then use that shared understanding to coordinate action. Unlike individual problem-solving (one person thinking through an issue), sense making is fundamentally social—meaning emerges through interaction, dialogue, and negotiation among multiple people with different perspectives and knowledge.

Sense making occurs in seven key activities:

**Noticing and Bracketing**: Groups collectively identify that something requires attention—an anomaly, failure, unexpected behavior, or opportunity. Not everything gets noticed; organizational attention is limited. Sense making begins when someone brackets an event as significant and worthy of interpretation. In AI systems: a model's accuracy drops, an agent produces bizarre output, a system fails under load. Bracketing: "This is important, we need to understand it."

**Retrospective Interpretation**: Groups make sense of what has happened by constructing narratives that explain observed events. This is retrospective—you can't make sense of something before it happens, only after. Teams review logs, examine data, discuss symptoms, and build stories: "Here's what we think occurred." In AI development: post-mortems after incidents, analyzing failed experiments, understanding why a model behaves unexpectedly.

**Multiple Perspectives**: Different team members bring different interpretations based on their roles, expertise, and past experiences. Data scientists see different things than infrastructure engineers; product managers notice different patterns than ML engineers. Sense making synthesizes these perspectives rather than having one "expert" dominate. The richness comes from diversity of interpretation.

**Social Construction**: Understanding isn't discovered (it existed waiting to be found); it's constructed through dialogue. Teams talk, debate, propose explanations, test them against evidence, and iteratively build shared mental models. This is social—meaning emerges from interaction, not individual reflection. Slack threads, incident channels, design discussions, architecture reviews are all venues for sense making.

**Identity and Plausibility**: People make sense through the lens of who they are and what seems plausible given their experience. An infrastructure engineer makes sense differently than a researcher. Sense making doesn't require "truth" or "correctness"—it requires plausibility (does this make sense given what we know?) and utility (does this help us act?). Multiple plausible interpretations can coexist until action forces commitment.

**Enactment**: Sense making isn't passive observation; the act of investigating and interpreting changes the situation. When debugging an AI system, the debugging process itself affects system state. When discussing architectural decisions, the discussion shapes what gets built. Sense making and action are intertwined—you make sense to act, and acting reveals more to make sense of.

**Ongoing Process**: Sense making never completely "finishes." You develop working understanding sufficient to act, then continue refining as you learn more. Unlike analysis (gather all data, reach conclusion), sense making is continuous updating. Yesterday's sense may be superseded by today's new information. AI systems are dynamic; sense making must be too.

In AI system development, sense making manifests in multiple contexts:

**Incident Response**: When production systems fail, distributed teams must quickly make sense: what failed, why, what's the impact, how to recover? Time pressure, incomplete information, and high stakes make this challenging. Effective sense making means rapid convergence on actionable understanding.

**Architectural Decisions**: Designing AI systems involves ambiguous tradeoffs with no clearly correct answers. Teams must collectively make sense of: requirements (often unclear or conflicting), technical constraints, architectural patterns, and implementation approaches. Good sense making produces coherent designs; poor sense making produces fragmented systems.

**Model Behavior Understanding**: ML models are black boxes that exhibit complex, sometimes unexpected behaviors. Teams must collectively interpret: why did the model make that prediction? Why does performance degrade on certain inputs? How does the model actually work? Sense making builds shared mental models of model behavior.

**Strategic Planning**: Deciding what AI systems to build, how to prioritize, what approaches to take requires sense making about: business needs, technical feasibility, competitive landscape, and resource constraints. Groups must construct shared understanding to align on direction.

**Learning from Failure**: When experiments fail, models underperform, or systems behave unexpectedly, teams must collectively make sense of why and what to do differently. This learning is organizational—it's not enough for one person to understand; the team must develop shared understanding.

### What It Isn't
Organizational sense making is not the same as problem-solving or rational decision-making. Problem-solving assumes a defined problem with discoverable solutions; sense making operates in situations where the problem itself is ambiguous and must be constructed. Rational decision-making assumes you can gather complete information, analyze options, and choose optimally; sense making acknowledges that you work with incomplete information, multiple interpretations, and must act before full understanding.

Sense making is also not consensus-building or agreement. Groups can make sense successfully while maintaining different interpretations. The goal isn't everyone agreeing on one truth, but developing sufficient shared understanding to coordinate action. You don't need identical mental models, just compatible ones that enable working together.

Sense making isn't purely logical or analytical. Emotions, politics, power dynamics, and social relationships all influence how groups make sense. A junior engineer's insight might be dismissed not because it's wrong, but because of status dynamics. An exec's interpretation might dominate not because it's best-supported, but because of authority. Understanding sense making requires acknowledging these social realities.

Sense making is also not a structured process or methodology. There's no "sense making framework" with defined steps that guarantee good outcomes. It's an emergent social process influenced by: who participates, how they interact, what information is available, time pressure, organizational culture, and countless other factors. You can create conditions that support good sense making, but you can't mechanize it.

Finally, sense making doesn't produce absolute truth or certainty. It produces plausible, useful working interpretations that enable action under conditions of ambiguity. Those interpretations may later prove incomplete or wrong—that's normal. The test isn't "is this interpretation true?" but "is it sufficient to act on and learn from?"

## How It Works
Supporting effective organizational sense making involves creating conditions and practices that enable collective interpretation:

1. **Create Shared Context**: Sense making requires common ground. Document: system architecture, key decisions and rationale, known issues and patterns, operational metrics and baselines. This shared context provides foundation for interpretation. When incidents occur, teams with shared context converge faster because they start from common understanding.

2. **Establish Communication Channels**: Designate venues for sense making. Dedicated Slack channels for incidents, architecture discussions, or specific projects. Regular meetings (stand-ups, retrospectives, design reviews) where sense making happens. Tools that capture sense making artifacts (incident timelines, decision logs, architecture diagrams). Make sense making visible and accessible.

3. **Include Diverse Perspectives**: Invite multiple viewpoints into sense making. When debugging production issues, include: operators (what they observed), engineers (what the code does), data scientists (what the models show), and product (what users experience). Different perspectives reveal different aspects. Cognitive diversity improves sense making quality.

4. **Encourage Narrative Building**: Let people tell stories about what they think happened. Stories are how humans make sense—they have temporal structure, causation, and context that lists of facts lack. In incident response: "I think what happened is..." In design discussions: "Here's how I see this working..." Narratives make abstract technical details concrete and comprehensible.

5. **Make Thinking Visible**: Externalize mental models so others can see and engage with them. Draw diagrams, write hypotheses on whiteboards, sketch system flows, create decision matrices. When thinking is visible, groups can collectively examine, refine, and align it. Hidden mental models can't be shared or improved.

6. **Test Interpretations Against Evidence**: Good sense making involves hypothesis testing. Team proposes explanation, then checks: "If that's true, we'd expect to see X in the logs." Look for X. Found it? Interpretation strengthened. Didn't find it? Revise interpretation. Grounding sense making in evidence prevents purely speculative explanations.

7. **Allow Time for Convergence**: Sense making takes time. Rushing to conclusions before collective understanding develops produces poor decisions. In high-pressure situations (production incidents), time is limited—but even there, 10 minutes of collective sense making beats 10 people immediately acting on different interpretations. Build in explicit time for sense making.

8. **Document Sense Making Artifacts**: Capture outcomes of sense making processes. Incident post-mortems document how teams made sense of failures. Architecture Decision Records capture sense making around design choices. Meeting notes preserve discussions and rationales. These artifacts enable future sense making by providing context for later decisions.

9. **Embrace Ambiguity Initially**: Early in sense making, ambiguity and multiple interpretations are normal. Don't force premature convergence. Allow space for: "We're not sure yet," "Here are three possible explanations," "More investigation needed." Premature closure on wrong interpretation is worse than maintaining productive ambiguity.

10. **Recognize Power Dynamics**: Be aware that authority, seniority, and expertise influence whose interpretations get heard and taken seriously. Create space for junior voices, alternative perspectives, and dissenting views. The quietest person might have the critical insight. Good facilitation manages power dynamics to enable better collective sense making.

11. **Learn from Sense Making**: Meta-sense making—making sense of how you make sense. After major incidents or decisions, reflect: How did our sense making process go? What helped us converge quickly? What created confusion? Where did we get stuck? Improving sense making capability is organizational learning.

12. **Build Psychological Safety**: People must feel safe proposing interpretations that might be wrong, asking "stupid" questions, admitting confusion, and challenging prevailing views. Without psychological safety, sense making becomes performance (looking smart) rather than genuine collective interpretation. Fear kills sense making quality.

## Think of It Like This
Imagine a team of detectives investigating a complex crime scene. No single detective sees everything—one notices the broken window, another finds footprints, a third discovers a discarded receipt. Each detective has theories based on what they've observed and their expertise (forensics, psychology, technology).

They gather to collectively make sense:
- Share observations: "I found X," "I noticed Y"
- Propose interpretations: "I think it means Z"
- Test against evidence: "If that's right, we'd expect to see W"
- Debate and refine: "But that doesn't explain..."
- Build a coherent narrative: "Here's what we think happened"

No single detective has the complete picture. The "truth" emerges through collective interpretation of ambiguous evidence. Different detectives see different things based on where they looked and their expertise. The team's shared understanding enables coordinated action—they know where to investigate next and what they're looking for.

Organizational sense making in AI development is similar. Complex systems fail in ambiguous ways. Multiple team members observe different symptoms. Through discussion, they collectively construct understanding: "Here's what we think is happening and why." That shared interpretation enables coordinated response.

The quality of sense making determines investigation speed and solution quality—teams that can rapidly converge on accurate-enough interpretations outperform teams that argue inefficiently or operate on divergent understandings.

## The "So What?" Factor
**If teams develop strong sense making capabilities:**
- Complex problems are diagnosed faster—shared interpretation from diverse perspectives
- Architectural decisions are more coherent—alignment on mental models before building
- Incidents are resolved efficiently—teams converge quickly on root cause and action
- Knowledge stays organizational—shared understanding persists beyond individual memory
- New team members onboard faster—existing sense making artifacts provide context
- Learning from failure is effective—collective interpretation of what went wrong
- Strategic alignment is stronger—shared understanding of direction and rationale
- Coordination overhead is lower—compatible mental models enable efficient collaboration

**If teams lack sense making capabilities:**
- Problems persist despite investigation—teams can't collectively interpret symptoms
- Architectural designs are fragmented—different components built on incompatible assumptions
- Incidents drag on—people operate on divergent theories, pulling in different directions
- Knowledge is siloed—individuals understand pieces but no shared organizational understanding
- Onboarding is painful—no artifacts capturing how the organization makes sense of systems
- Teams repeat mistakes—failures aren't collectively understood, so lessons don't stick
- Strategic confusion prevails—different groups have different interpretations of direction
- Coordination costs escalate—constant negotiation needed because mental models don't align

## Practical Checklist
To assess and improve organizational sense making, verify:
- [ ] Are there explicit venues for collective sense making (channels, meetings, forums)?
- [ ] Is diverse participation encouraged in sense making processes?
- [ ] Are sense making artifacts documented (post-mortems, ADRs, design docs)?
- [ ] Is shared context maintained (architecture docs, system overviews, baselines)?
- [ ] Do people feel safe proposing interpretations that might be wrong?
- [ ] Is time allowed for collective interpretation before action?
- [ ] Are mental models made visible (diagrams, written hypotheses, sketches)?
- [ ] Are interpretations tested against evidence rather than accepted on authority?
- [ ] Are power dynamics managed to hear all perspectives?
- [ ] Is ambiguity tolerated initially before forcing convergence?
- [ ] Does the team learn from sense making successes and failures?
- [ ] Can you trace major decisions back to the sense making that produced them?

## Watch Out For
⚠️ **Premature Convergence**: Rushing to interpretation before adequate collective sense making occurs. Under time pressure or need for action, teams jump to conclusions: "It's obviously X, let's fix it." But "obvious" to one person isn't obvious to others, and quick consensus often forms around wrong interpretations. Premature convergence leads to fixing wrong problems or implementing solutions that don't address root causes. Allow sufficient time for collective interpretation even under pressure.

⚠️ **Dominant Voice Bias**: Letting one person's interpretation dominate because of authority, seniority, expertise, or communication style. The CTO says "I think it's Y" and others defer rather than offering alternative interpretations. The most confident person drives interpretation even if others have doubts. This silences valuable perspectives and produces impoverished sense making. Good facilitation ensures all voices are heard and considered.

⚠️ **Narrative Fixation**: Becoming attached to initial interpretations and filtering new information to fit rather than updating understanding. Team decides "it's a data quality issue" and then interprets all subsequent evidence through that lens, missing contradictory signals. Confirmation bias at organizational level. Good sense making maintains openness to revising interpretations as new information emerges.

⚠️ **Missing Context**: Attempting sense making without adequate shared foundation. New team members in design discussions lack context about previous decisions, system constraints, or organizational history. Their sense making is handicapped by missing knowledge that others take for granted. Provide context actively: "Here's the background..." "Previously we decided..." "The constraint we're working under is..."

⚠️ **Undiscussable Topics**: Some interpretations are politically dangerous or threaten powerful stakeholders, so teams avoid them even if plausible. "We can't say the problem is poor product requirements even though we all think that." Organizational taboos limit sense making quality. Create safety for uncomfortable interpretations to be raised and examined.

⚠️ **Documentation Gaps**: Failing to capture sense making artifacts means future decisions lose context and understanding doesn't persist. Six months later: "Why did we design it this way?" Nobody remembers the sense making that led to that decision. Document: the problem as understood, alternatives considered, rationale for choices, known tradeoffs. Future sense making builds on past sense making only if artifacts exist.

## Connections
**Builds On:** 
- [Mental Model](mental_model.md) - Individual mental models that get synthesized
- [Tribal Knowledge](tribal_knowledge.md) - Often captured through sense making
- [Information Architecture](information_architecture.md) - Structure that enables sense making

**Works With:** 
- [Digital Transformation](digital_transformation.md) - Requires collective sense making about change
- [Change Management](change_management.md) - Managing sense making during transitions
- [Decision Framing](decision_framing.md) - How problems get framed for sense making
- [Discourse Mapping](discourse_mapping.md) - Capturing sense making conversations
- [Feedback Loops](feedback_loops.md) - Sense making from operational feedback
- [Perspective Decomposition](perspective_decomposition.md) - Breaking down viewpoints in sense making
- [Strategic Foresight](strategic_foresight.md) - Collective sense making about future

**Leads To:** 
- [Organizational Learning](organizational_learning.md) - Sense making enables learning
- [Knowledge Transfer](knowledge_transfer.md) - Sharing sense making outcomes
- [Collaborative Problem Solving](collaborative_problem_solving.md) - Acting on shared sense
- [Adaptive Organizations](adaptive_organizations.md) - Organizations that make sense well adapt better

## Quick Decision Guide
**Invest in sense making capabilities when:**
- Building complex AI systems requiring coordination across specialized roles
- Operating distributed teams that must align without co-location
- Facing ambiguous technical challenges with no clear solutions
- Experiencing repeated failures or persistent problems
- Onboarding new team members frequently
- Strategic direction is unclear or contested
- Different groups have conflicting interpretations of situations
- Incident response is slow and inefficient
- Architectural coherence is lacking
- Organizational learning from mistakes is weak

**Rely on individual expertise when:**
- Problems are well-defined with known solutions
- Single expert has complete context and authority
- Time pressure is extreme and coordination overhead unaffordable
- Issues are purely technical with minimal ambiguity
- Stakes are low and mistakes are easily reversible
- Team size is very small (2-3 people with shared context)

## Further Exploration
- 📖 [Sensemaking in Organizations](https://www.amazon.com/Sensemaking-Organizations-Foundations-Organizational-Science/dp/0803971779) by Karl Weick - Foundational work on organizational sense making
- 📖 [The Art of Action](https://www.amazon.com/Art-Action-Leaders-between-Actions/dp/1857885597) by Stephen Bungay - Sense making in strategy execution
- 💡 [How Organizations Learn](https://hbr.org/2015/03/why-organizations-dont-learn) - HBR article on organizational learning
- 💡 [Making Sense of Sensemaking](https://www.researchgate.net/publication/220591565_Making_Sense_of_Sensemaking_1_Alternative_Perspectives) - Academic review of sense making research
- 🎯 [Incident Review Best Practices](https://www.learningfromincidents.io/) - Applied sense making in software operations
- 💡 [Architecture Decision Records](https://adr.github.io/) - Capturing architectural sense making
- 🎯 [The DevOps Handbook](https://www.amazon.com/DevOps-Handbook-World-Class-Reliability-Organizations/dp/1942788002) - Learning from operational sense making

---
*Added: May 15, 2026 | Updated: May 15, 2026 | Confidence: High*