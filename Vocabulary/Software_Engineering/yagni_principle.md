# YAGNI Principle

## At a Glance
| | |
|---|---|
| **Category** | Software Development Principle |
| **Complexity** | Beginner |
| **Time to Learn** | 30 minutes to grasp, career to master |
| **Prerequisites** | Basic software development experience, understanding of [technical_debt](technical_debt.md) |

## One-Sentence Summary
YAGNI (You Aren't Gonna Need It) is a software development principle that advises against implementing functionality until you have a concrete, immediate need for it, preventing wasted effort on features that may never be used or may need to be implemented differently when actually required.

## Why This Matters to You
When building AI agent systems, the temptation to build "just in case" features is overwhelming—maybe you'll need multi-model support, maybe you'll need distributed processing, maybe you'll need advanced caching strategies. YAGNI saves you from these rabbit holes by keeping you focused on solving the problem in front of you today. In the fast-moving world of AI/ML, where frameworks, models, and best practices evolve monthly, building for hypothetical futures often means building the wrong thing. YAGNI helps you ship faster, learn quicker, and adapt more easily when requirements inevitably change.

## The Core Idea
### What It Is
YAGNI is a core principle from Extreme Programming that challenges developers to resist the urge to add functionality based on speculation about future needs. The principle recognizes that predicting future requirements is notoriously difficult, and that code written for hypothetical scenarios often turns out to be wrong, incomplete, or unnecessary when the actual requirement emerges.

In practice, YAGNI means writing only the code needed to pass your current tests, satisfy your current user stories, or solve your current problem. When you find yourself thinking "we might need this later" or "it would be easy to add support for X while we're here," YAGNI says to stop and ask: do we need it *right now*? If the answer is no, don't build it.

This principle is particularly powerful in AI agent development where the landscape shifts rapidly. You might think you'll need to support five different LLM providers, but starting with one and adding others only when needed prevents you from building abstractions that don't fit the models that actually get used. You might imagine needing a sophisticated caching layer, but YAGNI suggests starting simple and adding complexity only when performance measurements show it's necessary.

### What It Isn't
YAGNI is not an excuse for poor design or technical shortcuts. It doesn't mean ignoring obvious extension points or writing rigid code that's difficult to modify. When you build authentication today, YAGNI doesn't mean hardcoding everything—it means using standard patterns that are well-understood rather than building a complex, configurable framework for hypothetical auth providers you might add someday.

YAGNI also isn't about avoiding planning or architectural thinking. You still need to understand where your system is heading and make reasonable design decisions. The difference is between designing for known future needs (good) and implementing features for hypothetical scenarios (YAGNI violation). If you know you'll need to support multiple databases next quarter because it's on the roadmap, that's real planning. If you add database abstraction "just in case" we might support NoSQL someday, that's speculative and violates YAGNI.

Finally, YAGNI doesn't mean never writing reusable code or abstractions. It means waiting until you have at least two or three concrete use cases before extracting common patterns. The programming wisdom "don't repeat yourself until you've repeated yourself" captures this perfectly—write the code once, copy it the second time, and only on the third repetition should you consider abstracting.

## How It Works
1. **Identify the current requirement**: Look at your immediate user story, bug fix, or feature request. What specific problem are you solving right now?

2. **Resist the "while we're here" temptation**: When you catch yourself adding code for scenarios beyond the current requirement, stop and explicitly question whether it's needed today. Are you solving a real problem or an imagined one?

3. **Build the simplest thing that works**: Implement the straightforward solution for the current need. In an AI agent context, if you need to call one LLM, write code that calls that specific LLM. Don't build a provider abstraction layer yet.

4. **Write tests for actual behavior**: Your tests should verify what the system needs to do now, not what it might need to do later. This keeps your implementation grounded in reality.

5. **Refactor when patterns emerge**: When you add a second LLM provider, *then* you refactor to extract the common pattern. At this point, you have two concrete examples to guide your abstraction, making it far more likely to be useful.

6. **Document deferred decisions**: If you explicitly decide not to implement something, note it in comments or documentation. This prevents future developers (including your future self) from thinking it was overlooked.

## Think of It Like This
Imagine you're packing for a trip. The YAGNI violator packs formal shoes "just in case" there's a fancy dinner, a swimsuit "just in case" there's a pool, hiking boots "just in case" there's a trail, and so on until their suitcase weighs 50 pounds. The YAGNI practitioner checks the itinerary, sees they're going to business meetings in the city, and packs for that specific scenario. If plans change and they need hiking boots, they can buy them there or adjust—but 90% of the time, those hypothetical needs never materialize, and they've saved themselves from lugging unnecessary weight.

In code, every "just in case" feature is weight—it needs to be understood, maintained, tested, and documented. Most of it will never be needed, and when needs actually arise, they're often different from what you imagined anyway.

## The "So What?" Factor
**If you use this:**
- You ship features faster because you're not building hypothetical functionality
- Your codebase stays leaner and more comprehensible because it only contains code that's actually used
- When requirements change (and they will), you have less code to modify or throw away
- Your abstractions are better because they're based on real use cases, not speculation
- Testing is simpler because you're only testing functionality that actually exists for a reason

**If you don't:**
- You waste time building features that never get used (studies suggest 64% of features are rarely or never used)
- Your code becomes more complex, making bugs more likely and the system harder to understand
- When you finally do need new functionality, your speculative abstractions often don't fit the actual requirement
- Maintenance burden grows as you support code paths that have no users
- You make slower progress on features that actually matter because you're distracted by hypothetical scenarios

## Practical Checklist
Before implementing a feature, ask yourself:
- [ ] Do I have a concrete user story or requirement that needs this *right now*?
- [ ] Am I building this because someone asked for it, or because I think they might need it someday?
- [ ] If I don't build this now, what's the actual cost of adding it later when needed?
- [ ] Have I caught myself using the phrase "just in case" or "while we're here" when discussing this feature?
- [ ] Can I write a test for this feature that verifies current, real behavior rather than hypothetical scenarios?
- [ ] If this feature isn't used in the next six months, will I regret spending time on it?

## Watch Out For
⚠️ **The "it's so easy" trap**: Just because a feature is quick to implement doesn't mean you should build it now. Easy features still add complexity, maintenance burden, and cognitive load. The question isn't "is it easy?" but "do we need it?"

⚠️ **Confusing YAGNI with no planning**: YAGNI doesn't mean ignoring architecture or avoiding reasonable design decisions. It means not implementing features speculatively. Design for extension, but don't build extensions until they're needed.

⚠️ **Analysis paralysis**: Don't spend more time debating whether something violates YAGNI than it would take to build it. YAGNI is a guideline to help with common sense, not a religious doctrine requiring extensive philosophical debate.

⚠️ **False economies**: Some things genuinely are cheaper to do now than later. If you're setting up logging infrastructure and it takes 5 minutes to add structured logging instead of simple print statements, that's not a YAGNI violation—it's avoiding future technical debt. YAGNI is about *features*, not quality.

⚠️ **The pendulum swing**: Developers who discover YAGNI sometimes over-apply it, refusing to do any planning or make any reasonable design decisions. Balance is key—YAGNI prevents speculative features, not thoughtful engineering.

## Connections
**Builds On:** 
- [kiss_principle](kiss_principle.md) - Keep It Simple, Stupid complements YAGNI by focusing on simplicity
- [technical_debt](technical_debt.md) - Understanding technical debt helps you see the cost of speculative code

**Works With:** 
- [dry_principle](dry_principle.md) - Don't Repeat Yourself, but wait until you've repeated yourself before abstracting
- [refactoring](refactoring.md) - YAGNI encourages building simple first, then refactoring when patterns emerge
- [clean_code](clean_code.md) - Simple, clear code supports YAGNI by making changes easier
- [single_responsibility](single_responsibility.md) - Focused components are easier to extend when needs actually arise
- [separation_of_concerns](separation_of_concerns.md) - Good boundaries make YAGNI safer by limiting change impact

**Leads To:** 
- [solid_principles](solid_principles.md) - Particularly Open/Closed Principle for designing extensibility without speculation
- Lean Software Development - YAGNI is a core principle in Lean methodologies
- Iterative Development - YAGNI naturally supports incremental delivery and learning

**Related Patterns:**
- Spike Solutions - When you need to explore, do a time-boxed spike rather than building production code
- Walking Skeleton - Build the minimal end-to-end system first, then add features incrementally

## Quick Decision Guide
**Use this when you need to:**
- Decide whether to implement a feature that's not in the current requirements
- Evaluate whether to add "just in case" functionality
- Push back on stakeholders requesting speculative features
- Choose between a simple implementation and a more flexible but complex one
- Prioritize which features to build first

**Skip this when:**
- You have concrete evidence that a feature will be needed (it's on next quarter's roadmap, contracts are signed, etc.)
- The cost of adding something later is genuinely prohibitive (changing database schemas, shipping hardware, etc.)
- You're dealing with genuine quality concerns (logging, security, error handling) rather than features
- Regulatory or compliance requirements mandate functionality regardless of immediate use

## Further Exploration
- 📖 "Extreme Programming Explained" by Kent Beck - Original source of YAGNI principle
- 🎯 "The Agile Samurai" by Jonathan Rasmusson - Practical application of YAGNI in agile contexts
- 💡 Martin Fowler's "YAGNI" essay - Nuanced discussion of when and how to apply the principle
- 📖 "Refactoring" by Martin Fowler - How to evolve code from simple to complex as needs emerge
- 🎯 "Building Microservices" by Sam Newman - YAGNI applied to service boundaries and distributed systems
- 💡 "The Art of Agile Development" by James Shore - YAGNI in the context of agile engineering practices

---
*Added: 2026-05-19 | Updated: 2026-05-19 | Confidence: High*
