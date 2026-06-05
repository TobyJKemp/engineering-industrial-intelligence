# Webhook

## At a Glance
| | |
|---|---|
| **Category** | Integration Pattern |
| **Complexity** | Intermediate |
| **Time to Learn** | 2-3 hours for basics, ongoing for production reliability |
| **Prerequisites** | [REST API](rest_api.md), HTTP protocol, basic event-driven concepts |

## One-Sentence Summary
A webhook is an event-driven HTTP callback mechanism where one system automatically sends data to a specified URL when specific events occur, enabling real-time notifications without constant polling—critical for [AI agents](../Agent_and_Orchestration/ai_agent.md) that need to react immediately to external events like user actions, system state changes, or third-party service updates.

## Why This Matters to You
Your [AI agent](../Agent_and_Orchestration/ai_agent.md) needs to know when things happen—when a customer submits a form, when a payment completes, when a document is uploaded, when another system finishes processing. You could have your agent constantly ask "did anything happen yet?" every few seconds (polling), but that's wasteful, slow, and expensive. Webhooks flip this around: external systems notify your agent the instant something happens by sending an HTTP request to your endpoint. Your agent receives events in real-time, processes them immediately, and only runs when needed. For [multi-agent systems](../Agent_and_Orchestration/multi-agent_system.md), webhooks enable loosely coupled communication where agents don't need to know about each other's existence—they just subscribe to events they care about. Without webhooks, you're stuck with polling delays (events noticed seconds or minutes late), wasted resources (constant polling even when nothing happens), and coupling (agents must know how to query other systems). With webhooks, your agents are reactive, efficient, and event-driven.

## The Core Idea
### What It Is
A webhook is a user-defined HTTP callback: when an event occurs in System A, System A makes an HTTP POST request to a URL you've configured (your webhook endpoint), delivering event data as the request payload. Instead of your code constantly asking "has X happened yet?" (polling), System A proactively tells you "X just happened, here's the data" by calling your webhook. You register the webhook URL with System A during setup, and from then on, System A automatically notifies you whenever relevant events occur.

Webhooks implement a push model rather than pull model. In traditional [REST API](rest_api.md) interactions, clients pull data by making requests to servers. With webhooks, servers push data to clients by making requests to client-provided URLs. This inverts the typical client-server relationship: your webhook endpoint acts as a server receiving requests from the event source.

The webhook lifecycle has three phases: **Registration** (you tell System A "call this URL when events happen"), **Event Occurrence** (something happens in System A that triggers the webhook), and **Delivery** (System A makes HTTP POST to your URL with event data). Your webhook endpoint receives the POST request, validates it's legitimate, extracts the event data, and triggers appropriate actions in your [AI agent](../Agent_and_Orchestration/ai_agent.md) or system.

Webhooks are ubiquitous in modern APIs: payment processors (Stripe sends webhooks for completed payments), version control (GitHub sends webhooks for commits and pull requests), communication platforms (Slack sends webhooks for messages), CRM systems (Salesforce sends webhooks for record changes), and AI platforms (OpenAI sends webhooks for async completions). Any service that generates events you might care about likely supports webhooks.

### What It Isn't
A webhook is **not a [REST API](rest_api.md)** endpoint you call. It's the opposite—a REST API endpoint that gets called by external systems. When you build a webhook endpoint, you're creating a server that receives requests, not a client that makes requests. This reversal confuses many developers initially.

A webhook is **not guaranteed delivery**. Most webhook implementations make a best-effort attempt to deliver events, but if your endpoint is down, slow to respond, or returns errors, some systems retry (with exponential backoff) while others simply drop the event. Unlike message queues with guaranteed delivery semantics, webhooks don't inherently ensure you'll receive every event. You must design for reliability explicitly.

Webhooks are **not synchronous request-response communication**. When System A sends a webhook, it typically doesn't wait for or care about your response data (beyond checking for success/failure status codes). Webhooks deliver notifications; they don't request information. If you need bidirectional data exchange, webhooks might not be the right pattern—consider [REST API](rest_api.md) calls instead.

Webhooks are **not inherently secure**. Anyone who knows your webhook URL could potentially send fake requests to it. Webhook implementations include security measures (signature verification, IP allowlisting, secret tokens), but these must be implemented and validated—webhooks don't provide security automatically.

Finally, webhooks are **not real-time in the distributed systems sense**. There's latency between event occurrence and webhook delivery (typically milliseconds to seconds, but can be longer during outages or retries). They're near-real-time, not guaranteed instantaneous. For truly time-critical operations, consider WebSockets or message queues with stronger latency guarantees.

## How It Works
The webhook lifecycle in an AI agent system:

1. **Webhook Registration (Setup Phase)**
   - You configure webhook endpoint in external system (Stripe, GitHub, Slack, etc.)
   - Provide webhook URL: `https://your-agent.com/webhooks/stripe-events`
   - Select event types to receive (payment.succeeded, payment.failed, etc.)
   - System generates webhook signing secret for security validation
   - You store secret securely for later signature verification
   - Some systems require endpoint verification (respond to challenge request)

2. **Event Occurs in Source System**
   - User completes payment in Stripe
   - Code is pushed to GitHub repository  
   - Document uploaded to storage system
   - AI model finishes async processing
   - Any event you've subscribed to via webhook

3. **Webhook Payload Construction**
   - Source system creates HTTP POST request
   - Serializes event data as JSON payload:
     ```json
     {
       "event_id": "evt_123abc",
       "event_type": "payment.succeeded",
       "timestamp": "2026-05-13T10:30:00Z",
       "data": {
         "payment_id": "pay_456def",
         "amount": 5000,
         "customer_id": "cus_789ghi"
       }
     }
     ```
   - Adds signature header for security (HMAC of payload + secret)
   - Sets retry metadata (attempt number if this is a retry)

4. **Webhook Delivery**
   - Source system makes HTTP POST to your webhook URL
   - Includes headers:
     - `Content-Type: application/json`
     - `X-Webhook-Signature: sha256=abc123...` (for verification)
     - `X-Event-Type: payment.succeeded` (event classification)
     - `X-Webhook-ID: evt_123abc` (for idempotency)
   - Waits for response (typically with 5-30 second timeout)

5. **Your Webhook Endpoint Receives Request**
   - Web server receives POST request
   - Logs receipt for monitoring and debugging
   - Extracts event ID for idempotency checking (have we seen this before?)
   - If duplicate event: return 200 OK immediately (already processed)
   - If new event: proceed to validation

6. **Security Validation**
   - Verify request signature to ensure it's from legitimate source:
     - Extract signature from header
     - Compute expected signature: HMAC(webhook_secret, request_body)
     - Compare computed signature to provided signature
     - If mismatch: reject with 401 Unauthorized (potential attack)
   - Optionally: Verify request originated from expected IP ranges
   - Check timestamp to prevent replay attacks (reject very old events)

7. **Event Processing**
   - Parse JSON payload and extract event data
   - Route to appropriate handler based on event_type
   - For payment.succeeded: Trigger fulfillment [AI agent](../Agent_and_Orchestration/ai_agent.md)
   - For document.uploaded: Trigger document analysis workflow
   - For model.completed: Retrieve results and continue pipeline
   - Processing typically happens asynchronously (queue the work, respond quickly)

8. **Response to Source System**
   - Return HTTP 200 OK to acknowledge receipt
   - Respond quickly (< 5 seconds typical requirement)
   - Don't do lengthy processing before responding (queue it instead)
   - Other status codes signal problems:
     - 400: Malformed payload (won't retry)
     - 401: Invalid signature (won't retry)
     - 500: Processing error (will retry)
     - Timeout: No response (will retry)

9. **Retry Handling (Source System)**
   - If delivery fails (timeout, 5xx error, network issue)
   - Source system retries webhook delivery
   - Typically: Exponential backoff (5 sec, 15 sec, 1 min, 5 min, etc.)
   - Retry attempts: Usually 3-10 times over hours/days
   - Eventually gives up if endpoint never responds
   - Some systems provide webhook delivery logs/dashboard

10. **Idempotency Protection (Your Side)**
    - Track processed event IDs in database
    - Before processing, check: "Have we seen event_123abc before?"
    - If yes: Skip processing but still return 200 OK
    - If no: Process event and record event ID
    - Prevents duplicate processing when retries occur
    - Critical for non-idempotent operations (financial transactions, sending emails)

11. **Error Handling and Dead Letter Queues**
    - If webhook processing fails repeatedly
    - Move failed events to dead letter queue for investigation
    - Alert operations team about processing failures
    - Implement manual retry mechanism for recovered events
    - Log failures with full context for debugging

## Think of It Like This
Think of webhooks like emergency notification systems in a building. Instead of you constantly checking every room to see if there's a fire (polling), the building has smoke detectors that automatically call the fire department the instant they detect smoke (webhook). The fire department doesn't need to know anything about your building's internal layout or where detectors are located—they just register their phone number (webhook URL) with your system, and your detectors call them when something happens. This is far more efficient than having firefighters drive by every building every few minutes asking "is there a fire yet?"

The fire department answers the call (receives webhook), verifies it's a legitimate alarm (signature validation), checks if they've already responded to this exact alarm (idempotency), and then dispatches appropriate resources (event processing). If the phone line is busy when the detector calls (endpoint down), the building system tries calling again later (retry logic).

In our railway metaphor, webhooks are the signaling system where track sensors automatically notify the central dispatch station when trains pass checkpoints. Rather than dispatchers constantly asking "has Train-247 reached Junction-5 yet?" (polling), the track sensors at Junction-5 send a message to dispatch the moment Train-247 crosses (webhook). This enables the dispatcher to coordinate the entire network reactively—allocating tracks, adjusting signals, and notifying connecting trains—all triggered by real-time events from the track network. Each sensor knows where to send notifications (webhook URL registered with each sensor), and dispatch validates messages are from legitimate track infrastructure (signature verification) before updating the system state. If dispatch is temporarily unreachable, sensors buffer and retry notifications (webhook retry logic) until acknowledgment is received.

## The "So What?" Factor
**If you use webhooks effectively:**
- Your [AI agents](../Agent_and_Orchestration/ai_agent.md) respond immediately to events (sub-second latency vs. minutes of polling delay)
- You eliminate wasteful polling requests (only process when events actually occur)
- You reduce costs (no constant API calls checking for updates)
- You enable event-driven architecture (loosely coupled, scalable systems)
- You integrate seamlessly with third-party services (most modern APIs provide webhooks)
- You can trigger complex [orchestration](../Agent_and_Orchestration/orchestration.md) workflows from external events
- You maintain scalability (event sources notify you, you don't need to query all sources constantly)

**If you don't use webhooks (rely only on polling):**
- You face delays detecting important events (check every 30 seconds means 30-second average delay)
- You waste resources polling APIs that return "nothing new" 99% of the time
- You hit rate limits from constant polling (may get throttled or banned)
- You increase costs (every poll is a billable API request)
- You create tight coupling (your code must know how to query every external system)
- You struggle to scale (polling 100 external services every second becomes overwhelming)
- You miss events between poll intervals (event occurred and resolved before next check)

## Practical Checklist
Before implementing webhooks for your AI agent system, ask yourself:
- [ ] **Is my webhook endpoint publicly accessible?** (External systems must be able to reach your URL—consider firewalls, NAT, cloud networking)
- [ ] **How will I verify webhook authenticity?** (Implement signature verification using provider's secret—never trust unsigned webhooks)
- [ ] **Am I handling idempotency correctly?** (Track processed event IDs to prevent duplicate processing on retries)
- [ ] **Can I respond quickly enough?** (Respond within 5 seconds—queue lengthy processing, don't block the webhook response)
- [ ] **What happens if my endpoint is down?** (Understand provider's retry policy, implement monitoring, consider backup endpoints)
- [ ] **How will I test webhooks during development?** (Use tools like ngrok for local testing, or providers' webhook testing/replay features)
- [ ] **Do I have proper error handling?** (Return appropriate status codes, implement dead letter queues for failures)
- [ ] **Am I logging webhook deliveries?** (Log all receipts for debugging, [monitoring](../Agent_Operations/monitoring.md), and audit trails)

## Watch Out For
⚠️ **Missing Signature Verification:** Anyone who discovers your webhook URL can send fake requests if you don't verify signatures. Attackers can trigger workflows, corrupt data, or cause denial-of-service by flooding your endpoint. Always validate webhook signatures using the secret provided by the event source.

⚠️ **Blocking Response on Processing:** If your webhook handler does expensive processing (database queries, external API calls, ML inference) before responding, you'll timeout and the source system will retry, causing duplicate processing. Always respond quickly (< 5 seconds) by queuing work for background processing, then return 200 OK immediately.

⚠️ **No Idempotency Protection:** Webhook sources retry failed deliveries, meaning you might receive the same event multiple times. Without idempotency checks (tracking processed event IDs), you'll process duplicate events—potentially charging customers twice, sending duplicate notifications, or corrupting state. Always track and check event IDs.

⚠️ **Webhook URL Exposure:** If your webhook URLs are predictable or discoverable, attackers can flood them with requests. Use random, unguessable URLs (include cryptographic tokens), implement rate limiting, and consider IP allowlisting if the source provides fixed IP ranges.

⚠️ **Ignoring Retry Logic:** When your endpoint returns errors, sources retry with exponential backoff. If you don't understand the retry schedule, you might get surprised by delayed webhook deliveries (event happened hours ago, webhook finally succeeded after retries). Monitor webhook delivery timestamps vs. event timestamps.

⚠️ **Webhook Dependency Hell:** As you subscribe to webhooks from multiple providers (Stripe, GitHub, Salesforce, Slack), you accumulate different signature schemes, payload formats, and retry behaviors. Document each provider's specifics and consider building an abstraction layer to normalize webhook handling.

⚠️ **No Dead Letter Queue:** When webhook processing fails repeatedly (database down, bug in handler), events can be lost if not captured. Implement dead letter queues that preserve failed events for later manual processing or investigation. Don't let transient failures cause permanent data loss.

�antml:thinking>
I should continue with the Connections section and complete the entry. Let me think about the related vocabulary terms that exist:
- REST API (builds on)
- AI Agent (uses webhooks)
- Multi-agent system (coordination)
- Orchestration (workflows triggered by webhooks)
- API Gateway (may route webhooks)
- Authentication/Authorization (securing webhooks)
- Monitoring (tracking webhook health)
- Audit Trail (logging webhook events)

Let me complete the entry with Connections, Quick Decision Guide, Further Exploration, and metadata.
</thinking>

⚠️ **Security Through Obscurity:** Just because your webhook URL is "secret" doesn't mean it's secure. URLs leak in logs, browser history, monitoring tools, and referrer headers. Always implement proper authentication (signature verification), never rely solely on URL secrecy.

## Connections
**Builds On:** 
- [REST API](rest_api.md) - Webhooks use HTTP/REST as transport mechanism
- Event-driven architecture - Webhooks implement event notification patterns
- HTTP protocol - Understanding POST requests, headers, status codes

**Works With:** 
- [AI Agent](../Agent_and_Orchestration/ai_agent.md) - Agents triggered by webhook events to perform actions
- [Orchestration](../Agent_and_Orchestration/orchestration.md) - Webhooks initiate complex multi-step workflows
- [API Gateway](api_gateway.md) - Gateways can route, validate, and transform incoming webhooks
- [Authentication](authentication.md) - Webhook signature verification is a form of authentication
- [Monitoring](../Agent_Operations/monitoring.md) - Track webhook delivery success rates, latency, failures
- [Audit Trail](../Agent_Operations/audit_trail.md) - Log all webhook events for compliance and debugging

**Leads To:** 
- Event-driven architecture patterns
- Asynchronous processing and message queues
- Real-time system integration
- [Multi-agent system](../Agent_and_Orchestration/multi-agent_system.md) coordination via events
- Serverless computing (webhooks triggering functions)

## Quick Decision Guide
**Use webhooks when:**
- You need near-real-time notification of external events
- Polling would be wasteful (events are infrequent or unpredictable)
- You're integrating with third-party services that provide webhooks (payment processors, version control, CRMs)
- You're building event-driven [AI agent](../Agent_and_Orchestration/ai_agent.md) systems that react to external triggers
- You need to decouple systems (event producers don't need to know about consumers)
- You want to reduce API costs (webhooks are push, no polling required)

**Use polling instead when:**
- Webhook endpoint infrastructure is too complex for your use case
- Events are so frequent that webhooks would overwhelm your endpoint
- Event source doesn't provide webhooks (you have no choice)
- You need to maintain strict control over request timing and rate
- Your system cannot expose public endpoints (security/network constraints)

**Hybrid approach (webhooks + polling):**
- Use webhooks for immediate notification
- Use occasional polling as backup in case webhooks fail
- Best of both worlds: fast response + reliable fallback
- Example: Webhook notifies agent immediately, agent polls once per hour to catch any missed events

**Consider WebSockets instead when:**
- You need true bidirectional communication
- You need sub-second latency guarantees
- You need persistent connection for streaming data
- Examples: Live chat, real-time collaboration, streaming telemetry

## Further Exploration
- 📖 **Stripe Webhooks Guide** - Exemplary webhook implementation with clear docs and testing tools
- 🎯 **Webhook.site** - Tool for testing and debugging webhooks during development
- 💡 **ngrok** - Expose local development servers to internet for webhook testing
- 📖 **"Designing Event-Driven Systems" by Ben Stopford** - Event-driven architecture patterns including webhooks
- 🎯 **GitHub Webhooks Documentation** - Comprehensive example of webhook implementation in popular platform
- 💡 **OWASP Webhook Security** - Security best practices for webhook endpoints
- 📖 **Twilio Webhook Security Guide** - Practical guide to signature verification and webhook security

---
*Added: May 13, 2026 | Updated: May 13, 2026 | Confidence: High*