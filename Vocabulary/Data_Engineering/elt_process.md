# ELT Process

## At a Glance
| | |
|---|---|
| **Category** | Data Integration Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 hours |
| **Prerequisites** | Data lakes, cloud storage, and SQL basics |

## One-Sentence Summary
ELT (Extract, Load, Transform) is a data integration pattern where raw data is loaded into a target system before being transformed for analysis.

## Why This Matters to You
ELT leverages the scalability and performance of modern data platforms, enabling faster data ingestion and flexible transformations. It is a key pattern for cloud-native analytics and data lakes.

## The Core Idea
### What It Is
ELT reverses the traditional ETL process by loading raw data into a target system (e.g., data lake, warehouse) and performing transformations there. This approach takes advantage of the target system’s compute power and scalability.

### What It Isn't
ELT is not suitable for systems with limited compute or storage capabilities.

It is also not a replacement for ETL in all scenarios—ETL is still useful for complex, pre-load transformations.

## How It Works
1. Extract data from source systems.
2. Load raw data into the target system.
3. Transform data within the target system using SQL or other tools.

## Think of It Like This
Think of a train unloading raw materials at a factory, where they are processed into finished goods on-site.

## The "So What?" Factor
**If you use this:**
- You enable faster data ingestion and transformation.
- You reduce data movement and duplication.
- You leverage the scalability of modern data platforms.

**If you don't:**
- Data pipelines may become slower and less flexible.
- Transformation logic may be harder to scale.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Is the target system scalable and performant?
- [ ] Are transformations simple and SQL-friendly?
- [ ] Is raw data storage cost-effective?

## Watch Out For
⚠️ High storage costs for raw data.
⚠️ Complexity in managing transformation logic.

## Connections
**Builds On:** [data_lake.md](data_lake.md), [data_warehouse.md](data_warehouse.md)
**Works With:** [batch_processing.md](batch_processing.md), [data_quality.md](data_quality.md)
**Leads To:** [data_lineage.md](data_lineage.md), [stream_processing.md](stream_processing.md)

## Quick Decision Guide
**Use this when you need to:** Ingest and transform data at scale using modern platforms.
**Skip this when:** Pre-load transformations are complex or critical.

## Further Exploration
- [ELT vs. ETL](https://www.databricks.com/glossary/elt)
- [Modern data integration patterns](https://martinfowler.com/articles/data-lake.html)
- [Cloud-native ELT tools](https://docs.snowflake.com/en/)

---
*Added: May 21, 2026 | Updated: May 21, 2026 | Confidence: High*