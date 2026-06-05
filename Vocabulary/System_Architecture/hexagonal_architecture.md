# Hexagonal Architecture

## At a Glance
| | |
|---|---|
| **Category** | Architecture Pattern |
| **Complexity** | Advanced |
| **Time to Learn** | 3-5 days for concepts, 2-4 weeks for effective implementation |
| **Prerequisites** | Dependency injection, interfaces/abstractions, SOLID principles, layered architecture basics |

## One-Sentence Summary
Hexagonal architecture (also called ports and adapters) isolates your core business logic in the center of a hexagon, with all external concerns (databases, APIs, UIs, message queues) connected through well-defined ports (interfaces) and adapters (implementations), ensuring the core domain remains independent of infrastructure details.

## Why This Matters to You
When you build AI systems that need to work with multiple data sources (databases, APIs, file systems), serve predictions through different interfaces (REST API, message queue, batch processing), and potentially swap ML frameworks or model serving infrastructure, tightly coupling your core model logic to specific technologies creates fragility. Hexagonal architecture solves this by making your domain logic—the part that actually implements intelligence, makes predictions, and encodes business rules—completely independent of how data arrives, where it's stored, or how results are delivered. This means you can test your ML pipeline without a database, swap TensorFlow for PyTorch without rewriting your application, or add a new API endpoint without touching model code. In 2026's rapidly evolving AI landscape where model frameworks, serving infrastructure, and integration patterns change constantly, hexagonal architecture provides stability through radical decoupling—your valuable domain logic remains pristine while infrastructure churns around it.

## The Core Idea

### What It Is
Hexagonal architecture, introduced by Alistair Cockburn in 2005, organizes software around a central domain (the "hexagon") surrounded by ports and adapters that connect the domain to the outside world. The hexagon metaphor emphasizes that the core has multiple sides—there's no inherent "top" or "bottom" like in layered architecture. The domain sits in the center, and external systems connect from any direction through symmetric interfaces.

**The Three Core Concepts:**

**Domain (The Hexagon Core)** - Contains your pure business logic, domain models, and use cases—the essential intelligence of your system. In AI systems, this is where ML model orchestration lives, feature engineering logic, prediction pipelines, confidence scoring, business rule application, and domain-specific algorithms. The domain knows nothing about HTTP, SQL, message queues, or any external technology. It only knows domain concepts: "classify document," "recommend products," "detect anomalies," "generate response." This is pure, testable, framework-independent code.

**Ports (Interfaces)** - Define how the domain communicates with the outside world, but not through what concrete technology. Ports are interfaces/abstractions that specify contracts: "I need something that can retrieve user data" (port) but not "I need a PostgreSQL database" (implementation detail). Ports come in two flavors:

- **Primary/Driving Ports (Input)** - How external systems invoke the domain. These are the use cases or application services the domain exposes. Example: `IDocumentClassifier` interface with `classify(document)` method. The domain implements these ports. Web APIs, CLI tools, or batch jobs call through these ports to trigger domain logic.

- **Secondary/Driven Ports (Output)** - How the domain reaches out to external systems when it needs data or services. These are the dependencies the domain requires but doesn't implement. Example: `IModelRepository` interface with `loadModel(modelId)` method. External infrastructure implements these ports. The domain calls these ports when it needs model files, user data, configuration, or external services.

**Adapters (Implementations)** - Concrete implementations that connect ports to real technologies. Adapters translate between the domain's pure interfaces and messy external reality. Example adapters:

- **REST API Adapter (Primary)** - Flask/FastAPI controller that receives HTTP requests, converts them to domain objects, calls domain port methods, converts domain responses to HTTP responses. Sits outside the hexagon, calls inward.

- **Database Adapter (Secondary)** - PostgreSQL repository implementation that implements the domain's data access port. Converts domain queries into SQL, executes them, converts database rows back to domain objects. Domain calls this adapter through the port interface.

- **Message Queue Adapter (Primary)** - Kafka consumer that reads messages, deserializes them, calls domain methods. Another entry point into the hexagon.

- **File Storage Adapter (Secondary)** - S3 client that implements file storage port. Domain asks "save this model artifact," adapter handles S3 bucket details.

**The Critical Dependency Rule:** Dependencies point inward toward the domain. The domain depends on nothing external—zero imports of frameworks, libraries, or infrastructure code. Adapters depend on both the domain (they implement/call ports) and external technologies (they translate to/from those technologies). This is dependency inversion at the architecture level.

Visually:

```
        [REST API Adapter] ──→ (Primary Port) ──→
                                                  \
[Kafka Adapter] ──→ (Primary Port) ──→            ╔═══════════════╗
                                       ──→        ║               ║
[CLI Adapter] ──→ (Primary Port) ──→              ║    DOMAIN     ║ ←── (Pure Business Logic)
                                                  ║   (Hexagon)   ║
                        (Secondary Port) ←── ──   ║               ║
                       /                          ╚═══════════════╝
[Database Adapter] ←──                            /               \
                                                 /                 \
[S3 Storage Adapter] ←── (Secondary Port) ←── ──                   \
                                                                     \
[Model Serving Adapter] ←── (Secondary Port) ←── ────────────────────
```

External systems (left and right) connect through adapters. Adapters connect through ports (interfaces). Ports connect to the domain. The domain never knows about adapters or external systems—only ports.

**In AI Systems Context:**

A document classification system using hexagonal architecture might look like:

**Domain (Core Hexagon):**
- `DocumentClassifier` - Core business logic for classification
- `ConfidenceEvaluator` - Determines if predictions are trustworthy
- `DocumentPreprocessor` - Text cleaning and normalization
- `ClassificationResult` - Domain model representing predictions
- **No imports** of Flask, SQLAlchemy, boto3, TensorFlow, or any framework

**Primary Ports (Driving - Inward Calls):**
- `IClassificationService` - Interface: `classify(document: Document) -> ClassificationResult`
- Domain implements this interface through `DocumentClassificationService` class

**Secondary Ports (Driven - Outward Calls):**
- `IModelRepository` - Interface: `loadModel(modelId: str) -> Model`
- `IDocumentStore` - Interface: `saveClassification(result: ClassificationResult) -> void`
- `IFeatureStore` - Interface: `getFeatures(documentId: str) -> Features`
- Domain defines these interfaces but doesn't implement them—it calls them when needed

**Primary Adapters (Implement Entry Points):**
- `RestApiAdapter` - Flask controller, receives HTTP POST, calls `IClassificationService.classify()`
- `BatchProcessorAdapter` - Reads files from directory, calls classification service for each
- `MessageQueueAdapter` - Kafka consumer, deserializes messages, calls classification service

**Secondary Adapters (Implement Dependencies):**
- `S3ModelRepository` - Implements `IModelRepository`, loads models from S3 buckets
- `PostgresDocumentStore` - Implements `IDocumentStore`, saves to PostgreSQL database
- `RedisFeatureStore` - Implements `IFeatureStore`, retrieves cached features from Redis

The domain classification logic never mentions S3, PostgreSQL, Kafka, or Flask. It only knows "I need a model (through IModelRepository)" and "I should save results (through IDocumentStore)." This decoupling enables testing with mock repositories, swapping S3 for filesystem without touching domain code, adding GraphQL API without modifying classification logic, or switching databases with a new adapter.

### What It Isn't
Hexagonal architecture is not **layered architecture**, though they're related. Layered architecture organizes in horizontal strata (presentation → application → business → data) with dependencies flowing downward. Hexagonal architecture organizes around a central core with dependencies flowing inward from all sides. Layered architecture has asymmetry (top vs. bottom); hexagonal is symmetric (all external systems are equal). You can think of hexagonal as a more flexible, explicit form of layering where the "business logic layer" becomes the domain, and other layers become adapters. But the dependency inversion is more rigorous in hexagonal.

It's not **microservices architecture**. Hexagonal describes internal organization of a single application or service. Microservices describes distribution of functionality across multiple deployable services. You can (and should) apply hexagonal architecture within each microservice—they're complementary patterns at different scales. A microservice is a deployment unit; hexagonal architecture is an organizational pattern within that unit.

Hexagonal architecture is not **event-driven architecture**, though they work well together. Hexagonal describes how to structure code around a core domain. Event-driven describes communication patterns between components using asynchronous events. You can have hexagonal services that communicate via events—the event consumer would be a primary adapter, event emitter would be a secondary adapter. They address different concerns.

It's not **clean architecture** or **onion architecture**, though they're closely related cousins. All three emphasize dependency inversion, core domain isolation, and use of interfaces. The differences are mostly presentation and emphasis—hexagonal emphasizes ports and adapters metaphor, clean architecture emphasizes use cases and entities layers, onion emphasizes concentric circles of abstraction. In practice, a well-implemented hexagonal architecture looks remarkably like clean or onion architecture. Pick the metaphor that resonates with your team; the principles are nearly identical.

Hexagonal architecture is not overkill for every project—it's a tool, not a religion. Small scripts, simple CRUD apps, prototypes, and proof-of-concepts don't need elaborate port/adapter structure. The overhead is only justified when you have: complex domain logic worth protecting, multiple integration points with external systems, need for extensive testing, or systems that will evolve over time. Don't apply hexagonal architecture because it's "best practice"—apply it when the benefits outweigh the costs.

Finally, hexagonal architecture doesn't eliminate all coupling—it relocates it to the boundaries. Adapters are tightly coupled to both the domain (implement its interfaces) and external technologies (use framework-specific APIs). This is intentional—coupling is inevitable, so concentrate it in replaceable adapters while keeping the valuable domain pure. You're trading "coupling everywhere" for "coupling at boundaries," which is a massive improvement but not zero coupling.

## How It Works

**Building a Hexagonal AI System - Step by Step:**

1. **Identify the Core Domain** - What's the essential intelligence your system provides, stripped of all infrastructure concerns? For a recommendation system: "given user context and product catalog, generate ranked product recommendations applying business rules." Not "receive HTTP request, query PostgreSQL, call TensorFlow Serving, return JSON." The infrastructure details are secondary; the recommendation logic is the domain.

2. **Define Domain Models** - Create pure domain objects that represent your business concepts:
   ```python
   # Domain models - no framework imports
   from dataclasses import dataclass
   from typing import List, Dict
   
   @dataclass
   class UserContext:
       user_id: str
       viewing_history: List[str]
       purchase_history: List[str]
       preferences: Dict[str, any]
   
   @dataclass
   class Product:
       product_id: str
       category: str
       price: float
       attributes: Dict[str, any]
   
   @dataclass
   class Recommendation:
       product: Product
       score: float
       explanation: str
   ```
   These are pure data structures with zero dependencies on databases, web frameworks, or ML libraries.

3. **Define Secondary Ports (What Domain Needs)** - The domain needs external data and services. Define interfaces for these dependencies:
   ```python
   # Secondary ports - interfaces domain calls
   from abc import ABC, abstractmethod
   from typing import List
   
   class IUserRepository(ABC):
       @abstractmethod
       def get_user_context(self, user_id: str) -> UserContext:
           """Retrieve user viewing/purchase history and preferences"""
           pass
   
   class IProductCatalog(ABC):
       @abstractmethod
       def get_available_products(self, filters: Dict) -> List[Product]:
           """Get products matching filters"""
           pass
   
   class IRecommendationModel(ABC):
       @abstractmethod
       def score_products(self, user: UserContext, products: List[Product]) -> Dict[str, float]:
           """Return scores for each product given user context"""
           pass
   ```
   The domain defines these interfaces based on what it needs, not what databases/APIs happen to provide. This is crucial—domain dictates the contract, adapters conform.

4. **Implement Domain Logic Using Ports** - Write your core business logic referencing only domain models and secondary ports:
   ```python
   # Domain service - implements business logic
   class RecommendationEngine:
       def __init__(
           self,
           user_repo: IUserRepository,
           product_catalog: IProductCatalog,
           model: IRecommendationModel
       ):
           # Depend on interfaces, not concrete implementations
           self.user_repo = user_repo
           self.product_catalog = product_catalog
           self.model = model
       
       def generate_recommendations(
           self, 
           user_id: str, 
           num_recommendations: int = 10
       ) -> List[Recommendation]:
           # Pure business logic - no framework code
           
           # Get user context through port
           user = self.user_repo.get_user_context(user_id)
           
           # Apply business rule: filter products user already purchased
           purchased_ids = set(user.purchase_history)
           filters = {'exclude_ids': purchased_ids}
           
           # Get candidate products through port
           candidates = self.product_catalog.get_available_products(filters)
           
           # Score products through ML model port
           scores = self.model.score_products(user, candidates)
           
           # Apply business rule: minimum score threshold
           threshold = 0.5
           filtered_candidates = [
               p for p in candidates 
               if scores[p.product_id] >= threshold
           ]
           
           # Rank and select top N
           ranked = sorted(
               filtered_candidates,
               key=lambda p: scores[p.product_id],
               reverse=True
           )[:num_recommendations]
           
           # Create recommendation objects with explanations
           return [
               Recommendation(
                   product=p,
                   score=scores[p.product_id],
                   explanation=self._generate_explanation(user, p)
               )
               for p in ranked
           ]
       
       def _generate_explanation(self, user: UserContext, product: Product) -> str:
           # Business logic for explanation generation
           if product.category in user.preferences.get('favorite_categories', []):
               return f"You've shown interest in {product.category}"
           return "Recommended based on your preferences"
   ```
   Notice: zero imports of Flask, SQLAlchemy, TensorFlow, boto3. Pure business logic with dependencies injected through ports.

5. **Define Primary Port (How Domain Is Invoked)** - Define the interface that external systems use to invoke domain logic:
   ```python
   # Primary port - interface domain exposes
   class IRecommendationService(ABC):
       @abstractmethod
       def get_recommendations(self, user_id: str, count: int) -> List[Recommendation]:
           """Get product recommendations for user"""
           pass
   ```
   The domain's `RecommendationEngine` implements this interface. External adapters call through this interface.

6. **Implement Secondary Adapters** - Create concrete implementations that connect secondary ports to real technologies:
   ```python
   # PostgreSQL adapter - implements IUserRepository
   import psycopg2
   
   class PostgresUserRepository(IUserRepository):
       def __init__(self, connection_string: str):
           self.conn = psycopg2.connect(connection_string)
       
       def get_user_context(self, user_id: str) -> UserContext:
           cursor = self.conn.cursor()
           
           # Fetch viewing history
           cursor.execute(
               "SELECT product_id FROM views WHERE user_id = %s",
               (user_id,)
           )
           viewing_history = [row[0] for row in cursor.fetchall()]
           
           # Fetch purchase history  
           cursor.execute(
               "SELECT product_id FROM purchases WHERE user_id = %s",
               (user_id,)
           )
           purchase_history = [row[0] for row in cursor.fetchall()]
           
           # Fetch preferences
           cursor.execute(
               "SELECT preferences FROM users WHERE user_id = %s",
               (user_id,)
           )
           preferences = cursor.fetchone()[0]  # JSON column
           
           # Convert to domain model
           return UserContext(
               user_id=user_id,
               viewing_history=viewing_history,
               purchase_history=purchase_history,
               preferences=preferences
           )
   
   # S3 + TensorFlow adapter - implements IRecommendationModel
   import boto3
   import tensorflow as tf
   
   class TensorFlowRecommendationModel(IRecommendationModel):
       def __init__(self, model_s3_bucket: str, model_key: str):
           # Load model from S3
           s3 = boto3.client('s3')
           model_path = '/tmp/model.h5'
           s3.download_file(model_s3_bucket, model_key, model_path)
           self.model = tf.keras.models.load_model(model_path)
       
       def score_products(
           self, 
           user: UserContext, 
           products: List[Product]
       ) -> Dict[str, float]:
           # Convert domain objects to model features
           user_features = self._extract_user_features(user)
           product_features = [
               self._extract_product_features(p) for p in products
           ]
           
           # Run TensorFlow inference
           scores = self.model.predict([user_features, product_features])
           
           # Return dict mapping product_id -> score
           return {
               p.product_id: float(score)
               for p, score in zip(products, scores)
           }
       
       def _extract_user_features(self, user: UserContext):
           # Feature engineering logic
           return [...]  # Feature vector
       
       def _extract_product_features(self, product: Product):
           return [...]  # Feature vector
   ```
   Adapters are allowed to import external libraries (psycopg2, boto3, tensorflow). They handle messy real-world details—SQL queries, S3 downloads, TensorFlow API—and translate to/from clean domain interfaces.

7. **Implement Primary Adapters** - Create entry points that invoke the domain:
   ```python
   # Flask REST API adapter - primary adapter
   from flask import Flask, request, jsonify
   
   app = Flask(__name__)
   
   # Dependency injection - configure which adapters to use
   user_repo = PostgresUserRepository("postgresql://localhost/mydb")
   product_catalog = PostgresProductCatalog("postgresql://localhost/mydb")
   model = TensorFlowRecommendationModel("my-models-bucket", "rec-model-v3.h5")
   
   # Instantiate domain with dependencies
   recommendation_engine = RecommendationEngine(user_repo, product_catalog, model)
   
   @app.route('/recommendations/<user_id>', methods=['GET'])
   def get_recommendations(user_id):
       try:
           # Parse request parameters
           count = int(request.args.get('count', 10))
           
           # Call domain through primary port
           recommendations = recommendation_engine.generate_recommendations(
               user_id, count
           )
           
           # Convert domain objects to HTTP response
           return jsonify({
               'user_id': user_id,
               'recommendations': [
                   {
                       'product_id': rec.product.product_id,
                       'score': rec.score,
                       'explanation': rec.explanation
                   }
                   for rec in recommendations
               ]
           })
       except Exception as e:
           return jsonify({'error': str(e)}), 500
   
   # Batch processing adapter - another primary adapter
   import os
   
   class BatchRecommendationAdapter:
       def __init__(self, recommendation_engine: RecommendationEngine):
           self.engine = recommendation_engine
       
       def process_batch(self, user_ids_file: str, output_dir: str):
           # Read user IDs from file
           with open(user_ids_file) as f:
               user_ids = [line.strip() for line in f]
           
           # Process each user
           for user_id in user_ids:
               recommendations = self.engine.generate_recommendations(user_id)
               
               # Write to output file
               output_file = os.path.join(output_dir, f"{user_id}.json")
               with open(output_file, 'w') as f:
                   json.dump([
                       {'product_id': r.product.product_id, 'score': r.score}
                       for r in recommendations
                   ], f)
   ```
   Primary adapters receive requests from external systems (HTTP, files, messages), convert them to domain calls, and convert domain responses back to external formats. They're the "entry points" into the hexagon.

8. **Wire Everything Together** - Use dependency injection to assemble the system:
   ```python
   # Application startup / dependency injection configuration
   def create_application(config):
       # Instantiate secondary adapters based on configuration
       if config['user_repo'] == 'postgres':
           user_repo = PostgresUserRepository(config['db_connection'])
       elif config['user_repo'] == 'mock':
           user_repo = MockUserRepository()  # For testing
       
       if config['model'] == 'tensorflow':
           model = TensorFlowRecommendationModel(
               config['model_bucket'], 
               config['model_key']
           )
       elif config['model'] == 'sklearn':
           model = SklearnRecommendationModel(config['model_path'])
       
       # Instantiate domain with configured adapters
       engine = RecommendationEngine(user_repo, product_catalog, model)
       
       # Instantiate primary adapters
       api_adapter = create_flask_app(engine)
       batch_adapter = BatchRecommendationAdapter(engine)
       
       return {
           'api': api_adapter,
           'batch': batch_adapter
       }
   ```
   This is the only place where concrete adapter types are mentioned. The rest of the codebase works with interfaces.

**Testing Benefits:**

The architecture makes testing dramatically easier:

```python
# Test domain logic without any infrastructure
def test_recommendation_engine():
    # Create mock adapters that implement ports
    mock_user_repo = MockUserRepository()
    mock_user_repo.set_user(UserContext(
        user_id='user123',
        viewing_history=['product1', 'product2'],
        purchase_history=['product1'],
        preferences={'favorite_categories': ['electronics']}
    ))
    
    mock_catalog = MockProductCatalog()
    mock_catalog.set_products([
        Product('product2', 'electronics', 99.99, {}),
        Product('product3', 'books', 19.99, {}),
    ])
    
    mock_model = MockRecommendationModel()
    mock_model.set_scores({
        'product2': 0.8,
        'product3': 0.4  # Below threshold
    })
    
    # Instantiate domain with mocks
    engine = RecommendationEngine(mock_user_repo, mock_catalog, mock_model)
    
    # Test domain logic
    recommendations = engine.generate_recommendations('user123', 10)
    
    # Assertions
    assert len(recommendations) == 1  # Only product2 passes threshold
    assert recommendations[0].product.product_id == 'product2'
    assert recommendations[0].score == 0.8
    assert 'electronics' in recommendations[0].explanation

# Test ran in milliseconds, no database, no ML model, no HTTP server
```

You can test the domain exhaustively with simple mocks. Then test adapters independently (does PostgresUserRepository correctly query the database?). Then test integration (does everything wire together correctly?). The clear separation makes each testing level obvious.

## Think of It Like This

Imagine building a smart home system. At the center is your home automation brain—the logic that decides "if it's dark and someone's home, turn on lights" or "if temperature drops below 65°F, increase heating." This is your domain—the intelligence.

Your brain doesn't directly wire to light switches, thermostats, or motion sensors. Instead, it has **ports**—standardized interfaces like "I need something that can detect motion" or "I need something that can control lights." These ports define what capabilities the brain requires without specifying the technology.

**Adapters** connect these ports to actual devices. You might have:
- **Philips Hue Adapter** - Implements the "control lights" port using Hue API
- **Nest Thermostat Adapter** - Implements the "control temperature" port using Nest API  
- **Z-Wave Motion Sensor Adapter** - Implements the "detect motion" port using Z-Wave protocol
- **Alexa Adapter** - Implements "voice commands" input port, converts speech to commands for the brain
- **Mobile App Adapter** - Implements "user interface" input port, provides GUI to control the brain

The beautiful part: your brain's logic ("turn on lights when motion detected after sunset") never changes when you replace Philips Hue with LIFX bulbs, swap Nest for Ecobee thermostat, or add a web dashboard alongside the mobile app. You just swap adapters while the core logic remains untouched.

The brain depends on ports (abstractions), not adapters (implementations). Adapters depend on both the brain (they implement its ports) and specific technologies (they speak Hue API, Nest protocol, etc.). All dependencies point inward—the brain is protected from external change.

That's hexagonal architecture: protect your intelligent core (domain) behind ports (interfaces), connect to the messy real world through replaceable adapters (implementations).

## The "So What?" Factor

**If you use this:**
- **Test without infrastructure** - Test your core ML logic without starting databases, APIs, or GPU servers. Mock the ports, run thousands of tests in seconds, get instant feedback. Your test suite runs in milliseconds, not minutes. This dramatically increases development velocity—you can iterate on core logic without waiting for slow infrastructure.
- **Swap implementations freely** - Replace PostgreSQL with MongoDB, S3 with Azure Blob Storage, TensorFlow with PyTorch, REST API with GraphQL—all without touching domain code. Each swap is a new adapter. The domain never changes. This enables pragmatic technology choices: use SQLite in development, PostgreSQL in production, in-memory mocks in tests—same domain code.
- **Delay infrastructure decisions** - Start building domain logic before deciding on databases, cloud providers, or ML frameworks. Use mocks initially. Make infrastructure choices when you have real requirements and evidence, not upfront guesses. This is especially valuable in AI projects where the best serving infrastructure isn't clear until you know model size, latency requirements, and scale.
- **Isolate from framework churn** - When web frameworks evolve (Flask → FastAPI → next hot thing) or ML libraries change (TensorFlow 2.x → 3.x breaking changes), only adapters need updates. Your domain—the valuable IP where your intelligence lives—remains untouched. This protects your investment in core logic as technology churns.
- **Enable parallel development** - Different teams work on domain vs. adapters simultaneously. ML team builds recommendation logic with mock data sources. Data engineering team builds real database adapters against the port interface. Frontend team builds UI adapter calling mocked domain. Teams converge when adapters are complete—integration is just wiring, not rewriting.
- **Simplify upgrades and migrations** - Migrate from legacy systems incrementally by writing new adapters while keeping old ones. Run both adapters simultaneously, gradually shift traffic, validate new adapter correctness. When confident, delete old adapter. No big-bang migrations—smooth, reversible transitions.
- **Improve system understanding** - Clear boundaries make architecture explicit. New developers see: "this is the core domain, these are the ports it needs, these are our adapter implementations." No hunting through tangled code to understand responsibilities. Architecture is documented through structure, not separate diagrams.

**If you don't:**
- **Domain logic scattered everywhere** - ML model code mixed with HTTP request handlers mixed with database queries mixed with message queue consumers. Can't understand the recommendation algorithm without also understanding Flask routes and SQL queries. Cognitive overload makes everything harder.
- **Untestable business logic** - Can't test recommendation engine without starting PostgreSQL, loading TensorFlow model, and spinning up Flask server. Tests are slow (minutes), brittle (break when database schema changes), and environment-dependent (work on your laptop, fail in CI). This kills productivity—developers stop testing because it's too painful.
- **Technology lock-in** - Choosing Flask at project start means you're stuck with Flask. Database choice is permanent. ML framework can't be swapped. Every technology choice is a one-way door. When better options emerge or requirements change, you're trapped or forced into expensive rewrites.
- **Rippling changes** - Switching from PostgreSQL to MongoDB requires touching every file that mentions data: domain logic, tests, API handlers, background jobs. Changes cascade unpredictably. Migration projects drag on for months. High risk of breaking production during transition.
- **Difficult parallel development** - Can't build ML logic without database adapter finished. Can't build API without model code done. Can't test UI without backend deployed. Sequential dependencies slow everyone down. Adding developers doesn't speed up development—they block on each other.
- **Framework upgrade nightmares** - When TensorFlow releases breaking changes or Flask deprecates APIs, updates touch your core business logic. Risk breaking domain code while upgrading infrastructure. Upgrades become risky, expensive projects postponed indefinitely. Technical debt accumulates.

## Practical Checklist

Before implementing hexagonal architecture, ask yourself:

- [ ] **Do I have complex domain logic worth protecting?** - If your system is mostly CRUD with trivial logic, hexagonal might be overkill. If you have sophisticated ML pipelines, complex business rules, or valuable algorithms, the protection is worth it. Simple apps: skip it. Complex domains: embrace it.
- [ ] **Will I need multiple adapters for the same port?** - If you'll only ever have one database, one API, one model framework, adapter abstraction is pure overhead. If you'll test with mocks + run with real implementations, or support multiple platforms, or migrate technologies, ports/adapters pay off. One adapter per port: questionable value. Multiple adapters: clear win.
- [ ] **Can I resist framework invasiveness?** - Some frameworks (Django, Rails) tightly couple to your code. Keeping the domain pure requires discipline—fight the framework's tendency to spread everywhere. Other frameworks (Flask, Express) are more amenable to hexagonal. Assess whether you can actually maintain the boundaries with your chosen tools.
- [ ] **Do I understand dependency injection?** - Hexagonal architecture requires injecting port implementations into domain constructors. If your team isn't comfortable with DI, the pattern will feel awkward and get implemented incorrectly (new'd up dependencies instead of injected, defeating the purpose). Either learn DI first or choose simpler patterns.
- [ ] **Where do my secondary ports live?** - Ports are interfaces the domain defines. Put them in the domain package/module, not with adapters. The domain owns its dependencies' contracts—adapters conform to domain needs, not vice versa. If ports live with adapters, you've inverted the relationship and lost the benefit.
- [ ] **What's my port granularity?** - Too fine-grained: 50 ports, each with one method. Too coarse: one port with 50 methods. Find balance: group related operations (IUserRepository with get, create, update, delete), but don't create god interfaces. Aim for cohesive responsibilities.
- [ ] **How will I handle transactions across ports?** - If a domain operation calls multiple secondary ports and you need atomicity (all succeed or all fail), you need transaction management. Options: pass transaction context through ports, use unit-of-work pattern, or accept eventual consistency. Plan this upfront—retrofitting transactions is painful.
- [ ] **Will I use a dependency injection framework?** - Hand-wiring dependencies works for small apps (create adapters in main function, pass to domain). Larger apps benefit from DI containers (Spring, Guice in Java; dependency-injector in Python). Choose based on complexity: <5 dependencies → hand-wire. >10 → use container.
- [ ] **How will I organize files/packages?** - Common structure: `domain/` (core logic, models, ports), `adapters/primary/` (REST, CLI, batch), `adapters/secondary/` (database, storage, external APIs), `main.py` or `app.py` (wiring). Clear structure reinforces boundaries. Don't mix adapters into domain packages.
- [ ] **What testing strategy will I use?** - Test pyramid: many fast domain unit tests (mock ports), moderate adapter integration tests (test against real tech), few end-to-end tests (full system). Focus on domain—that's where your valuable logic lives. Adapters are simpler—mostly translation code. Test proportionally.
- [ ] **How do I prevent adapter details from leaking?** - Use domain models, not adapter models, for port parameters/returns. Don't return SQLAlchemy ORM objects through ports—return domain objects. Don't accept HTTP Request objects in domain—accept domain commands. Convert at adapter boundaries. This is tedious but essential.

## Watch Out For

⚠️ **Anemic ports** - Ports that are too thin, just barely wrapping database calls without adding domain value. Example: `IUserRepository` with methods like `executeQuery(sql)`. This doesn't isolate the domain—you're just adding indirection without abstraction. Ports should be domain-centric: `getUserByEmail(email)`, not tech-centric: `query(table, conditions)`. Make ports express domain needs, not infrastructure operations.

⚠️ **Leaky abstractions** - Port interfaces that expose adapter implementation details. Example: `IModelRepository.loadModelFromS3(bucket, key)` instead of `IModelRepository.loadModel(modelId)`. The "FromS3" reveals implementation. The domain shouldn't know about S3—that's an adapter detail. Keep ports pure: define what the domain needs (a model), not how to get it (from S3).

⚠️ **Adapter logic creeping into domain** - Domain code checking "if adapter is PostgresAdapter, do X; if MongoAdapter, do Y." This defeats the entire purpose—domain should be adapter-agnostic. If different adapters require different domain behavior, you haven't abstracted correctly. Fix the port interface to hide those differences.

⚠️ **Too many layers of indirection** - Hexagonal + layered architecture + microservices + event sourcing + CQRS = architecture astronaut territory. You can over-engineer yourself into paralysis. Start simple: just hexagonal. Add other patterns only when you have specific problems they solve. Each pattern adds complexity—ensure the benefits exceed the costs.

⚠️ **Ports defined by adapters** - The adapter team says "we're using PostgreSQL, here's the interface it provides" and the domain team adapts to that interface. Backwards! The domain defines the interface based on what it needs; adapters implement that interface however they want. Domain dictates, adapters comply. This is dependency inversion—get the direction right.

⚠️ **Ignoring adapter complexity** - Assuming adapters are trivial "just translation" code. In reality, adapters handle messy concerns: retries, timeouts, connection pooling, error handling, caching, logging. They can be quite complex. Don't starve adapter development—allocate proper time and expertise. Complex adapters deserve tests too (integration tests against real infrastructure).

⚠️ **Mapper hell** - Converting between domain objects, adapter models, and external DTOs creates mapping code. Lots of it. `toUserEntity(domainUser)`, `fromDbRow(row)`, `toApiResponse(domainModel)`. This is boilerplate that feels wasteful. Tools help (AutoMapper, dataclass transformations), but you'll still write mapping code. Accept this as the price of decoupling. The tedium is worth the flexibility.

⚠️ **Not testing the domain in isolation** - Having hexagonal architecture but still starting a database for domain tests. You've missed the point. Domain tests should run in milliseconds with zero infrastructure. If your domain tests require a database, you haven't achieved decoupling—check for leaky ports or domain code directly importing infrastructure.

⚠️ **Forgetting about configuration** - Adapters need configuration (database URLs, API keys, model paths). Don't hardcode in adapters. Don't pass through domain (domain shouldn't know about config). Instead, inject configured adapters: `PostgresUserRepository(config.db_url)` → inject into domain. Keep config at the edges (main/startup), pass configured objects inward.

⚠️ **Inconsistent naming** - Mixing terminology: ports/adapters, interfaces/implementations, contracts/services. Pick consistent names: "ports" for interfaces the domain defines, "adapters" for implementations that connect to tech, "domain services" for core logic classes. Consistent terminology reduces confusion, especially for newcomers.

⚠️ **Premature optimization** - Worrying that adapter abstraction adds performance overhead. For 99% of systems, the indirection is negligible compared to database queries, network calls, or ML inference. Measure before optimizing. If you're in the 1% where nanoseconds matter, you probably shouldn't use hexagonal. For everyone else, the overhead is unmeasurable and the benefits are massive.

## Connections

**Builds On:**
- Dependency inversion principle (high-level modules depend on abstractions)
- Interface segregation (ports are focused interfaces)
- Single responsibility (domain, ports, and adapters have distinct responsibilities)
- Separation of concerns (domain separate from infrastructure)

**Works With:**
- [layered_architecture](layered_architecture.md) - Hexagonal can be viewed as a more rigorous, explicit form of layering with inward dependencies
- [microservices](microservices.md) - Apply hexagonal within each microservice for clean internal architecture
- Domain-driven design (DDD) - Hexagonal provides infrastructure for DDD's domain model patterns
- Test-driven development (TDD) - Hexagonal enables fast, isolated unit tests essential for TDD

**Leads To:**
- Clean architecture (Uncle Bob's concentric circles variant)
- Onion architecture (Jeffrey Palermo's layered variant with dependencies flowing inward)
- Event-driven hexagonal systems (adapters communicate via events)
- CQRS (command query responsibility segregation) with hexagonal structure

## Quick Decision Guide

**Use hexagonal architecture when:**
- Building systems with complex domain logic (AI/ML pipelines, sophisticated business rules)
- Need extensive testing without infrastructure (fast test suites, TDD workflows)
- Will integrate with multiple external systems (different databases, APIs, message queues, model frameworks)
- Expect technology changes over time (migrate databases, upgrade frameworks, swap cloud providers)
- Want to delay infrastructure decisions (focus on domain first, choose tech later)
- Team large enough that parallel development on domain vs. adapters makes sense
- Building systems for long-term evolution (5+ year lifespan, multiple teams, ongoing feature development)

**Skip hexagonal architecture when:**
- Building simple CRUD apps with trivial logic (cost exceeds benefit)
- Prototyping or proof-of-concept (speed over structure)
- System has minimal domain logic, mostly integration (data pipelines with little transformation)
- Solo developer on small project (<5,000 lines, <6 months)
- Team unfamiliar with dependency injection and interfaces (too steep a learning curve without training)
- Performance is so critical that abstraction overhead matters (rare—measure first)
- Using framework that fights hexagonal (Django, Rails) without the discipline to enforce boundaries

**Choose hexagonal over layered when:**
- Need symmetric architecture (multiple entry points: REST, batch, CLI, message queue)
- Want explicit dependency inversion (all dependencies flow inward to domain)
- Need to swap implementations frequently (multiple adapters per port)
- Testing without infrastructure is critical (isolated domain tests)

**Choose layered over hexagonal when:**
- Asymmetric architecture (clear presentation → business → data flow)
- Simpler mental model for team (horizontal strata easier to explain than ports/adapters)
- Less emphasis on swappable implementations (single database, single API style)
- Team prefers familiar patterns over newer concepts

## Further Exploration

- 📖 **"Hexagonal Architecture" by Alistair Cockburn** - Original article explaining the pattern from the creator; available at alistair.cockburn.us
- 📖 **"Get Your Hands Dirty on Clean Architecture"** by Tom Hombergs - Practical guide to hexagonal/clean architecture with Java examples
- 🎯 **"Implementing Domain-Driven Design"** by Vaughn Vernon - Shows how hexagonal architecture supports DDD patterns
- 💡 **"Clean Architecture"** by Robert C. Martin - Uncle Bob's variant emphasizing use cases and entities layers
- 🎯 **"Ports and Adapters in Practice"** - Netflix Tech Blog series on applying hexagonal at scale
- 💡 **"Architecture Patterns with Python"** by Harry Percival & Bob Gregory - TDD and hexagonal architecture with Python examples
- 📖 **"Growing Object-Oriented Software, Guided by Tests"** by Freeman & Pryce - Test-driven approach naturally leads to hexagonal structure
- 🎯 **"Hexagonal Architecture in Action"** course by Valentina Cupać - Hands-on tutorial building hexagonal systems
- 💡 **"The Clean Code Blog"** by Robert C. Martin - Regular articles on architecture principles underlying hexagonal
- 🎯 **"Designing Event-Driven Systems"** by Ben Stopford - Combining hexagonal architecture with event-driven patterns
- 💡 **"Domain-Driven Design Distilled"** by Vaughn Vernon - Concise DDD guide showing hexagonal's role
- 📖 **"Software Architecture in Practice"** by Bass, Clements, Kazman - Academic perspective on architectural patterns including ports/adapters

---
*Added: May 19, 2026 | Updated: May 19, 2026 | Confidence: High*
