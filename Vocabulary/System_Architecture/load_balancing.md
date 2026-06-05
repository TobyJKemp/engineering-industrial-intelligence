# Load Balancing

## At a Glance
| | |
|---|---|
| **Category** | Infrastructure Pattern / Network Component |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 days for concepts, 1-2 weeks for production configuration |
| **Prerequisites** | Basic networking (TCP/IP, HTTP), server architecture, distributed systems concepts |

## One-Sentence Summary
Load balancing is the practice of distributing incoming network traffic, requests, or computational work across multiple servers or resources to prevent any single resource from becoming overwhelmed, improving both performance and reliability.

## Why This Matters to You
When you deploy AI models that need to serve thousands of inference requests per second, or build agent systems that must remain available during server failures, load balancing becomes your first line of defense against both performance bottlenecks and system outages. A single GPU can handle maybe 50 inference requests per second; a load balancer distributing across 10 GPUs handles 500. A single server will eventually fail; a load balancer routing around failures keeps your service running. Without load balancing, you're forced to vertically scale (buy bigger servers—expensive and eventually impossible) rather than horizontally scale (add more servers—cheaper and unlimited). In 2026's AI landscape where model serving, agent fleets, and real-time processing dominate, load balancing is infrastructure that separates hobby projects from production systems.

## The Core Idea

### What It Is
Load balancing is a network or application-layer component (called a load balancer) that sits between clients and servers, receiving incoming requests and distributing them across a pool of backend servers according to various algorithms and health status. Think of it as an intelligent traffic director that ensures no single server gets overwhelmed while others sit idle, and that requests never get sent to servers that are down or struggling.

The fundamental problem load balancing solves is **resource utilization and resilience**. If you have three servers each capable of handling 1,000 requests per second, and all traffic goes to server one while servers two and three sit idle, you can only handle 1,000 RPS total despite having 3,000 RPS capacity. A load balancer distributes traffic evenly, unlocking the full 3,000 RPS. Similarly, if server one crashes without a load balancer, all requests fail; with a load balancer, it automatically stops sending traffic to the failed server and redistributes to the healthy two servers, maintaining 2,000 RPS capacity during the outage.

Load balancers operate at different network layers and levels of sophistication. **Layer 4 (Transport Layer) load balancers** operate at the TCP/UDP level, making routing decisions based on IP addresses and port numbers without inspecting packet contents—fast but limited in routing intelligence. **Layer 7 (Application Layer) load balancers** inspect HTTP headers, URLs, cookies, and message content, enabling sophisticated routing rules like "send /api/inference requests to GPU servers, /api/upload requests to storage servers"—slower but much more flexible.

Modern load balancers provide several critical features beyond simple distribution: **health checking** (automatically remove unhealthy servers from the pool), **SSL termination** (decrypt HTTPS traffic once at the load balancer rather than at every backend server), **session persistence** (ensure a user's subsequent requests go to the same server when needed), **connection pooling** (reuse TCP connections to backends), and **observability** (detailed metrics on traffic patterns, latency, and errors).

In AI systems, load balancing serves multiple roles: distributing inference requests across GPU clusters for model serving, routing traffic between different model versions for A/B testing, managing agent fleet workloads where specialized agents run on different servers, balancing batch processing jobs across compute nodes, and providing high availability for critical ML services. For example, a chatbot service might use a load balancer to distribute user queries across 20 inference servers, each running the same LLM on different GPUs, automatically removing servers that become unresponsive and routing around hardware failures.

The value extends beyond just spreading load—load balancers enable **zero-downtime deployments** (gradually shift traffic from old version to new), **geographic distribution** (route users to nearest datacenter), **rate limiting** (protect backends from overload), and **canary releases** (send 5% of traffic to new code to test before full rollout). They transform fragile single-server deployments into resilient, scalable distributed systems.

### What It Isn't
Load balancing is not the same as **auto-scaling**. A load balancer distributes work across existing servers; auto-scaling creates or destroys servers based on demand. They work together—auto-scaling adds servers when load increases, load balancer incorporates new servers into the pool—but they're separate concerns. Don't expect a load balancer to magically add capacity; it only utilizes the capacity you've provisioned.

It's not a replacement for proper capacity planning. If you have three servers each handling 1,000 RPS at 90% CPU utilization, a load balancer can't create 4,000 RPS capacity—it can only distribute the 3,000 RPS more evenly. Load balancers optimize utilization of existing resources; they don't create resources from thin air. You still need enough total capacity for your peak load.

A load balancer is not a caching layer, though many have caching capabilities. Its primary job is distributing requests, not storing responses. If you need to cache expensive AI inference results to avoid recomputation, you need a separate caching layer (Redis, Memcached) in front of or behind the load balancer. Some load balancers support basic caching, but dedicated cache systems provide better features and performance.

Load balancing is not the same as **message queueing**. While both distribute work, load balancers operate synchronously (client waits for response from whichever backend processes the request) whereas message queues operate asynchronously (client sends message and continues, consumer processes later). Load balancers are for request-response patterns; queues are for fire-and-forget or eventual consistency patterns. You might use both—a load balancer distributes HTTP API traffic to application servers, which then publish work to message queues for backend processing.

Finally, load balancing doesn't guarantee perfect distribution. Depending on the algorithm, connection patterns, and timing, you might see one server at 80% utilization while another is at 60%—this is normal and acceptable. Perfect balance is neither achievable nor necessary; "good enough" distribution that prevents any single server from being overwhelmed is the goal.

## How It Works

**Basic Request Flow:**

1. **Client Initiates Connection** - A user, application, or AI agent sends a request to the load balancer's public IP address or DNS name (e.g., `https://api.example.com/predict`). The client has no knowledge of the backend servers; it only knows the load balancer's address. This abstraction is key—backend servers can be added, removed, or replaced without client configuration changes.

2. **Load Balancer Receives Request** - The load balancer accepts the incoming connection on its public interface. For HTTPS traffic, it may terminate SSL (decrypt the request) or pass through encrypted traffic depending on configuration. It inspects the request to the degree necessary for its routing algorithm—a Layer 4 balancer looks at IP/port, a Layer 7 balancer examines HTTP headers and URL path.

3. **Health Check Evaluation** - Before selecting a backend, the load balancer consults its current health status table. This table is continuously updated by periodic health checks—the load balancer sends requests (e.g., `GET /health`) to each backend server every few seconds. Servers responding with success codes (HTTP 200) are marked healthy; those timing out or returning errors are marked unhealthy and excluded from consideration.

4. **Server Selection Algorithm** - The load balancer applies its configured algorithm to choose a backend server from the healthy pool. Different algorithms optimize for different goals (described in detail below). The choice considers factors like current connections, response times, server weights, and request characteristics (sticky sessions, content-based routing).

5. **Request Forwarding** - The load balancer establishes (or reuses) a connection to the selected backend server and forwards the client's request. It may modify headers to add information like the client's original IP address (`X-Forwarded-For`) since the backend sees the load balancer as the client. It may also add timing information or request IDs for tracing.

6. **Backend Processing** - The backend server processes the request normally—runs AI inference, queries database, executes business logic, etc.—and returns a response. The backend is unaware it's behind a load balancer; it just sees another HTTP request to handle.

7. **Response Return** - The load balancer receives the response from the backend and forwards it to the original client. For SSL-terminated connections, it re-encrypts the response before sending. It may modify response headers, add caching directives, or inject monitoring headers before returning to the client.

8. **Metrics Collection** - Throughout this process, the load balancer records metrics: request count, latency, error rate, backend response times, active connections per server. These metrics feed monitoring dashboards and alert systems.

**Load Balancing Algorithms:**

**Round Robin** - Cycles through servers in order: server1, server2, server3, server1, server2, etc. Simplest algorithm; works well when all servers have identical capacity and requests have similar processing costs. Problem: doesn't account for varying server loads or request complexity. One server might get 10 fast requests while another gets 10 slow requests, creating imbalance.

**Weighted Round Robin** - Like round robin but servers are assigned weights (e.g., server1: weight 2, server2: weight 1). Server1 receives twice as many requests as server2. Use when servers have different capacities (new GPU with 2x performance gets weight 2). Requires manual weight configuration and doesn't adapt to real-time conditions.

**Least Connections** - Sends new requests to the server with fewest active connections. Better than round robin for long-lived connections or variable request durations. If server1 has 10 active connections and server2 has 15, new request goes to server1. Problem: doesn't account for connection complexity—a server with 10 heavy AI inference connections may be more loaded than one with 20 simple health checks.

**Weighted Least Connections** - Combines least connections with server weights. Balances connections proportional to capacity: a server with weight 2 and 20 connections is considered equally loaded as a server with weight 1 and 10 connections. Good for heterogeneous server pools with varying capabilities.

**Least Response Time (Least Time)** - Sends requests to the server with the lowest average response time and fewest active connections. Adapts to real-time server performance—if a server slows down (disk filling up, background process competing for CPU), it automatically receives less traffic. More sophisticated but requires tracking response time metrics.

**IP Hash (Source IP Hash)** - Hashes the client's IP address to consistently route a client to the same backend server. Provides implicit session persistence without cookies or sticky sessions. Same client always reaches same server, maintaining session state. Problem: clients behind NAT may appear as same IP, creating hotspots. Doesn't adapt to server failures gracefully—when a server goes down, its clients must rehash to new servers, losing session state.

**Consistent Hashing** - Advanced hashing that minimizes disruption when servers are added/removed. Uses a hash ring where both servers and requests are hashed to positions. Each request goes to the next server clockwise on the ring. When a server fails, only its requests are reassigned (to the next server on the ring); all other assignments remain stable. Critical for distributed caches and stateful systems where session migration is expensive.

**URL Hash / Content-Based Routing** - Routes based on request URL, headers, or payload content. Example: send `/api/vision/*` to GPU servers with image processing models, `/api/nlp/*` to servers with language models, `/api/batch/*` to high-capacity batch processing servers. Enables specialization—different server types for different workloads. Requires Layer 7 load balancer.

**Random Selection** - Picks a random server from the healthy pool. Surprisingly effective for stateless applications with many servers—over large numbers of requests, distribution approaches uniformity. Simple to implement, low overhead, no state tracking required. Used more often in service meshes (Envoy, Istio) than traditional load balancers.

**Adaptive (Dynamic)** - Modern cloud load balancers use ML models to predict optimal server selection based on real-time metrics: CPU utilization, memory pressure, queue depth, response time trends. More complex but can achieve better utilization than static algorithms. Still emerging in 2026—AWS ALB and Azure Application Gateway have basic adaptive features, but custom ML-driven balancers are rare in production.

**Health Checking Mechanisms:**

**Active Health Checks** - Load balancer periodically sends requests to each backend server (e.g., every 5 seconds) to an endpoint like `/health` or `/ping`. If the endpoint returns HTTP 200, server is healthy; if it times out or returns 5xx error, server is unhealthy. After N consecutive failures (typically 3), server is removed from the pool. After M consecutive successes (typically 2), it's returned to the pool. This prevents flapping (rapid removal/addition) from transient errors.

**Passive Health Checks (Circuit Breaking)** - Monitor actual production traffic and mark servers unhealthy based on error rates or timeouts. Example: if 5 consecutive requests to a server fail or timeout, temporarily remove it from rotation for 30 seconds, then retry. Complements active checks—can detect issues that don't appear on health endpoints (e.g., database connection pool exhausted, but health check passes).

**Deep Health Checks** - Health endpoint doesn't just return "OK" but actually exercises critical dependencies—query database, check message queue connection, verify model loaded in memory. Slower but catches more failure modes. Example: AI inference server health check runs a tiny inference request to confirm model is responsive, not just that the HTTP server is alive.

**Session Persistence (Sticky Sessions):**

Many applications require that a user's subsequent requests reach the same backend server—for example, if session state is stored in server memory rather than shared storage. Load balancers provide several stickiness mechanisms:

**Cookie-Based Persistence** - Load balancer inserts a cookie (e.g., `SERVERID=server2`) in the first response. Subsequent requests include this cookie; load balancer routes them to server2. Works across network changes (client IP changes don't break session). Cookie can be encrypted and signed to prevent tampering.

**IP-Based Persistence** - Remember which server a client IP was routed to for a configurable duration (e.g., 30 minutes). Simpler than cookies but breaks if client IP changes (mobile users switching networks, corporate networks with rotating egress IPs). Good for APIs where cookies aren't practical.

**Application-Controlled Persistence** - Application sets a cookie or header indicating which server it wants future requests routed to. Gives application control over session management. More complex but more flexible.

**Trade-off:** Sticky sessions improve cache hit rates and simplify application architecture (no shared session store needed) but reduce load distribution flexibility (can't balance as evenly) and complicate server removal (draining a server requires waiting for all sessions to expire).

**Layer 4 vs. Layer 7 Load Balancing:**

**Layer 4 (Transport Layer / TCP/UDP):**
- Operates on IP addresses, port numbers, TCP connection state
- Doesn't inspect application data (HTTP headers, request content)
- Very fast—minimal processing overhead, microsecond latency
- Simple routing decisions—can only balance based on connection count, source IP
- Can't do content-based routing, URL-based rules, or HTTP-specific features
- Lower cost, simpler configuration, higher throughput
- Examples: AWS NLB (Network Load Balancer), HAProxy in TCP mode, NGINX stream module
- Best for: non-HTTP protocols, extreme performance requirements, simple distribution needs

**Layer 7 (Application Layer / HTTP/HTTPS):**
- Inspects HTTP headers, URLs, methods, cookies, request/response bodies
- Enables sophisticated routing: URL path routing, header-based routing, A/B testing
- Can modify requests/responses: rewrite URLs, add headers, compress responses
- SSL termination, HTTP/2 support, WebSocket handling
- Higher latency—millisecond processing overhead per request
- More complex, more expensive, lower maximum throughput
- Examples: AWS ALB (Application Load Balancer), NGINX in HTTP mode, HAProxy in HTTP mode, Envoy
- Best for: HTTP APIs, microservices, content-based routing, SSL offloading

**AI/ML Specific Use Cases:**

**Model Serving Load Balancing** - Distribute inference requests across multiple GPU servers, each running the same model. Use least response time algorithm to avoid overloading slow GPUs. Implement health checks that run test inferences to detect GPU failures or CUDA errors. Example: 20 GPUs serving a large language model, load balancer ensures no GPU exceeds 80% utilization.

**Multi-Model Routing** - Use content-based routing to direct requests to appropriate model servers based on request type. Example: image classification requests to vision model servers, text generation to language model servers, speech transcription to audio model servers—all behind one load balancer with URL path routing (`/api/vision/classify`, `/api/nlp/generate`, `/api/audio/transcribe`).

**A/B Testing for Models** - Use weighted routing to split traffic between model versions. Example: 90% of traffic goes to production model v2, 10% goes to candidate model v3 for evaluation. Gradually increase v3's weight as confidence grows. Monitor error rates and latency for each version separately.

**Agent Fleet Balancing** - Distribute work across a fleet of AI agents, each specialized for certain tasks. Use consistent hashing so related requests go to the same agent (maintains conversation context). Health checks verify agent responsiveness and memory usage (agents can degrade over time without restarting).

**Batch Processing Distribution** - Load balance batch inference jobs across worker nodes. Use least connections to avoid overloading workers with long-running jobs. Workers report remaining capacity via health endpoint (e.g., "2/10 job slots available"), load balancer uses this to route new jobs to least-loaded workers.

**Common Implementation Technologies (2026):**

**NGINX** - Most popular open-source web server and load balancer. Excellent HTTP/HTTPS load balancing, SSL termination, caching, compression. Configuration via text files. Supports Layer 4 (stream module) and Layer 7 (http module). NGINX Plus (commercial) adds active health checks, dynamic reconfiguration, advanced monitoring. Used by 33% of all websites. Strengths: mature, well-documented, performant. Weaknesses: configuration can be complex, reload required for changes.

**HAProxy** - High-performance open-source TCP/HTTP load balancer. Renowned for reliability and low latency. Rich feature set: health checks, SSL termination, sticky sessions, content-based routing. Configuration via text file. Often used in high-traffic environments (Reddit, GitHub, Instagram). Strengths: fastest pure load balancer, excellent observability. Weaknesses: less flexible than NGINX for web serving, steeper learning curve.

**Envoy** - Modern cloud-native load balancer designed for microservices and service meshes. Dynamic configuration via APIs (no reload needed). Advanced features: HTTP/2, gRPC load balancing, distributed tracing, circuit breaking, retry logic. Used as data plane in Istio, AWS App Mesh. Strengths: designed for containers/Kubernetes, excellent observability, modern protocols. Weaknesses: complex configuration, heavy resource usage, younger ecosystem.

**AWS Elastic Load Balancing (ELB)** - Managed cloud load balancers: ALB (Application/Layer 7), NLB (Network/Layer 4), GLB (Gateway for third-party appliances). Zero operational overhead, automatic scaling, integrated health checks. ALB supports Lambda targets, container routing. NLB handles millions of RPS with microsecond latency. Strengths: fully managed, integrates with AWS ecosystem, auto-scaling. Weaknesses: AWS-only, higher cost than self-hosted, some feature limitations.

**Azure Load Balancer / Application Gateway** - Microsoft's load balancing offerings. Standard Load Balancer (Layer 4), Application Gateway (Layer 7 with WAF). Deep integration with Azure services, availability zones, virtual networks. Application Gateway includes web application firewall, SSL offloading, URL-based routing. Strengths: Azure-native, good for Microsoft shops, reasonable pricing. Weaknesses: Azure-only, less mature than AWS offerings.

**Google Cloud Load Balancing** - Global load balancing across regions, Layer 4 (Network Load Balancer), Layer 7 (HTTP(S) Load Balancing). Unique global anycast architecture—single IP address load balances across continents. Automatic DDoS protection, Cloud CDN integration. Strengths: truly global distribution, high performance, unified management. Weaknesses: GCP-only, complex pricing, feature gaps vs. AWS.

**Kubernetes Ingress Controllers** - Load balancing within Kubernetes clusters. Popular controllers: NGINX Ingress, Traefik, Kong, Istio Ingress Gateway. Route traffic to services based on hostnames and paths. SSL termination, authentication, rate limiting. Strengths: Kubernetes-native, declarative configuration, automatic discovery. Weaknesses: cluster-internal only (needs external LB in front), varied feature sets across controllers.

**Service Meshes (Istio, Linkerd, Consul Connect)** - Provide load balancing as part of broader service mesh functionality. Sidecar proxies (Envoy) intercept service-to-service traffic, apply load balancing, retries, timeouts, circuit breaking. Observability and security built-in. Strengths: comprehensive microservices infrastructure, automatic mTLS, rich telemetry. Weaknesses: complexity, resource overhead, operational learning curve.

## Think of It Like This
Imagine a busy restaurant with one entrance but three identical kitchens (each with a complete cooking staff). Without a host managing the flow, all customers might crowd into kitchen one because it's closest to the entrance, overwhelming those cooks while kitchens two and three sit mostly empty. The restaurant can only serve as many meals as kitchen one can produce, despite having triple that capacity.

A host at the entrance (the load balancer) solves this. She tracks which kitchen has the fewest active orders, how long each kitchen's average order takes, and whether any kitchen is closed for cleaning (unhealthy). When customers arrive, she directs them to the optimal kitchen—spreading orders evenly, avoiding overloaded kitchens, never sending customers to closed kitchens. Now the restaurant serves three times as many meals because all three kitchens operate at capacity. If kitchen one's stove breaks, the host routes all customers to kitchens two and three—service continues (at 67% capacity) rather than completely failing.

The host can also do sophisticated routing: send simple orders (salads) to any kitchen, but route complex orders (five-course tasting menus) to the kitchen with the most experienced chef. This is content-based load balancing. She can also ensure that if you order an appetizer in kitchen one, your entree also goes to kitchen one (sticky sessions) so they can coordinate timing.

That's load balancing: intelligent traffic direction that maximizes resource utilization, prevents overload, and maintains service during failures.

## The "So What?" Factor

**If you use this:**
- **Handle traffic spikes gracefully** - When your AI API suddenly receives 10x normal traffic (viral social media post, unexpected customer influx), the load balancer distributes across all servers rather than overloading a few. System degrades linearly (slower responses across the board) rather than catastrophically (some servers crash, cascade failure).
- **Achieve high availability** - Any individual server can fail (hardware fault, software bug, deployment gone wrong) and the system continues operating with remaining servers. Load balancer detects failures within seconds via health checks and stops routing traffic to failed servers. Users experience minimal disruption—maybe a few failed requests during detection, then seamless operation.
- **Deploy without downtime** - Rolling deployment pattern: deploy new code to one server, verify health, move it into rotation, remove another server for upgrade, repeat. Users never experience service interruption because healthy servers always remain in the pool. Blue-green deployments: run old version on servers 1-3, new version on servers 4-6, gradually shift load balancer traffic from old to new, rollback instantly if issues arise.
- **Scale horizontally** - Add more servers to increase capacity rather than upgrading existing servers (vertical scaling). Horizontal scaling is cheaper (commodity hardware), more flexible (add exactly the capacity needed), and more resilient (more failure domains). Load balancer automatically incorporates new servers via health checks—no reconfiguration on clients or other servers.
- **Optimize resource utilization** - Ensure all servers operate at similar utilization levels rather than some overloaded and others idle. This improves response times (no hot spots) and reduces costs (get full value from every provisioned server). For GPU clusters, this means every expensive GPU stays busy rather than some maxed out while others idle.
- **Enable multi-region deployments** - Use geographic load balancing (DNS-based or anycast) to route users to nearest datacenter. Improves latency (shorter network path), regulatory compliance (data stays in region), and disaster recovery (entire datacenter can fail without global outage).
- **Simplify client configuration** - Clients connect to one stable load balancer address rather than managing lists of backend servers. Backend server IPs can change, servers can be added/removed, even entire datacenters can change—clients never need configuration updates. This decoupling is essential for large-scale systems.

**If you don't:**
- **Single point of failure** - If your one server fails, your entire service is down until you manually intervene and restart or replace it. Mean time to recovery measured in minutes to hours rather than seconds. No automatic failover, no redundancy.
- **Wasted capacity** - Multiple servers require manual traffic distribution. Users might not discover alternate servers, or traffic might be unevenly distributed by client-side logic. Common pattern: 70% of traffic hits server one (slow, sometimes crashing), 20% on server two, 10% on server three. Effective capacity is limited by the hotspot server.
- **Risky deployments** - Deploying new code requires taking the service offline (maintenance window), or gambling on in-place upgrades that might break production. No way to test new code with partial traffic. Rollback requires another full deployment cycle. This slows development velocity and increases deployment anxiety.
- **Hard vertical scaling limits** - Eventually you hit the ceiling of vertical scaling—no bigger GPU exists, no faster CPU is available, costs become exponential. Without load balancing enabling horizontal scale, you're stuck. This limit arrives faster than expected with AI workloads due to model size and memory requirements.
- **Poor user experience during traffic spikes** - Single server gets overwhelmed, response times climb from milliseconds to seconds to timeouts. Users see errors, slow loading, failed requests. No graceful degradation—just hard failure. Damages reputation and loses business.
- **Complex client logic** - If clients must manage lists of backend servers and implement their own failover and retries, complexity spreads across every client. This is error-prone, hard to update, and creates inconsistent behavior as different clients implement different retry strategies.

## Practical Checklist

Before implementing load balancing, ask yourself:

- [ ] **Do I have multiple backend servers to balance across?** - If you only have one server, a load balancer adds latency and complexity without benefit. Start with one server; add load balancing when you need multiple servers for capacity or availability.
- [ ] **What's my consistency requirement?** - If requests must hit the same server (stateful application with in-memory sessions), configure sticky sessions. If requests are stateless (read from shared database, pure computation), any server can handle any request—simpler and better distribution.
- [ ] **Layer 4 or Layer 7?** - If you only need basic TCP/UDP distribution and don't need HTTP-aware features, Layer 4 is faster and simpler. If you need URL routing, header inspection, SSL termination, or content-based decisions, use Layer 7. When in doubt, start with Layer 7—flexibility is usually worth the small latency cost.
- [ ] **What health check makes sense?** - Simple health checks (TCP connection succeeds, HTTP returns 200) detect server crashes but not degraded performance. Consider deep health checks that verify critical dependencies (database reachable, model loaded, disk space available). Balance thoroughness vs. overhead (deep checks every 30 seconds, not every 5).
- [ ] **Which load balancing algorithm?** - For stateless applications with homogeneous servers, round robin is fine. For heterogeneous servers (different CPU/GPU), use weighted algorithms. For long-lived connections or variable request duration, use least connections. For maximum sophistication, use least response time. Start simple; add complexity only if you observe imbalance.
- [ ] **How will I handle session state?** - Best option: make applications stateless (store session in Redis/database, use JWTs). If unavoidable: use sticky sessions with cookie-based persistence. Avoid in-memory sessions without stickiness—requests will hit random servers and lose state.
- [ ] **What happens when a server fails?** - Configure health check intervals, failure thresholds, and recovery thresholds. Example: check every 10 seconds, mark unhealthy after 3 failures (30 seconds), mark healthy after 2 successes (20 seconds). Too aggressive: flapping from transient errors. Too lenient: slow failure detection.
- [ ] **Do I need SSL termination?** - Terminating SSL at load balancer simplifies backend servers (no cert management) and improves performance (decrypt once vs. per backend). But backend traffic is unencrypted—only acceptable in secure private networks. For end-to-end encryption, use SSL passthrough (slower but more secure).
- [ ] **How will I monitor load balancer health?** - Track key metrics: requests per second, error rate (4xx, 5xx), latency percentiles (p50, p95, p99), active connections, backend health status. Alert on: error rate spike, latency increase, unhealthy backend count, load balancer CPU/memory. Test failover periodically—don't discover health checks broken during a real incident.
- [ ] **What's my capacity buffer?** - Don't run at 100% capacity—you need headroom for traffic spikes and server failures. Rule of thumb: with N servers, provision capacity assuming N-1 are healthy (N+1 redundancy). This ensures losing one server doesn't overload remaining servers.
- [ ] **How do I drain servers for maintenance?** - Configure "draining" state: server stops receiving new requests but completes in-flight requests before removal. This prevents abrupt connection termination during deploys. Set appropriate drain timeout (how long to wait for connections to finish before forcing close).

## Watch Out For

⚠️ **Sticky sessions reduce distribution quality** - When sessions stick to servers, load balancing becomes less effective. If 100 users each have 10-minute sessions across 5 servers, distribution is lumpy—one server might get 30 long-lived users while another gets 10. This is acceptable for stateful apps but understand the trade-off. Consider: do you actually need stickiness, or can you externalize state to Redis/database and gain better distribution?

⚠️ **Health checks can create false positives** - A health endpoint that just returns "OK" doesn't prove the server is healthy—just that the web server process is alive. The database connection pool might be exhausted, memory might be 99% full, the ML model might be unloaded. Implement health checks that exercise critical paths (query database, run tiny inference, check disk space). But don't make health checks too expensive—running a 30-second inference every 10 seconds defeats the purpose.

⚠️ **Connection pooling between load balancer and backends matters** - If the load balancer opens a new TCP connection for every client request, you waste time on TCP handshakes and overwhelm backend connection limits. Configure connection pooling (HTTP keep-alive) so the load balancer maintains persistent connections to backends. This dramatically improves throughput and reduces latency (no handshake overhead). Most modern load balancers default to pooling, but verify configuration.

⚠️ **The load balancer itself can become a bottleneck** - A single load balancer instance can fail or become overwhelmed. For production systems, deploy load balancers in high-availability pairs (active-standby or active-active with DNS failover). Cloud providers solve this automatically (AWS ELB, Azure LB are multi-instance by design). Self-hosted solutions need HA configuration: keepalived, VRRP, floating IPs, or DNS-based failover.

⚠️ **Round robin assumes equal server capacity** - If servers have different CPU, memory, or GPU capabilities, round robin distributes requests evenly by count but not by load. A weak server gets the same number of requests as a powerful server, causing imbalance. Use weighted algorithms when server capacity varies. Alternatively, use identical server specs to avoid this complexity.

⚠️ **Least connections can concentrate long-running requests** - If some requests take 10 seconds and others take 10 milliseconds, least connections might send all the long requests to one server (it had fewest connections at the moment) and all short requests elsewhere. The "least connections" server actually has highest load. Consider least response time or least time (combines connections and latency) for better distribution with variable request durations.

⚠️ **Cookie-based stickiness can be defeated by cookie rejection** - If users disable cookies, browsers in private mode, or bots that don't process cookies, sticky session cookies don't work—subsequent requests hit random servers. Have a fallback plan: store sessions in shared storage (Redis), use IP-based stickiness (weaker but doesn't require cookies), or design stateless APIs (best option).

⚠️ **Passive health checks (circuit breaking) need tuning** - If you mark a server unhealthy after 5 consecutive errors, but those errors are due to invalid client requests (400 Bad Request) not server problems, you'll incorrectly remove healthy servers. Distinguish between client errors (4xx—don't count toward unhealthy) and server errors (5xx, timeouts—do count). Also set appropriate circuit breaker reset times—too short and you hammer a struggling server, too long and you waste capacity.

⚠️ **Geographic load balancing adds latency for global state** - Routing users to nearest datacenter improves latency for stateless requests but complicates stateful systems. If user data lives in US datacenter but user is routed to EU datacenter, the EU servers must fetch data from US (cross-region latency). Solutions: replicate data globally (expensive, consistency challenges), use sticky routing (user always goes to datacenter where their data lives), or accept cross-region latency for stateful operations.

⚠️ **SSL termination exposes decrypted traffic** - When load balancer terminates SSL, backend traffic is unencrypted HTTP within your network. This is fine for secure private networks (VPC, corporate LAN) but unacceptable if backend traffic crosses untrusted networks. In cloud environments, VPCs provide isolation, but understand the security model. For end-to-end encryption, use SSL passthrough (load balancer forwards encrypted traffic to backends) or re-encrypt between load balancer and backends (most secure, highest latency).

⚠️ **Draining doesn't guarantee graceful shutdown** - Setting a server to "draining" stops new requests but doesn't force existing requests to complete quickly. If you have long-running requests (5-minute batch inference jobs), drain might wait 5 minutes. Set appropriate drain timeouts and force-close after timeout. For truly long operations (10+ minutes), consider async patterns (message queues, webhooks) so client connections don't need to stay open.

⚠️ **Weight changes require careful rollout** - If you suddenly change server weights (e.g., server1 from weight 1 to weight 5), traffic shifts immediately—server1 might go from 20% to 60% of traffic instantly. This can overwhelm it before it warms up (caches empty, connection pools cold). Gradually adjust weights over minutes, monitoring server metrics as load increases. Or use percentage-based canary routing if your load balancer supports it.

## Connections

**Builds On:**
- Networking fundamentals (TCP/IP, HTTP, DNS)
- Distributed systems principles (replication, consistency, fault tolerance)
- Health monitoring and observability practices

**Works With:**
- [scalability](scalability.md) - Load balancing enables horizontal scaling by distributing work across multiple servers
- [microservices](microservices.md) - Each microservice typically sits behind a load balancer for high availability
- [message_queue](message_queue.md) - Complementary distribution patterns—load balancers for synchronous traffic, queues for asynchronous work
- [operational_design](operational_design.md) - Load balancers are essential operational infrastructure requiring monitoring, alerts, runbooks

**Leads To:**
- Service meshes (Istio, Linkerd) - Advanced load balancing with automatic discovery, mTLS, observability
- Global load balancing and multi-region deployments - Geographic traffic distribution
- Auto-scaling patterns - Dynamic server pool management based on load metrics
- Rate limiting and API gateways - Layer 7 load balancers often include rate limiting, authentication, API management

## Quick Decision Guide

**Use load balancing when you need to:**
- Run multiple servers for capacity or availability—distribute traffic evenly across them
- Achieve high availability with automatic failover when servers fail
- Deploy new code without downtime via rolling or blue-green deployments
- Scale horizontally by adding servers rather than upgrading existing ones
- Simplify client configuration with a single stable endpoint address
- Route traffic intelligently based on URL, headers, or request content (Layer 7)
- Distribute AI inference requests across multiple GPU servers for parallel processing

**Skip load balancing when:**
- You have only one server and don't need redundancy (adds latency and complexity without benefit)
- Your system is small enough that direct client-to-server connections are manageable
- You're prototyping or in early development (premature infrastructure complexity)
- All traffic must hit the exact same server for consistency (though this suggests architectural issues)
- You have extremely simple request routing that DNS round-robin can handle (rare but valid for homogeneous read-only services)

**Choose Layer 4 (TCP/UDP) when:**
- You need maximum performance and minimal latency (microseconds matter)
- Your protocol isn't HTTP (database connections, custom TCP protocols, UDP streaming)
- You don't need content-aware routing (all backends are equivalent)
- You want simplicity and lower operational overhead

**Choose Layer 7 (HTTP/HTTPS) when:**
- You need URL-based routing, header inspection, or content-based decisions
- You want SSL termination to simplify backend certificate management
- You're building microservices with different services behind one load balancer
- You need advanced features: A/B testing, canary deployments, request rewriting
- You need WebSocket support, HTTP/2, or gRPC load balancing

## Further Exploration

- 📖 **"The Load Balancer Handbook"** - Comprehensive guide covering algorithms, high availability, operational best practices; free at loadbalancer.org
- 📖 **"Site Reliability Engineering"** (Google) - Chapter 19 on Load Balancing covers Google's approach to global load distribution and failover
- 🎯 **NGINX Load Balancing Documentation** (https://docs.nginx.com/nginx/admin-guide/load-balancer/) - Practical configurations for HTTP, TCP, health checks, sticky sessions
- 🎯 **HAProxy Configuration Manual** (http://www.haproxy.org/#docs) - Detailed reference for one of the most powerful load balancers; excellent algorithms section
- 💡 **AWS Elastic Load Balancing Best Practices** - Cloud provider perspective on load balancer selection (ALB vs NLB vs GLB), target groups, health checks
- 💡 **Azure Load Balancer vs Application Gateway Comparison** - When to use Layer 4 vs Layer 7 in Azure, feature matrices, pricing considerations
- 🎯 **Envoy Proxy Documentation** (https://www.envoyproxy.io/docs/envoy/latest/) - Modern load balancer used in service meshes; advanced features like circuit breaking, outlier detection
- 📖 **"Designing Data-Intensive Applications"** by Martin Kleppmann - Chapter 8 discusses distributed system challenges including load balancing and replication
- 💡 **Consistent Hashing Explained** - Research papers and blog posts on how Dynamo, Cassandra, and CDNs use consistent hashing for load distribution
- 🎯 **Load Testing with Locust or k6** - Practical tools for testing load balancer behavior under various traffic patterns; validate your configuration works as expected
- 💡 **"Load Balancing in the Cloud"** (NSDI paper) - Academic research on cloud load balancing algorithms, comparing random selection, least connections, and power of two choices
- 🎯 **Kubernetes Ingress Controllers Comparison** - Feature comparison of NGINX Ingress, Traefik, Kong, Istio for cluster load balancing

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
