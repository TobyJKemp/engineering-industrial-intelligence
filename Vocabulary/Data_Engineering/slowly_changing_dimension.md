# Slowly Changing Dimension (SCD)

## At a Glance
| | |
|---|---|
| **Category** | Data Warehousing Concept |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Data warehousing, dimensional modeling |

## One-Sentence Summary
A Slowly Changing Dimension (SCD) is a data warehousing technique for managing changes to dimension data over time while preserving historical accuracy.

## Why This Matters to You
SCDs enable accurate historical analysis and reporting by tracking changes to dimension attributes. They are essential for building reliable, time-aware data warehouses and analytics systems.

## The Core Idea
### What It Is
SCDs handle changes to dimension data (e.g., customer address) using techniques like overwriting, versioning, or adding timestamps. Common types include:
- **Type 1:** Overwrite changes.
- **Type 2:** Add new rows for changes.
- **Type 3:** Add new columns for changes.

### What It Isn't
SCDs are not transactional—they are designed for analytical systems.

They are also not always simple—choosing the right type depends on business requirements.

## How It Works
1. Identify dimension attributes that may change over time.
2. Choose an SCD type based on analysis needs.
3. Implement ETL logic to handle changes appropriately.

## Think of It Like This
Think of a train schedule that updates routes over time while keeping historical schedules for reference.

## The "So What?" Factor
**If you use this:**
- You enable accurate historical analysis.
- You preserve data integrity and consistency.
- You support time-aware reporting and analytics.

**If you don't:**
- Historical data may be lost or overwritten.
- Analytics and reporting become less reliable.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Are historical changes important for analysis?
- [ ] Is the SCD type aligned with business requirements?
- [ ] Is ETL logic tested for accuracy and performance?

## Watch Out For
⚠️ Increased storage costs for Type 2 SCDs.
⚠️ Complexity in managing multiple SCD types.

## Connections
**Builds On:** [data_warehouse.md](data_warehouse.md), [etl_process.md](etl_process.md)
**Works With:** [data_quality.md](data_quality.md), [schema_design.md](schema_design.md)
**Leads To:** [historical_analysis.md](historical_analysis.md), [data_lineage.md](data_lineage.md)

## Quick Decision Guide
**Use this when you need to:** Track changes to dimension data over time.
**Skip this when:** Historical changes are irrelevant or data is immutable.

## Further Exploration
- [SCD overview](https://en.wikipedia.org/wiki/Slowly_changing_dimension)
- [Kimball dimensional modeling](https://www.kimballgroup.com/)
- [SCD implementation best practices](https://www.databricks.com/blog/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*