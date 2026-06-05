# Industrial Knowledge Graph

## At a Glance
| | |
|---|---|
| **Category** | Knowledge Representation / Data Architecture |
| **Complexity** | Advanced |
| **Time to Learn** | 3-4 weeks to understand concepts, 2-6 months to implement effectively |
| **Prerequisites** | Knowledge graphs, graph databases, ontologies, industrial domain knowledge, semantic web technologies |

## One-Sentence Summary
An Industrial Knowledge Graph is a structured, semantically rich representation of industrial domain knowledge—equipment, processes, materials, relationships, procedures, and historical data—that enables AI systems, engineers, and operations to query, reason about, and optimize complex manufacturing, energy, or infrastructure systems through a unified, context-aware knowledge model.

## Why This Matters to You
Your manufacturing plant has 5,000 pieces of equipment across 12 production lines, maintained by 50 technicians using 200 different procedures, with sensor data from 10,000 monitoring points, and maintenance records spanning 20 years across three legacy systems (CMMS, SCADA, ERP). When equipment fails, technicians spend hours searching: Which procedures apply to this specific model? What were past failure modes? Which spare parts are compatible? What upstream/downstream equipment is affected? The information exists but is scattered, siloed, and lacking context. A pump failure costs 2 hours of troubleshooting and $50,000 in downtime because the technician didn't know this pump model had a known bearing issue fixed by Bulletin TB-2019-045, which was documented in a PDF on a shared drive that only three people knew existed.

An Industrial Knowledge Graph changes this fundamentally: equipment, procedures, parts, failure modes, and their relationships are captured in a unified semantic model. When the pump fails, AI-powered systems instantly query the graph: "For Equipment ID P-1234 (centrifugal pump, Model KSB-Etanorm-125, installed 2018), what are historical failure modes?" Graph returns: bearing failures (12 instances), cavitation issues (5 instances), seal leaks (8 instances). "What maintenance procedures address bearing failures for this model?" Graph returns: Procedure MP-1847 with step-by-step instructions, required tools, safety precautions, and estimated time. "Which spare parts are needed?" Graph returns: Bearing SKF-6309, Seal Kit KSB-98234, O-Ring OR-175 with current inventory levels and supplier information. "Which technicians are certified for this procedure?" Graph returns: 8 technicians with MP-1847 certification, 3 currently on shift. The technician has complete context in 30 seconds, reducing troubleshooting from 2 hours to 20 minutes. In 2026, Industrial Knowledge Graphs are transforming: predictive maintenance (AI queries relationships between sensor patterns and failure modes), training (new technicians query graph for procedures and historical lessons), supply chain optimization (graph models part compatibility and supplier relationships), and regulatory compliance (graph captures traceability and audit trails). For complex industrial systems, a well-designed knowledge graph is the foundation for intelligent operations.

## The Core Idea
### What It Is
An Industrial Knowledge Graph is a graph-structured knowledge base specifically designed to represent the entities, relationships, constraints, and context of industrial domains—manufacturing, energy, utilities, transportation, infrastructure, mining, chemical processing, and similar sectors. It extends general knowledge graph principles with industrial-specific semantics, standards, and requirements.

Core components of an Industrial Knowledge Graph:

**Industrial Entities (Nodes)** - Represent domain-specific concepts: physical assets (equipment, machines, instruments, facilities, locations), materials and products (raw materials, intermediate products, finished goods, specifications), processes and operations (production steps, procedures, recipes, workflows), people and organizations (technicians, operators, engineers, suppliers, contractors), documents and data (manuals, procedures, drawings, sensor data, reports), and events and incidents (failures, maintenance actions, quality issues, safety events). Each entity has properties (attributes) and a type from an industrial ontology.

**Industrial Relationships (Edges)** - Capture how entities connect: physical relationships (part-of, connected-to, located-at, upstream-of, downstream-of), functional relationships (maintains, operates, produces, consumes, requires), temporal relationships (precedes, follows, occurred-during, valid-from/to), causal relationships (caused-by, results-in, correlates-with), and procedural relationships (step-of, requires-tool, requires-skill, requires-part). Relationships are typed and often have properties (relationship strength, confidence, temporal validity).

**Industrial Ontologies and Taxonomies** - Define structure and semantics: equipment taxonomies (pump → centrifugal pump → end-suction pump → specific model), material classifications (steel → stainless steel → 316L stainless → heat-treated 316L), process hierarchies (manufacturing → assembly → sub-assembly → component installation), and failure mode taxonomies (mechanical failure → bearing failure → inner race failure). Ontologies provide shared vocabulary, enable reasoning, and facilitate interoperability. Industry standards like ISO 15926, IEC 62264, ISA-95 inform ontology design.

**Contextual Metadata** - Rich context enables intelligent querying: temporal context (when was this relationship valid? Installation date, decommission date), spatial context (where? Plant, building, line, zone), provenance (who created/modified this knowledge? Source system, confidence level, last verified date), and versioning (knowledge evolves; graph tracks changes over time). Metadata enables trust and traceability.

**Integration with Operational Data** - Industrial Knowledge Graphs aren't just static reference data; they integrate dynamic operational data: sensor telemetry (graph relates sensors to equipment, enabling "show me temperatures for all pumps on Line 3"), maintenance records (graph connects maintenance actions to equipment and failure modes), quality data (graph links quality measurements to processes and materials), and supply chain data (graph models inventory, procurement, logistics). This hybrid of reference knowledge and live operational data is powerful.

Industrial Knowledge Graphs leverage graph database technologies (Neo4j, Amazon Neptune, Azure Cosmos DB with Gremlin, TigerGraph, Stardog for RDF/OWL-based graphs) and semantic web standards (RDF, OWL, SPARQL for more formal semantic graphs). The choice depends on requirements: property graphs (Neo4j, Gremlin) for flexibility and performance; RDF/OWL for formal semantics, standardization, and reasoning.

Use cases enabled by Industrial Knowledge Graphs:

**Intelligent Maintenance** - Predictive and prescriptive maintenance powered by graph queries: "Which equipment has sensor patterns similar to past failures?" (graph relates current sensor data to historical failure patterns), "What maintenance procedures prevent this failure mode?" (graph connects failure modes to preventive procedures), "Which spare parts are needed for likely failures in next 30 days?" (graph predicts failures, maps to parts, checks inventory), and "Optimize maintenance scheduling across all equipment considering dependencies" (graph knows upstream/downstream relationships, schedules to minimize production impact).

**Root Cause Analysis** - When incidents occur, graph-powered RCA: "What changed in the 24 hours before the failure?" (graph tracks configuration changes, material batches, personnel, environmental conditions), "Which upstream equipment or process issues might have caused this?" (traverse graph from failed equipment upstream through process flow), "What are common factors across similar failures?" (graph pattern matching finds recurring themes), and "Visualize the causal chain leading to this event" (graph renders causal paths for investigation teams).

**Process Optimization** - Manufacturing and process optimization using graph insights: "Which process parameters most influence product quality?" (graph models relationships between parameters and outcomes), "What are alternative material suppliers with compatible specifications?" (graph models material properties, supplier capabilities, qualification status), "How does changing this process step affect downstream operations?" (graph simulates impact propagation), and "Identify bottlenecks and optimization opportunities across production lines" (graph analysis finds constraints).

**Compliance and Traceability** - Regulatory compliance and audit trails: "Trace this product batch back to raw material sources" (graph captures full material genealogy), "Which equipment was involved in producing this batch?" (graph links batches to production equipment and personnel), "Verify all required quality checks were performed" (graph models quality procedures and execution records), and "Generate audit reports showing compliance with regulations" (graph queries extract evidence for audits).

**Knowledge Discovery and Training** - Organizational knowledge management: "Find all documents and procedures related to this equipment" (graph links equipment to procedures, manuals, work instructions), "What lessons learned are relevant to this situation?" (graph connects incidents to lessons learned), "Which experts have experience with this failure mode?" (graph tracks personnel skills and historical actions), and "Generate training materials for new operators on this process" (graph extracts relevant knowledge for curriculum).

**Supply Chain Intelligence** - Supply chain and inventory optimization: "Which parts are single-source or have long lead times?" (graph models supplier relationships and constraints), "What are substitute parts for critical components?" (graph captures part compatibility and alternatives), "Predict part demand based on equipment failure patterns" (graph relates equipment reliability to spare parts consumption), and "Optimize inventory levels considering equipment criticality and failure rates" (graph-based optimization).

For AI systems in 2026, Industrial Knowledge Graphs are foundational:

**Context for AI Models** - Knowledge graphs provide context that improves AI: augment sensor data with equipment metadata (model, age, maintenance history) for better predictions, ground language models in factual industrial knowledge (LLMs query graph for accurate domain information), enable explainable AI (graph shows reasoning paths: why did model predict failure? Because sensor pattern X correlates with failure mode Y in graph), and facilitate few-shot learning (graph provides examples and relationships for new scenarios).

**Multi-Agent Coordination** - In multi-agent industrial systems, the knowledge graph is shared state: maintenance scheduling agent queries graph for equipment dependencies, inventory management agent updates graph with stock levels, quality assurance agent records quality data in graph, and production planning agent queries graph for capacity and constraints. The graph enables agents to coordinate through shared, semantically consistent knowledge.

**Digital Twin Integration** - Industrial Knowledge Graphs underpin digital twins: the graph is the "skeleton" connecting physical assets to their digital representations, simulation models query graph for asset properties and relationships, real-time data from digital twin feeds back to graph (closing the loop), and the combination enables sophisticated simulations (e.g., "simulate impact of equipment failure on production, considering all dependencies in graph").

### What It Isn't
An Industrial Knowledge Graph is not just a relational database with foreign keys. While relational databases model relationships through keys and joins, knowledge graphs provide: richer semantics (relationships are first-class citizens with types and properties), flexible schema (easy to add new relationship types without schema migration), graph-specific queries (traversals, pattern matching, centrality analysis), and reasoning capabilities (infer new knowledge from existing relationships). Knowledge graphs complement, not replace, operational databases.

It's also not a document management system or data lake. While these store industrial documents and data, they lack semantic structure: documents are opaque blobs, search is keyword-based, relationships are implicit (not explicit and queryable), and reasoning is impossible. Knowledge graphs extract structured knowledge from documents and data, making it queryable and actionable.

Industrial Knowledge Graphs are not static reference data. They're living knowledge bases: continuously updated with operational data (sensor readings, maintenance records, quality measurements), versioned and evolved (ontologies refined, relationships added, corrections made), and queried in real-time (power operational decisions, not just reporting). Treating knowledge graphs as static data warehouses misses their value.

The pattern is not universally applicable. Building and maintaining a knowledge graph requires significant investment: ontology design (domain expertise, consensus building), data integration (mapping legacy systems to graph model), quality assurance (ensuring accuracy and consistency), and governance (who owns which knowledge? Who can modify?). For simple domains or small-scale operations, simpler approaches (spreadsheets, relational databases, documentation wikis) may suffice. Knowledge graphs are justified when complexity, scale, and integration needs demand their capabilities.

Finally, Industrial Knowledge Graphs don't eliminate human expertise. They augment humans: codifying expertise makes it accessible, but human judgment is still needed for complex decisions, edge cases, and novel situations. Graphs are tools for experts, not replacements. Over-reliance on graph queries without human oversight risks propagating errors or missing context.

## How It Works
Implementing an Industrial Knowledge Graph follows these patterns:

1. **Define Scope and Use Cases** - Start with clear objectives: which business problems will the graph solve? (maintenance optimization, compliance traceability, process optimization?), which domains to include? (equipment, materials, processes, all of the above?), which users and applications will consume the graph? (technicians, AI models, business analysts?), and what ROI is expected? (reduced downtime, improved compliance, faster troubleshooting?). Scope determines ontology complexity and data integration priorities.

2. **Design Industrial Ontology** - Create domain-specific ontology: identify entity types (equipment classes, material types, process types, document types), define relationship types (physical connections, functional dependencies, procedural steps), establish taxonomies and hierarchies (equipment taxonomy, failure mode taxonomy), incorporate industry standards (ISO 15926 for process industries, IEC 62264 for manufacturing, ISA-95 for automation), and involve domain experts (engineers, operators, maintenance teams validate ontology). Document ontology formally (OWL, RDFS) or informally (diagrams, specification documents).

3. **Assess Data Sources** - Inventory existing data to populate graph: equipment master data (CMMS, EAM systems), process and instrumentation diagrams (P&IDs, CAD drawings), maintenance records (work orders, failure reports), sensor and telemetry data (SCADA, historians), quality data (QMS, laboratory systems), documents (manuals, procedures, technical bulletins), and tribal knowledge (interviews, workshops with experienced personnel). Map each source to ontology entities and relationships.

4. **Implement Data Integration** - Extract, transform, load (ETL) data into graph: build connectors to source systems (APIs, database queries, file exports), map source data to graph ontology (equipment records → equipment nodes with properties), resolve entities (same equipment appearing in multiple systems), infer relationships (extract relationships from P&IDs, procedure documents, maintenance records), and validate data quality (completeness, accuracy, consistency). Use ETL tools (Informatica, Talend), custom scripts, or graph-native ingestion (Neo4j import, RDF bulk loaders).

5. **Choose Graph Database Technology** - Select appropriate graph database: property graphs (Neo4j for mature ecosystem and performance, Amazon Neptune for AWS-native, TigerGraph for massive scale, Azure Cosmos DB for Azure integration), RDF/OWL graphs (Stardog for formal reasoning and standards, GraphDB for semantic search, Apache Jena for open-source), or hybrid (some systems support both). Consider query patterns, scale requirements, reasoning needs, and existing technology stack.

6. **Build Graph Querying APIs** - Provide access to graph knowledge: query API (REST or GraphQL API exposing common queries: "get equipment by ID," "find related equipment," "search by property"), graph query language access (Cypher for Neo4j, Gremlin for Tinkerpop, SPARQL for RDF—for advanced users), natural language query interface (LLM-powered: "show me all pumps with high vibration"), and visualization (graph rendering for exploration, dashboards for operational monitoring). Design APIs for target users (technicians need simple queries, data scientists need full graph access).

7. **Implement Knowledge Enrichment** - Continuously improve graph: entity resolution and deduplication (merge duplicate equipment records from different sources), relationship inference (if A connects to B and B connects to C, infer A upstream-of C), knowledge extraction from documents (NLP to extract entities and relationships from procedures, manuals, incident reports), and reasoning (ontology-based reasoning: if X is-a subtype of Y, inherit Y's properties). Enrichment improves graph completeness and utility.

8. **Integrate with Operational Systems** - Make graph operational, not just analytical: real-time data integration (stream sensor data, maintenance updates, quality measurements into graph), bidirectional sync (updates in CMMS reflected in graph, graph-based decisions written back to CMMS), AI/ML integration (models query graph for context, write predictions back to graph), and application embedding (maintenance apps, operator interfaces query graph for context-aware information). Graph becomes living operational knowledge base.

9. **Establish Governance and Quality** - Ensure graph accuracy and trust: data stewardship (assign ownership for domains: equipment data owner, process data owner), quality metrics (completeness, accuracy, freshness—monitor and report), update procedures (how are changes approved? Who can modify ontology? Data?), and versioning (track ontology versions, data provenance, audit trail of changes). Governance is essential for enterprise adoption—poor quality graphs lose trust.

10. **Build User Interfaces and Applications** - Enable access for different personas: technician mobile app (query graph for equipment info, procedures, troubleshooting guides), engineer workbench (graph exploration, analysis, knowledge curation), operator dashboard (real-time equipment status, alerts, relationships), and analyst tools (graph analytics, pattern discovery, optimization). Applications make graph valuable; raw database access isn't sufficient.

11. **Implement Graph Analytics** - Extract insights from graph structure: centrality analysis (identify most critical equipment—many connections, high betweenness centrality), community detection (find clusters of related equipment or failure modes), path analysis (shortest path between equipment, trace material flow), pattern matching (find recurring failure patterns, similar equipment configurations), and graph-based machine learning (node classification, link prediction, graph neural networks). Analytics unlock deeper insights than simple queries.

12. **Enable Continuous Learning** - Graph evolves with operational experience: capture feedback (users flag incorrect relationships, add missing knowledge), integrate lessons learned (post-incident reports enrich failure mode knowledge), track model performance (AI predictions using graph—track accuracy, update graph to improve), and refine ontology (add entity types, relationship types as understanding deepens). Static graphs become stale; continuous learning maintains relevance.

13. **Scale and Optimize Performance** - As graph grows, optimize: indexing (index frequently queried properties), query optimization (analyze slow queries, optimize traversals), partitioning/sharding (for massive graphs, partition across servers), caching (cache frequently accessed subgraphs), and archival (move historical data to cold storage, keep recent data hot). Monitor query performance and graph size.

14. **Integrate with AI/ML Workflows** - Use graph to enhance AI: feature engineering (graph features: node degree, centrality, neighborhood properties enrich ML features), graph neural networks (GNNs learn representations from graph structure), knowledge graph embeddings (TransE, DistMult, ComplEx—create vector representations of entities for similarity, prediction), and hybrid reasoning (combine graph queries with ML predictions for explainable AI). Graph + AI is more powerful than either alone.

## Think of It Like This
Imagine a massive industrial facility as a city, and you need to navigate and understand it. A traditional database is like an address book: lists of buildings, people, and phone numbers—useful for lookups but tells you nothing about relationships. An Industrial Knowledge Graph is like a detailed city map with metadata: not just building locations but also what they're connected to (roads, utilities, communication lines), who uses them (businesses, residents), their history (construction dates, renovations, incidents), and rules governing them (zoning, regulations, access controls). When you need to understand "if this power substation fails, what's affected?"—the map shows you immediately through visual connections. When you ask "which buildings had similar fire safety issues?"—the map's metadata reveals patterns. When you plan maintenance "which road closures minimize traffic impact?"—the map's relationships enable optimization. Industrial Knowledge Graphs are this rich, connected, context-aware map for complex industrial systems—enabling navigation, understanding, and intelligent decision-making that flat lists of data can't provide.

## The "So What?" Factor
**If you use Industrial Knowledge Graphs:**
- Troubleshooting accelerates—technicians find relevant procedures, parts, and historical context in seconds instead of hours
- AI models improve—contextual knowledge enhances predictions, enables explainability, grounds LLMs in facts
- Compliance simplifies—complete traceability and audit trails are queries away, not manual report generation
- Knowledge preserved—tribal knowledge codified, survives retirements and turnover
- Integration unified—heterogeneous systems (CMMS, ERP, SCADA, QMS) connected through semantic layer
- Optimization enabled—graph analytics identify bottlenecks, inefficiencies, and improvement opportunities
- Training accelerated—new personnel access complete operational knowledge, reducing onboarding time

**If you don't:**
- Knowledge remains siloed—information trapped in systems, documents, and individuals' heads
- Troubleshooting is slow—hours wasted searching for procedures, parts, precedents across systems
- AI lacks context—models operate on raw data without domain knowledge, limiting accuracy and explainability
- Compliance is manual—generating audit trails requires laborious data gathering from multiple sources
- Integration is point-to-point—N systems × M systems = N×M integration points, fragile and costly
- Optimization is guesswork—lack of holistic view prevents identifying systemic inefficiencies
- Knowledge loss—retirements and turnover take critical operational knowledge with them

## Practical Checklist
Before implementing an Industrial Knowledge Graph, ask yourself:
- [ ] Do I have complex industrial systems with many interrelated entities (equipment, processes, materials)?
- [ ] Is knowledge currently siloed across multiple systems (CMMS, ERP, SCADA, documents)?
- [ ] Do I have use cases that require understanding relationships and context (maintenance, compliance, optimization)?
- [ ] Am I prepared to invest in ontology design and domain expert involvement?
- [ ] Can I integrate multiple data sources and ensure ongoing data quality?
- [ ] Do I have graph database expertise or ability to acquire it (or partners/vendors)?
- [ ] Are there clear ROI drivers (reduced downtime, faster troubleshooting, better compliance)?
- [ ] Can I establish governance for a shared knowledge base (ownership, quality, update processes)?
- [ ] Do I have executive sponsorship and cross-functional buy-in for this strategic initiative?
- [ ] Is my organization ready for cultural shift toward shared, structured knowledge?

## Watch Out For
⚠️ **Ontology Design Complexity** - Designing good industrial ontologies is hard: balancing generality (flexible, reusable) vs specificity (captures domain nuances), achieving consensus among diverse stakeholders (engineers, operators, IT), evolving ontology as understanding deepens without breaking existing applications, and avoiding over-engineering (overly complex ontologies nobody uses). Start simple, iterate based on use cases, involve domain experts heavily, and accept that ontology will evolve—design for evolution.

⚠️ **Data Quality and Integration Challenges** - Industrial data is notoriously messy: inconsistent identifiers (same equipment different IDs in different systems), missing data (incomplete maintenance records, undocumented relationships), errors (typos, outdated information, incorrect relationships), and semantic mismatches (different systems use different terminology). Plan for extensive data cleaning, validation, and ongoing quality monitoring. Poor data quality → poor graph quality → lost user trust.

⚠️ **Scope Creep and Over-Ambition** - The temptation to model everything is strong: every asset, every process, every relationship across the entire enterprise. This leads to: multi-year projects that never deliver value, complexity that overwhelms users and maintainers, and stakeholder fatigue. Start with focused use cases (predictive maintenance for critical equipment, compliance traceability for one product line), prove value, expand incrementally. MVP approach over big-bang deployment.

⚠️ **Governance and Change Management** - A shared knowledge base requires shared governance, which is organizationally challenging: who owns equipment data? Process data? Who approves ontology changes? How to handle conflicts? And culturally, shifting from personal knowledge ("I know where the info is") to shared knowledge ("it's in the graph") meets resistance. Establish governance early, involve stakeholders in design, demonstrate value to overcome resistance, and provide training. Technical success without organizational adoption fails.

⚠️ **Performance at Scale** - Graph databases have different performance characteristics than relational databases: certain queries (multi-hop traversals, pattern matching) can be slow on large graphs, some graph databases struggle with billions of nodes/edges, and query optimization requires different thinking (graph-specific patterns, indexing strategies). Test performance early with realistic data volumes and query patterns, optimize indexes, consider sharding for massive scale, and cache frequently accessed subgraphs.

⚠️ **Integration Maintenance Burden** - Once built, the graph must stay synchronized with source systems: data integration pipelines require ongoing maintenance (APIs change, schemas evolve, systems are upgraded), data quality degrades without monitoring and correction, and bidirectional sync (if implemented) creates complexity and potential conflicts. Budget for operational maintenance—graph isn't build-once-and-forget; it's continuous integration effort.

⚠️ **Reasoning Complexity and Pitfalls** - Automated reasoning (inferring new knowledge from ontology rules) can introduce: inference explosions (small ontology changes create millions of inferred triples), reasoning performance issues (complex ontologies slow query performance), and incorrect inferences (bugs in ontology logic create wrong relationships). Use reasoning judiciously, test ontology logic thoroughly, monitor inferred knowledge for errors, and provide mechanisms to override incorrect inferences.

## Connections
**Builds On:** Knowledge graphs, graph databases, ontologies, semantic web (RDF, OWL, SPARQL), industrial domain knowledge

**Works With:** Digital twins, predictive maintenance systems, CMMS/EAM systems, process historians, AI/ML pipelines

**Leads To:** Cognitive industrial systems, autonomous operations, industrial metaverse, graph neural networks for industrial applications

## Quick Decision Guide
**Use this when you need to:** Integrate knowledge across siloed industrial systems, enable intelligent maintenance and operations through contextual information, provide traceability and compliance for complex processes, support AI/ML with rich domain context, or scale knowledge management across large industrial operations.

**Skip this when:** Domain is simple with few entities and relationships (spreadsheet suffices), knowledge is already well-integrated (single source of truth exists), organization lacks maturity for semantic data management, or use cases don't require understanding relationships and context (reporting, simple lookups fine).

## Further Exploration
- 📖 [Knowledge Graphs: Data in Context for Responsive Businesses](https://www.manning.com/books/knowledge-graphs) - Jesús Barrasa et al. on knowledge graph design and implementation
- 🎯 [ISO 15926: Industrial Data Standards](https://www.iso.org/standard/29557.html) - International standard for industrial knowledge representation
- 💡 [Neo4j Use Cases: Manufacturing and Supply Chain](https://neo4j.com/use-cases/manufacturing-supply-chain/) - Industrial knowledge graph examples
- 📖 [Building Knowledge Graphs](https://www.oreilly.com/library/view/building-knowledge-graphs/9781098127091/) - Douglas McIlwraith on practical knowledge graph construction
- 🎯 [Stardog: Enterprise Knowledge Graphs](https://www.stardog.com/) - Industrial RDF/OWL knowledge graph platform
- 💡 [Asset Administration Shell (AAS)](https://www.plattform-i40.de/IP/Redaktion/EN/Standardartikel/specification-administrationshell.html) - Industry 4.0 digital twin and knowledge model standard
- 📖 [The Knowledge Graph Cookbook](https://github.com/wsheridan/knowledge-graph-cookbook) - Practical recipes for building domain-specific knowledge graphs
- 🎯 [AWS Industrial Knowledge Graphs](https://aws.amazon.com/neptune/knowledge-graphs-on-aws/) - Cloud-based industrial KG solutions

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
