# Publish-Subscribe (Pub/Sub)

## At a Glance
| | |
|---|---|
| **Category** | Messaging Pattern / Integration Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 3-5 days to understand concepts, 2-3 weeks to implement effectively |
| **Prerequisites** | Distributed systems basics, asynchronous communication, message queues |

## One-Sentence Summary
Publish-Subscribe (Pub/Sub) is a messaging pattern where message producers (publishers) send messages to named topics or channels without knowledge of message consumers (subscribers), enabling dynamic, scalable, loosely-coupled communication where multiple subscribers can independently receive and process messages based on their interests.

## Why This Matters to You
You're building an AI agent system where a document processing agent extracts insights, multiple downstream agents need those insights (summarization agent, classification agent, knowledge graph builder, search indexer), and a monitoring dashboard needs real-time status updates. With point-to-point messaging, your document agent must know about every downstream consumer and send separate messages to each—adding a new consumer requires modifying the document agent code. When a downstream service goes offline, your document agent must handle failures, implement retries, and manage queues for each consumer individually. The tight coupling means every change cascades through your system, and scaling becomes a coordination nightmare as you track dependencies between dozens of agents.

Pub/Sub solves this: your document agent publishes "DocumentProcessed" events to a topic and continues working—it doesn't know or care who's listening. Each downstream agent subscribes to the topic and receives events independently. Adding a new agent (fraud detection, audit logging) requires zero changes to the document agent—just subscribe to the topic. If the summarization agent goes offline, only it misses messages; other subscribers are unaffected. The monitoring dashboard subscribes to the same topic to display real-time progress. This decoupling is fundamental to scalable, evolvable AI systems. In 2026's multi-agent environments—where agents are dynamically added, removed, scaled, and reconfigured—Pub/Sub is the standard pattern for agent-to-agent communication, event-driven workflows, real-time data distribution, and system observability.

## The Core Idea
### What It Is
Publish-Subscribe (Pub/Sub) is a messaging pattern that decouples message senders from message receivers through an intermediary abstraction called a topic (or channel, subject, or exchange depending on the implementation). Publishers send messages to topics without knowledge of subscribers; subscribers express interest in topics and receive all messages published to those topics without knowledge of publishers. A message broker or event bus manages topic subscriptions, message routing, and delivery.

The pattern has three core components:

**Publishers** - Services or components that produce messages and publish them to named topics. Publishers are unaware of subscribers: they don't know how many there are, which ones exist, or whether any are listening. Publishers simply send messages to a topic identifier (e.g., "user.registered," "document.processed," "model.inference.completed") and continue their work. Publishing is typically fire-and-forget: the publisher receives acknowledgment that the message was accepted by the broker, not that subscribers processed it successfully.

**Topics/Channels** - Named logical channels representing message categories or event types. Topics serve as the decoupling layer: publishers target topics, subscribers select topics. Topics can be structured hierarchically (e.g., "sensors.temperature.warehouse.zone-a") enabling subscription wildcards or filters. Messages sent to a topic are distributed to all subscribers of that topic (fanout pattern). Topics persist in the broker until subscribers consume messages (depending on broker guarantees and configuration).

**Subscribers** - Services or components that register interest in one or more topics and receive messages published to those topics. Subscribers can subscribe at any time—before publishers start publishing or dynamically during runtime. Multiple subscribers can listen to the same topic, each receiving their own copy of every message (broadcast). Subscribers process messages asynchronously and independently; one subscriber failing or being slow doesn't affect others. Subscribers can be added or removed without publisher changes.

The **Message Broker** (or Event Bus) sits between publishers and subscribers, handling:
- **Topic Management** - Creating, configuring, and maintaining topics/channels
- **Subscription Management** - Tracking which subscribers are interested in which topics
- **Message Routing** - Delivering published messages to all active subscribers of the target topic
- **Delivery Guarantees** - Ensuring messages are delivered according to configured semantics (at-most-once, at-least-once, exactly-once)
- **Message Persistence** - Storing messages until subscribers acknowledge consumption (for durable subscriptions)
- **Filtering** - Supporting message filtering based on content, headers, or patterns so subscribers receive only relevant subset

Common Pub/Sub implementations include:
- **Apache Kafka** - Distributed streaming platform, high-throughput, persistent topics (partitioned logs), strong ordering guarantees, ideal for event sourcing and real-time data pipelines
- **RabbitMQ** - Message broker supporting multiple patterns including Pub/Sub via exchanges, flexible routing, strong AMQP standard support
- **Google Cloud Pub/Sub** - Fully managed serverless messaging, global scale, automatic retry and dead-letter queuing, integrates with Google Cloud services
- **AWS SNS/SQS** - SNS for fanout (pub/sub), SQS for queuing (point-to-point), often combined for scalable distributed messaging
- **Azure Service Bus** - Enterprise messaging with topics and subscriptions, advanced features like sessions, transactions, duplicate detection
- **Redis Pub/Sub** - Lightweight, low-latency messaging, no persistence (in-memory only), ideal for real-time notifications
- **MQTT** - Lightweight protocol for IoT and mobile, hierarchical topics, quality-of-service levels, used in telemetry and sensor networks
- **NATS** - High-performance cloud-native messaging, subject-based addressing, lightweight and simple

Pub/Sub patterns vary in delivery semantics:

**At-Most-Once Delivery** - Messages delivered zero or one time; if delivery fails, message is lost. Lowest overhead, fastest, acceptable for non-critical data (metrics, logs, sensor readings where occasional loss is tolerable). Redis Pub/Sub operates this way.

**At-Least-Once Delivery** - Messages delivered one or more times; duplicates possible if retries occur after transient failures. Requires idempotent message processing (handlers must safely handle duplicate messages). Most common in production systems (Kafka, RabbitMQ, cloud services). Balances reliability and performance.

**Exactly-Once Delivery** - Messages delivered exactly one time, no duplicates. Most complex to implement, requires distributed coordination between broker and subscribers. Kafka provides exactly-once semantics with careful configuration; cloud services offer similar guarantees. Necessary for financial transactions, critical state updates, or workflows where duplicates cause incorrect behavior.

Pub/Sub supports several advanced patterns:

**Topic Hierarchies and Wildcards** - Topics organized hierarchically (e.g., "app.service.event") with wildcard subscriptions: "app.service.*" receives all events for that service, "app.#" receives all events under app. MQTT, NATS, and some AMQP brokers support this.

**Content-Based Filtering** - Subscribers specify filters (message attributes, header values, or content matching expressions) so broker delivers only matching messages. Reduces network traffic and unnecessary processing. AWS SNS, Azure Service Bus support filter expressions.

**Message Replay** - Kafka's log-based architecture allows subscribers to rewind and replay messages from past offsets, enabling recovery from failures, backfilling new subscribers, or reprocessing for corrections. Essential for event sourcing and data pipeline debugging.

**Dead-Letter Queues** - Messages that fail processing repeatedly (after configured retry attempts) are moved to dead-letter topics/queues for investigation, preventing poison messages from blocking subscriptions. Google Pub/Sub, AWS, Azure provide built-in dead-letter handling.

For AI and ML systems in 2026, Pub/Sub is foundational:

**Multi-Agent Communication** - Agents publish events (task completed, insight discovered, decision made) to topics; other agents subscribe to relevant topics and react. Enables composable, loosely-coupled agent ecosystems where agents can be added/removed dynamically without central coordination.

**Real-Time Data Pipelines** - Streaming data (logs, sensor telemetry, user events, application metrics) published to topics flows through ML pipelines: feature extraction, model inference, result storage, alerting. Each stage subscribes to input topics and publishes to output topics. Kafka is standard for this.

**Model Serving and Inference** - Applications publish inference requests to "inference.request" topic; model serving infrastructure subscribes, processes requests, publishes results to "inference.response" topic. Decouples clients from model servers, enables A/B testing (multiple model versions subscribe to same topic), and simplifies scaling (add more subscribers for capacity).

**Training Data Collection** - Application events, user interactions, and system telemetry published to topics are consumed by data collection pipelines that curate training datasets, label data, and trigger model retraining workflows. Pub/Sub enables continuous learning loops.

**Monitoring and Observability** - All system components publish metrics, logs, and traces to observability topics; monitoring dashboards, alerting systems, and analytics tools subscribe. Centralized telemetry without tight coupling between application components and monitoring infrastructure.

**Human-in-the-Loop Workflows** - AI agents publish events requiring human judgment ("approval.needed," "ambiguous.result," "confidence.low"); human interface applications subscribe and present items for review. Human decisions are published to response topics, feeding back to agent workflows. Pub/Sub decouples AI processing from UI/human interaction layers.

### What It Isn't
Pub/Sub is not the same as point-to-point messaging (message queues). In point-to-point, messages sent to a queue are consumed by exactly one consumer (competing consumers pattern); in Pub/Sub, messages sent to a topic are received by all subscribers (broadcast pattern). Many brokers support both: RabbitMQ queues for point-to-point, exchanges for Pub/Sub; AWS SQS for queues, SNS for Pub/Sub; Kafka partitions can model both depending on consumer group configuration.

It's also not synchronous request-response. Pub/Sub is asynchronous and fire-and-forget: publishers don't wait for subscriber processing or responses. For request-response semantics, use RPC patterns, REST APIs, or combine Pub/Sub with correlation IDs (publish request, subscribe to reply topic with matching correlation ID). Pub/Sub suits event notification, data distribution, and decoupled workflows, not interactive query/response.

Pub/Sub doesn't guarantee ordering across topics or for all subscribers. Kafka provides ordering within a partition (messages with same key go to same partition and are ordered); other brokers may deliver messages in published order to individual subscribers but not across subscribers or topics. If ordering is critical, use single-partition topics or ordered message brokers, or design message processing to handle out-of-order delivery.

The pattern is not fire-and-forget without consequences. Publishers are decoupled from subscribers, but messages still must be processed. Unprocessed messages accumulate (backpressure), failed processing requires retry logic or dead-lettering, and downstream failures aren't visible to publishers unless explicitly monitored. Pub/Sub shifts responsibility from publishers to subscribers and operational monitoring—don't assume "publish and forget" means problems disappear.

Finally, Pub/Sub isn't a database or persistent storage system (with the exception of Kafka's log-based architecture). Messages are transient: once consumed and acknowledged, they're typically deleted. For durable storage, combine Pub/Sub with databases (subscribers write to databases), event sourcing (messages are append-only logs), or use Kafka's persistent topics for replay. Pub/Sub is transport and communication, not long-term data storage.

## How It Works
Implementing and using Pub/Sub follows these patterns:

1. **Choose a Message Broker** - Select broker based on requirements: throughput (Kafka for high-volume streaming, RabbitMQ for moderate enterprise workloads), persistence (Kafka for replay, Redis for ephemeral), delivery guarantees (exactly-once needs Kafka or careful configuration), operational preferences (managed cloud services like Google Pub/Sub/AWS SNS vs self-hosted), ecosystem integration (existing infrastructure, client library support), and cost (cloud managed services vs infrastructure costs).

2. **Design Topic Structure** - Name topics clearly and consistently: use hierarchical naming (e.g., "domain.entity.event" like "inventory.product.updated"), avoid overly broad topics (don't publish everything to "events"), group related events logically, and consider future evolution (versioning topics like "user.v1.registered" for schema changes). Topic design affects subscription management and system clarity.

3. **Configure Delivery Semantics** - Set appropriate guarantees: at-most-once for telemetry and non-critical logs (performance priority), at-least-once for most application events (balance reliability and performance, ensure idempotent subscribers), and exactly-once for financial transactions and critical state changes (accept complexity and potential throughput reduction). Configure broker-specific settings: Kafka producer acks, consumer offsets, RabbitMQ acknowledgments.

4. **Implement Publishers** - Publishers connect to broker, publish messages to topics, and handle failures. Best practices: include message metadata (timestamp, source, correlation ID for tracing), use structured formats (JSON, Avro, Protocol Buffers) for schema evolution, batch messages when appropriate for throughput (Kafka supports batching), handle broker unavailability (retry with exponential backoff, dead-letter for permanent failures), and monitor publish latency and success rates.

5. **Implement Subscribers** - Subscribers connect to broker, subscribe to topics, process messages, and acknowledge consumption. Best practices: process messages idempotently (assume at-least-once delivery even if broker claims exactly-once), handle malformed messages gracefully (validation, logging, dead-letter), implement error handling and retries (transient vs permanent failures), ack messages only after successful processing (prevents message loss), and monitor processing latency and error rates.

6. **Handle Backpressure** - When subscribers can't keep up with message rate, messages accumulate in broker (topic lag in Kafka terms). Mitigate with: scaling subscribers horizontally (add more instances consuming from same topic/partition), optimizing message processing (reduce per-message latency), batching (process multiple messages together), filtering (subscribe only to necessary messages), and alerting on lag thresholds (detect backpressure early).

7. **Manage Subscriptions** - Track active subscriptions: which services subscribe to which topics, subscription lifecycle (when created, by whom), and subscription health (are subscribers processing messages or stuck?). For durable subscriptions (messages persist until acknowledged), monitor unconsumed message counts. For ephemeral subscriptions (Redis Pub/Sub), track subscriber connection status.

8. **Implement Message Schemas and Versioning** - Define message structure: required fields, data types, validation rules. Use schema registries (Confluent Schema Registry for Kafka, AWS Glue Schema Registry) to enforce compatibility. Version schemas to enable evolution: add optional fields (backward compatible), deprecate fields with migration periods (forward compatible), or create new topic versions for breaking changes.

9. **Add Observability** - Instrument publishers and subscribers: publish metrics (message publish rate, payload size, topic distribution), subscriber metrics (consumption rate, processing latency, error rate, lag), broker metrics (topic depth, consumer lag, partition distribution). Use distributed tracing with correlation IDs to track messages through Pub/Sub workflows end-to-end. Centralized logging for message content (with privacy/security considerations).

10. **Handle Dead-Letter Scenarios** - Messages that fail processing repeatedly shouldn't block subscriptions. Configure dead-letter topics/queues: after N failed processing attempts, move message to dead-letter destination for investigation. Implement dead-letter monitoring and alerting (new messages in dead-letter indicate processing issues). Establish processes for reviewing, fixing, and replaying dead-letter messages.

11. **Test Failure Scenarios** - Test not just happy path but failure modes: subscriber crashes (are messages redelivered?), broker outages (do publishers handle unavailability gracefully?), message malformation (do subscribers skip without crashing?), high message rates (does system handle backpressure?), network partitions (do subscriptions recover?), and duplicate messages (is processing idempotent?).

12. **Secure Communication** - Implement authentication (only authorized publishers can publish to topics), authorization (subscribers can only access permitted topics), encryption (messages encrypted in transit and at rest if sensitive), and audit logging (who published what, who subscribed to what). Cloud brokers provide identity integration (IAM, Azure AD); self-hosted brokers use SASL, TLS, and access control lists.

## Think of It Like This
Imagine a newsroom: journalists (publishers) write articles and submit them to topic desks (sports, politics, technology, entertainment). They don't know who reads their articles—they just write for the appropriate desk. Subscribers are readers who express interest in topics: some subscribe to sports only, others to technology and entertainment, some to everything. When a journalist publishes an article to the sports desk, all sports subscribers receive it automatically—no journalist needs to track subscriber lists or distribute articles individually. New readers can subscribe to topics anytime without journalists changing anything. If a subscriber goes on vacation (offline), they miss articles published during that time (unless the newsroom keeps archives for later pickup, like Kafka's persistent logs). This is exactly how Pub/Sub works: publishers broadcast to topics, subscribers receive what interests them, and the system (newsroom/broker) handles distribution.

## The "So What?" Factor
**If you use Pub/Sub:**
- Services are decoupled—publishers and subscribers evolve independently, adding/removing subscribers requires no publisher changes
- System is scalable—add subscribers without publisher coordination, add publishers without subscriber changes, scale each independently
- Real-time data flows naturally—events broadcast immediately to interested parties, enabling reactive architectures and event-driven workflows
- Integration is simplified—new services join by subscribing to relevant topics, no point-to-point integration for each new consumer
- Resilience improves—one subscriber failing doesn't affect publishers or other subscribers, failures are isolated
- Observability is unified—publish system events to topics, all monitoring tools subscribe, centralized visibility without tight coupling

**If you don't:**
- Services become tightly coupled—publishers must know all consumers, adding consumers requires publisher changes, dependency management becomes complex
- Scaling is coordinated—adding capacity requires changing multiple services, N publishers × M consumers = N×M integrations
- Real-time distribution requires custom logic—each publisher implements its own fanout, duplicate code, inconsistent patterns
- Integration complexity grows—every new consumer requires point-to-point integration with every relevant publisher, integration burden grows quadratically
- Failures cascade—publisher failures affect all consumers, slow consumers block publishers, resilience requires complex retry logic per integration
- Observability is fragmented—each service implements its own monitoring, no unified view, gaps in visibility

## Practical Checklist
Before implementing Pub/Sub, ask yourself:
- [ ] Do I need to distribute messages to multiple independent consumers (fanout pattern)?
- [ ] Are publishers and subscribers evolving at different rates or by different teams?
- [ ] Is asynchronous communication acceptable for my use case (vs synchronous request-response)?
- [ ] Can my subscribers tolerate occasional message duplication (at-least-once delivery)?
- [ ] Do I need to add/remove subscribers dynamically without changing publishers?
- [ ] Am I building event-driven workflows or real-time data pipelines?
- [ ] Do I have infrastructure for running a message broker (or budget for managed cloud services)?
- [ ] Can I implement idempotent message processing in subscribers?
- [ ] Do I need message ordering, and if so, can I work within broker ordering guarantees?
- [ ] Am I prepared to monitor topic lag, subscription health, and broker performance?

## Watch Out For
⚠️ **Message Ordering Challenges** - Pub/Sub systems don't always guarantee ordering, especially with multiple publishers, multiple subscribers, or concurrent processing. Kafka provides ordering within partitions (same key → same partition → ordered), but across partitions or for different keys, ordering isn't guaranteed. If strict ordering is required, design carefully: single partition (limits scalability), sequence numbers in messages (subscribers reorder), or use message brokers with ordering guarantees (though performance may suffer).

⚠️ **Backpressure and Lag Accumulation** - When subscribers can't process messages as fast as publishers produce them, messages accumulate (lag). This consumes broker storage, increases processing latency (messages wait longer), and can lead to out-of-memory errors or disk exhaustion. Monitor lag closely, implement alerting thresholds, and have scaling strategies ready (horizontal scaling, processing optimization). Don't assume infinite buffering—all brokers have limits.

⚠️ **Lack of Acknowledgment to Publishers** - Publishers fire-and-forget; they don't know if subscribers processed messages successfully. This is by design (decoupling) but creates operational blind spots: publishers can't directly tell if their messages had impact, downstream failures may go unnoticed, and end-to-end success requires separate monitoring. Mitigate with observability (publishers and subscribers both emit metrics), health checks (monitor subscription health), and business-level acknowledgments if needed (subscribers publish completion events that original publishers monitor).

⚠️ **Duplicate Message Processing** - At-least-once delivery means duplicates are possible after retries, network issues, or subscriber restarts. Subscribers must be idempotent: processing the same message multiple times has the same effect as processing once. Techniques: deduplicate by message ID (cache recently processed IDs), use idempotent operations (set operations, upserts), or maintain processing state with transactions (database record + message acknowledgment in same transaction). Don't assume messages arrive exactly once unless using exactly-once semantics (rare and complex).

⚠️ **Topic Explosion and Management Overhead** - Creating too many fine-grained topics (one per user, per event type variant, per version) leads to operational complexity: many topics to monitor, subscription management complexity, broker resource overhead. Balance granularity: too broad (everything in one topic) forces subscribers to filter, too fine-grained creates management burden. Use hierarchical topics and wildcards, content-based filtering, or careful topic design (semantic grouping).

⚠️ **Schema Evolution Pain** - Message formats evolve: new fields added, old fields deprecated, data types change. Without schema management, incompatible changes break subscribers. Implement schema versioning: use schema registries (Confluent, AWS Glue), design for backward/forward compatibility (optional fields, default values), version topics for breaking changes ("user.v1.registered" → "user.v2.registered"), and coordinate subscriber migrations. Don't publish arbitrary message structures without schema governance.

⚠️ **Security and Access Control Complexity** - With many publishers and subscribers, managing who can publish to which topics and who can subscribe to what becomes complex. Implement least-privilege access (subscribers only access topics they need), authentication (verify publisher/subscriber identity), encryption (protect sensitive messages), and audit logging (track access patterns). Cloud brokers integrate with IAM; self-hosted brokers require careful ACL configuration. Don't assume default-open access is acceptable.

## Connections
**Builds On:** [message_queue](message_queue.md), asynchronous messaging, distributed systems, topics/channels abstraction

**Works With:** [event_driven_architecture](event_driven_architecture.md), [microservices](microservices.md), [saga_pattern](saga_pattern.md) (choreography), [workflow_engines_and_durable_execution](workflow_engines_and_durable_execution.md)

**Leads To:** Event sourcing, CQRS (Command Query Responsibility Segregation), stream processing, reactive systems

## Quick Decision Guide
**Use this when you need to:** Distribute messages to multiple independent consumers (fanout), decouple publishers from subscribers (services evolve independently), build event-driven architectures or real-time data pipelines, enable dynamic subscription management (add/remove consumers without publisher changes), or broadcast events for monitoring/observability.

**Skip this when:** Communication is one-to-one (use message queues for point-to-point), synchronous request-response is required (use RPC/REST APIs), message ordering is critical and broker can't guarantee it, system complexity doesn't justify broker infrastructure overhead, or tight coupling between producer and consumer is actually desired (simple direct integration acceptable).

## Further Exploration
- 📖 [Enterprise Integration Patterns: Pub/Sub Channel](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html) - Gregor Hohpe's canonical pattern description
- 🎯 [Apache Kafka Documentation](https://kafka.apache.org/documentation/) - Comprehensive guide to Kafka's Pub/Sub streaming architecture
- 💡 [Building Event-Driven Microservices](https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/) - Adam Bellemare's practical guide to event-driven systems
- 📖 [Google Cloud Pub/Sub Overview](https://cloud.google.com/pubsub/docs/overview) - Managed Pub/Sub service concepts and best practices
- 🎯 [AWS SNS + SQS Fanout Pattern](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html) - Practical serverless Pub/Sub implementation
- 💡 [Designing Data-Intensive Applications](https://dataintensive.net) - Martin Kleppmann's chapter on message brokers and stream processing
- 📖 [RabbitMQ Pub/Sub Tutorial](https://www.rabbitmq.com/tutorials/tutorial-three-python.html) - Hands-on introduction to Pub/Sub with RabbitMQ
- 🎯 [NATS Pub/Sub Documentation](https://docs.nats.io/nats-concepts/core-nats/pubsub) - High-performance cloud-native messaging patterns

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*