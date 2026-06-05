# Versioning Strategy

## At a Glance

| Aspect | Details |
|--------|---------|
| **What It Is** | A systematic approach to tracking, identifying, and managing different versions of artifacts (code, models, data, documentation, configurations) over time—enabling reproducibility, rollback, compatibility management, and coordinated evolution of complex systems |
| **Key Principle** | Every significant change creates a new identifiable version—making "what changed, when, and why" explicit rather than implicit |
| **Primary Use** | Code releases, API evolution, ML model deployment, dataset tracking, configuration management, documentation versioning, dependency coordination across multi-artifact systems |
| **Critical Success Factor** | Version identifiers convey meaningful information about compatibility, breaking changes, and relationship between versions |
| **Common Mistake** | Random version numbers without semantic meaning, making it impossible to predict compatibility or understand change significance |
| **2026 AI Context** | AI systems require coordinated versioning across code, models, datasets, prompts, and configurations—versioning strategy critical for reproducibility, A/B testing, rollback, and managing model-code-data interdependencies |

## One-Sentence Summary

**Versioning strategy is a systematic approach to identifying and tracking different versions of artifacts over time using meaningful identifiers that communicate compatibility, change significance, and relationships—enabling reproducibility, safe evolution, and coordinated management of complex multi-artifact systems.**

## Why This Matters to You

If you've ever:
- **Deployed a change** that broke production and couldn't remember what the working version was
- **Tried to reproduce results** from three months ago but couldn't figure out which model version, dataset version, or code version was used
- **Updated a library** only to discover it broke everything that depended on it—with no warning it would happen
- **Worked on two features** simultaneously and needed to deploy one without the other but everything was tangled together
- **Debugged an issue** and couldn't tell if the problem was new or existed in previous versions
- **Tested multiple models** in production and lost track of which version performed best with which configuration
- **Collaborated on AI systems** where someone says "the model isn't working" but you don't know if they mean v1, v2, or the experimental version
- **Needed to roll back** a deployment but had no idea what to roll back to or what else would be affected

...then understanding versioning strategy transforms how you build and operate systems that evolve over time.

Here's the reality: **Without versioning strategy, you're navigating blind**. You can't reproduce results because you don't know what versions you used. You can't coordinate changes because you don't know what's compatible. You can't roll back safely because you don't know what was working. You can't deploy gradually because you can't identify specific versions. Every change becomes a gamble instead of a managed evolution.

This gets exponentially worse with AI systems because you're not just versioning code—you're versioning **models** (which version of GPT-4? Which fine-tuned checkpoint?), **datasets** (training data from March or May?), **prompts** (the prompt that worked or the "improved" one that didn't?), **configurations** (temperature 0.7 or 0.9?), and **code** simultaneously. These artifacts interdepend—model v2 requires dataset v3, which requires processing code v1.5, which requires config v4. Without versioning strategy, these dependencies become an invisible web of "it works on my machine but not yours" chaos.

In 2026, versioning strategy isn't optional—it's **the foundation of reproducible AI**. When someone reports "the agent is hallucinating," you need to know: Which model version? Which prompt version? Which code version? Which configuration? Without version identifiers, that question is unanswerable. With proper versioning strategy, it's a quick lookup: "Oh, that's model v2.1 with prompt v3 and config v1.2—known issue, fixed in v2.2."

**Bottom line**: Versioning strategy is how you transform chaos into controlled evolution. It's the difference between "I think this might work" and "I know this combination of versions works because it's been validated." It's prerequisite to reproducibility, reliability, and professional software delivery.

## The Core Idea

### What It Is

**Versioning strategy** is a systematic approach characterized by:

**Core Components**:
- **Identification scheme**: Convention for assigning version identifiers (numbers, dates, hashes, labels)
- **Significance levels**: What different version changes mean (major/minor/patch, breaking/compatible)
- **Change tracking**: Recording what changed between versions and why
- **Compatibility rules**: How to determine if versions work together
- **Release cadence**: When and why new versions are created
- **Artifact scope**: What gets versioned (code, models, data, docs, configs, APIs)
- **Coordination mechanism**: How versions across multiple artifacts relate to each other

**Common Versioning Schemes**:

**1. Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`
```
Format: v2.4.7

MAJOR (2): Breaking changes—incompatible with v1.x
MINOR (4): New features—backward compatible with v2.0+
PATCH (7): Bug fixes—backward compatible with v2.4.0+

Examples:
v1.0.0 → Initial release
v1.1.0 → Added feature (compatible with v1.0.0)
v1.1.1 → Fixed bug (compatible with v1.1.0)
v2.0.0 → Breaking change (NOT compatible with v1.x)

Promise: v1.x.x all work together, v2.0.0+ breaks something
```

**2. Calendar Versioning (CalVer)**: Date-based
```
Format: YYYY.MM.DD or YYYY.MM.MICRO

Examples:
2026.05.15 → Released May 15, 2026
2026.05.1 → First May 2026 release
2026.06.1 → First June 2026 release

Use when: Release timing matters more than change significance
Common in: Ubuntu (22.04 = April 2022), datasets ("May 2026 dataset")
```

**3. Hash-Based**: Git commit SHA
```
Format: 7-40 character hexadecimal

Examples:
a3f2b1c → Short SHA (7 chars)
a3f2b1c4d5e6f7890abcdef → Full SHA (40 chars)

Use when: Exact reproduction critical, continuous deployment
Common in: Docker images, build artifacts, ML experiment tracking
```

**4. Sequential**: Simple incrementing numbers
```
Format: 1, 2, 3, 4...

Examples:
Model v1, Model v2, Model v3
Build 1234, Build 1235

Use when: Simple progression sufficient, compatibility not encoded
Common in: Internal builds, model experiments
```

**5. Named/Labeled**: Descriptive names
```
Examples:
"Alpha", "Beta", "Stable", "LTS"
"Nightly", "Experimental", "Production"
"GPT-4-turbo", "GPT-4-vision", "GPT-4-32k"

Use when: Marketing names, deployment channels, capability variants
Often combined: v2.0.0-beta, v3.1.0-LTS
```

**Version Relationships**:

```
Single Artifact Versioning:
Code v1.0 → v1.1 → v1.2 → v2.0 → v2.1

Multi-Artifact Versioning (AI System):
Code v1.0 + Model v1.0 + Data v1.0 = System v1.0
Code v1.1 + Model v1.0 + Data v1.0 = System v1.1 (code updated)
Code v1.1 + Model v2.0 + Data v1.0 = System v2.0 (model updated)
Code v1.1 + Model v2.0 + Data v2.0 = System v2.1 (data updated)

Each artifact versions independently, system version coordinates.
```

**The Critical Insight**: Version identifiers must **communicate meaning**, not just distinguish versions. "v2.0.0" tells you "this breaks compatibility." "2026.05.15" tells you "this is from May 15." "a3f2b1c" tells you "this is exact commit." Random numbers like "v17" tell you nothing—useless for decision-making.

**2026 AI Context**:

AI systems require versioning strategy for multiple interdependent artifacts:

**Code Versioning**:
```python
# Agent framework code
agent_framework v1.0.0: Initial release
agent_framework v1.1.0: Added tool calling (compatible)
agent_framework v2.0.0: New memory system (breaks v1.x agents)
```

**Model Versioning**:
```python
# ML model artifacts
gpt-4-0314: March 14, 2023 version
gpt-4-turbo-2024-04-09: April 9, 2024 version
fine-tuned-classifier-v2.3: Your fine-tuned model version 2.3

# Custom model versioning
customer_intent_classifier:
  v1.0: 85% accuracy, 10ms latency (baseline)
  v1.1: 87% accuracy, 10ms latency (improved training)
  v2.0: 89% accuracy, 50ms latency (larger model—breaking SLA!)
```

**Dataset Versioning**:
```python
# Training/eval data
training_data_2026_05: May 2026 snapshot
training_data_v2.1: Cleaned version, outliers removed
synthetic_examples_v3: Third generation of synthetic data

# Version affects reproducibility
Model v2 trained on data_v1 ≠ Model v2 trained on data_v2
```

**Prompt Versioning**:
```python
# Prompt templates
system_prompt_v1 = "You are a helpful assistant."
system_prompt_v2 = "You are a helpful assistant. Today is {date}."
system_prompt_v3 = """You are a helpful assistant.
Today is {date}.
Always cite sources using [[Source Name]]."""

# Prompt version dramatically affects behavior
# Must track which version produced which results
```

**Configuration Versioning**:
```python
# Model configurations
config_v1 = {"temperature": 0.7, "max_tokens": 500}
config_v2 = {"temperature": 0.9, "max_tokens": 1000, "top_p": 0.95}

# Config changes affect outputs—must version
```

**The 2026 Challenge**: An AI system's behavior emerges from **combination of versions**:
```
System behavior = f(code_version, model_version, data_version, 
                    prompt_version, config_version)

To reproduce results, must track ALL versions.
To debug issues, must know ALL versions.
To deploy safely, must coordinate ALL versions.
```

### What It Isn't

**Not just incrementing numbers**: `v1, v2, v3` without meaning—versions must communicate significance (breaking changes, compatibility, etc.)

**Not only for code**: Versioning strategy applies to models, data, documentation, APIs, configurations, prompts—any artifact that evolves

**Not the same as version control (Git)**: Git tracks changes, versioning strategy defines what identifiers mean and how artifacts coordinate

**Not only for external APIs**: Internal components benefit from versioning—knowing which internal model version is deployed

**Not set-it-and-forget-it**: Versioning strategy evolves as understanding deepens—may start simple, add sophistication as needed

**Not guaranteeing backward compatibility**: Versioning strategy IDENTIFIES compatibility, doesn't create it—still need to design for compatibility

## How It Works

### Choosing a Versioning Scheme

**Decision Matrix**:

| Artifact Type | Recommended Scheme | Rationale |
|--------------|-------------------|-----------|
| **Public APIs** | SemVer (MAJOR.MINOR.PATCH) | Compatibility promises critical for consumers |
| **ML Models** | Sequential + metadata (model-v3) | Simple progression, metadata tracks performance |
| **Training Data** | CalVer (YYYY-MM) | Data freshness often matters most |
| **Prompts** | Sequential + description (prompt-v2-citations) | Iterative improvement, description helps |
| **Configurations** | SemVer or hash | Breaking config changes like breaking code changes |
| **Docker Images** | Hash + tag (sha256:abc...def, tag: v2.1.0) | Exact reproduction + human-readable tag |
| **Internal Code** | SemVer or hash | Coordination with other components |
| **Experimental** | Hash or sequential | Rapid iteration, exact tracking |

**Hybrid Approaches** (common in practice):
```
v2.1.3+20260515.a3f2b1c
│ │ │  │        └─ Git hash (exact commit)
│ │ │  └─ Build date (calendar component)
│ │ └─ Patch (bug fixes)
│ └─ Minor (features)
└─ Major (breaking changes)

Combines: Semantic meaning + date context + exact reproducibility
```

### Implementing Versioning Strategy

**1. Single Artifact Versioning (Code Library)**

```python
# Your Python package
pyproject.toml:
  version = "1.2.3"

# Semantic Versioning rules
1.2.3 → 1.2.4: Bug fix (patch bump)
1.2.3 → 1.3.0: New feature, backward compatible (minor bump)
1.2.3 → 2.0.0: Breaking change (major bump)

# What's a breaking change?
- Removing a function
- Changing function signature
- Changing return type
- Changing behavior that breaks existing use

# What's a minor change?
- Adding new function (existing code still works)
- Adding optional parameter with default
- Fixing bug that doesn't change API

# What's a patch?
- Bug fix with no API change
- Documentation update
- Performance improvement
```

**2. ML Model Versioning**

```python
# Model artifact versioning
models/
  customer_intent_classifier/
    v1.0/
      model.pkl
      metadata.json: {
        "version": "1.0",
        "trained_date": "2026-04-15",
        "dataset_version": "2026-04-01",
        "accuracy": 0.85,
        "latency_ms": 10
      }
    v1.1/
      model.pkl
      metadata.json: {
        "version": "1.1",
        "trained_date": "2026-05-01",
        "dataset_version": "2026-04-15",  # Same data, better training
        "accuracy": 0.87,
        "latency_ms": 10,
        "improvements": "Hyperparameter tuning"
      }
    v2.0/
      model.pkl
      metadata.json: {
        "version": "2.0",
        "trained_date": "2026-05-15",
        "dataset_version": "2026-05-01",  # New data
        "accuracy": 0.89,
        "latency_ms": 50,  # BREAKING: Latency increased!
        "breaking_changes": "Larger model—may break latency SLAs"
      }

# Version communicates: v2.0 = breaking change (latency)
```

**3. Dataset Versioning**

```python
# Dataset versioning with CalVer
datasets/
  customer_conversations/
    2026-03/
      data.jsonl
      schema.json
      stats.json: {"size": 100000, "date_range": "2026-03-01 to 2026-03-31"}
    2026-04/
      data.jsonl
      schema.json  # Schema evolved
      schema_changes.md: "Added 'sentiment' field"
      stats.json: {"size": 120000, "date_range": "2026-04-01 to 2026-04-30"}
    2026-05/
      data.jsonl
      schema.json
      stats.json: {"size": 150000, "date_range": "2026-05-01 to 2026-05-31"}

# CalVer communicates: Data freshness
# Schema changes documented when version changes
```

**4. Prompt Versioning**

```python
# Prompt template versioning
prompts/
  system_prompt_v1.txt:
    "You are a helpful AI assistant."
  
  system_prompt_v2.txt:
    "You are a helpful AI assistant. Today is {{date}}. 
     Always cite sources."
  
  system_prompt_v3.txt:
    "You are a helpful AI assistant. Today is {{date}}.
     Always cite sources using [[Source Name]].
     If you're uncertain, say so explicitly."
  
  prompt_registry.json: {
    "v1": {"file": "system_prompt_v1.txt", "deployed": "2026-03-01"},
    "v2": {"file": "system_prompt_v2.txt", "deployed": "2026-04-15"},
    "v3": {"file": "system_prompt_v3.txt", "deployed": "2026-05-15"}
  }

# Track which prompt version produced which results
logging: {
  "timestamp": "2026-05-15T10:30:00Z",
  "prompt_version": "v3",
  "model_version": "gpt-4-turbo-2024-04-09",
  "response": "..."
}
```

**5. Coordinated Multi-Artifact Versioning**

```python
# System manifest coordinating versions
deployment_manifest.yaml:
  system_version: "2.1.0"
  components:
    code: 
      version: "1.3.0"
      repo: "github.com/org/ai-agent"
      commit: "a3f2b1c"
    model:
      version: "2.0"
      artifact: "models/intent_classifier/v2.0/model.pkl"
      sha256: "def456..."
    dataset:
      version: "2026-05"
      location: "datasets/customer_conversations/2026-05/"
    prompt:
      version: "v3"
      file: "prompts/system_prompt_v3.txt"
    config:
      version: "1.2.0"
      file: "configs/production.yaml"
  
  compatibility_notes: "Model v2.0 requires code v1.3.0+"

# This manifest enables:
# 1. Exact reproduction (all versions specified)
# 2. Compatibility checking (before deployment)
# 3. Rollback (revert to previous manifest)
# 4. Debugging (know exact combination that failed)
```

### Version Compatibility Management

**Compatibility Guarantees** (SemVer example):

```python
# Library A versions
v1.0.0: Initial release
v1.1.0: Added new_feature() [compatible with v1.0.0 code]
v1.2.0: Added another_feature() [compatible with v1.0.0, v1.1.0 code]
v2.0.0: Removed deprecated_function() [BREAKS v1.x code using that function]

# Compatibility promise
Code using: "A >= 1.0.0, < 2.0.0"
Works with: v1.0.0, v1.1.0, v1.2.0, v1.3.0, etc.
Breaks with: v2.0.0+

# Semantic promise: Major version bump = breaking change
```

**Dependency Version Constraints**:

```python
# requirements.txt with version constraints
# Exact version (reproducibility)
openai==1.12.0

# Compatible versions (allow patches)
requests>=2.31.0,<2.32.0  # Allow 2.31.x patches

# Major version constraint (allow minor + patches)
langchain>=0.1.0,<0.2.0  # Allow 0.1.x updates

# Flexible (dangerous—any version)
numpy>=1.24.0  # Could break with v2.0.0

# Best practice: Pin major, allow minor/patch
transformers>=4.30.0,<5.0.0
```

**Model-Code Compatibility**:

```python
# Code checks model version compatibility
def load_model(model_path):
    metadata = json.load(f"{model_path}/metadata.json")
    model_version = metadata["version"]
    
    # Check compatibility
    if model_version.startswith("1."):
        return load_v1_model(model_path)
    elif model_version.startswith("2."):
        if CODE_VERSION < "1.3.0":
            raise ValueError(
                f"Model v{model_version} requires code v1.3.0+, "
                f"but running code v{CODE_VERSION}"
            )
        return load_v2_model(model_path)
    else:
        raise ValueError(f"Unknown model version: {model_version}")

# Explicit compatibility checking prevents runtime failures
```

### Version Lifecycle

**Typical Lifecycle**:

```
Development → Testing → Staging → Production → Deprecated → Retired

Example (API versioning):
v1.0: 2024-01-01: Released
v1.1: 2024-03-01: Released (v1.0 still supported)
v2.0: 2024-06-01: Released (v1.x still supported)
v2.1: 2024-09-01: Released
      2024-10-01: v1.x deprecated (warning, still works)
      2025-01-01: v1.x retired (shut down)
      
Lifecycle: 6 months supported + 3 months deprecated + shut down
Users have 9 months to migrate from v1.x to v2.x
```

**Deprecation Strategy**:

```python
# Version 1.5: Introduce new API, deprecate old
@deprecated(version="1.5.0", removal="2.0.0", alternative="new_function()")
def old_function():
    warnings.warn("old_function() deprecated, use new_function()", 
                  DeprecationWarning)
    return new_function()

# Version 2.0: Remove old API
# old_function() no longer exists

# Users had v1.5-v1.9 to migrate
# v2.0 major bump signals: "breaking changes"
```

## Think of It Like This

### The House Address Analogy

**Without Versioning Strategy = "The blue house"**

You're trying to deliver a package:
- "Take this to the blue house"
- You drive around: "There are 50 blue houses on this street. Which one?"
- "The one with the tree in front"
- "30 of them have trees. Which one??"
- "Um... the one that was painted last year?"
- **Result**: Can't reliably identify the right house

**With Versioning Strategy = "123 Main Street, Apartment 4B"**

You're trying to deliver a package:
- "Take this to 123 Main Street, Apartment 4B"
- You drive directly to 123 Main Street
- Enter building, find apartment 4B
- Deliver package successfully
- **Result**: Clear, unambiguous identification

**The Key Insight**: Version identifiers are like addresses—they must **uniquely and unambiguously identify** what you're referring to. "The latest model" (like "the blue house") is ambiguous. "model-v2.3-2026-05-15-a3f2b1c" (like "123 Main St, Apt 4B") is precise.

### The Evolution Story Analogy

**Traditional Software = Novel Editions**

You're publishing a novel:
- **First Edition (v1.0)**: Original book published
- **Second Edition (v2.0)**: Revised, some chapters rewritten, new ending
- **Third Edition (v3.0)**: Major rewrite
- Editions clearly marked, readers know what they're getting
- Can find "Second Edition" years later and know it's the revised version

**AI System Without Versioning = Oral Tradition**

You're telling a story passed down orally:
- You tell the story to someone
- They tell it to someone else, add details, change parts
- That person tells another person, modifies it further
- Six people later: "Wait, what was the original story?"
- **No one knows** what the original was or how it evolved
- Can't go back to "the version from three retellings ago"

**AI System With Versioning = Git History for Everything**

You're tracking story evolution:
- **v1.0**: Original story recorded (model, data, prompt, config)
- **v1.1**: Added detail to middle section (updated prompt)
- **v2.0**: Changed main character (new model, breaking change)
- **v2.1**: Added new ending (compatible update)
- Can checkout any version, see exactly what changed, reproduce any version
- **Clear lineage** from origin to current state

**The Key Insight**: Without versions, evolution is chaos—can't go back, can't reproduce, can't compare. With versions, evolution is documented history—every state preserved, every change traceable.

## The "So What?" Factor

### Why Versioning Strategy Transforms System Management

**1. Enables Reproducibility**

Without versioning:
```
User: "The agent was working perfectly last month!"
You: "What model were you using?"
User: "The agent model... the one we had?"
You: "Which one? We've updated it 15 times..."
User: "I don't know... the working one."

Result: Can't reproduce "the working one"—lost forever.
```

With versioning:
```
User: "The agent was working perfectly last month!"
You: (Checks logs) "You were using system v2.3.1:"
    - code v1.2.0
    - model-v5 (trained 2026-04-15)
    - prompt v7
    - config v3.1
You: (Deploys exact version) "Try this—it's the exact combination from last month."

Result: Reproduced in 5 minutes.
```

**Real Impact**: Without versions, **"it was working before" is unsolvable**. With versions, it's a lookup and redeployment. Bug reports become actionable instead of mysteries.

### 2. Enables Safe Rollback

Without versioning:
```
Deploy new model → Production breaks
You: "Roll back!"
Team: "Roll back to what? We've deployed 20 times this month..."
You: "The last working version!"
Team: "Which one was that? And which code version worked with it?"

Result: Panic, guessing, possibly making it worse.
```

With versioning:
```
Deploy system v3.1.0 → Production breaks
You: "Roll back to v3.0.5" (last verified working version)
Script: Deploys exact manifest:
  - code v1.4.2
  - model v7
  - prompt v9
  - config v4.0
Verify: Production restored
Post-mortem: Compare v3.0.5 vs v3.1.0 manifests to find issue

Result: 5-minute recovery, clear investigation path.
```

**Real Impact**: Mean time to recovery (MTTR) drops from **hours to minutes** when you can precisely identify and deploy working versions.

### 3. Enables Coordinated Multi-Artifact Evolution

Without versioning:
```
Engineer A: Updates model (better accuracy!)
Engineer B: Updates code (refactored!)
Engineer C: Updates prompts (improved!)

Deploy all three → System breaks

Who broke it?
- Model update incompatible with old code?
- Code update incompatible with old prompts?
- Prompt update incompatible with old model?
- Combination of all three?

Result: Debugging nightmare—no way to isolate issue.
```

With versioning:
```
Engineer A: model v7 → v8 (metadata: "requires code v1.5+")
Engineer B: code v1.4 → v1.5 (breaking: new model API)
Engineer C: prompt v9 → v10 (compatible with code v1.4+)

Deploy:
1. code v1.5 + model v7 + prompt v10 → Test (works)
2. code v1.5 + model v8 + prompt v10 → Test (works)
3. Deploy to production with confidence

Result: Isolated changes, tested combinations, confident deployment.
```

**Real Impact**: **Coordinated evolution becomes possible** instead of Russian roulette. Can test combinations before production, understand dependencies, deploy incrementally.

### 4. Enables A/B Testing and Gradual Rollout

Without versioning:
```
Want to test new model:
- Deploy to 10% of traffic
- Realize: Can't identify which model served which request
- Can't compare performance model-to-model
- Can't route specific users to specific versions

Result: A/B testing impossible, must deploy to 100% or nothing.
```

With versioning:
```
A/B test:
- 50% traffic → system v2.0 (model-v5)
- 50% traffic → system v2.1 (model-v6)

Log every request with system version:
{
  "request_id": "req-123",
  "system_version": "2.0",
  "model_version": "v5",
  "latency_ms": 120,
  "user_rating": 4.5
}

Analyze after 1 week:
- Model v5 avg rating: 4.3, avg latency: 120ms
- Model v6 avg rating: 4.6, avg latency: 110ms

Decision: Roll out v6 to 100%

Result: Data-driven decisions, controlled risk.
```

**Real Impact**: **Gradual rollout and A/B testing require versions**. Without them, you're flying blind—can't compare, can't route, can't attribute behavior to specific configurations.

### 5. Enables Clear Communication

Without versioning:
```
User: "The model is broken!"
You: "Which model?"
User: "The intent classifier"
You: "We have three intent classifiers... which one?"
User: "The one in production"
You: "We're running different versions for different customers..."
User: "The one that's broken!"

Result: 20-minute conversation to figure out what they're talking about.
```

With versioning:
```
User: "Model v2.3 is returning wrong intents for support queries!"
You: (Checks) "v2.3 deployed to enterprise customers, handles support queries"
You: "Can you share request ID?"
User: "req-abc-123"
You: (Looks up) "Used model v2.3, prompt v8, config v3.1—reproduced issue"
You: "Rolling back to v2.2 for your account, will fix v2.3 and redeploy"

Result: 5-minute conversation, immediate action.
```

**Real Impact**: Versions create **common language** for discussing system state. "Model v2.3 has issue X" is precise. "The model is broken" is vague.

### 6. Enables Compliance and Auditability

Without versioning:
```
Auditor: "Which model version did you use to make this credit decision on March 15?"
You: "Um... the model we had in March?"
Auditor: "Which one specifically? Can you reproduce the decision?"
You: "We've updated the model 10 times since March..."

Result: Compliance failure, potential legal issues.
```

With versioning:
```
Auditor: "Which model version made this credit decision on March 15?"
You: (Checks logs) "System v3.2.1—model-v8 trained on 2026-02-dataset"
Auditor: "Can you reproduce the decision?"
You: (Deploys v3.2.1 in test env) "Here's exact reproduction with same inputs"

Result: Full auditability, compliance maintained.
```

**Real Impact**: Regulated industries (finance, healthcare, legal) **require** reproducibility for compliance. Versioning isn't optional—it's legal necessity.

### The Bottom Line

Versioning strategy transforms system management from:
- **Reproducibility**: "It was working" → Can recreate exact state
- **Debugging**: "Something broke" → "v3.1 broke compared to v3.0, here's diff"
- **Rollback**: Panic and guessing → 5-minute precise restoration
- **Testing**: All-or-nothing deployment → Gradual rollout with A/B testing
- **Communication**: Vague references → Precise identifiers
- **Compliance**: "Trust us" → Auditable reproduction

The result: **Systems you can reason about, debug, evolve safely, and operate professionally** instead of systems that are black boxes where changes are gambling.

## Practical Checklist

### Implementing Versioning Strategy

**Step 1: Choose Schemes Per Artifact**

- [ ] **Code/Libraries**: Use SemVer (MAJOR.MINOR.PATCH)—communicate compatibility
- [ ] **ML Models**: Use sequential + metadata (model-v5)—track performance evolution
- [ ] **Training Data**: Use CalVer (YYYY-MM)—communicate freshness
- [ ] **Prompts**: Use sequential + description (prompt-v3-citations)—track iterations
- [ ] **APIs**: Use SemVer or URL versioning (`/v1/endpoint`, `/v2/endpoint`)
- [ ] **Configurations**: Use SemVer or hash—breaking config = version bump
- [ ] **Docker Images**: Use hash + tag—exact reproduction + human readability

**Step 2: Define What Changes Require Version Bumps**

SemVer rules (for code/APIs):
- [ ] **Major bump (v1 → v2)**: Breaking changes (removed features, changed APIs, incompatible behavior)
- [ ] **Minor bump (v1.1 → v1.2)**: New features, backward compatible additions
- [ ] **Patch bump (v1.1.1 → v1.1.2)**: Bug fixes, no API changes

Model versioning rules:
- [ ] **New version**: Retrained model, architecture change, or significant performance change
- [ ] **Track metadata**: Accuracy, latency, training date, dataset version

**Step 3: Create Version Manifests**

- [ ] **System manifest**: Coordinate versions of all components
- [ ] **Example**:
```yaml
system_version: "2.1.0"
components:
  code: {version: "1.3.0", commit: "a3f2b1c"}
  model: {version: "v7", trained: "2026-05-01"}
  data: {version: "2026-05", schema: "v3"}
  prompt: {version: "v10"}
  config: {version: "1.2.0"}
compatibility_notes: "Model v7 requires code v1.3.0+"
```

**Step 4: Tag Versions in Version Control**

- [ ] **Git tags**: Create annotated tags for releases
```bash
git tag -a v1.2.0 -m "Release v1.2.0: Added feature X"
git push origin v1.2.0
```
- [ ] **Naming convention**: Consistent format (v1.2.0, not 1.2, not v1.2, not version-1.2.0)

**Step 5: Document Compatibility**

- [ ] **CHANGELOG.md**: Document what changed in each version
- [ ] **Breaking changes**: Clearly mark incompatibilities
- [ ] **Migration guides**: How to upgrade from vN to vN+1
- [ ] **Deprecation warnings**: Announce removals before they happen

**Step 6: Log Versions**

- [ ] **Every request/response**: Log which versions served the request
```json
{
  "request_id": "req-123",
  "timestamp": "2026-05-15T10:30:00Z",
  "system_version": "2.1.0",
  "model_version": "v7",
  "prompt_version": "v10",
  "config_version": "1.2.0"
}
```
- [ ] **Debugging**: Can correlate issues with specific versions
- [ ] **A/B testing**: Can compare performance across versions

**Step 7: Automate Version Checking**

- [ ] **CI/CD**: Enforce version bumps for releases
- [ ] **Compatibility checks**: Test version combinations before deployment
- [ ] **Dependency constraints**: Fail if incompatible versions detected

```python
# Example compatibility check
def check_compatibility(manifest):
    code_ver = parse_version(manifest["code"]["version"])
    model_ver = parse_version(manifest["model"]["version"])
    
    if model_ver.major >= 7 and code_ver < Version("1.3.0"):
        raise IncompatibilityError(
            f"Model v{model_ver} requires code v1.3.0+, "
            f"got v{code_ver}"
        )
```

### Operating with Versions

**Daily Practices**:

- [ ] **Check version before debugging**: "What versions are running?"
- [ ] **Specify versions in bug reports**: "Issue in system v2.1.0 (model v7, prompt v10)"
- [ ] **Log versions on every operation**: Make versions searchable in logs
- [ ] **Compare versions when behavior changes**: "What changed between v2.0 and v2.1?"

**Deployment Practices**:

- [ ] **Version every release**: No unversioned deployments to production
- [ ] **Test version combinations**: Not just individual components
- [ ] **Gradual rollout**: Deploy new versions to subset first (10% → 50% → 100%)
- [ ] **Monitor by version**: Track metrics per version to detect regressions
- [ ] **Keep rollback ready**: Previous version on standby for fast recovery

**Debugging Practices**:

- [ ] **Start with versions**: "What versions were running when issue occurred?"
- [ ] **Reproduce with exact versions**: Deploy same combination in test environment
- [ ] **Compare versions**: Diff between working and broken versions
- [ ] **Bisect if needed**: Binary search through versions to find breaking change

## Watch Out For

### Critical Anti-Patterns

**1. Random Version Numbers**

❌ **Problem**: Version numbers don't communicate meaning
```
v17 → v18 → v19
What changed? Who knows!
Is v19 compatible with v17? No idea!
Should I upgrade? Can't tell!

Result: Versions exist but convey zero information.
```

✅ **Solution**: Use semantic versioning that communicates significance
```
v1.2.3 → v1.2.4: Patch (safe, bug fix)
v1.2.4 → v1.3.0: Minor (safe, new feature)
v1.3.0 → v2.0.0: Major (warning! breaking change)

Result: Version number tells you compatibility.
```

**Why This Matters**: **Useless versions are worse than no versions**—they create false confidence without providing information needed for decisions.

---

**2. Version Drift Across Artifacts**

❌ **Problem**: Components versions uncoordinated
```
Production Environment 1:
  code v1.2, model v5, prompt v7

Production Environment 2:
  code v1.3, model v5, prompt v8

Production Environment 3:
  code v1.2, model v6, prompt v7

Result: Three different combinations in production.
Which is the "official" configuration?
Can't compare performance—too many variables.
```

✅ **Solution**: System-level versions coordinating components
```
System v2.0: code v1.2, model v5, prompt v7
System v2.1: code v1.3, model v5, prompt v8
System v2.2: code v1.3, model v6, prompt v8

Deploy system versions, not individual components.
All environments running same system version = consistent.
```

**Why This Matters**: **Uncoordinated versions create endless combinations**—can't reproduce, can't compare, can't debug effectively.

---

**3. Missing Version in Logs**

❌ **Problem**: Logs don't capture which versions served requests
```
ERROR: Model returned invalid response
Request ID: req-abc-123
Timestamp: 2026-05-15T10:30:00Z

Which model version? Which code version? Which prompt?
No way to reproduce—critical information missing.
```

✅ **Solution**: Log all versions for every significant operation
```json
{
  "level": "ERROR",
  "message": "Model returned invalid response",
  "request_id": "req-abc-123",
  "timestamp": "2026-05-15T10:30:00Z",
  "system_version": "2.1.0",
  "model_version": "v7",
  "prompt_version": "v10",
  "config_version": "1.2.0",
  "code_commit": "a3f2b1c"
}

Can reproduce exact combination in test environment.
```

**Why This Matters**: **Logs without versions make debugging impossible**—can't reproduce, can't correlate issues with deployments.

---

**4. No Breaking Change Communication**

❌ **Problem**: Breaking changes hidden in minor version bumps
```
v1.2.0: API endpoint `/predict` accepts `input` parameter
v1.3.0: Changed to `data` parameter (BREAKING!)

But version says "minor" (should be v2.0.0)

Consumers upgrade expecting compatibility → Everything breaks
"We upgraded from v1.2 to v1.3 and it broke!"
```

✅ **Solution**: Major version bumps for breaking changes, clear communication
```
v1.2.0: API endpoint `/predict` accepts `input` parameter
v2.0.0: BREAKING: Changed parameter from `input` to `data`

CHANGELOG:
v2.0.0 (BREAKING CHANGES):
- Changed `/predict` endpoint parameter from `input` to `data`
- Migration: Replace `{"input": x}` with `{"data": x}`

Consumers see v2.0.0 → "major bump, check breaking changes"
```

**Why This Matters**: **Breaking compatibility promise destroys trust**. If minor versions break things, consumers can't safely upgrade automatically.

---

**5. Forgetting to Version Non-Code Artifacts**

❌ **Problem**: Only code is versioned, models/prompts/data aren't
```
code v1.2.3 (versioned in Git)
model.pkl (no version—which training run?)
prompt.txt (no version—which iteration?)
data/ (no version—which dataset?)

Result: Can version control code but not reproduce system behavior.
```

✅ **Solution**: Version ALL artifacts that affect behavior
```
code v1.2.3
models/classifier/v5/model.pkl (versioned)
prompts/system_prompt_v7.txt (versioned)
datasets/training_2026_05/ (versioned by date)

manifest.yaml: {
  "code": "v1.2.3",
  "model": "v5",
  "prompt": "v7",
  "data": "2026-05"
}

Can reproduce exact system state.
```

**Why This Matters**: **AI system behavior depends on ALL artifacts**—versioning only code gives false sense of reproducibility.

---

**6. Reusing Version Numbers**

❌ **Problem**: Publishing, deleting, republishing same version
```
Deploy model-v5 → Has bug → Delete → Train new model → Deploy as model-v5

But these are TWO DIFFERENT MODELS with same version!

Users who downloaded first model-v5: Different behavior than second model-v5
Impossible to tell which model-v5 someone is using.
```

✅ **Solution**: Versions are immutable—once published, never changed
```
Deploy model-v5 → Has bug → Keep v5 for history
Train new model → Deploy as model-v6

model-v5: Always refers to same artifact (even if deprecated)
model-v6: New artifact, new version

Users can specify exact version, guaranteed consistent.
```

**Why This Matters**: **Reusing versions destroys reproducibility**—"model-v5" must mean ONE thing, not different things at different times.

---

**7. No Rollback Plan**

❌ **Problem**: Can identify versions but can't redeploy them
```
System v2.1.0 deployed → Breaks production
You: "Roll back to v2.0.5!"
Engineer: "We don't have v2.0.5 artifacts anymore..."
You: "We deleted old Docker images to save space..."

Result: Know what to roll back to, but CAN'T.
```

✅ **Solution**: Retain artifacts for rollback window
```
Policy: Keep last 5 production versions' full artifacts
- system-v2.0.5 artifacts: Available
- system-v2.0.4 artifacts: Available
- system-v2.0.3 artifacts: Available
- system-v2.0.2 artifacts: Available
- system-v2.0.1 artifacts: Available

Can roll back to any recent version in 5 minutes.
Older versions: Archive for compliance, but may take longer to restore.
```

**Why This Matters**: **Versions without artifacts are useless**—must be able to actually redeploy old versions for rollback.

---

**8. Over-Versioning (Version on Every Commit)**

❌ **Problem**: Creating new version for every tiny change
```
v1.0.0: Initial release
v1.0.1: Fixed typo in comment
v1.0.2: Reformatted code
v1.0.3: Updated docstring
v1.0.4: Fixed another typo

Result: 100 versions per month, nobody can track what matters.
```

✅ **Solution**: Version meaningful releases, not every commit
```
Commits: Continuous (100+ per month)
Versions: When releasing (2-4 per month)

v1.0.0: Initial release
... (50 commits) ...
v1.1.0: Added feature X (released to production)
... (30 commits) ...
v1.2.0: Added feature Y (released to production)

Commits tracked in Git, versions mark release milestones.
```

**Why This Matters**: **Too many versions = signal lost in noise**—version should mark significant milestones, not every edit.

---

**9. Inconsistent Version Format**

❌ **Problem**: Different formats across team/projects
```
Project A: v1.2.3, v1.2.4, v2.0.0
Project B: version-1.2, version-1.3
Project C: 2026.05.15, 2026.05.16
Project D: r1, r2, r3

Result: Can't write tools that work across projects, confusion in discussions.
```

✅ **Solution**: Standardize format across organization
```
Code/APIs: SemVer (v1.2.3)
Models: Sequential + metadata (model-v5)
Data: CalVer (YYYY-MM or YYYY-MM-DD)
System: SemVer coordinating components (v2.1.0)

Documented in engineering guidelines, enforced in CI/CD.
```

**Why This Matters**: **Consistency enables tooling and communication**—standardized formats allow automated processing, clear understanding.

---

**10. No Deprecation Process**

❌ **Problem**: Old versions supported forever or killed without warning
```
v1.0 released 2024
v2.0 released 2025
v3.0 released 2026

Still supporting v1.0? When will it end?
Or: "v1.0 shut down tomorrow!" (users panic)

Result: Maintenance burden forever OR angry surprised users.
```

✅ **Solution**: Clear deprecation lifecycle
```
v3.0 released 2026-05-01:
  Announcement: "v1.x deprecated—supported until 2027-05-01, then retired"
  
2026-05 to 2027-05: Deprecation period
  - v1.x still works
  - Warnings in logs: "Using deprecated v1.x, upgrade to v3.x"
  - Migration guide published
  - Support team helps migrations
  
2027-05-01: v1.x retired (shut down)
  - Users had 12 months notice
  - Migration support provided

Result: Planned retirement, no surprises.
```

**Why This Matters**: **Versions need end-of-life process**—can't support everything forever, but can't kill things without warning.

## Connections

This concept relates to other vocabulary terms in this repository:

### Direct Connections (Core Relationships)

- **[[semantic_coupling]]**: Versioning makes semantic coupling explicit—which versions depend on shared understanding of specific concepts
- **[[dependency_injection]]**: Version compatibility critical when injecting dependencies—must ensure compatible versions injected
- **[[documentation_as_code]]**: Documentation versions should track code versions—versioning strategy applies to docs
- **[[knowledge_extraction]]**: Extracting knowledge from versioned artifacts requires tracking which version produced which insights

### Knowledge Management Connections

- **[[metadata_strategy]]**: Version numbers are critical metadata—identifying artifacts and their relationships
- **[[information_architecture]]**: Versioning strategy is part of information architecture—how knowledge evolves and is organized over time
- **[[tribal_knowledge]]**: Versioning prevents tribal knowledge ("use the version from before the rewrite")—makes implicit knowledge explicit
- **[[wayfinding]]**: Versions help navigate through time—"find the version that worked", "see how concept evolved"
- **[[wiki_pattern]]**: Wiki pages can be versioned like code—tracking evolution of knowledge over time

### Software Engineering Connections

- **[[interface_design]]**: API versioning is interface design—managing evolution while maintaining compatibility
- **[[separation_of_concerns]]**: Different artifacts (code, models, data) can version independently—loosely coupled evolution
- **[[bounded_context]]**: Version boundaries often align with bounded contexts—v1 API, v2 API may represent different contexts
- **[[modular_architecture]]**: Versioning enables modular evolution—upgrade one module without touching others

### AI Systems Connections

- **[[retrieval_augmented_generation]]**: RAG systems need versioned knowledge bases—which version of documentation was retrieved?
- **[[knowledge_representation]]**: Versioning applies to knowledge representations—ontology v1 vs v2
- **[[chunking_strategy]]**: Chunking logic changes require versioning—different versions produce different chunks

### Operational Connections

- **[[configuration_management]]**: Configurations need versioning—breaking config changes require version bumps
- **[[template_design]]**: Templates evolve and need versioning—template v1 incompatible with v2

## Quick Decision Guide

### "What versioning scheme should I use?"

**Use Semantic Versioning (MAJOR.MINOR.PATCH) if**:
- ✅ Public API or library with consumers who need compatibility promises
- ✅ Code with clear breaking vs compatible changes
- ✅ Multiple versions supported simultaneously

**Use Calendar Versioning (YYYY-MM-DD) if**:
- ✅ Data/datasets where freshness matters most
- ✅ Regular release schedule (monthly, weekly)
- ✅ Time-based snapshots

**Use Sequential (v1, v2, v3) if**:
- ✅ ML models with performance progression
- ✅ Internal experiments where simple numbering suffices
- ✅ Compatibility not encoded in version number

**Use Hash-Based (Git SHA) if**:
- ✅ Exact reproducibility critical (research, debugging)
- ✅ Continuous deployment
- ✅ Combined with human-readable tag

**Use Hybrid if**:
- ✅ Need multiple pieces of information (v2.1.0+20260515.a3f2b1c)
- ✅ Complex systems benefiting from rich versioning

### "When should I bump the version?"

**Major bump (v1.x.x → v2.0.0)**:
- Removed features or endpoints
- Changed API signatures incompatibly
- Changed behavior breaking existing use cases
- Requires consumers to change their code

**Minor bump (v1.1.x → v1.2.0)**:
- Added new features (backward compatible)
- Added new optional parameters
- Deprecated (but didn't remove) features
- Consumers can upgrade without changes

**Patch bump (v1.1.1 → v1.1.2)**:
- Bug fixes with no API changes
- Performance improvements
- Documentation updates
- Security patches

### "How many versions should I support?"

**General guidance**:
- **Latest stable**: Always supported
- **Previous major**: Supported for 6-12 months (overlap period)
- **Two versions back**: Deprecated (works but warned)
- **Three+ versions back**: Retired (shut down)

**Example timeline**:
```
v3.0 released 2026-01: Latest
v2.x (2025-01 to now): Previous major, supported until 2026-07
v1.x (2024-01 to 2025-01): Deprecated 2026-01, retired 2026-07
```

**Adjust based on**:
- Customer migration speed (enterprise = longer support)
- Breaking change frequency (frequent = shorter support)
- Maintenance cost (more versions = more cost)

### "How do I manage multi-artifact versioning?"

**Option 1: System-level version coordinating components**
```yaml
system_v2.1.0:
  code: v1.3.0
  model: v7
  prompt: v10
  config: v1.2.0
```
✅ Use when: Artifacts tightly coupled, deployed together
✅ Benefit: Single version identifies entire system state

**Option 2: Independent versioning with compatibility matrix**
```yaml
code v1.3.0: compatible with model v5-v7, prompt v8-v10
model v7: requires code v1.3.0+, works with any prompt v8+
```
✅ Use when: Artifacts loosely coupled, deployed independently
✅ Benefit: Flexibility to mix/match compatible versions

**Option 3: Hybrid**
```yaml
system_v2.1.0:  # Tested/validated combination
  code: v1.3.0
  model: v7
  prompt: v10
  
But also: Can deploy code v1.4.0 with model v7 (compatible)
```
✅ Use when: Need both validation and flexibility

### "How do I communicate versions to users?"

**In APIs**: URL or header versioning
```
Option 1: URL versioning
  GET /v1/predict
  GET /v2/predict

Option 2: Header versioning
  GET /predict
  Header: API-Version: 2.0

Recommendation: URL versioning (clearer, easier to cache)
```

**In Libraries**: Version in package name/import
```python
# Python
import mylibrary  # Uses version in pip install
pip install mylibrary==1.2.3

# Shows version
mylibrary.__version__  # "1.2.3"
```

**In Documentation**: Version picker
```
Documentation site:
[Docs v3.0] [Docs v2.0] [Docs v1.0]
  ↑ Current     ↑ Previous  ↑ Legacy
```

### "How do I test version compatibility?"

**Compatibility test matrix**:
```python
# Test new code with old models
test_code_v1_3_with_model_v5()
test_code_v1_3_with_model_v6()
test_code_v1_3_with_model_v7()

# Test new model with old code
test_model_v7_with_code_v1_2()
test_model_v7_with_code_v1_3()

# Fail fast on incompatibilities
if model_version >= 7 and code_version < "1.3.0":
    raise IncompatibilityError(...)
```

**Automated in CI/CD**:
- Version bump detected → Run compatibility tests
- Deploy blocked if incompatible versions detected
- Gradual rollout starts only after compatibility validated

## Further Exploration

### Foundational Resources

**Versioning Standards**:
- Semantic Versioning (semver.org) - Canonical SemVer specification
- Calendar Versioning (calver.org) - Date-based versioning patterns
- "Software Versioning" (Wikipedia) - Overview of schemes and practices

**API Versioning**:
- "RESTful API Versioning" by Troy Hunt - URL vs header versioning
- "API Evolution" by Mark Nottingham - Managing API changes over time
- OpenAPI/Swagger specifications - Versioning in API specs

### AI/ML Specific Versioning

**Model Versioning**:
- ML Model Registry patterns (MLflow, Weights & Biases) - Tracking model versions
- "Versioning for ML Models" (AWS SageMaker docs) - Model lifecycle management
- DVC (Data Version Control) - Versioning data and models with Git

**Data Versioning**:
- "Data Versioning" (Pachyderm, DVC) - Version control for datasets
- "ML Dataset Versioning Best Practices" - Managing dataset evolution
- Delta Lake/Iceberg - Time travel for data (versioning built into data lakes)

**Experiment Tracking**:
- MLflow Tracking - Versioning experiments, models, artifacts
- Weights & Biases - Experiment versioning and comparison
- Neptune.ai - ML metadata versioning

### Software Engineering Practices

**Version Control**:
- "Pro Git" by Chacon & Straub - Git fundamentals including tagging
- "Trunk Based Development" - Versioning with continuous integration
- Git workflows (Git Flow, GitHub Flow) - Release branching strategies

**Dependency Management**:
- "Dependency Hell" solutions - Managing version constraints
- Poetry, Pipenv (Python), npm (JavaScript) - Lock files and version pinning
- Semantic versioning for dependencies - Compatible version ranges

### Production Systems

**Deployment Strategies**:
- "Blue-Green Deployment" - Running multiple versions simultaneously
- "Canary Releases" - Gradual version rollout
- "Feature Flags" - Runtime version switching without redeployment

**Container Versioning**:
- Docker image tagging best practices - Versioning container images
- Kubernetes rollout strategies - Version management in orchestration
- Container registries (ACR, ECR, Docker Hub) - Storing versioned images

### Academic & Research

**Reproducibility**:
- "Reproducibility in Machine Learning" papers - Importance of versioning for science
- "Artifact Evaluation" (conference standards) - Versioning research artifacts
- "Papers with Code" - Linking code versions to papers

**Research Directions**:
- Automated version inference - Detecting breaking changes automatically
- Semantic versioning automation - AI suggesting version bumps based on diffs
- Cross-artifact dependency resolution - Managing multi-version compatibility
- Temporal knowledge graphs - Representing knowledge evolution through versions

### Industry Case Studies

**Large-Scale Versioning**:
- Google's monorepo versioning - Single version across massive codebase
- Netflix API versioning - Managing versions at scale
- AWS API versioning - Maintaining backward compatibility for years
- OpenAI model versioning - versioned model releases (GPT-3.5-turbo-0301, etc.)

### Tools and Platforms

**Version Management Tools**:
- Bump2version, semantic-release - Automated version bumping
- Changesets - Version and changelog management
- Release-please (Google) - Automated releases from conventional commits

**Model Registries**:
- MLflow Model Registry
- Azure ML Model Registry
- Vertex AI Model Registry
- Hugging Face Hub - Community model versioning

---

*Vocabulary entry version 1.0 | Last updated: May 15, 2026 | Confidence: High*

*This term represents an established software engineering practice with clear industry standards (SemVer, CalVer) and proven patterns. The 2026 AI extensions reflect emerging practices for versioning ML artifacts alongside code, actively being adopted across the industry as AI systems move to production at scale.*