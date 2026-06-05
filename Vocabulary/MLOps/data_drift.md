# Data Drift

## At a Glance
| | |
|---|---|
| **Category** | Model Monitoring Concept |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Data distribution, model evaluation |

## One-Sentence Summary
Data drift refers to changes in the statistical properties of input data over time, which can impact model performance.

## Why This Matters to You
Data drift can lead to reduced model accuracy and reliability in production. Detecting and addressing drift ensures that models remain effective and trustworthy. Understanding data drift is essential for maintaining robust AI systems.

## The Core Idea
### What It Is
Data drift occurs when the distribution of input features changes over time. This can happen due to changes in user behavior, data collection methods, or external factors.

Types of data drift include:
- **Covariate Drift:** Changes in feature distributions.
- **Prior Probability Shift:** Changes in the distribution of target classes.
- **Concept Drift:** Changes in the relationship between features and the target variable.

### What It Isn't
Data drift is not the same as concept drift, which involves changes in the feature-target relationship.

It is also not always harmful—some drift may be benign or expected.

## How It Works
1. Monitor input data distributions over time.
2. Compare current distributions to historical baselines.
3. Trigger alerts or retraining workflows when drift exceeds thresholds.

## Think of It Like This
Think of a river that changes its course over time, requiring adjustments to bridges and infrastructure.

## The "So What?" Factor
**If you use this:**
- You maintain model accuracy and reliability.
- You adapt to changing data environments.
- You reduce the risk of poor decision-making.

**If you don't:**
- Models become less effective over time.
- Business outcomes and user trust are negatively impacted.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are drift detection metrics and thresholds defined?
- [ ] Is monitoring automated and real-time?
- [ ] Are retraining workflows in place?

## Watch Out For
⚠️ False positives from normal data variability.
⚠️ Delayed detection leading to performance degradation.

## Connections
**Builds On:** [model_monitoring.md](model_monitoring.md), [concept_drift.md](concept_drift.md)
**Works With:** [model_retraining.md](model_retraining.md), [experiment_tracking.md](experiment_tracking.md)
**Leads To:** [adaptive_models.md](adaptive_models.md), [data_quality.md](data_quality.md)

## Quick Decision Guide
**Use this when you need to:** Detect and address changes in input data distributions.
**Skip this when:** The data environment is static and unchanging.

## Further Exploration
- [Data drift overview](https://en.wikipedia.org/wiki/Data_drift)
- [Drift detection techniques](https://www.kdnuggets.com/)
- [MLOps monitoring tools](https://mlops.org/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*