# Evaluation Metrics

## At a Glance
| | |
|---|---|
| **Category** | Measurement / Quality Assurance |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-4 hours for fundamentals, ongoing refinement for domain-specific application |
| **Prerequisites** | Basic statistics, understanding of system requirements, familiarity with [benchmark](benchmark.md) concepts |

## One-Sentence Summary
Evaluation metrics are quantitative measurements that objectively assess system performance, quality, cost, or behavior—transforming subjective questions like "is my agent good enough?" into concrete, measurable answers like "achieves 92% accuracy with 1.2 second average latency at $0.03 per query."

## Why This Matters to You
When you build AI agent systems in 2026, you constantly face questions that feel subjective: Is this model good enough? Did my prompt change improve quality? Should I use GPT-4 or Claude? Is my RAG system working well? Without evaluation metrics, these questions get answered with gut feelings, cherry-picked examples, and arguments—leading to poor decisions, wasted resources, and production failures. Evaluation metrics transform these fuzzy questions into measurable reality: accuracy increased from 78% to 85%, latency dropped by 200ms, cost reduced by 40%, hallucination rate fell from 12% to 3%. Metrics let you compare objectively (Model A vs Model B on the same criteria), track progress (quality trend over 6 months), validate improvements (did that optimization actually help?), and set thresholds (deploy only if accuracy > 90% AND latency < 2s). In production systems, metrics are how you detect degradation, justify costs to stakeholders, make data-driven architecture decisions, and know whether you're building the right thing. Without metrics, you're flying blind—metrics are your instruments.

## The Core Idea
### What It Is
An evaluation metric is a quantitative measurement that captures some aspect of system performance, quality, or behavior. Instead of saying "the agent seems pretty accurate," you say "the agent achieves 87% accuracy on our support benchmark." Instead of "responses are fast," you say "P95 latency is 1.8 seconds."

**Key Characteristics:**

**1. Quantitative**: Produces numbers you can track, compare, and analyze over time.

**2. Measurable**: Can be computed automatically from system outputs and test data.

**3. Relevant**: Reflects aspects of performance that actually matter for your use case.

**4. Interpretable**: Clear meaning—higher is better or lower is better, and what the numbers represent.

**In 2026 AI Agent Systems, metrics fall into several categories:**

**Accuracy/Quality Metrics** (Is the output correct/good?):
```python
# Classification metrics
accuracy = correct_predictions / total_predictions
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1_score = 2 * (precision * recall) / (precision + recall)

# Text generation quality
bleu_score = compute_bleu(reference_text, generated_text)  # 0-1
rouge_score = compute_rouge(reference_text, generated_text)  # 0-1

# Semantic similarity (RAG, question answering)
semantic_similarity = cosine_similarity(
    embed(expected_answer),
    embed(generated_answer)
)  # -1 to 1, typically 0-1 range

# LLM-as-judge (2026 standard for complex evaluation)
quality_score = llm_judge.evaluate(
    task="rate answer quality on 1-10 scale",
    question=question,
    answer=agent_response,
    criteria=["accuracy", "completeness", "clarity"]
)

# Factual correctness
factuality_score = check_facts_against_sources(
    answer=agent_response,
    sources=retrieved_documents
)  # 0-1
```

**Operational Metrics** (How fast/reliable is it?):
```python
# Latency measurements
latency = response_time - request_time  # seconds
p50_latency = np.percentile(latencies, 50)  # median
p95_latency = np.percentile(latencies, 95)  # 95th percentile
p99_latency = np.percentile(latencies, 99)  # worst 1%

# Throughput
requests_per_second = total_requests / time_window
tokens_per_second = total_tokens_generated / time_window

# Reliability
success_rate = successful_requests / total_requests
error_rate = failed_requests / total_requests
availability = uptime / (uptime + downtime)  # percentage

# Efficiency
cache_hit_rate = cache_hits / total_lookups
retry_rate = requests_retried / total_requests
```

**Cost Metrics** (How expensive is it?):
```python
# Direct costs
cost_per_query = total_llm_costs / total_queries
cost_per_user = total_costs / active_users
monthly_burn_rate = sum(daily_costs_this_month)

# Cost breakdown
prompt_tokens_cost = prompt_tokens * input_token_price
completion_tokens_cost = completion_tokens * output_token_price
embedding_cost = embedding_calls * embedding_price
tool_execution_cost = api_calls * api_price

# Efficiency metrics
cost_per_success = total_costs / successful_outcomes
cost_to_quality_ratio = total_costs / average_quality_score
```

**Safety/Compliance Metrics** (Is it safe/appropriate?):
```python
# Content safety
harmful_output_rate = harmful_responses / total_responses
toxicity_score = toxicity_detector.score(response)  # 0-1
pii_leak_rate = responses_containing_pii / total_responses

# Correctness
hallucination_rate = hallucinated_responses / total_responses
citation_accuracy = correctly_cited / total_citations
knowledge_cutoff_compliance = rate_of_declining_recent_events

# Compliance
policy_violation_rate = policy_violations / total_responses
terms_acceptance_rate = users_accepting_terms / total_users
audit_trail_completeness = logged_decisions / total_decisions
```

**User Experience Metrics** (Do users like it?):
```python
# Engagement
user_satisfaction_score = avg(user_ratings)  # 1-5 scale
net_promoter_score = promoters_pct - detractors_pct  # -100 to 100
task_completion_rate = successful_tasks / attempted_tasks

# Behavior
conversation_length = avg(messages_per_conversation)
abandonment_rate = conversations_abandoned / total_conversations
retry_rate = user_retries / total_requests  # User had to ask again
```

**Domain-Specific Metrics** (Your use case):
```python
# Customer support
first_contact_resolution = resolved_on_first_message / total_tickets
average_handle_time = sum(resolution_times) / total_tickets
escalation_rate = escalated_to_human / total_tickets

# Code generation
code_correctness = tests_passing / total_generated_functions
compilation_rate = compiles_successfully / total_code_outputs
security_issue_rate = security_vulnerabilities_found / total_code

# RAG systems
retrieval_precision = relevant_docs_retrieved / total_docs_retrieved
retrieval_recall = relevant_docs_retrieved / total_relevant_docs
answer_attribution_rate = answers_with_citations / total_answers
```

### What It Isn't
Evaluation metrics are not **the complete picture**. A system with perfect accuracy but 30-second latency is unusable. High precision with 20% recall misses most cases. Low cost but terrible quality is worthless. You need multiple metrics covering different dimensions—accuracy AND latency AND cost AND safety.

They're not **requirements**. A metric tells you where you are; requirements tell you where you need to be. "P95 latency is 2.1 seconds" is a metric. "P95 latency must be under 2 seconds" is a requirement. Use metrics to measure against requirements.

Metrics are not **understanding**. High accuracy doesn't tell you why the system works or fails. Metrics identify problems ("accuracy dropped from 85% to 78%"), but you need investigation, [observability](../Agent_Operations/observability.md), and [logging](../Agent_Operations/logging.md) to understand root causes.

They're not **stable**. What metrics matter evolves as your system matures. Early prototypes focus on accuracy. Production systems add latency, cost, safety. After optimization, you track efficiency. After incidents, you add reliability metrics. Metric selection evolves with system lifecycle.

Evaluation metrics are not **universal**. The right metrics depend entirely on your use case. Customer support agents need first-contact resolution and customer satisfaction. Code generation needs correctness and security. Content moderation needs precision (low false positives) over recall. Choose metrics that matter for your specific context.

Finally, metrics are not **foolproof**. You can game metrics (optimize for the measurement rather than the goal), choose misleading metrics (vanity metrics that look good but don't matter), or measure the wrong things (technical accuracy when user satisfaction matters more). Goodhart's Law applies: "When a measure becomes a target, it ceases to be a good measure."

## How It Works

### Choosing the Right Metrics

**Step 1: Identify What Matters**
What outcomes do users/stakeholders care about?
- Correctness: Getting the right answer
- Speed: Fast responses
- Cost: Affordable to operate
- Reliability: Works consistently
- Safety: No harmful outputs
- User satisfaction: Pleasant experience

**Step 2: Map to Measurable Metrics**
Translate outcomes to quantitative measurements:
```python
metric_mapping = {
    "correctness": ["accuracy", "f1_score", "semantic_similarity"],
    "speed": ["p50_latency", "p95_latency", "throughput"],
    "cost": ["cost_per_query", "monthly_burn_rate"],
    "reliability": ["success_rate", "availability", "error_rate"],
    "safety": ["hallucination_rate", "toxicity_score", "policy_violations"],
    "satisfaction": ["user_ratings", "task_completion_rate", "nps"]
}
```

**Step 3: Implement Measurement**
Build instrumentation to collect metrics:
```python
class MetricsCollector:
    """Collect evaluation metrics for agent system."""
    
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def record_query(self, query_data: dict):
        """Record metrics from a single query."""
        # Extract metrics
        self.metrics["latency"].append(query_data["latency"])
        self.metrics["tokens_used"].append(query_data["tokens"])
        self.metrics["cost"].append(query_data["cost"])
        self.metrics["success"].append(query_data["success"])
        
        # Quality metrics (if available)
        if "quality_score" in query_data:
            self.metrics["quality"].append(query_data["quality_score"])
        
        # Safety metrics
        if query_data.get("flagged"):
            self.metrics["safety_violations"].append(1)
        else:
            self.metrics["safety_violations"].append(0)
    
    def compute_aggregate_metrics(self) -> dict:
        """Compute summary statistics."""
        return {
            # Latency
            "p50_latency": np.percentile(self.metrics["latency"], 50),
            "p95_latency": np.percentile(self.metrics["latency"], 95),
            "p99_latency": np.percentile(self.metrics["latency"], 99),
            "mean_latency": np.mean(self.metrics["latency"]),
            
            # Success/Reliability
            "success_rate": np.mean(self.metrics["success"]),
            
            # Cost
            "total_cost": sum(self.metrics["cost"]),
            "cost_per_query": np.mean(self.metrics["cost"]),
            
            # Quality
            "mean_quality": np.mean(self.metrics["quality"]) if self.metrics["quality"] else None,
            
            # Safety
            "violation_rate": np.mean(self.metrics["safety_violations"]),
            
            # Volume
            "total_queries": len(self.metrics["latency"])
        }
```

**Step 4: Set Baselines and Targets**
Establish where you are and where you need to be:
```python
# Current baseline (measured)
baseline_metrics = {
    "accuracy": 0.82,
    "p95_latency": 2.4,  # seconds
    "cost_per_query": 0.045,  # dollars
    "success_rate": 0.94
}

# Target requirements (desired)
target_metrics = {
    "accuracy": 0.90,  # +8 points
    "p95_latency": 2.0,  # -0.4s
    "cost_per_query": 0.030,  # -33%
    "success_rate": 0.98  # +4 points
}

# Calculate gaps
gaps = {
    metric: target - baseline_metrics[metric]
    for metric, target in target_metrics.items()
}
```

**Step 5: Track Over Time**
Monitor metrics continuously:
```python
def track_metrics_over_time():
    """Monitor metrics and detect changes."""
    # Compute current metrics
    current = compute_current_metrics()
    
    # Compare to historical baseline
    historical = load_historical_metrics(days=30)
    
    # Detect significant changes
    for metric_name in current.keys():
        current_value = current[metric_name]
        historical_mean = np.mean(historical[metric_name])
        historical_std = np.std(historical[metric_name])
        
        # Z-score for anomaly detection
        z_score = (current_value - historical_mean) / historical_std
        
        if abs(z_score) > 3:  # 3 sigma = significant change
            alert_team(
                f"Metric {metric_name} changed significantly: "
                f"{historical_mean:.3f} -> {current_value:.3f} "
                f"(z-score: {z_score:.2f})"
            )
    
    # Store current metrics
    store_metrics(timestamp=datetime.now(), metrics=current)
```

**Step 6: Use Metrics for Decisions**
Apply metrics to guide choices:
```python
def choose_best_model(models: list, test_set: list) -> str:
    """Select best model based on multiple metrics."""
    results = {}
    
    for model in models:
        metrics = evaluate_model(model, test_set)
        
        # Compute composite score with weights
        composite_score = (
            0.4 * metrics["accuracy"] +          # Quality matters most
            0.2 * (1 - metrics["p95_latency"]/5) +  # Latency (normalized)
            0.2 * (1 - metrics["cost_per_query"]/0.1) +  # Cost (normalized)
            0.2 * metrics["success_rate"]        # Reliability
        )
        
        results[model] = {
            "metrics": metrics,
            "composite_score": composite_score
        }
    
    # Choose highest composite score
    best_model = max(results.keys(), key=lambda m: results[m]["composite_score"])
    
    print(f"Selected {best_model}:")
    print(f"  Accuracy: {results[best_model]['metrics']['accuracy']:.1%}")
    print(f"  P95 Latency: {results[best_model]['metrics']['p95_latency']:.2f}s")
    print(f"  Cost/Query: ${results[best_model]['metrics']['cost_per_query']:.3f}")
    print(f"  Success Rate: {results[best_model]['metrics']['success_rate']:.1%}")
    
    return best_model
```

### Common Metric Patterns in 2026

**LLM-as-Judge for Quality**:
```python
def evaluate_with_llm_judge(question: str, answer: str, context: str) -> dict:
    """Use LLM to evaluate response quality."""
    judge_prompt = f"""
    Evaluate this answer on a scale of 1-10 for each criterion:
    
    Question: {question}
    Context: {context}
    Answer: {answer}
    
    Rate on:
    1. Accuracy: Is the answer factually correct based on context?
    2. Completeness: Does it fully address the question?
    3. Clarity: Is it well-organized and easy to understand?
    4. Conciseness: Is it appropriately brief without missing key points?
    
    Respond in JSON format:
    {{"accuracy": <1-10>, "completeness": <1-10>, "clarity": <1-10>, "conciseness": <1-10>, "explanation": "<brief justification>"}}
    """
    
    response = llm.complete(judge_prompt, temperature=0.1)
    scores = json.loads(response)
    
    # Compute overall score
    scores["overall"] = np.mean([
        scores["accuracy"],
        scores["completeness"],
        scores["clarity"],
        scores["conciseness"]
    ])
    
    return scores
```

**Retrieval Metrics for RAG**:
```python
def evaluate_rag_retrieval(queries: list, relevance_labels: dict) -> dict:
    """Evaluate RAG retrieval quality."""
    precisions = []
    recalls = []
    ndcgs = []
    
    for query in queries:
        # Retrieve documents
        retrieved = vector_store.search(query, top_k=10)
        retrieved_ids = [doc.id for doc in retrieved]
        
        # Get ground truth relevant documents
        relevant_ids = relevance_labels[query]
        
        # Precision: fraction of retrieved that are relevant
        relevant_retrieved = set(retrieved_ids) & set(relevant_ids)
        precision = len(relevant_retrieved) / len(retrieved_ids)
        
        # Recall: fraction of relevant that are retrieved
        recall = len(relevant_retrieved) / len(relevant_ids)
        
        # NDCG: ranking quality
        ndcg = compute_ndcg(retrieved_ids, relevant_ids)
        
        precisions.append(precision)
        recalls.append(recall)
        ndcgs.append(ndcg)
    
    return {
        "mean_precision": np.mean(precisions),
        "mean_recall": np.mean(recalls),
        "mean_ndcg": np.mean(ndcgs),
        "mrr": compute_mrr(queries, relevance_labels)  # Mean reciprocal rank
    }
```

## Think of It Like This
Imagine you're a sports coach evaluating player performance.

**Without metrics**, you say "Smith is a pretty good player, seems solid." That's subjective, hard to compare, and doesn't guide improvement.

**With metrics**, you track specific measurements: Smith averages 18.5 points per game, 6.2 rebounds, 4.1 assists, 47% field goal percentage, 85% free throw percentage. Now you can:
- Compare objectively (Smith vs Jones: who contributes more?)
- Track progress (Smith improved from 15.2 to 18.5 points over the season)
- Identify weaknesses (47% shooting is below team average—focus on shot technique)
- Make decisions (Who starts? Who gets more playing time?)
- Set goals (Target: improve free throws to 90%, increase assists to 5.0)

In AI agent systems, evaluation metrics are your performance statistics—they transform "seems good" into "achieves 87% accuracy with 1.8s latency at $0.03 per query," enabling objective comparison, progress tracking, weakness identification, and data-driven decisions.

## The "So What?" Factor
**If you use evaluation metrics systematically:**
- You make objective comparisons (GPT-4 vs Claude) based on data, not marketing
- You validate whether changes improve or degrade performance with quantitative evidence
- You detect quality degradation early by monitoring metrics over time
- You justify costs and resource allocation with concrete ROI calculations
- You set realistic expectations with stakeholders backed by measured capabilities
- You identify optimization opportunities by analyzing metric breakdowns
- You gate deployments on measurable criteria (deploy only if metrics meet thresholds)
- You track progress toward goals with clear, quantifiable milestones
- You debug issues efficiently by correlating metrics with system changes
- You align team efforts around shared, measurable objectives

**If you don't:**
- Decisions about models, architectures, and optimizations rely on gut feelings and anecdotes
- You can't tell whether changes helped or hurt without subjective post-hoc assessment
- Quality degradation goes unnoticed until users complain
- Cost justifications are vague ("it's pretty efficient") rather than data-driven
- Stakeholder expectations don't match reality because capabilities weren't measured
- Optimization is guesswork without data on what's slow, expensive, or inaccurate
- Deployments carry uncertainty about whether quality meets production standards
- Progress is unmeasurable—you can't tell if you're improving
- Debugging is slow because you lack quantitative evidence of what changed
- Team alignment suffers from subjective disagreements about quality and priorities

## Practical Checklist
Before implementing evaluation metrics, ask yourself:
- [ ] Have I identified 3-5 metrics covering different dimensions (quality, speed, cost, reliability)?
- [ ] Do my chosen metrics align with actual user and business requirements?
- [ ] Can I measure these metrics automatically with available data?
- [ ] Do I have baselines (where we are) and targets (where we need to be)?
- [ ] Am I tracking metrics over time, not just point-in-time measurements?
- [ ] Have I considered trade-offs (e.g., accuracy vs cost, latency vs quality)?
- [ ] Do I have alerting for significant metric degradation?
- [ ] Are metrics interpretable to stakeholders, not just engineers?
- [ ] Am I measuring multiple aspects to avoid gaming single metrics?
- [ ] Do I review and evolve metrics as the system and requirements mature?
- [ ] Have I validated that metrics correlate with real user satisfaction?
- [ ] Am I using metrics to drive decisions, not just dashboards?

## Watch Out For
⚠️ **Vanity metrics**: Metrics that look impressive but don't drive value. "10 million tokens processed!" sounds great but doesn't tell you if users are satisfied, tasks are completed, or business goals are met. Focus on metrics tied to outcomes that matter.

⚠️ **Gaming metrics**: When you optimize for a metric, behavior shifts. If you measure only accuracy, agents might refuse ambiguous questions to avoid errors. If you measure speed only, quality suffers. If you measure cost only, latency explodes. Use multiple balanced metrics and watch for gaming behavior.

⚠️ **Misleading aggregates**: Average latency of 1.2s might hide that 10% of requests take 15+ seconds. Mean accuracy of 85% might mask that specific categories have 40% accuracy. Use percentiles (P50, P95, P99) and segment-level metrics (by category, user type, complexity) to reveal hidden problems.

⚠️ **Lagging indicators**: Many metrics (user satisfaction, churn, NPS) lag by days or weeks. By the time metrics show degradation, damage is done. Combine lagging indicators (ultimate outcomes) with leading indicators (technical metrics like error rate, latency) that signal problems earlier.

⚠️ **Metric proliferation**: Tracking 50 metrics is overwhelming—you can't focus on what matters. Start with 3-5 key metrics tied to critical requirements. Add more only when specific needs arise. "What gets measured gets managed" cuts both ways.

⚠️ **Goodhart's Law**: "When a measure becomes a target, it ceases to be a good measure." Optimizing for accuracy might lead to rejecting hard questions. Optimizing for low cost might sacrifice quality. Use metrics to inform decisions, not as rigid targets that distort behavior.

⚠️ **Ignoring context**: A metric in isolation is meaningless. 2-second latency is fast for complex analysis, slow for simple lookup. 90% accuracy is excellent for medical diagnosis, terrible for spam detection. Always interpret metrics in context of use case, expectations, and alternatives.

⚠️ **Measurement overhead**: Computing metrics has costs—running LLM-as-judge evaluations, logging detailed data, processing evaluations. In production, extensive evaluation can double costs or latency. Use sampling (evaluate 10% of requests), offline evaluation (batch processing), or tiered metrics (lightweight in production, comprehensive in testing).

## Connections
**Builds On:**
- Statistical analysis and data interpretation
- System instrumentation and [logging](../Agent_Operations/logging.md)
- Understanding of [benchmark](benchmark.md) design
- Requirements definition and success criteria

**Works With:**
- [benchmark](benchmark.md) - Standardized test suites use evaluation metrics to score performance
- [a_b_testing](a_b_testing.md) - Metrics determine which variant performs better
- [monitoring](../Agent_Operations/monitoring.md) - Production metrics tracking in real-time
- [observability](../Agent_Operations/observability.md) - Deep insight into system behavior beyond surface metrics
- [performance_metrics](../Agent_Operations/performance_metrics.md) - Specific focus on operational performance
- [model_monitoring](../MLOps/model_monitoring.md) - Tracking ML model metrics in production
- [experiment_tracking](../MLOps/experiment_tracking.md) - Recording metrics across experiments
- [validation](../Safety_and_Control/validation.md) - Metrics validate that outputs meet standards

**Leads To:**
- Data-driven decision making
- Continuous improvement cycles
- SLA/SLO definition (service level objectives based on metrics)
- Cost optimization and resource allocation
- Quality assurance and production confidence

**Related Patterns:**
- [regression_testing](regression_testing.md) - Metrics detect regressions
- [end_to_end_testing](end_to_end_testing.md) - E2E tests measure complete workflow metrics
- [model_drift](../MLOps/model_drift.md) - Metrics detect when model behavior changes
- [confidence_threshold](../Safety_and_Control/confidence_threshold.md) - Metrics determine when confidence is sufficient
- [guardrails](../Safety_and_Control/guardrails.md) - Metrics measure guardrail effectiveness

## Quick Decision Guide
**Invest in comprehensive metrics when:**
- Building production systems where reliability and quality are critical
- Need to justify costs, resource allocation, or technical decisions to stakeholders
- Choosing between multiple models, architectures, or approaches
- Tracking system improvement over time or validating optimization efforts
- Running continuous experiments and need objective comparison
- Quality or performance degradation would have significant user impact
- Operating at scale where manual quality assessment isn't feasible

**Use lightweight or skip when:**
- Building early prototypes where rapid iteration matters more than measurement
- Outcomes are immediately obvious without quantification
- System is simple enough that issues are self-evident
- Resources for instrumentation and analysis exceed benefits
- Changes are trivial and low-risk (fixing typos, minor UI tweaks)
- You're in exploratory phase and don't yet know what matters

## Further Exploration
- 📖 "Designing Data-Intensive Applications" (Martin Kleppmann) - Chapter on metrics and monitoring
- 🎯 OpenAI Evals repository - Practical evaluation frameworks and metrics
- 💡 "Measuring Machine Learning Models" (Google) - ML metrics best practices
- 📖 "Accelerate" (Forsgren et al.) - Research on software delivery metrics
- 🎯 LangChain evaluation modules - Metrics for LLM applications
- 💡 Weights & Biases documentation - Experiment tracking and metrics
- 📖 "How to Measure Anything" (Douglas Hubbard) - Making intangibles measurable
- 🎯 Microsoft Foundry evaluation framework - Enterprise metrics for agent systems (2026)
- 💡 HELM (Holistic Evaluation of Language Models) - Comprehensive LLM evaluation methodology
- 📖 "The Goal" (Eliyahu Goldratt) - Theory of Constraints and meaningful metrics

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
