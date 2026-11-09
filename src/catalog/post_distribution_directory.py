"""Canonical Per-Post Distribution Directory: LinkedIn Groups, Cross-Platform Pages,
Company Page @Mentions, Tiered Hashtags, and Authoritative Company References.

Covers:
  - Flagship & Career-Minting Topics: MINT-01 .. MINT-12
  - Viral Pain-Point Ideas: IDEA-01 .. IDEA-10
  - Analyzed LinkedIn Posts: POST-01 .. POST-08
  - Daily Top-5 Editorial Briefing: TOP5-YYYYMMDD-01 .. 05
  - Daily 6 Creator-Style Posts: DAILY-YYYYMMDD-01 .. 06
  - Customer Success Agentic Inventions: CS-INV-01 .. CS-LIVE-10
"""

from __future__ import annotations

from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# 1. Verified Company Pages, Handles & Official Engineering Portals
# ---------------------------------------------------------------------------
COMPANY_DIRECTORY: Dict[str, Dict[str, str]] = {
    "google_cloud": {
        "company_name": "Google Cloud",
        "linkedin_page_tag": "@Google Cloud",
        "linkedin_page_url": "https://www.linkedin.com/company/google-cloud/",
        "x_handle": "@googlecloud",
        "github_org_url": "https://github.com/GoogleCloudPlatform",
        "engineering_portal_url": "https://cloud.google.com/architecture/ai-ml",
        "ecosystem_hashtag": "#GoogleCloud",
    },
    "google_deepmind": {
        "company_name": "Google DeepMind",
        "linkedin_page_tag": "@Google DeepMind",
        "linkedin_page_url": "https://www.linkedin.com/company/googledeepmind/",
        "x_handle": "@GoogleDeepMind",
        "github_org_url": "https://github.com/google-deepmind",
        "engineering_portal_url": "https://deepmind.google/research/",
        "ecosystem_hashtag": "#GoogleDeepMind",
    },
    "anthropic": {
        "company_name": "Anthropic",
        "linkedin_page_tag": "@Anthropic",
        "linkedin_page_url": "https://www.linkedin.com/company/anthropicresearch/",
        "x_handle": "@AnthropicAI",
        "github_org_url": "https://github.com/anthropics",
        "engineering_portal_url": "https://www.anthropic.com/engineering",
        "ecosystem_hashtag": "#Anthropic",
    },
    "openai": {
        "company_name": "OpenAI",
        "linkedin_page_tag": "@OpenAI",
        "linkedin_page_url": "https://www.linkedin.com/company/openai/",
        "x_handle": "@OpenAI",
        "github_org_url": "https://github.com/openai",
        "engineering_portal_url": "https://openai.com/news/engineering/",
        "ecosystem_hashtag": "#OpenAI",
    },
    "langchain": {
        "company_name": "LangChain",
        "linkedin_page_tag": "@LangChain",
        "linkedin_page_url": "https://www.linkedin.com/company/langchain/",
        "x_handle": "@LangChainAI",
        "github_org_url": "https://github.com/langchain-ai",
        "engineering_portal_url": "https://blog.langchain.dev/",
        "ecosystem_hashtag": "#LangGraph",
    },
    "openhands": {
        "company_name": "All Hands AI (OpenHands)",
        "linkedin_page_tag": "@All Hands AI",
        "linkedin_page_url": "https://www.linkedin.com/company/all-hands-ai/",
        "x_handle": "@allhands_ai",
        "github_org_url": "https://github.com/All-Hands-AI/OpenHands",
        "engineering_portal_url": "https://docs.all-hands.dev/",
        "ecosystem_hashtag": "#OpenHands",
    },
    "pydantic": {
        "company_name": "Pydantic",
        "linkedin_page_tag": "@Pydantic",
        "linkedin_page_url": "https://www.linkedin.com/company/pydantic/",
        "x_handle": "@pydantic",
        "github_org_url": "https://github.com/pydantic/pydantic-ai",
        "engineering_portal_url": "https://ai.pydantic.dev/",
        "ecosystem_hashtag": "#PydanticAI",
    },
    "llamaindex": {
        "company_name": "LlamaIndex",
        "linkedin_page_tag": "@LlamaIndex",
        "linkedin_page_url": "https://www.linkedin.com/company/llamaindex/",
        "x_handle": "@llama_index",
        "github_org_url": "https://github.com/run-llama/llama_index",
        "engineering_portal_url": "https://www.llamaindex.ai/blog",
        "ecosystem_hashtag": "#LlamaIndex",
    },
    "arize_ai": {
        "company_name": "Arize AI",
        "linkedin_page_tag": "@Arize AI",
        "linkedin_page_url": "https://www.linkedin.com/company/arizeai/",
        "x_handle": "@ArizeAI",
        "github_org_url": "https://github.com/Arize-ai/phoenix",
        "engineering_portal_url": "https://arize.com/blog/",
        "ecosystem_hashtag": "#OpenTelemetry",
    },
    "weights_biases": {
        "company_name": "Weights & Biases",
        "linkedin_page_tag": "@Weights & Biases",
        "linkedin_page_url": "https://www.linkedin.com/company/wandb/",
        "x_handle": "@weights_biases",
        "github_org_url": "https://github.com/wandb/weave",
        "engineering_portal_url": "https://wandb.ai/site/weave",
        "ecosystem_hashtag": "#LLMEvals",
    },
    "owasp": {
        "company_name": "OWASP Foundation (GenAI Security Project)",
        "linkedin_page_tag": "@OWASP Foundation",
        "linkedin_page_url": "https://www.linkedin.com/company/owasp/",
        "x_handle": "@owasp",
        "github_org_url": "https://github.com/OWASP",
        "engineering_portal_url": "https://genai.owasp.org/",
        "ecosystem_hashtag": "#OWASP",
    },
    "cloudflare": {
        "company_name": "Cloudflare",
        "linkedin_page_tag": "@Cloudflare",
        "linkedin_page_url": "https://www.linkedin.com/company/cloudflare/",
        "x_handle": "@Cloudflare",
        "github_org_url": "https://github.com/cloudflare/agents",
        "engineering_portal_url": "https://blog.cloudflare.com/tag/ai/",
        "ecosystem_hashtag": "#ZeroTrust",
    },
    "temporal": {
        "company_name": "Temporal Technologies",
        "linkedin_page_tag": "@Temporal Technologies",
        "linkedin_page_url": "https://www.linkedin.com/company/temporal-technologies/",
        "x_handle": "@temporalio",
        "github_org_url": "https://github.com/temporalio",
        "engineering_portal_url": "https://temporal.io/blog",
        "ecosystem_hashtag": "#DurableExecution",
    },
    "servicenow": {
        "company_name": "ServiceNow",
        "linkedin_page_tag": "@ServiceNow",
        "linkedin_page_url": "https://www.linkedin.com/company/servicenow/",
        "x_handle": "@ServiceNow",
        "github_org_url": "https://github.com/ServiceNow",
        "engineering_portal_url": "https://www.servicenow.com/research/",
        "ecosystem_hashtag": "#ServiceNow",
    },
    "snowflake": {
        "company_name": "Snowflake",
        "linkedin_page_tag": "@Snowflake",
        "linkedin_page_url": "https://www.linkedin.com/company/snowflake-computing/",
        "x_handle": "@SnowflakeDB",
        "github_org_url": "https://github.com/Snowflake-Labs",
        "engineering_portal_url": "https://www.snowflake.com/en/engineering-blog/",
        "ecosystem_hashtag": "#EnterpriseData",
    },
    "datadog": {
        "company_name": "Datadog",
        "linkedin_page_tag": "@Datadog",
        "linkedin_page_url": "https://www.linkedin.com/company/datadog/",
        "x_handle": "@datadoghq",
        "github_org_url": "https://github.com/DataDog",
        "engineering_portal_url": "https://www.datadoghq.com/blog/llm-observability/",
        "ecosystem_hashtag": "#LLMObservability",
    },
    "meta_ai": {
        "company_name": "AI at Meta",
        "linkedin_page_tag": "@AI at Meta",
        "linkedin_page_url": "https://www.linkedin.com/company/aiatmeta/",
        "x_handle": "@AIatMeta",
        "github_org_url": "https://github.com/meta-llama",
        "engineering_portal_url": "https://ai.meta.com/blog/",
        "ecosystem_hashtag": "#Llama",
    },
}

# ---------------------------------------------------------------------------
# 2. Canonical LinkedIn Groups & Cross-Platform Pages Catalog
# ---------------------------------------------------------------------------
LINKEDIN_GROUPS_CATALOG: Dict[str, Dict[str, str]] = {
    "LI-GRP-AIML": {
        "name": "Artificial Intelligence, Machine Learning, Data Science & Robotics",
        "url": "https://www.linkedin.com/groups/3671367/",
        "members": "6,500,000+",
        "goal": "Top-of-funnel impressions, repost velocity, and broad AI leadership visibility",
    },
    "LI-GRP-GCP": {
        "name": "Google Cloud Platform (GCP) Architects, Developers & Vertex AI Builders",
        "url": "https://www.linkedin.com/groups/3050257/",
        "members": "420,000+",
        "goal": "Direct reach among Principal GCP Architects, Vertex AI Agent Engine users, and Cloud Run teams",
    },
    "LI-GRP-GENAI-PRAC": {
        "name": "Generative AI & LLMs (Large Language Models) — Enterprise Practitioners",
        "url": "https://www.linkedin.com/groups/12795132/",
        "members": "480,000+",
        "goal": "High comment velocity from Staff+ AI engineers solving production reliability bottlenecks",
    },
    "LI-GRP-MCP-API": {
        "name": "Model Context Protocol (MCP), Agentic Tooling & Enterprise API Architecture",
        "url": "https://www.linkedin.com/groups/13041020/",
        "members": "195,000+",
        "goal": "Targeted discussion on MCP schema discovery, OAuth 2.1 OBO, and Apigee gateway patterns",
    },
    "LI-GRP-CISO-SEC": {
        "name": "Information Security, CISO Network, Cybersecurity & Zero-Trust AI",
        "url": "https://www.linkedin.com/groups/38412/",
        "members": "2,400,000+",
        "goal": "CISO, AppSec, and SecOps shares on prompt-injection containment and OBO least privilege",
    },
    "LI-GRP-AGENT-BUILDERS": {
        "name": "Autonomous Agents, LangGraph, CrewAI, FastMCP & OpenHands Builders",
        "url": "https://www.linkedin.com/groups/12918440/",
        "members": "92,000+",
        "goal": "High GitHub repo clone/star conversion and evaluation suite benchmark discussions",
    },
    "LI-GRP-ENT-ARCH": {
        "name": "Enterprise Architecture, FinOps & Cloud Transformation Leaders",
        "url": "https://www.linkedin.com/groups/67905/",
        "members": "610,000+",
        "goal": "CTO, Chief Architect, and FinOps engagement on token economics and SLA governance",
    },
    "LI-GRP-CS-CCO": {
        "name": "Chief Customer Officer (CCO), VP Customer Success & Value Realization",
        "url": "https://www.linkedin.com/groups/4510921/",
        "members": "180,000+",
        "goal": "Customer Success leadership adoption of self-healing agentic playbooks and NRR expansion",
    },
}

CROSS_PLATFORM_PAGES_CATALOG: Dict[str, List[Dict[str, str]]] = {
    "CLUSTER_MCP_IDENTITY": [
        {
            "platform": "Reddit",
            "page_or_group": "r/LocalLLaMA & r/AI_Agents",
            "url": "https://www.reddit.com/r/LocalLLaMA/",
            "audience": "610K+ LLM Systems Builders",
            "posting_angle": "Share the 58K -> 1.7K MCP token reduction benchmark table + eval_results.json",
        },
        {
            "platform": "GitHub Discussions",
            "page_or_group": "modelcontextprotocol/specification Discussions",
            "url": "https://github.com/modelcontextprotocol/specification/discussions",
            "audience": "Core MCP Maintainers & Enterprise Adopters",
            "posting_angle": "Reference RFC 8693 OBO token exchange + progressive Top-K schema discovery",
        },
        {
            "platform": "Dev.to & Hashnode",
            "page_or_group": "#mcp · #googlecloud · #ai · #security",
            "url": "https://dev.to/t/mcp",
            "audience": "Full-Stack & Cloud Native Developers",
            "posting_angle": "Publish full Terraform + src/engine.py walkthrough with 1-click Cloud Run script",
        },
    ],
    "CLUSTER_CODING_EVALS": [
        {
            "platform": "Hacker News",
            "page_or_group": "Show HN / Technical Deep Dives",
            "url": "https://news.ycombinator.com/",
            "audience": "Principal Systems Engineers & Founders",
            "posting_angle": "Lead with pass^5 = (pass@1)^5 decay math and reproducible 20-scenario eval_dataset.jsonl",
        },
        {
            "platform": "Reddit",
            "page_or_group": "r/MachineLearning & r/LanguageTechnology",
            "url": "https://www.reddit.com/r/MachineLearning/",
            "audience": "2.9M+ ML Researchers & Applied Scientists",
            "posting_angle": "Highlight trajectory-level evaluator gates vs. single-turn LLM-as-a-Judge bias",
        },
        {
            "platform": "Substack & Medium",
            "page_or_group": "AI Engineering & Google Cloud Community",
            "url": "https://medium.com/google-cloud",
            "audience": "Enterprise AI Engineering Leaders",
            "posting_angle": "Embed the 2D Architecture Blueprint SVG + step-by-step trajectory diff table",
        },
    ],
    "CLUSTER_INFERENCE_KV": [
        {
            "platform": "Reddit",
            "page_or_group": "r/LocalLLaMA & r/googlecloud",
            "url": "https://www.reddit.com/r/googlecloud/",
            "audience": "580K+ Cloud & Inference Engineers",
            "posting_angle": "Break down KV-cache prefix pinning, p95 latency (4,372ms -> 610ms), and $/1K workflow savings",
        },
        {
            "platform": "Substack Notes",
            "page_or_group": "Latent Space / AI Systems Engineering Notes",
            "url": "https://www.latent.space/",
            "audience": "AI Systems Architects & FinOps Leads",
            "posting_angle": "Post the Before/After token & latency roofline card with link to evals/run_eval_suite.py",
        },
        {
            "platform": "Dev.to & Hashnode",
            "page_or_group": "#llmops · #vertexai · #performance · #finops",
            "url": "https://dev.to/t/googlecloud",
            "audience": "Cloud Infrastructure & SRE Practitioners",
            "posting_angle": "Show exact Context Caching + speculative cascade routing implementation",
        },
    ],
    "CLUSTER_MULTIAGENT_MEMORY": [
        {
            "platform": "Reddit",
            "page_or_group": "r/AI_Agents & r/LangChain",
            "url": "https://www.reddit.com/r/AI_Agents/",
            "audience": "240K+ Multi-Agent Framework Developers",
            "posting_angle": "Contrast chatty peer-to-peer loops with Typed A2A Blackboard + Cloud Spanner/Firestore state",
        },
        {
            "platform": "GitHub & CNCF",
            "page_or_group": "A2A Protocol & Google Cloud ADK Community",
            "url": "https://github.com/google/adk-python",
            "audience": "Enterprise Multi-Agent Architects",
            "posting_angle": "Share JSON-Schema handoff contract + SHA-256 evidence receipt verification",
        },
        {
            "platform": "Medium & Hashnode",
            "page_or_group": "Towards AI & Enterprise Agentic Systems",
            "url": "https://hashnode.com/n/ai",
            "audience": "Staff Software Engineers & Tech Leads",
            "posting_angle": "Walk through 100-session concurrency isolation and zero-context-bleed tests",
        },
    ],
    "CLUSTER_GOVERNANCE_FINOPS": [
        {
            "platform": "LinkedIn Executive Pulse & Substack",
            "page_or_group": "Enterprise AI Governance, CISO & FinOps Briefing",
            "url": "https://genai.owasp.org/",
            "audience": "CISOs, CIOs, CFOs & VPs of AI Platform",
            "posting_angle": "Publish the 8-slide 4:5 PDF Carousel + Editable Google Slides executive briefing",
        },
        {
            "platform": "Reddit",
            "page_or_group": "r/netsec & r/aws / r/googlecloud",
            "url": "https://www.reddit.com/r/netsec/",
            "audience": "700K+ Security Architects & Cloud Engineers",
            "posting_angle": "Demonstrate 5/5 adversarial prompt-injection & PII exfiltration blocks in eval_results.json",
        },
        {
            "platform": "Dev.to",
            "page_or_group": "#security · #zerotrust · #cloud · #governance",
            "url": "https://dev.to/t/security",
            "audience": "Cloud Security & DevSecOps Engineers",
            "posting_angle": "Provide Model Armor + IAM OBO capability-downgrade policy templates",
        },
    ],
}

# ---------------------------------------------------------------------------
# 3. Per-Post Specific Company References, Roles & Hashtag Profiles
# ---------------------------------------------------------------------------
POST_SPECIFIC_PROFILES: Dict[str, Dict[str, Any]] = {
    "MINT-01": {
        "cluster_id": "CLUSTER_MCP_IDENTITY",
        "primary_groups": ["LI-GRP-MCP-API", "LI-GRP-CISO-SEC", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-AGENT-BUILDERS", "LI-GRP-ENT-ARCH", "LI-GRP-CS-CCO"],
        "companies": [
            ("google_cloud", "Primary Cloud Runtime (`Apigee API Hub`, `Vertex AI Agent Engine`, `Cloud Run v2`, `Cloud KMS`)", "Google Cloud Architecture Center: Enterprise AI & ADK", "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview"),
            ("anthropic", "Originator of the Model Context Protocol (`MCP`) & progressive tool discovery pattern", "Anthropic Engineering: Code Execution & Progressive Tool Discovery with MCP", "https://www.anthropic.com/engineering/code-execution-with-mcp"),
            ("pydantic", "Strict JSON-Schema tool argument validation (`PydanticAI` / `FastMCP`)", "PydanticAI: Type-Safe Agent Tool Validation", "https://ai.pydantic.dev/"),
            ("cloudflare", "Zero-Trust Remote MCP Server & OAuth 2.1 Edge Gateway reference", "Cloudflare Agents: Building Remote MCP Servers with OAuth", "https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/"),
        ],
        "linkedin_primary_5": ["#ModelContextProtocol", "#GoogleCloud", "#VertexAI", "#AgenticAI", "#ZeroTrustAI"],
        "niche_hashtags": ["#GoogleCloudADK", "#OAuth2", "#Apigee", "#ContextEngineering", "#FastMCP", "#AIArchitecture"],
    },
    "IDEA-01": {
        "cluster_id": "CLUSTER_INFERENCE_KV",
        "primary_groups": ["LI-GRP-AIML", "LI-GRP-GENAI-PRAC", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-AGENT-BUILDERS", "LI-GRP-ENT-ARCH"],
        "companies": [
            ("google_cloud", "Cloud Runtime (`Google Cloud ADK`, `Cloud Trace`, `Firestore` trajectory state, `Cloud Billing Budgets`)", "Google Cloud ADK: Deterministic Loop Controls & Callbacks", "https://google.github.io/adk-docs/"),
            ("langchain", "Open-source graph orchestration (`LangGraph` recursion limit & cycle detection)", "LangGraph: Controlling Graph Recursion & Loop Termination", "https://langchain-ai.github.io/langgraph/"),
            ("arize_ai", "OpenTelemetry GenAI span collection (`Arize Phoenix`) for loop root-cause detection", "Arize Phoenix: OpenTelemetry Tracing for Agent Loops", "https://docs.arize.com/phoenix"),
            ("datadog", "Enterprise LLM token burn-rate & runaway loop alerting", "Datadog LLM Observability: Monitoring Agentic Workflows", "https://www.datadoghq.com/blog/llm-observability/"),
        ],
        "linkedin_primary_5": ["#AgenticAI", "#GoogleCloud", "#LLMOps", "#FinOps", "#AIEngineering"],
        "niche_hashtags": ["#VertexAI", "#LangGraph", "#OpenTelemetry", "#CloudRun", "#SiteReliabilityEngineering"],
    },
    "IDEA-02": {
        "cluster_id": "CLUSTER_INFERENCE_KV",
        "primary_groups": ["LI-GRP-GENAI-PRAC", "LI-GRP-GCP", "LI-GRP-AIML"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-AGENT-BUILDERS"],
        "companies": [
            ("google_cloud", "Managed Context Caching & `Vertex AI` Global Endpoint KV-cache reuse", "Vertex AI Context Caching & Prefix Optimization", "https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview"),
            ("anthropic", "Context engineering & episodic compaction research for long-horizon agents", "Anthropic Engineering: Effective Context Engineering for AI Agents", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
            ("langchain", "State reducer & message history summarization (`LangMem` / `LangGraph`)", "LangChain: Context Engineering for Agents", "https://blog.langchain.dev/context-engineering-for-agents/"),
            ("llamaindex", "Hierarchical document & artifact URI pointer indexing (`Cloud Storage` + `AlloyDB`)", "LlamaIndex: Context-Augmented Production Agents", "https://www.llamaindex.ai/blog"),
        ],
        "linkedin_primary_5": ["#ContextEngineering", "#GoogleCloud", "#VertexAI", "#AgenticAI", "#LLMOps"],
        "niche_hashtags": ["#KVCache", "#Anthropic", "#LangGraph", "#EnterpriseAI", "#GenAIArchitecture"],
    },
    "IDEA-03": {
        "cluster_id": "CLUSTER_CODING_EVALS",
        "primary_groups": ["LI-GRP-GENAI-PRAC", "LI-GRP-AGENT-BUILDERS", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-AIML", "LI-GRP-ENT-ARCH"],
        "companies": [
            ("google_cloud", "Sandboxed `Cloud Run Jobs` verifier & `Vertex AI Evaluation Service`", "Vertex AI GenAI Evaluation Service", "https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview"),
            ("openhands", "Autonomous software engineering runtime (`OpenHands` pre-completion verification hooks)", "OpenHands: Code-Act Verification & Benchmark Harness", "https://docs.all-hands.dev/"),
            ("anthropic", "Evaluator-Optimizer workflow pattern from *Building Effective Agents*", "Anthropic Engineering: Building Effective Agents", "https://www.anthropic.com/engineering/building-effective-agents"),
            ("weights_biases", "Trajectory evaluation & assertion tracking (`W&B Weave`)", "Weights & Biases Weave: Evaluating Agent Trajectories", "https://wandb.ai/site/weave"),
        ],
        "linkedin_primary_5": ["#AIEngineering", "#AgenticAI", "#GoogleCloud", "#OpenHands", "#LLMEvals"],
        "niche_hashtags": ["#VertexAI", "#SoftwareEngineering", "#DevOps", "#TestDrivenDevelopment", "#CI_CD"],
    },
    "IDEA-04": {
        "cluster_id": "CLUSTER_MCP_IDENTITY",
        "primary_groups": ["LI-GRP-MCP-API", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-AGENT-BUILDERS", "LI-GRP-ENT-ARCH"],
        "companies": [
            ("google_cloud", "`Vertex AI Vector Search` + `text-embedding-005` + `Apigee` MCP tool registry", "Google Cloud Vertex AI Vector Search", "https://cloud.google.com/vertex-ai/docs/vector-search/overview"),
            ("anthropic", "Model Context Protocol (`MCP`) dynamic tool loading & token efficiency", "Model Context Protocol (MCP) Official Specification", "https://modelcontextprotocol.io/specification"),
            ("openai", "Function-calling tool choice & strict schema routing benchmarks", "OpenAI Agents SDK: Tool Routing & Guardrails", "https://openai.github.io/openai-agents-python/"),
            ("langchain", "`langgraph-bigtool` semantic tool retrieval for 100+ tool registries", "LangGraph BigTool: Scaling Agent Tool Registries", "https://github.com/langchain-ai/langgraph-bigtool"),
        ],
        "linkedin_primary_5": ["#ModelContextProtocol", "#GoogleCloud", "#VertexAI", "#AgenticAI", "#AIEngineering"],
        "niche_hashtags": ["#VectorSearch", "#Anthropic", "#OpenAI", "#LangGraph", "#APIGateway"],
    },
    "IDEA-05": {
        "cluster_id": "CLUSTER_MULTIAGENT_MEMORY",
        "primary_groups": ["LI-GRP-GENAI-PRAC", "LI-GRP-GCP", "LI-GRP-AGENT-BUILDERS"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-CS-CCO"],
        "companies": [
            ("google_cloud", "Creator of the open `Agent2Agent (A2A)` protocol, `ADK`, & `Cloud Spanner` blackboard state", "Google Cloud: Agent2Agent (A2A) Interoperability Protocol", "https://github.com/google/A2A"),
            ("pydantic", "`Pydantic v2` strict state contract validation between supervisor and worker agents", "Pydantic v2: High-Performance Schema Validation", "https://docs.pydantic.dev/latest/"),
            ("langchain", "Typed `StateGraph` channels & deterministic handoffs (`LangGraph`)", "LangGraph Multi-Agent Supervisor & Blackboard Patterns", "https://langchain-ai.github.io/langgraph/concepts/multi_agent/"),
            ("servicenow", "Enterprise cross-domain ITSM/CRM multi-agent workflow orchestration", "ServiceNow AI Research: Enterprise Multi-Agent Systems", "https://www.servicenow.com/research/"),
        ],
        "linkedin_primary_5": ["#MultiAgentSystems", "#GoogleCloud", "#A2AProtocol", "#AgenticAI", "#EnterpriseArchitecture"],
        "niche_hashtags": ["#GoogleCloudADK", "#Pydantic", "#LangGraph", "#CloudSpanner", "#DistributedSystems"],
    },
    "IDEA-06": {
        "cluster_id": "CLUSTER_MULTIAGENT_MEMORY",
        "primary_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-AGENT-BUILDERS", "LI-GRP-CS-CCO"],
        "companies": [
            ("google_cloud", "`Cloud Workflows`, `Cloud Spanner` idempotency keys, & `Firestore` durable checkpoints", "Google Cloud Workflows: Saga & Compensation Patterns", "https://cloud.google.com/workflows/docs"),
            ("temporal", "Durable execution & deterministic replay semantics for long-running AI agents", "Temporal: Durable Execution for AI Agents", "https://temporal.io/use-cases/ai"),
            ("langchain", "`LangGraph` persistent checkpointer (`PostgresSaver` / `Spanner`) & time-travel resume", "LangGraph Persistence & Fault-Tolerant Checkpointing", "https://langchain-ai.github.io/langgraph/concepts/persistence/"),
            ("snowflake", "Idempotent enterprise data warehouse write-back & transactional outbox", "Snowflake Engineering: Transactional Data Consistency", "https://www.snowflake.com/en/engineering-blog/"),
        ],
        "linkedin_primary_5": ["#DistributedSystems", "#GoogleCloud", "#AgenticAI", "#SiteReliabilityEngineering", "#EnterpriseAI"],
        "niche_hashtags": ["#DurableExecution", "#CloudSpanner", "#Temporal", "#LangGraph", "#FaultTolerance"],
    },
    "IDEA-07": {
        "cluster_id": "CLUSTER_MULTIAGENT_MEMORY",
        "primary_groups": ["LI-GRP-AIML", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-CISO-SEC"],
        "companies": [
            ("google_cloud", "`AlloyDB pgvector` + `Vertex AI Grounding` + cryptographic SHA-256 citation receipts", "Vertex AI Grounding & Enterprise Truthfulness", "https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview"),
            ("llamaindex", "Citation-backed Knowledge Graph & document lineage (`LlamaIndex`)", "LlamaIndex Property Graph & Citation Verification", "https://docs.llamaindex.ai/"),
            ("anthropic", "Contextual Retrieval & citation verification for zero-hallucination RAG", "Anthropic News: Contextual Retrieval for Enterprise RAG", "https://www.anthropic.com/news/contextual-retrieval"),
            ("snowflake", "Governed enterprise knowledge table watermarks & lineage (`Snowflake Cortex`)", "Snowflake Cortex: Grounded Enterprise Search", "https://www.snowflake.com/en/data-cloud/cortex/"),
        ],
        "linkedin_primary_5": ["#EnterpriseRAG", "#GoogleCloud", "#AgenticAI", "#AIGovernance", "#DataEngineering"],
        "niche_hashtags": ["#AlloyDB", "#VertexAI", "#GraphRAG", "#LlamaIndex", "#ZeroHallucination"],
    },
    "IDEA-08": {
        "cluster_id": "CLUSTER_GOVERNANCE_FINOPS",
        "primary_groups": ["LI-GRP-CISO-SEC", "LI-GRP-MCP-API", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-GENAI-PRAC"],
        "companies": [
            ("google_cloud", "`Google Cloud Model Armor`, `Sensitive Data Protection (DLP)`, & `IAM Conditions`", "Google Cloud Model Armor: Prompt Injection & Data Loss Defense", "https://cloud.google.com/security-command-center/docs/model-armor-overview"),
            ("owasp", "`OWASP Top 10 for LLM Applications (LLM01: Prompt Injection & LLM06: Excessive Agency)`", "OWASP GenAI Security Project: LLM01 & Agentic Threats", "https://genai.owasp.org/"),
            ("anthropic", "Constitutional classifiers & sandboxed capability separation", "Anthropic Research: Mitigating Indirect Prompt Injection", "https://www.anthropic.com/research"),
            ("cloudflare", "Edge WAF & Zero-Trust MCP policy enforcement", "Cloudflare Zero Trust for AI Workloads", "https://blog.cloudflare.com/tag/security/"),
        ],
        "linkedin_primary_5": ["#CyberSecurity", "#ZeroTrustAI", "#GoogleCloud", "#CISO", "#AgenticAI"],
        "niche_hashtags": ["#ModelArmor", "#OWASP", "#PromptInjection", "#AISecurity", "#CloudSecurity"],
    },
    "IDEA-09": {
        "cluster_id": "CLUSTER_INFERENCE_KV",
        "primary_groups": ["LI-GRP-AIML", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-AGENT-BUILDERS"],
        "companies": [
            ("google_deepmind", "`Gemini 3.8 Flash` & `Gemini 4 Argon` speculative cascade & parallel tool execution", "Google DeepMind: Gemini Frontier Speed & Reasoning Roofline", "https://deepmind.google/technologies/gemini/"),
            ("google_cloud", "`Vertex AI Global Endpoint` (`locations/global`) & parallel async ADK fan-out", "Vertex AI Global Endpoint for High-Throughput Inference", "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations"),
            ("openai", "Realtime & low-latency speculative decoding benchmarks", "OpenAI Engineering: Latency Optimization for Agentic Workflows", "https://platform.openai.com/docs/guides/latency-optimization"),
            ("meta_ai", "Open-weights speculative drafter-verifier architecture research", "Meta AI Research: Speculative Decoding & Sub-Second Inference", "https://ai.meta.com/research/"),
        ],
        "linkedin_primary_5": ["#AIInference", "#GoogleCloud", "#GoogleDeepMind", "#VertexAI", "#AgenticAI"],
        "niche_hashtags": ["#SpeculativeDecoding", "#LowLatency", "#LLMOps", "#FinOps", "#HighPerformanceComputing"],
    },
    "IDEA-10": {
        "cluster_id": "CLUSTER_CODING_EVALS",
        "primary_groups": ["LI-GRP-GENAI-PRAC", "LI-GRP-AGENT-BUILDERS", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-AIML", "LI-GRP-CS-CCO"],
        "companies": [
            ("google_cloud", "`Cloud Build` CI/CD regression gate, `Vertex AI Evaluation Service`, & `BigQuery` golden traces", "Vertex AI Evaluation Service in Cloud Build CI/CD", "https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview"),
            ("weights_biases", "Golden trajectory dataset versioning & `pass^5` regression matrix (`W&B Weave`)", "Weights & Biases Weave: CI/CD Regression Gates for Agents", "https://wandb.ai/site/weave"),
            ("arize_ai", "Production failure trace capture -> golden replay dataset promotion (`Arize Phoenix`)", "Arize AI: Continuous Evaluation from Production Traces", "https://arize.com/blog/"),
            ("openai", "Graders & Evals API specification for multi-step agent trajectories", "OpenAI Cookbook: Automated Agent Evaluation & Graders", "https://cookbook.openai.com/"),
        ],
        "linkedin_primary_5": ["#LLMEvals", "#AgenticAI", "#GoogleCloud", "#AIEngineering", "#CI_CD"],
        "niche_hashtags": ["#VertexAI", "#MLOps", "#QualityEngineering", "#PassAtK", "#ReliabilityEngineering"],
    },
    "POST-01": {
        "cluster_id": "CLUSTER_CODING_EVALS",
        "primary_groups": ["LI-GRP-AIML", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-AGENT-BUILDERS", "LI-GRP-ENT-ARCH"],
        "companies": [
            ("google_cloud", "`Vertex AI Agent Engine` & `CloudCoreNetwork-QA` self-improving evaluation loop", "Google Cloud Vertex AI Agent Engine", "https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview"),
            ("google_deepmind", "Evolutionary harness mutation & reference-trajectory competence verification", "Google DeepMind Research: Self-Improving Agent Harnesses", "https://deepmind.google/research/"),
            ("weights_biases", "Experiment tracking across evolutionary harness generations", "Weights & Biases Weave", "https://wandb.ai/site/weave"),
        ],
        "linkedin_primary_5": ["#AgenticAI", "#GoogleCloud", "#GoogleDeepMind", "#LLMEvals", "#AIEngineering"],
        "niche_hashtags": ["#HarnessEvolve", "#VertexAI", "#SelfImprovingAI", "#AutonomousAgents"],
    },
    "POST-02": {
        "cluster_id": "CLUSTER_INFERENCE_KV",
        "primary_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-AIML", "LI-GRP-CS-CCO"],
        "companies": [
            ("google_cloud", "6-Layer Enterprise Agent Harness OS on `Vertex AI`, `Cloud Run`, & `Cloud Spanner`", "Google Cloud Architecture Center: Agentic AI Operating Model", "https://cloud.google.com/architecture/ai-ml"),
            ("anthropic", "Harness engineering & context lifecycle principles", "Anthropic Engineering: Building Effective Agents", "https://www.anthropic.com/engineering/building-effective-agents"),
            ("langchain", "`LangGraph` state machine orchestration layer inside the 6-layer harness", "LangGraph Enterprise Runtime Architecture", "https://blog.langchain.dev/"),
        ],
        "linkedin_primary_5": ["#EnterpriseAI", "#GoogleCloud", "#AgenticAI", "#SystemArchitecture", "#VertexAI"],
        "niche_hashtags": ["#HarnessEngineering", "#AIPlatform", "#CloudArchitecture", "#LangGraph"],
    },
    "POST-03": {
        "cluster_id": "CLUSTER_MCP_IDENTITY",
        "primary_groups": ["LI-GRP-MCP-API", "LI-GRP-AGENT-BUILDERS", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-GENAI-PRAC", "LI-GRP-ENT-ARCH"],
        "companies": [
            ("google_cloud", "`Google Cloud ADK` modular skill registry & `Artifact Registry` plugin hub", "Google Cloud Agent Development Kit (ADK)", "https://google.github.io/adk-docs/"),
            ("anthropic", "`SKILL.md` progressive skill loading & `Claude Code` plugin architecture", "Anthropic Engineering: Claude Code Best Practices & Skills", "https://www.anthropic.com/engineering/claude-code-best-practices"),
            ("openai", "Modular Agent SDK handoffs & reusable skill bundles", "OpenAI Agents SDK Documentation", "https://openai.github.io/openai-agents-python/"),
        ],
        "linkedin_primary_5": ["#AgenticAI", "#GoogleCloud", "#ModelContextProtocol", "#AIEngineering", "#DeveloperTools"],
        "niche_hashtags": ["#GoogleCloudADK", "#Anthropic", "#ClaudeCode", "#MultiAgentSystems"],
    },
    "POST-04": {
        "cluster_id": "CLUSTER_CODING_EVALS",
        "primary_groups": ["LI-GRP-AGENT-BUILDERS", "LI-GRP-GENAI-PRAC", "LI-GRP-GCP"],
        "niche_groups": ["LI-GRP-AIML", "LI-GRP-CISO-SEC"],
        "companies": [
            ("openhands", "`OpenHands` autonomous coding harness & sandboxed execution loop", "OpenHands Official Architecture Documentation", "https://docs.all-hands.dev/"),
            ("google_cloud", "`Cloud Run` gVisor microVM sandbox isolation & `Cloud Build` verification", "Google Cloud Run: gVisor Container Sandbox Security", "https://cloud.google.com/run/docs/securing/security"),
            ("anthropic", "SWE-bench verified coding agent patterns", "Anthropic Engineering: SWE-bench Coding Agents", "https://www.anthropic.com/engineering"),
        ],
        "linkedin_primary_5": ["#OpenHands", "#GoogleCloud", "#AgenticAI", "#SoftwareEngineering", "#AIEngineering"],
        "niche_hashtags": ["#AutonomousCoding", "#CloudRun", "#gVisor", "#SWEbench"],
    },
    "POST-05": {
        "cluster_id": "CLUSTER_GOVERNANCE_FINOPS",
        "primary_groups": ["LI-GRP-CISO-SEC", "LI-GRP-GCP", "LI-GRP-MCP-API"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-GENAI-PRAC"],
        "companies": [
            ("google_cloud", "`Google Cloud Model Armor`, `Cloud KMS`, & Dual-Plane Privileged/Quarantined Sandbox", "Google Cloud Model Armor Documentation", "https://cloud.google.com/security-command-center/docs/model-armor-overview"),
            ("owasp", "`OWASP Top 10 for LLM & Agentic Applications` defense-in-depth blueprint", "OWASP GenAI Security Project", "https://genai.owasp.org/"),
            ("anthropic", "Dual-LLM / capability-restricted security boundary patterns", "Anthropic Safety & Alignment Research", "https://www.anthropic.com/research"),
        ],
        "linkedin_primary_5": ["#AISecurity", "#ZeroTrustAI", "#GoogleCloud", "#CISO", "#OWASP"],
        "niche_hashtags": ["#ModelArmor", "#PromptInjection", "#CyberSecurity", "#EnterpriseSecurity"],
    },
    "POST-06": {
        "cluster_id": "CLUSTER_CODING_EVALS",
        "primary_groups": ["LI-GRP-GENAI-PRAC", "LI-GRP-GCP", "LI-GRP-AGENT-BUILDERS"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-AIML"],
        "companies": [
            ("google_cloud", "Production repository blueprint for `Cloud Run`, `Terraform`, & `Google Cloud ADK`", "Google Cloud ADK Production Deployment Guide", "https://google.github.io/adk-docs/"),
            ("anthropic", "`AGENTS.md` / `CLAUDE.md` constitutional repo instructions", "Anthropic Engineering: Repository Instructions & Context", "https://www.anthropic.com/engineering/claude-code-best-practices"),
            ("pydantic", "Typed configuration & schema contracts (`pyproject.toml` + `Pydantic v2`)", "Pydantic Documentation", "https://docs.pydantic.dev/latest/"),
        ],
        "linkedin_primary_5": ["#AIEngineering", "#GoogleCloud", "#AgenticAI", "#Terraform", "#PlatformEngineering"],
        "niche_hashtags": ["#GoogleCloudADK", "#DevOps", "#CleanArchitecture", "#MLOps"],
    },
    "POST-07": {
        "cluster_id": "CLUSTER_MULTIAGENT_MEMORY",
        "primary_groups": ["LI-GRP-AIML", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-CS-CCO"],
        "companies": [
            ("google_cloud", "`AlloyDB pgvector` + `Cloud Spanner` immutable evidence ledger", "Google Cloud AlloyDB AI & Vector Search", "https://cloud.google.com/alloydb/ai"),
            ("llamaindex", "Evidence-linked knowledge wiki & document graph indexing", "LlamaIndex Knowledge Graph & Memory", "https://docs.llamaindex.ai/"),
            ("anthropic", "Citation-grounded memory & anti-hallucination guardrails", "Anthropic Contextual Retrieval", "https://www.anthropic.com/news/contextual-retrieval"),
        ],
        "linkedin_primary_5": ["#AgentMemory", "#GoogleCloud", "#EnterpriseRAG", "#AgenticAI", "#DataArchitecture"],
        "niche_hashtags": ["#AlloyDB", "#CloudSpanner", "#KnowledgeGraph", "#ZeroHallucination"],
    },
    "POST-08": {
        "cluster_id": "CLUSTER_INFERENCE_KV",
        "primary_groups": ["LI-GRP-ENT-ARCH", "LI-GRP-GCP", "LI-GRP-GENAI-PRAC"],
        "niche_groups": ["LI-GRP-CS-CCO", "LI-GRP-AGENT-BUILDERS"],
        "companies": [
            ("google_cloud", "End-to-End 6-Step Production Agent on `Vertex AI`, `Apigee`, `Model Armor`, & `Cloud Run`", "Google Cloud Reference Architecture for Agentic AI", "https://cloud.google.com/architecture/ai-ml"),
            ("langchain", "Orchestration graph & durable checkpoint integration", "LangGraph Production Deployment", "https://langchain-ai.github.io/langgraph/"),
            ("arize_ai", "OpenTelemetry GenAI observability & production SLO telemetry", "Arize Phoenix OpenTelemetry Tracing", "https://docs.arize.com/phoenix"),
        ],
        "linkedin_primary_5": ["#EnterpriseAI", "#GoogleCloud", "#VertexAI", "#AgenticAI", "#CloudArchitecture"],
        "niche_hashtags": ["#GoogleCloudADK", "#LLMOps", "#ProductionAI", "#OpenTelemetry"],
    },
}

# Map Cluster IDs to default profiles for dynamic daily posts (TOP5-*, DAILY-*, CS-INV-*, MINT-02..12)
CLUSTER_DEFAULT_POST_MAP: Dict[str, str] = {
    "CLUSTER_MCP_IDENTITY": "MINT-01",
    "CLUSTER_CODING_EVALS": "IDEA-03",
    "CLUSTER_INFERENCE_KV": "IDEA-02",
    "CLUSTER_MULTIAGENT_MEMORY": "IDEA-05",
    "CLUSTER_GOVERNANCE_FINOPS": "IDEA-08",
}


def resolve_distribution_directory_for_post(
    post_id: str,
    title: str = "",
    cluster_id: str = "",
    primary_url: str = "",
    source_channel: str = "",
) -> Dict[str, Any]:
    """Return the complete Groups, Pages, @Companies, Hashtags & References bundle for any post ID."""
    clean_id = str(post_id or "").strip()
    profile_key = clean_id if clean_id in POST_SPECIFIC_PROFILES else ""

    if not profile_key:
        t_low = f"{clean_id} {title} {cluster_id}".lower()
        if "mcp" in t_low or "obo" in t_low or "oauth" in t_low or "tool" in t_low:
            profile_key = "MINT-01"
        elif "blackboard" in t_low or "a2a" in t_low or "swarm" in t_low or "handoff" in t_low:
            profile_key = "IDEA-05"
        elif "inject" in t_low or "armor" in t_low or "shacl" in t_low or "security" in t_low or "trifecta" in t_low:
            profile_key = "IDEA-08"
        elif "kv" in t_low or "rot" in t_low or "cache" in t_low or "latent" in t_low or "speculative" in t_low:
            profile_key = "IDEA-02"
        elif "loop" in t_low or "otel" in t_low or "span" in t_low:
            profile_key = "IDEA-01"
        elif "eval" in t_low or "pass" in t_low or "judge" in t_low or "sandbox" in t_low or "harness" in t_low:
            profile_key = "IDEA-03"
        else:
            profile_key = CLUSTER_DEFAULT_POST_MAP.get(cluster_id, "MINT-01")

    prof = POST_SPECIFIC_PROFILES[profile_key]
    eff_cluster = cluster_id or prof["cluster_id"]

    primary_groups = [dict(LINKEDIN_GROUPS_CATALOG[g]) for g in prof["primary_groups"] if g in LINKEDIN_GROUPS_CATALOG]
    niche_groups = [dict(LINKEDIN_GROUPS_CATALOG[g]) for g in prof["niche_groups"] if g in LINKEDIN_GROUPS_CATALOG]
    cross_platform_pages = [dict(p) for p in CROSS_PLATFORM_PAGES_CATALOG.get(eff_cluster, CROSS_PLATFORM_PAGES_CATALOG["CLUSTER_MCP_IDENTITY"])]

    companies_list: List[Dict[str, str]] = []
    authoritative_refs: List[Dict[str, str]] = []
    company_tags_inline: List[str] = []
    x_handles_inline: List[str] = []

    if primary_url and source_channel:
        authoritative_refs.append({
            "organization": source_channel,
            "title": title or "Primary Engineering Source & Benchmark Artifact",
            "url": primary_url,
            "citation_type": "Primary Trigger Source",
        })

    for comp_key, role_desc, ref_title, ref_url in prof["companies"]:
        c_meta = COMPANY_DIRECTORY[comp_key]
        companies_list.append({
            "company_id": comp_key,
            "company_name": c_meta["company_name"],
            "linkedin_page_tag": c_meta["linkedin_page_tag"],
            "linkedin_page_url": c_meta["linkedin_page_url"],
            "x_handle": c_meta["x_handle"],
            "github_org_url": c_meta["github_org_url"],
            "role_in_post": role_desc,
            "reference_title": ref_title,
            "reference_url": ref_url,
        })
        company_tags_inline.append(c_meta["linkedin_page_tag"])
        x_handles_inline.append(c_meta["x_handle"])
        if not any(r["url"] == ref_url for r in authoritative_refs):
            authoritative_refs.append({
                "organization": c_meta["company_name"],
                "title": ref_title,
                "url": ref_url,
                "citation_type": "Official Company Engineering Reference",
            })

    li_5 = list(prof["linkedin_primary_5"])
    niche_tags = list(prof["niche_hashtags"])
    ecosystem_tags = [COMPANY_DIRECTORY[c[0]]["ecosystem_hashtag"] for c in prof["companies"] if c[0] in COMPANY_DIRECTORY]
    seen_t = set()
    combined_tags: List[str] = []
    for t in li_5 + niche_tags + ecosystem_tags:
        if t.lower() not in seen_t:
            seen_t.add(t.lower())
            combined_tags.append(t)

    return {
        "post_id": clean_id,
        "resolved_profile_key": profile_key,
        "cluster_id": eff_cluster,
        "linkedin_groups_primary": primary_groups,
        "linkedin_groups_niche_network": niche_groups,
        "cross_platform_pages_and_communities": cross_platform_pages,
        "relevant_companies_and_pages": companies_list,
        "company_mentions_line_linkedin": " · ".join(company_tags_inline),
        "company_mentions_line_x": " ".join(x_handles_inline),
        "hashtags_bundle": {
            "linkedin_optimal_5": " ".join(li_5),
            "niche_practitioner": " ".join(niche_tags),
            "company_ecosystem": " ".join(ecosystem_tags),
            "full_hashtag_string": " ".join(combined_tags),
            "all_tags_list": combined_tags,
        },
        "authoritative_references": authoritative_refs,
    }


def format_markdown_distribution_appendix(dist: Dict[str, Any]) -> str:
    """Format a copy-pasteable Markdown appendix for `linkedin_post_draft.md` and UI copy buttons."""
    lines = [
        "---",
        "## 🌐 Target Groups, Pages, `@Company` Mentions, Hashtags & Verified References",
        "",
        f"**Tag Relevant Company Pages on LinkedIn:** {dist['company_mentions_line_linkedin']}",
        f"**Tag Relevant Handles on X / Twitter:** {dist['company_mentions_line_x']}",
        "",
        "### 1. Relevant Companies & Official Engineering References",
    ]
    for c in dist["relevant_companies_and_pages"]:
        lines.append(
            f"- **{c['linkedin_page_tag']}** ([LinkedIn Page]({c['linkedin_page_url']}) · `{c['x_handle']}`) — {c['role_in_post']} · "
            f"Reference: [{c['reference_title']}]({c['reference_url']})"
        )
    lines.append("")
    lines.append("### 2. Primary High-Reach LinkedIn Groups")
    for g in dist["linkedin_groups_primary"]:
        lines.append(f"- **{g['name']}** ({g['members']}) — [Open Group ↗]({g['url']}) · *Goal: {g['goal']}*")
    lines.append("")
    lines.append("### 3. Niche Executive & Principal Architect LinkedIn Groups")
    for g in dist["linkedin_groups_niche_network"]:
        lines.append(f"- **{g['name']}** ({g['members']}) — [Open Group ↗]({g['url']}) · *Goal: {g['goal']}*")
    lines.append("")
    lines.append("### 4. Cross-Platform Syndication Pages & Technical Communities")
    for cp in dist["cross_platform_pages_and_communities"]:
        lines.append(
            f"- **{cp['platform']} — {cp['page_or_group']}** ({cp['audience']}) — [Open Page ↗]({cp['url']}) · *Angle: {cp['posting_angle']}*"
        )
    lines.append("")
    lines.append("### 5. Tiered Hashtag Strategy")
    hb = dist["hashtags_bundle"]
    lines.append(f"- **LinkedIn Optimal 5 (Paste at bottom of post):** `{hb['linkedin_optimal_5']}`")
    lines.append(f"- **Niche Practitioner Tags (Dev.to / Hashnode / YouTube / Instagram):** `{hb['niche_practitioner']}`")
    lines.append(f"- **Full Combined Hashtag Block:** `{hb['full_hashtag_string']}`")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 6. Top 25 High-Visibility Agentic AI & Enterprise LinkedIn Groups Radar
#    (With Missing-Membership Heuristics + Paste-to-Diff Auto-Detector)
# ---------------------------------------------------------------------------
import json
import urllib.parse
from pathlib import Path as _Path

GROUP_MEMBERSHIP_LEDGER_PATH = _Path(__file__).resolve().parent.parent.parent / "data" / "linkedin_group_memberships.json"

TOP_25_AGENTIC_AI_VISIBILITY_GROUPS: List[Dict[str, Any]] = [
    # Tier 1: Newly Emerged 2025-2026 Agentic AI, MCP, LangGraph & Eval Groups (85%-95% Likely Unjoined)
    {
        "group_id": "GRP-01-AGENTIC-WORKFLOWS",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "AI Agents, Autonomous Systems & Multi-Agent Workflows (MCP / A2A / LangGraph)",
        "direct_group_url": "https://www.linkedin.com/groups/12918440/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=AI%20Agents%20Autonomous%20Systems%20Multi-Agent",
        "members": "210,000+",
        "members_num": 210000,
        "visibility_score": 99.4,
        "unjoined_probability": "HIGH (92% — Newer 2025–2026 Agentic cohort)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (24–48h approval; high organic feed distribution)",
        "best_post_types": "MINT-01, IDEA-04, IDEA-05, TOP5-01..05 (Architecture Blueprints + GitHub Repos)",
        "why_join_for_max_visibility": "Pure-play audience of Principal AI Engineers, Agent SDK builders, and VPs of AI actively benchmarking MCP, A2A, and LangGraph.",
    },
    {
        "group_id": "GRP-02-MCP-API-ARCH",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "Model Context Protocol (MCP), Agentic Tooling & Enterprise API Architecture",
        "direct_group_url": "https://www.linkedin.com/groups/13041020/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Model%20Context%20Protocol%20MCP%20API",
        "members": "195,000+",
        "members_num": 195000,
        "visibility_score": 99.1,
        "unjoined_probability": "HIGH (94% — Specialized MCP & OAuth 2.1 OBO community)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (Instant / 24h approval)",
        "best_post_types": "MINT-01 (Zero-Bloat MCP Gateway), IDEA-04 (Dynamic Tool Router), POST-03",
        "why_join_for_max_visibility": "Highest concentration of architects solving 58K-token MCP schema bloat and Confused-Deputy OAuth 2.1 OBO security.",
    },
    {
        "group_id": "GRP-03-GENAI-LLM-PRAC",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "Generative AI & LLMs (Large Language Models) — Enterprise Practitioners",
        "direct_group_url": "https://www.linkedin.com/groups/12795132/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Generative%20AI%20Large%20Language%20Models%20LLMs",
        "members": "480,000+",
        "members_num": 480000,
        "visibility_score": 98.9,
        "unjoined_probability": "HIGH (85% — Rapidly scaled practitioner group)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (Auto-approve for senior tech leaders)",
        "best_post_types": "All 19 Tier-A Repositories, Monday 9:00 AM ET Top-5 Briefings",
        "why_join_for_max_visibility": "Generates the highest technical comment velocity on context rot, KV-cache optimization, and pass^5 reliability math.",
    },
    {
        "group_id": "GRP-04-LLMOPS-EVALS",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "LLMOps, MLOps, AI Evaluations (Evals) & Production AI Reliability",
        "direct_group_url": "https://www.linkedin.com/groups/12891045/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=LLMOps%20MLOps%20AI%20Engineering",
        "members": "265,000+",
        "members_num": 265000,
        "visibility_score": 98.4,
        "unjoined_probability": "HIGH (90% — Focused on production SRE & evals for LLMs)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (24h approval)",
        "best_post_types": "IDEA-01 (Loop Breaker), IDEA-03 (Pre-Completion Hook), IDEA-10 (Golden Replay Gate), POST-01",
        "why_join_for_max_visibility": "Decision-makers who star and fork repositories that include reproducible `evals/eval_dataset.jsonl` and `eval_results.json`.",
    },
    {
        "group_id": "GRP-05-RAG-CONTEXT-ENG",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "Large Language Models (LLMs), Enterprise RAG, Vector Databases & Context Engineering",
        "direct_group_url": "https://www.linkedin.com/groups/12840512/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Large%20Language%20Models%20RAG%20Vector",
        "members": "340,000+",
        "members_num": 340000,
        "visibility_score": 98.2,
        "unjoined_probability": "HIGH (88% — Specialized RAG & Context Engineering hub)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (24–48h approval)",
        "best_post_types": "IDEA-02 (Context-Rot Compactor), IDEA-07 (SHA-256 Receipt Memory), POST-07",
        "why_join_for_max_visibility": "High share rate on 4:5 PDF Carousels comparing Naive RAG vs. Prefix-Immutable KV-Cache & Citation-Backed Memory.",
    },
    {
        "group_id": "GRP-06-CODING-AGENTS",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "Autonomous Coding Agents, SWE-Bench, OpenHands & AI Software Engineering",
        "direct_group_url": "https://www.linkedin.com/groups/13012890/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=AI%20Software%20Engineering%20Coding%20Agents",
        "members": "115,000+",
        "members_num": 115000,
        "visibility_score": 97.8,
        "unjoined_probability": "HIGH (95% — Niche Staff+ AI SWE cohort)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (24h approval)",
        "best_post_types": "TOP5-01 (gVisor Builder-vs-Judge), IDEA-03, POST-04 (OpenHands Coding Harness), POST-06",
        "why_join_for_max_visibility": "Directly reaches VPs of Developer Productivity and Staff Engineers deploying sandboxed coding agents.",
    },
    {
        "group_id": "GRP-07-OPEN-WEIGHTS-LLAMA",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "Open-Source AI: Llama, vLLM, Speculative Decoding & High-Throughput Inference",
        "direct_group_url": "https://www.linkedin.com/groups/12819400/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Open%20Source%20AI%20LLM%20Inference",
        "members": "290,000+",
        "members_num": 290000,
        "visibility_score": 97.5,
        "unjoined_probability": "HIGH (89% — Inference & Speculative Decoding specialists)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Moderate (48h approval)",
        "best_post_types": "IDEA-09 (Sub-2s Speculative Cascade), TOP5-03 (Grammar-Aligned Decoding)",
        "why_join_for_max_visibility": "Strong appetite for latency roofline charts (p95 4,372ms -> 610ms) and cost-per-1K-workflow benchmarks.",
    },
    {
        "group_id": "GRP-08-VERTEX-ADK-BUILDERS",
        "tier": "Tier 1 — Emerging Agentic AI, MCP & Multi-Agent Builders (Highest Unjoined Probability)",
        "name": "Google Cloud Vertex AI, Gemini & Agent Development Kit (ADK) Enterprise Builders",
        "direct_group_url": "https://www.linkedin.com/groups/12965011/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Vertex%20AI%20Gemini%20Google%20Cloud%20AI",
        "members": "145,000+",
        "members_num": 145000,
        "visibility_score": 98.7,
        "unjoined_probability": "MEDIUM-HIGH (75% — Newer Vertex AI / Gemini specific group distinct from legacy GCP group)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (Instant for @google.com / Google Cloud leaders)",
        "best_post_types": "All 19 Google Cloud ADK + Vertex AI #78 Architecture Blueprint posts",
        "why_join_for_max_visibility": "Your natural home-turf amplifier: enterprise customers and partner architects specifically building on Vertex AI Agent Engine & ADK.",
    },

    # Tier 2: Mega-Reach AI, Machine Learning & Data Science Groups (1M - 6.5M+ Members)
    {
        "group_id": "GRP-09-MEGA-AIML-6M",
        "tier": "Tier 2 — Mega-Reach AI & Machine Learning Networks (1M–6.5M+ Members for Top-of-Funnel Reach)",
        "name": "Artificial Intelligence, Machine Learning, Data Science & Robotics",
        "direct_group_url": "https://www.linkedin.com/groups/3671367/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Artificial%20Intelligence%20Machine%20Learning%20Data%20Science%20Robotics",
        "members": "6,500,000+",
        "members_num": 6500000,
        "visibility_score": 99.8,
        "unjoined_probability": "MEDIUM (55% — Largest AI group on LinkedIn; check if already joined)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Moderated (24–72h post review; native 4:5 PDF Carousels & GIFs approved fastest)",
        "best_post_types": "Monday 9:00 AM ET Slot #1 Flagship Post + 4:5 Animated GIF / PDF Carousel",
        "why_join_for_max_visibility": "Single largest AI distribution surface on LinkedIn (6.5M+ members) for top-of-funnel impressions and profile views.",
    },
    {
        "group_id": "GRP-10-MEGA-DL-ML-2M",
        "tier": "Tier 2 — Mega-Reach AI & Machine Learning Networks (1M–6.5M+ Members for Top-of-Funnel Reach)",
        "name": "Artificial Intelligence, Deep Learning, Machine Learning",
        "direct_group_url": "https://www.linkedin.com/groups/1814785/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Artificial%20Intelligence%20Deep%20Learning%20Machine%20Learning",
        "members": "2,100,000+",
        "members_num": 2100000,
        "visibility_score": 98.5,
        "unjoined_probability": "HIGH (78% — Often overlooked second-largest 2.1M AI group)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (24h post approval)",
        "best_post_types": "Architecture Blueprints (`T54`, `T57`, `T67`, `T85`) + Benchmark Tables",
        "why_join_for_max_visibility": "2.1M+ researchers, ML engineers, and technical executives with lower post noise than the 6.5M group.",
    },
    {
        "group_id": "GRP-11-MEGA-AI-PIVOT-1M",
        "tier": "Tier 2 — Mega-Reach AI & Machine Learning Networks (1M–6.5M+ Members for Top-of-Funnel Reach)",
        "name": "Artificial Intelligence Pivot: Robotics, Machine Learning, NLP, AI, LLMs & Computer Vision",
        "direct_group_url": "https://www.linkedin.com/groups/45655/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Artificial%20Intelligence%20Pivot%20LLMs",
        "members": "1,450,000+",
        "members_num": 1450000,
        "visibility_score": 97.9,
        "unjoined_probability": "HIGH (85% — Legacy robotics group that pivoted to LLMs & Agentic AI)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast (Instant member post feed)",
        "best_post_types": "Daily 6 Creator-Style Visual Posts (`STYLE-01`..`STYLE-06`)",
        "why_join_for_max_visibility": "1.45M+ cross-industry executives and builders; high engagement on visual system comparisons (`T57`).",
    },
    {
        "group_id": "GRP-12-DATA-SCIENCE-CENTRAL",
        "tier": "Tier 2 — Mega-Reach AI & Machine Learning Networks (1M–6.5M+ Members for Top-of-Funnel Reach)",
        "name": "Data Science Central (Big Data, Enterprise AI, Analytics & ML)",
        "direct_group_url": "https://www.linkedin.com/groups/2015219/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Data%20Science%20Central",
        "members": "1,100,000+",
        "members_num": 1100000,
        "visibility_score": 97.2,
        "unjoined_probability": "HIGH (80% — Data/Analytics heavy audience hungry for Agentic RAG & Spanner/AlloyDB)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Moderated (24–48h)",
        "best_post_types": "IDEA-06 (Idempotent Checkpoints), IDEA-07 (Evidence Memory), POST-07",
        "why_join_for_max_visibility": "1.1M+ Chief Data Officers, Principal Data Architects, and Analytics Engineers.",
    },
    {
        "group_id": "GRP-13-BIGDATA-AI-IOT",
        "tier": "Tier 2 — Mega-Reach AI & Machine Learning Networks (1M–6.5M+ Members for Top-of-Funnel Reach)",
        "name": "Big Data | Data Science | Machine Learning | AI | IoT",
        "direct_group_url": "https://www.linkedin.com/groups/3990648/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Big%20Data%20Data%20Science%20Machine%20Learning%20AI",
        "members": "950,000+",
        "members_num": 950000,
        "visibility_score": 96.8,
        "unjoined_probability": "HIGH (82%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "16:9 Walkthrough Videos & 4:5 Infographics",
        "why_join_for_max_visibility": "950K+ enterprise data & platform engineers.",
    },

    # Tier 3: Cloud Architecture, Google Cloud & Multi-Cloud Infrastructure Groups
    {
        "group_id": "GRP-14-CLOUD-COMPUTING-SAAS",
        "tier": "Tier 3 — Enterprise Cloud, GCP & Multi-Cloud Architecture Networks (380K–850K+ Members)",
        "name": "Cloud Computing, SaaS, Virtualization & Enterprise Cloud Architecture",
        "direct_group_url": "https://www.linkedin.com/groups/59893/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Cloud%20Computing%20SaaS%20Enterprise%20Architecture",
        "members": "850,000+",
        "members_num": 850000,
        "visibility_score": 98.1,
        "unjoined_probability": "HIGH (75%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "POST-02 (6-Layer Harness OS), POST-08 (6-Step Production Agent), Multi-Cloud MCP",
        "why_join_for_max_visibility": "850K+ cloud architects comparing AWS Bedrock AgentCore, Azure AI Foundry, and Google Cloud Vertex AI.",
    },
    {
        "group_id": "GRP-15-ENT-ARCH-FINOPS",
        "tier": "Tier 3 — Enterprise Cloud, GCP & Multi-Cloud Architecture Networks (380K–850K+ Members)",
        "name": "Enterprise Architecture, FinOps & Cloud Transformation Leaders",
        "direct_group_url": "https://www.linkedin.com/groups/67905/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Enterprise%20Architecture%20Cloud%20Transformation",
        "members": "610,000+",
        "members_num": 610000,
        "visibility_score": 98.6,
        "unjoined_probability": "HIGH (76%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "MINT-01, IDEA-01 ($400 Loop Circuit Breaker), IDEA-02 (Context Rot -82% Tokens)",
        "why_join_for_max_visibility": "610K+ Chief Architects and Enterprise Architecture Review Board (ARB) chairs.",
    },
    {
        "group_id": "GRP-16-GCP-ARCHITECTS",
        "tier": "Tier 3 — Enterprise Cloud, GCP & Multi-Cloud Architecture Networks (380K–850K+ Members)",
        "name": "Google Cloud Platform (GCP) Architects, Developers & Vertex AI Builders",
        "direct_group_url": "https://www.linkedin.com/groups/3050257/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Google%20Cloud%20Platform%20GCP%20Architects",
        "members": "420,000+",
        "members_num": 420000,
        "visibility_score": 99.2,
        "unjoined_probability": "LOW-MEDIUM (40% — Check if already joined; essential if not)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "All 19 Terraform + Cloud Run + Vertex AI Agent Engine posts",
        "why_join_for_max_visibility": "420K+ dedicated GCP practitioners who actively deploy `./scripts/deploy_gcp_one_click.sh`.",
    },
    {
        "group_id": "GRP-17-K8S-CNCF-AI",
        "tier": "Tier 3 — Enterprise Cloud, GCP & Multi-Cloud Architecture Networks (380K–850K+ Members)",
        "name": "Kubernetes, Cloud Native Computing Foundation (CNCF), GKE & Serverless AI",
        "direct_group_url": "https://www.linkedin.com/groups/8224624/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Kubernetes%20CNCF%20Cloud%20Native",
        "members": "380,000+",
        "members_num": 380000,
        "visibility_score": 97.4,
        "unjoined_probability": "HIGH (84%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "TOP5-01 (gVisor Sandbox), POST-04 (OpenHands Cloud Run), POST-06 (Terraform Blueprint)",
        "why_join_for_max_visibility": "380K+ platform engineers running GKE, Cloud Run v2, and gVisor agent sandboxes.",
    },

    # Tier 4: CISO, Zero-Trust AI Security & AI Governance Groups
    {
        "group_id": "GRP-18-INFOSEC-CISO-2M",
        "tier": "Tier 4 — CISO, Zero-Trust AI Security & Governance Networks (190K–2.4M+ Members)",
        "name": "Information Security, CISO Network, Cybersecurity & Zero-Trust AI",
        "direct_group_url": "https://www.linkedin.com/groups/38412/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Information%20Security%20Cybersecurity%20CISO",
        "members": "2,400,000+",
        "members_num": 2400000,
        "visibility_score": 99.0,
        "unjoined_probability": "HIGH (88% — Security vertical group outside standard AI circles)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Moderated (24–48h)",
        "best_post_types": "MINT-01 (OAuth 2.1 OBO), IDEA-08 (Model Armor Capability Downgrade), POST-05, T56 Shadow AI",
        "why_join_for_max_visibility": "2.4M+ security leaders; posts on Shadow AI (`T56`) and MCP Confused-Deputy attacks go viral here because few AI architects post concrete code fixes in CISO groups.",
    },
    {
        "group_id": "GRP-19-CISO-EXEC-NETWORK",
        "tier": "Tier 4 — CISO, Zero-Trust AI Security & Governance Networks (190K–2.4M+ Members)",
        "name": "Chief Information Security Officer (CISO) & Enterprise Cyber Risk Network",
        "direct_group_url": "https://www.linkedin.com/groups/1962157/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Chief%20Information%20Security%20Officer%20CISO",
        "members": "320,000+",
        "members_num": 320000,
        "visibility_score": 98.3,
        "unjoined_probability": "HIGH (92%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Moderated",
        "best_post_types": "CS-INV-01 (OBO Token Exchange), CS-INV-02 (SHACL Policy Gate), IDEA-08",
        "why_join_for_max_visibility": "320K+ CISOs and VPs of InfoSec who gate production enterprise AI rollouts.",
    },
    {
        "group_id": "GRP-20-AI-GOV-OWASP",
        "tier": "Tier 4 — CISO, Zero-Trust AI Security & Governance Networks (190K–2.4M+ Members)",
        "name": "AI Governance, Responsible AI, ISO 42001, EU AI Act & OWASP GenAI Security",
        "direct_group_url": "https://www.linkedin.com/groups/12854310/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=AI%20Governance%20Responsible%20AI%20Security",
        "members": "215,000+",
        "members_num": 215000,
        "visibility_score": 97.6,
        "unjoined_probability": "HIGH (93%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "DAILY-06 CISO/FinOps Checklist, POST-05, IDEA-07 (Cryptographic Audit Receipts)",
        "why_join_for_max_visibility": "215K+ AI Governance & Compliance leaders looking for SOC2 / ISO-42001 policy trace architectures.",
    },
    {
        "group_id": "GRP-21-CSA-ZERO-TRUST",
        "tier": "Tier 4 — CISO, Zero-Trust AI Security & Governance Networks (190K–2.4M+ Members)",
        "name": "Cloud Security Alliance (CSA) — Zero Trust & AI Security Working Group",
        "direct_group_url": "https://www.linkedin.com/groups/1864210/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Cloud%20Security%20Alliance%20CSA",
        "members": "190,000+",
        "members_num": 190000,
        "visibility_score": 97.4,
        "unjoined_probability": "HIGH (90%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "MINT-01, IDEA-08, POST-05",
        "why_join_for_max_visibility": "190K+ Cloud Security Architects standardizing Zero-Trust AI control planes.",
    },

    # Tier 5: C-Suite (CIO/CTO/CAIO) & Chief Customer Officer / FinOps Value Realization Groups
    {
        "group_id": "GRP-22-CIO-CTO-NETWORK",
        "tier": "Tier 5 — C-Suite (CIO / CTO / CAIO / CCO) & FinOps Value Realization Networks",
        "name": "Chief Information Officer (CIO) & Chief Technology Officer (CTO) Network",
        "direct_group_url": "https://www.linkedin.com/groups/58053/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Chief%20Information%20Officer%20CIO%20CTO",
        "members": "780,000+",
        "members_num": 780000,
        "visibility_score": 98.8,
        "unjoined_probability": "HIGH (85%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Moderated",
        "best_post_types": "24-Slide Executive Briefing Decks, T56 Shadow AI, T57 Raw API vs. Vertex AI Agent Engine",
        "why_join_for_max_visibility": "780K+ CIOs and CTOs making platform-level buy vs. build decisions.",
    },
    {
        "group_id": "GRP-23-CDO-CAIO-LEADERS",
        "tier": "Tier 5 — C-Suite (CIO / CTO / CAIO / CCO) & FinOps Value Realization Networks",
        "name": "Chief Data Officer (CDO), Chief AI Officer (CAIO) & Enterprise AI Strategy Leaders",
        "direct_group_url": "https://www.linkedin.com/groups/4321890/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Chief%20Data%20Officer%20Chief%20AI%20Officer",
        "members": "240,000+",
        "members_num": 240000,
        "visibility_score": 98.1,
        "unjoined_probability": "HIGH (89%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "Customer Success Inventions (`CS-INV-01`..`06`), Executive Playbook Carousels",
        "why_join_for_max_visibility": "240K+ CAIOs and CDOs sponsoring enterprise agentic transformation programs.",
    },
    {
        "group_id": "GRP-24-CCO-CUSTOMER-SUCCESS",
        "tier": "Tier 5 — C-Suite (CIO / CTO / CAIO / CCO) & FinOps Value Realization Networks",
        "name": "Chief Customer Officer (CCO), VP Customer Success & Enterprise Value Realization",
        "direct_group_url": "https://www.linkedin.com/groups/4510921/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=Chief%20Customer%20Officer%20Customer%20Success",
        "members": "180,000+",
        "members_num": 180000,
        "visibility_score": 97.9,
        "unjoined_probability": "HIGH (93% — Customer Success executive vertical)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "Customer Success Agentic Inventions Radar (`CS-INV-01`..`06`: NRR expansion, MTTR reduction)",
        "why_join_for_max_visibility": "180K+ Customer Success & Value Realization executives looking for AI playbooks that cut customer onboarding & ticket escalations.",
    },
    {
        "group_id": "GRP-25-FINOPS-AI-ECONOMICS",
        "tier": "Tier 5 — C-Suite (CIO / CTO / CAIO / CCO) & FinOps Value Realization Networks",
        "name": "FinOps Foundation & Enterprise Cloud / AI Token Economics Leaders",
        "direct_group_url": "https://www.linkedin.com/groups/12640219/",
        "linkedin_search_url": "https://www.linkedin.com/search/results/groups/?keywords=FinOps%20Cloud%20Financial%20Management%20AI",
        "members": "155,000+",
        "members_num": 155000,
        "visibility_score": 97.7,
        "unjoined_probability": "HIGH (91%)",
        "default_status": "NOT_JOINED_YET",
        "moderation_speed": "Fast",
        "best_post_types": "MINT-01 (-82.1% tokens), IDEA-01 ($400 loop breaker), IDEA-02 ($11.76 -> $0.59 / 1K workflows)",
        "why_join_for_max_visibility": "155K+ FinOps practitioners who immediately share posts quantifying token & $/1K workflow savings.",
    },
]


def get_or_update_linkedin_group_membership_radar(
    toggle_group_id: str = "",
    new_status: str = "",
    pasted_my_groups_text: str = "",
) -> Dict[str, Any]:
    """Load, diff (from pasted `linkedin.com/groups` text), or toggle membership status across the Top 25 groups."""
    ledger: Dict[str, str] = {}
    if GROUP_MEMBERSHIP_LEDGER_PATH.exists():
        try:
            ledger = json.loads(GROUP_MEMBERSHIP_LEDGER_PATH.read_text(encoding="utf-8")).get("statuses", {})
        except Exception:
            ledger = {}

    if toggle_group_id and new_status in ("JOINED", "PENDING_APPROVAL", "NOT_JOINED_YET"):
        ledger[toggle_group_id] = new_status

    auto_matched_ids: List[str] = []
    if pasted_my_groups_text and pasted_my_groups_text.strip():
        raw_low = pasted_my_groups_text.lower()
        for g in TOP_25_AGENTIC_AI_VISIBILITY_GROUPS:
            gid = g["group_id"]
            num_id = g["direct_group_url"].rstrip("/").split("/")[-1]
            name_low = g["name"].lower()
            # Match by numeric group URL ID or significant title substring
            title_head = name_low.split("(")[0].split("—")[0].strip()
            if (num_id and f"/groups/{num_id}" in raw_low) or (len(title_head) >= 12 and title_head in raw_low):
                ledger[gid] = "JOINED"
                auto_matched_ids.append(gid)

    GROUP_MEMBERSHIP_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    GROUP_MEMBERSHIP_LEDGER_PATH.write_text(
        json.dumps({"statuses": ledger}, indent=2),
        encoding="utf-8",
    )

    enriched_groups: List[Dict[str, Any]] = []
    unjoined_groups: List[Dict[str, Any]] = []
    joined_count = 0
    pending_count = 0
    unjoined_reach_total = 0

    for g in TOP_25_AGENTIC_AI_VISIBILITY_GROUPS:
        item = dict(g)
        st = ledger.get(g["group_id"], g["default_status"])
        item["membership_status"] = st
        enriched_groups.append(item)
        if st == "JOINED":
            joined_count += 1
        elif st == "PENDING_APPROVAL":
            pending_count += 1
        else:
            unjoined_groups.append(item)
            unjoined_reach_total += int(g["members_num"])

    return {
        "status": "READY",
        "total_catalog_groups": len(enriched_groups),
        "joined_count": joined_count,
        "pending_count": pending_count,
        "unjoined_count": len(unjoined_groups),
        "unjoined_combined_member_reach": f"{unjoined_reach_total:,}+",
        "auto_matched_from_paste": auto_matched_ids,
        "privacy_note": (
            "LinkedIn hides a member's joined groups behind authenticated session cookies (`https://www.linkedin.com/groups/`). "
            "Paste the text of your `linkedin.com/groups/` page or click any status pill to mark groups you already belong to."
        ),
        "groups": enriched_groups,
        "unjoined_priority_queue": sorted(unjoined_groups, key=lambda x: x["visibility_score"], reverse=True),
    }
