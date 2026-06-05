# Few-Shot Learning

## At a Glance
| | |
|---|---|
| **Category** | Learning Technique |
| **Complexity** | Beginner to Intermediate |
| **Time to Learn** | 30-45 minutes |
| **Prerequisites** | [Large language models](large_language_model.md), [prompt engineering](prompt_engineering.md), [tokens](token.md) |

## One-Sentence Summary
Few-shot learning is a technique where you teach an [AI agent](../Agent_and_Orchestration/ai_agent.md) or [large language model](large_language_model.md) how to perform a task by providing just a handful of examples (typically 2-10) within the prompt, allowing the model to infer the pattern and apply it to new cases without any additional training.

## Why This Matters to You
Few-shot learning is one of the most practical and immediately useful capabilities of modern [large language models](large_language_model.md). Instead of spending weeks collecting thousands of labeled examples and [fine-tuning](fine_tuning.md) a model, you can often achieve good results by simply showing the model 3-5 examples of what you want in your prompt. This matters because it dramatically lowers the barrier to customizing AI behavior—you don't need ML expertise, training infrastructure, or massive datasets. Just craft a prompt with a few examples and the model often "gets it." For [AI agent](../Agent_and_Orchestration/ai_agent.md) developers, few-shot learning is your first tool for adapting model behavior to specific tasks, formats, or domains. It's faster to iterate than [fine-tuning](fine_tuning.md), requires no code changes, and works immediately. Understanding when few-shot is sufficient versus when you need fine-tuning or [zero-shot](zero_shot_learning.md) approaches is essential for efficient development.

## The Core Idea
### What It Is
Few-shot learning refers to a model's ability to learn a new task from just a small number of examples provided at inference time—typically within the prompt itself. The model wasn't explicitly trained on your specific task, but by seeing 2-10 examples of input-output pairs, it can infer the pattern and apply it to new inputs.

This works through **in-context learning**, a capability that emerged in large-scale [transformers](transformer.md). When you provide examples in the prompt, the model's [attention mechanism](attention_mechanism.md) allows it to recognize patterns across those examples and generalize to the new case you're asking about. Remarkably, this happens without updating the model's [parameters](model_parameters.md)—the model learns purely from the context you provide within its [context window](../Data_and_Retrieval_Patterns/context_window.md).

A classic few-shot prompt structure looks like this:
```
Translate English to French:
English: Hello → French: Bonjour
English: Goodbye → French: Au revoir  
English: Thank you → French: Merci
English: How are you? → French:
```

The model sees the pattern (English-French translation) from the three examples and applies it to generate "Comment allez-vous?" for the final case. You've taught the model what to do through demonstration, not through explicit instruction.

Few-shot learning scales along a spectrum: **one-shot** (a single example), **few-shot** (2-10 examples), and **many-shot** (10+ examples, approaching fine-tuning territory). The optimal number depends on task complexity, model capability, and [context window](../Data_and_Retrieval_Patterns/context_window.md) size. More examples generally improve performance but consume more context and increase latency.

The power of few-shot learning comes from [transfer learning](transfer_learning.md)—the model learned general patterns during [training](training.md) on massive datasets, and now applies that knowledge to your specific task when you show examples. It's not learning from scratch; it's specializing its existing knowledge based on your demonstrations.

### What It Isn't
Few-shot learning is not traditional machine learning training. The model's weights don't change—there's no backpropagation, no gradient descent, no parameter updates. The "learning" happens entirely through pattern recognition within the current context.

It's not guaranteed to work for every task. Few-shot learning effectiveness depends on whether the task is within the model's capability space and whether sufficient patterns exist in the examples. Highly specialized domains, tasks requiring precise factual knowledge the model wasn't trained on, or cases needing consistent behavior across thousands of edge cases may need [fine-tuning](fine_tuning.md) instead.

Few-shot learning isn't magic or reasoning in the human sense. The model recognizes statistical patterns in your examples and extrapolates. If your examples are inconsistent, ambiguous, or don't clearly demonstrate the pattern, performance suffers. The model doesn't "understand" the task conceptually; it pattern-matches based on [attention](attention_mechanism.md) over your examples.

It's also not always better than [zero-shot learning](zero_shot_learning.md). Sometimes clear instructions work better than examples, especially for models trained with instruction-following (like GPT-4 or Claude). Examples can even confuse the model if they're poorly chosen. The "few-shot vs. zero-shot" decision depends on task complexity and how well the model already understands what you want.

Finally, few-shot learning is not permanent. Each new conversation or API call starts fresh—the model doesn't remember examples from previous interactions unless you include them in every prompt. If you need persistent adaptation, consider [fine-tuning](fine_tuning.md) or an external memory system for your [AI agent](../Agent_and_Orchestration/ai_agent.md).

## How It Works
Few-shot learning operates through these mechanisms:

1. **Example Encoding**: Your examples are tokenized into [tokens](token.md) and included in the [context window](../Data_and_Retrieval_Patterns/context_window.md) alongside the query. The model processes all of this as a single sequence.

2. **Pattern Recognition via Attention**: The model's [attention mechanism](attention_mechanism.md) allows later tokens (your query) to attend back to earlier tokens (your examples). When generating output, the model compares the current query against the patterns demonstrated in the examples.

3. **In-Context Generalization**: The model identifies structural similarities between your examples and applies the inferred transformation or classification logic to the new input. This happens through the same [inference](inference.md) process used for all predictions, just with richer context.

4. **Format Matching**: The model learns output formatting from examples. If all your examples show "Input: X → Output: Y" format, the model maintains that structure. Consistent formatting helps the model understand boundaries and structure.

5. **Confidence Calibration**: More examples generally increase model confidence and consistency. With one example, the model might hedge or vary its approach. With five examples, it's more certain about the pattern and produces more consistent outputs.

6. **Token Budget Management**: Examples consume [context window](../Data_and_Retrieval_Patterns/context_window.md) space. If you have 8,000 tokens available and each example costs 50 tokens, you can include ~160 examples before hitting limits—though practical few-shot typically uses 2-10 examples to leave room for the actual task.

**Key insight**: Few-shot learning leverages the model's pre-existing capabilities. The model already "knows" about translation, summarization, classification, and countless other tasks from [training](training.md). Your examples don't teach it these tasks from scratch—they specify *which* task you want and *how* you want it performed.

## Think of It Like This
Imagine hiring a highly experienced chef who's worked in dozens of cuisines. You want them to make a dish from your grandmother's recipe, but you don't have time for weeks of training.

**Zero-shot approach**: You just say "Make Nonna's special pasta" and hope they figure it out from their general knowledge.

**Few-shot approach**: You show them three photos of the dish from different angles, let them taste a saved portion, and show them how Nonna plated it. The chef, drawing on decades of experience, quickly infers the technique, ingredients, and presentation style, then replicates it successfully.

**Fine-tuning approach**: You'd have the chef work with Nonna for a month, making the dish hundreds of times until it's muscle memory.

The chef isn't learning cooking from scratch—they're specializing their existing expertise based on the specific examples you provide. Few-shot learning works the same way: showing the [LLM](large_language_model.md) a few examples helps it specialize its broad knowledge to your specific need.

Using our railway metaphor: if the [large language model](large_language_model.md) is a locomotive that can pull many types of cargo, few-shot learning is like showing the locomotive engineer three previous trains with similar cargo arrangements, then asking them to configure the current train to match. The engineer (model) uses experience to recognize the pattern and applies it to the new train.

## The "So What?" Factor
**If you use this:**
- Rapidly prototype and iterate on [AI agent](../Agent_and_Orchestration/ai_agent.md) behaviors without infrastructure
- Customize model outputs for specific formats, styles, or domains in minutes
- Reduce development time from weeks (for [fine-tuning](fine_tuning.md)) to minutes
- Avoid the cost and complexity of collecting large labeled datasets
- Test whether a task is feasible before investing in custom training
- Achieve good performance on many tasks without specialized ML expertise
- Maintain flexibility to adjust examples and behavior instantly

**If you don't:**
- Struggle with inconsistent or off-target model outputs that don't match your needs
- Waste time trying to describe complex patterns in words when examples would be clearer
- Jump straight to expensive [fine-tuning](fine_tuning.md) for tasks that few-shot could handle
- Miss opportunities to guide model behavior toward specific formats or styles
- Face longer iteration cycles when adjusting AI agent behavior
- Require more sophisticated [prompt engineering](prompt_engineering.md) to achieve similar results

## Practical Checklist
Before implementing few-shot learning, ask yourself:
- [ ] Have I chosen diverse, representative examples that clearly demonstrate the pattern?
- [ ] Are my examples consistent in format and structure?
- [ ] Does each example clearly show the input-output relationship I want?
- [ ] Am I using enough examples (typically 3-5) without wasting [context window](../Data_and_Retrieval_Patterns/context_window.md) space?
- [ ] Have I tested whether [zero-shot](zero_shot_learning.md) instructions might work better?
- [ ] Do I understand how many tokens my examples consume?
- [ ] Am I including edge cases or just typical cases in my examples?
- [ ] Have I validated that few-shot examples improve performance over zero-shot for my task?
- [ ] Is the task simple enough that few-shot can handle it, or do I need [fine-tuning](fine_tuning.md)?

## Watch Out For
⚠️ **Example quality matters more than quantity** - Three excellent, diverse examples typically outperform ten mediocre examples. Choose examples that clearly demonstrate the pattern, cover edge cases, and are unambiguous. Bad examples can actively hurt performance.

⚠️ **Order effects** - Example ordering can influence model behavior. The last example often has slightly more weight. If you have one edge case example, placing it strategically can help the model handle similar cases.

⚠️ **Context window consumption** - Examples can consume significant [context window](../Data_and_Retrieval_Patterns/context_window.md) space, especially for verbose tasks. Balance example count against available context for the actual task. Consider whether fewer examples with better instructions might work.

⚠️ **Inconsistency across examples** - If your examples show different formatting, styles, or patterns, the model may struggle to identify what to learn. Consistency is critical. Verify all examples follow the same structural pattern.

⚠️ **Overfitting to examples** - The model might match surface features of your examples too closely rather than learning the underlying pattern. This is especially problematic with very few examples. Test with diverse inputs to verify generalization.

⚠️ **Not always better than zero-shot** - Modern instruction-tuned models sometimes perform better with clear instructions than with examples, especially for straightforward tasks. A/B test both approaches.

## Connections
**Builds On:** [Large language models](large_language_model.md), [prompt engineering](prompt_engineering.md), [attention mechanism](attention_mechanism.md), [context window](../Data_and_Retrieval_Patterns/context_window.md), [tokens](token.md)

**Works With:** [Zero-shot learning](zero_shot_learning.md) (complementary approach), [system prompts](../Agent_and_Orchestration/system_prompt.md) (combining instructions with examples), [chain-of-thought](../Agent_and_Orchestration/chain-of-thought.md) (few-shot reasoning examples)

**Leads To:** [Fine-tuning](fine_tuning.md) (when few-shot isn't enough), [transfer learning](transfer_learning.md) (underlying capability), [AI agent](../Agent_and_Orchestration/ai_agent.md) design patterns

## Quick Decision Guide
**Use this when you need to:** Quickly adapt model behavior to specific formats or domains, demonstrate complex patterns that are hard to describe, iterate rapidly on [AI agent](../Agent_and_Orchestration/ai_agent.md) behavior, or test task feasibility before heavier investment

**Skip this when:** The task is simple enough for [zero-shot](zero_shot_learning.md) instructions, you need guaranteed consistency across thousands of edge cases (use [fine-tuning](fine_tuning.md)), examples would consume too much [context window](../Data_and_Retrieval_Patterns/context_window.md), or the model already performs the task well without examples

## Further Exploration
- 📖 "Language Models are Few-Shot Learners" (Brown et al., 2020) - GPT-3 paper demonstrating few-shot capabilities
- 🎯 OpenAI's few-shot learning guide - Practical examples and best practices
- 💡 "What Makes Good In-Context Examples for GPT-3?" - Research on example selection
- 📖 "Rethinking the Role of Demonstrations" - Academic analysis of how few-shot learning works
- 🎯 Prompt engineering libraries (LangChain, Guidance) - Tools for managing few-shot examples

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*