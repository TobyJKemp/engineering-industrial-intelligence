# Sampling

## At a Glance
| | |
|---|---|
| **Category** | Technique / Configuration Parameter |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 30-45 minutes |
| **Prerequisites** | [Large Language Models](large_language_model.md), [Temperature](temperature.md), [Tokens](token.md), basic probability concepts |

## One-Sentence Summary
Sampling is the method by which language models choose the next token from their probability distributions during text generation—ranging from always picking the most likely word (deterministic) to randomly selecting from a curated set of possibilities (creative), with various strategies balancing quality and diversity.

## Why This Matters to You
Every time a [large language model](large_language_model.md) generates text, it's making hundreds of sampling decisions—one per [token](token.md). The sampling method you choose fundamentally shapes the output: greedy sampling produces safe but repetitive text, top-k gives you controlled variety, top-p (nucleus sampling) adapts to context dynamically. Understanding sampling helps you tune AI behavior for your use case—if your chatbot sounds robotic and boring, you might need different sampling. If your creative writing assistant produces nonsense, you might be sampling too broadly. Sampling works hand-in-hand with [temperature](temperature.md) to control the randomness-quality tradeoff. Most developers leave sampling at defaults without understanding what they're missing—knowing these techniques lets you fine-tune generation quality, avoid repetitive outputs, control computational cost, and debug unexpected model behavior. Sampling is the final step in text generation, and getting it right is the difference between outputs that feel natural versus those that feel off.

## The Core Idea
### What It Is
Sampling is the process of selecting a specific token from the probability distribution that a language model produces for the next position in a sequence. After processing your prompt and any previously generated tokens, the model produces a probability score for every token in its vocabulary—perhaps "the" has 8% probability, "a" has 5%, "some" has 2%, and thousands of other words share the remaining probability. Sampling is the algorithm that takes these probabilities and chooses which token to actually generate.

The simplest sampling method is greedy sampling (also called argmax): always pick the token with the highest probability. This is completely deterministic—the same prompt produces identical output every time. It's fast and consistent but can produce repetitive, unnatural text because the model takes no chances. Real language has variety and surprise; greedy sampling eliminates both.

More sophisticated sampling methods introduce controlled randomness. Random sampling treats the probabilities as a weighted lottery—tokens with higher probability are more likely to be selected, but lower-probability tokens have chances too. This creates variety but can select very unlikely tokens that produce nonsense. The art of sampling is constraining randomness to maintain quality while enabling creativity.

Modern sampling strategies use various constraints to balance these concerns. Top-k sampling only considers the k most probable tokens, ignoring the long tail of unlikely options. Top-p sampling (nucleus sampling) selects tokens until their cumulative probability reaches a threshold p (like 0.9), creating a dynamic set that adapts to the distribution—sometimes considering many tokens, sometimes just a few. These methods prevent the model from selecting absurdly unlikely tokens while maintaining useful variety.

Sampling interacts critically with [temperature](temperature.md). Temperature modifies the probability distribution before sampling occurs—low temperature makes the distribution more peaked (high probabilities get higher, low ones get lower), while high temperature flattens it. After temperature adjusts probabilities, the sampling method determines final token selection. The two parameters work together: temperature shapes the distribution, sampling picks from it.

### What It Isn't
Sampling is not the same as [temperature](temperature.md), though they're closely related and often confused. Temperature modifies probability distributions; sampling chooses from those distributions. You can have high temperature with greedy sampling (flatten probabilities then pick the highest) or low temperature with random sampling (sharpen probabilities then randomly select). They're complementary controls that work together.

Sampling is not "creativity" itself, though it enables variety that can feel creative. The model's probability distributions reflect its training—sampling doesn't make the model think of new ideas, it just determines how the model selects among ideas it already considered. High-variance sampling can produce unexpected combinations, but the underlying concepts come from training data, not from the sampling method.

Sampling is not a solution for poor model quality. If the model doesn't know the right answer or doesn't have relevant capabilities, clever sampling won't fix it. Sampling affects how the model selects from what it already believes—it doesn't improve the underlying beliefs. A model that doesn't understand your domain will produce wrong answers whether you use greedy or nucleus sampling; sampling just changes which wrong answers appear.

Sampling is also not random in the common sense, except for pure random sampling which is rarely used. Most sampling methods are pseudorandom with constraints—they use randomness but within carefully designed boundaries. Top-k and top-p sampling are deterministic algorithms that happen to use random number generators as one component.

Finally, sampling is not a one-time decision. During text generation, the model samples once per token—potentially hundreds of times for a single response. Each sampling decision affects what comes next because the generated token feeds back into the context for the next prediction. This autoregressive process means sampling effects compound through the generation.

## How It Works
Different sampling strategies and how they select tokens:

1. **Greedy Sampling (Argmax)**:
   - Algorithm: Always select the token with the highest probability
   - Deterministic: Same input always produces identical output
   - Fast: No randomness to compute, just find the maximum
   - Characteristics: Safe, consistent, but repetitive and predictable
   - Use case: When you want completely deterministic output, like [unit testing](../Testing_and_Evaluation/unit_testing.md)

2. **Random Sampling (Multinomial)**:
   - Algorithm: Treat probabilities as weights, randomly select proportionally
   - Every token has a chance proportional to its probability
   - Pure random selection without constraints
   - Characteristics: High variety but can select very unlikely nonsensical tokens
   - Rarely used alone: Usually combined with temperature or other constraints

3. **Top-k Sampling**:
   - Algorithm: Filter to k most probable tokens, renormalize probabilities, then randomly sample
   - Fixed-size candidate set (e.g., k=40 means only consider 40 most likely tokens)
   - Eliminates long tail of improbable options
   - Characteristics: Controlled variety, prevents extreme unlikely selections
   - Use case: When you want creativity but with safety bounds

4. **Top-p Sampling (Nucleus Sampling)**:
   - Algorithm: Sort tokens by probability, select smallest set whose cumulative probability exceeds p (e.g., p=0.9)
   - Dynamic candidate set: Sometimes considers many tokens, sometimes few
   - Adapts to distribution shape: When model is confident (one clear answer), nucleus is small; when uncertain, nucleus is large
   - Characteristics: Context-sensitive variety, generally produces more natural text than top-k
   - Use case: Default for most production applications, balances quality and diversity

5. **Combined Strategies**:
   - Temperature + Top-p: Most common combination—temperature adjusts distribution shape, top-p constrains candidate set
   - Temperature + Top-k: Alternative combination with fixed candidate size
   - Min-p, Top-a: Advanced variants adjusting thresholds dynamically
   - Beam search: Not strictly sampling—maintains multiple candidate sequences, selects best (used for translation)

6. **The Generation Loop**:
   - Model produces probability distribution over vocabulary
   - Temperature scaling adjusts probabilities (if temperature ≠ 1.0)
   - Sampling method filters and selects from adjusted probabilities
   - Selected token is generated and fed back into context
   - Process repeats for next token position
   - Continues until stop token, maximum length, or other termination condition

## Think of It Like This
**The Restaurant Menu Analogy**: Imagine choosing from a restaurant menu where each dish has a recommendation score. Greedy sampling always orders the top-rated dish—reliable but boring if you eat there daily. Random sampling spins a weighted roulette wheel including even the 1-star items—you'll occasionally get the weird experimental dish that's terrible. Top-k sampling says "only consider the top 10 dishes" then randomly picks among those—you get variety but stay within good options. Top-p (nucleus) sampling is smarter: if there's one standout dish with 80% of recommendations, it mostly picks that with small chances for alternatives; but if five dishes are equally recommended at 15% each, it considers all five. The sampling method determines how adventurous you are while staying within quality bounds.

**Railway Metaphor**: Think of sampling as a railway dispatcher choosing which track a train takes at a junction. The model's probability distribution is like track quality assessments—main line is 70% optimal, branch line A is 15%, branch line B is 10%, risky spur line C is 5%. Greedy sampling always sends trains on the main line—safe but every train follows identical routes. Random sampling rolls dice weighted by track quality—usually picks good routes but occasionally sends trains down terrible spurs. Top-k sampling says "only consider the best 3 tracks" and randomly picks among those—you get route variety while excluding dangerous options. Top-p (nucleus) sampling adapts: when one track is clearly best (70%+), it mostly uses that; when options are similar (four tracks at 20% each), it distributes traffic across them. Different situations need different flexibility.

## The "So What?" Factor
**If you understand sampling:**
- You can tune output quality for your specific use case (consistency vs. creativity)
- You can debug unexpected model behavior by checking sampling settings
- You can avoid repetitive outputs by using appropriate sampling strategies
- You can optimize computational costs (greedy is fastest, random sampling with constraints slower)
- You can implement appropriate sampling for different tasks (strict for data extraction, creative for writing)
- You can understand why the same prompt sometimes gives different answers
- You can communicate effectively about generation quality with engineers

**If you don't understand sampling:**
- You'll be confused why model outputs vary (or don't vary) from run to run
- You won't know how to fix robotic, repetitive outputs
- You'll struggle when creative sampling produces occasional nonsense
- You might use inappropriate sampling for your task (creative sampling for structured data extraction)
- You won't understand relationships between temperature, sampling, and output quality
- You'll miss optimization opportunities (unnecessary randomness has computational cost)
- You'll have difficulty debugging generation quality issues

## Practical Checklist
Before configuring sampling for your application, ask yourself:
- [ ] **Do I need deterministic outputs?** If yes, use greedy sampling or set [temperature](temperature.md) to 0.
- [ ] **What's my creativity-quality tradeoff?** Higher-variance sampling enables creativity but risks quality.
- [ ] **Am I generating structured data or creative text?** Structured data wants greedy/low-variance; creative writing wants higher-variance.
- [ ] **How will I handle occasional bad outputs?** All non-greedy sampling occasionally produces duds—plan for this.
- [ ] **What sampling method does my model provider recommend?** Different models are tuned for different sampling strategies.
- [ ] **Do I need to test multiple variations?** If so, higher-variance sampling generates diverse options.
- [ ] **What's my computational budget?** More sophisticated sampling has overhead (usually negligible but measurable).

## Watch Out For
⚠️ **Sampling Without Temperature Control**: Adjusting sampling method without appropriate temperature can produce poor results. Top-k with very low temperature mostly picks the same token anyway (wasting computation). Random sampling with high temperature can select nonsense. Tune both together.

⚠️ **Inconsistent Repetition Detection**: Even with good sampling, models can get stuck in loops ("the the the..."). This isn't a sampling problem—it's a model issue. Repetition penalties (reducing probability of recently-generated tokens) help but are separate from sampling methods.

⚠️ **Assuming Top-p Is Always Best**: While top-p (nucleus) sampling is often default and generally good, it's not universally superior. Some tasks work better with top-k, others with greedy. Always test what works for your specific use case.

⚠️ **Ignoring Task-Specific Needs**: Creative writing, structured data extraction, translation, and code generation each have different optimal sampling strategies. Don't use one-size-fits-all settings across different task types.

⚠️ **Over-Engineering Sampling**: For many applications, default settings (temperature 0.7-0.9, top-p 0.9) work well. Don't waste time hyper-optimizing sampling when prompts or model selection matter more. Optimize sampling after getting other fundamentals right.

⚠️ **Forgetting Sampling Affects Cost**: API pricing often charges per token, and generation takes time. Greedy sampling is faster and more predictable. If you're doing high-volume generation where creative variety isn't needed, greedy sampling reduces both latency and cost variance.

## Connections
**Builds On:** [Large Language Model](large_language_model.md) (generates probability distributions), [Tokens](token.md) (units being sampled), [Inference](inference.md) (process where sampling occurs)  
**Works With:** [Temperature](temperature.md) (adjusts distributions before sampling), [Prompt Engineering](prompt_engineering.md) (prompts affect distributions that get sampled)  
**Leads To:** Text generation quality, output diversity, [AI Agent](../Agent_and_Orchestration/ai_agent.md) behavior control, deterministic vs. creative outputs

## Quick Decision Guide
**Use greedy sampling (or temperature=0) when:**
- You need deterministic outputs for testing or reproducibility
- Extracting structured data (JSON, lists, classifications)
- Quality consistency matters more than variety
- Debugging prompts and want to eliminate randomness as a variable

**Use top-p (nucleus) sampling when:**
- Building general-purpose applications (chatbots, assistants)
- Balancing quality and variety
- Want context-adaptive behavior (conservative when certain, diverse when uncertain)
- Using modern LLMs (most are tuned expecting top-p)

**Use top-k sampling when:**
- Want fixed bounds on variety regardless of context
- Working with models trained or tuned with top-k
- Need predictable computational costs (fixed candidate set size)

**Use high-variance sampling (high temp + top-p) when:**
- Generating creative content (stories, marketing copy, brainstorming)
- Exploring multiple solution variations
- Want unexpected combinations and surprising outputs
- Quality filtering happens downstream (generate many, pick best)

**Avoid pure random sampling:**
- Rarely optimal without constraints (top-k/top-p)
- High risk of nonsensical outputs
- Better to use constrained random methods

## Further Exploration
- 📖 **"The Curious Case of Neural Text Degeneration"**: Research paper introducing nucleus (top-p) sampling and analyzing why it works
- 🎯 **Interactive Sampling Demo**: Tools showing how different sampling strategies select tokens in real-time
- 💡 **Beam Search vs. Sampling**: Understanding when beam search (deterministic, searches multiple paths) beats sampling approaches
- 📖 **Repetition Penalties**: Techniques for preventing sampling from getting stuck in loops
- 🎯 **Sampling Playground**: Experiment with temperature and sampling parameters to see effects on output
- 💡 **Constrained Sampling**: Advanced techniques for sampling under constraints (format requirements, content filtering)
- 📖 **Model-Specific Tuning**: How different models (GPT, Claude, Llama) are tuned for different sampling assumptions

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*