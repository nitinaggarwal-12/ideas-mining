"""Open-Source + Google Cloud Stack Pairings.

Single source of truth for presenting every Google Cloud service side by side with its open-source equivalent across
the Top 10 ideas, the 8 analyzed posts, the dynamic moving-arrow diagrams, the 20 template gallery, READMEs, and the Studio UI.

Accuracy notes (verified facts, no marketing claims):
- Google ADK (google/adk-python) is itself open source under Apache-2.0; OpenHands is MIT-licensed.
- Agent2Agent (A2A) was announced by Google in April 2025 and contributed to the Linux Foundation in June 2025.
- Model Context Protocol (MCP) is an open specification with open-source SDKs (announced Nov 2024).
- Cloud Run is built on Knative; gVisor (Cloud Run / GKE Sandbox isolation) is Google open source.
- OpenTofu is the open-source fork of Terraform (Terraform moved to the BSL license in 2023).
"""

from typing import Any, Dict, List, Optional


OSS_GOOGLE_PAIRINGS: List[Dict[str, str]] = [
    {
        "capability": "Agent orchestration & harness loop",
        "google": "Google Cloud ADK (google/adk-python, Apache-2.0) • Vertex AI Agent Engine",
        "oss": "LangGraph • CrewAI • Microsoft AutoGen • OpenAI Agents SDK • smolagents",
        "note": "ADK is open source itself; the loop guards map 1:1 to LangGraph recursion_limit, CrewAI max_iter, AutoGen max_turns, OpenHands max_iterations.",
    },
    {
        "capability": "Frontier & open-weight models",
        "google": "Vertex AI Gemini 4 Argon / Gemini 3.8 Flash (locations/global)",
        "oss": "Gemma 3 • Llama 3.x • Qwen served by vLLM / Ollama / SGLang behind LiteLLM",
        "note": "Keep the Flash/Argon tiering logic identical when routing sensitive or offline steps to open weights.",
    },
    {
        "capability": "Prompt-injection & content safety",
        "google": "Google Cloud Model Armor • Cloud DLP",
        "oss": "Llama Guard / Prompt Guard • NVIDIA NeMo Guardrails • Rebuff • LLM Guard",
        "note": "Scan ingress and egress with either; always pair the scanner with deterministic capability downgrading.",
    },
    {
        "capability": "Durable state, checkpoints & idempotency",
        "google": "Cloud Firestore • Cloud Workflows",
        "oss": "PostgreSQL (LangGraph PostgresSaver) • Redis SETNX • Temporal",
        "note": "Idempotency keys belong in a transactional store; Temporal adds durable retries, timers, and workflow IDs.",
    },
    {
        "capability": "Memory & vector retrieval",
        "google": "AlloyDB (pgvector, FORCE RLS) • Vertex AI Vector Search",
        "oss": "PostgreSQL + pgvector • Qdrant • Chroma • Weaviate • Mem0 • Letta • LangMem",
        "note": "Whatever the store, bind every memory claim to a source file + git blob SHA receipt.",
    },
    {
        "capability": "Trajectory warehouse & eval data",
        "google": "BigQuery",
        "oss": "ClickHouse • DuckDB • Apache Parquet on object storage (MinIO)",
        "note": "Keep every step-level trajectory so failures can be replayed as golden fixtures.",
    },
    {
        "capability": "Tracing, metrics & observability",
        "google": "Cloud Trace • Cloud Logging • Cloud Monitoring",
        "oss": "OpenTelemetry • Langfuse • Arize Phoenix • Prometheus + Grafana",
        "note": "OpenTelemetry spans are the common currency; export them to either backend without code changes.",
    },
    {
        "capability": "Sandboxed code execution",
        "google": "Cloud Run (gVisor-isolated) • GKE Sandbox",
        "oss": "OpenHands (MIT) • E2B • gVisor • Firecracker microVMs",
        "note": "Never run agent-written code on the host; gVisor is Google open source and powers both columns.",
    },
    {
        "capability": "Evaluation & regression gates",
        "google": "Vertex AI GenAI Evaluation Service",
        "oss": "Promptfoo • DeepEval • Ragas • Inspect AI",
        "note": "Golden trajectory suites run in CI on Cloud Build or GitHub Actions / Argo Workflows.",
    },
    {
        "capability": "Identity, secrets & tool policy",
        "google": "Cloud IAP • Workload Identity Federation • Cloud KMS",
        "oss": "Keycloak • SPIFFE / SPIRE • HashiCorp Vault / OpenBao • Open Policy Agent (OPA)",
        "note": "Tool permissions are policy decisions made outside the model — OPA or IAM, never prompt text.",
    },
    {
        "capability": "Serving & infrastructure as code",
        "google": "Cloud Run v2 • GKE • Cloud Build • Artifact Registry",
        "oss": "Knative • Kubernetes • GitHub Actions / Argo • Harbor • OpenTofu / Terraform",
        "note": "Cloud Run is built on Knative; OpenTofu is the open-source Terraform fork.",
    },
    {
        "capability": "Agent-to-agent & tool protocols",
        "google": "Agent2Agent (A2A, now Linux Foundation) • ADK A2A server",
        "oss": "Model Context Protocol (MCP) SDKs • A2A Python / JS SDKs • JSON Schema + Pydantic contracts",
        "note": "Both protocols are open specifications; typed contracts always beat prose handoffs.",
    },
]


# Open-source equivalent for each Google Cloud primitive used by the Tomorrow Morning EST Top 10 dynamic steps.
OSS_STEP_EQUIVALENTS: Dict[str, Dict[str, str]] = {
    "IDEA-01": {"01": "LangGraph pre_model_hook", "02": "Redis sliding window (ZADD)", "03": "Gemma 3 via vLLM / LiteLLM", "04": "recursion_limit + max_budget_per_task"},
    "IDEA-02": {"01": "vLLM / SGLang prefix caching", "02": "LangGraph subgraph / CrewAI crew", "03": "MinIO (S3) + PostgreSQL pointers", "04": "LangMem / Letta compaction"},
    "IDEA-03": {"01": "LangGraph conditional edge", "02": "OpenHands (MIT) / E2B sandbox", "03": "Aider / SWE-agent repair loop", "04": "git notes + PostgreSQL receipts"},
    "IDEA-04": {"01": "MCP server registry (open SDK)", "02": "pgvector / Qdrant + BGE embeddings", "03": "LangChain bind_tools per step", "04": "LiteLLM proxy middleware"},
    "IDEA-05": {"01": "PostgreSQL JSONB blackboard", "02": "Pydantic / JSON Schema validator", "03": "OpenHands worker / CrewAI agent", "04": "DeepEval / Promptfoo judge"},
    "IDEA-06": {"01": "Temporal workflow IDs", "02": "Redis SETNX / Postgres UNIQUE", "03": "LangGraph PostgresSaver", "04": "Temporal worker on Kubernetes"},
    "IDEA-07": {"01": "PostgreSQL + git blob SHA", "02": "git rev-parse / libgit2 check", "03": "Mem0 / LangMem metadata flag", "04": "OpenHands + PostgreSQL sync"},
    "IDEA-08": {"01": "Llama Guard / NeMo Guardrails", "02": "LangGraph state taint flag", "03": "Open Policy Agent tool policy", "04": "Keycloak OIDC + HITL approval"},
    "IDEA-09": {"01": "vLLM / SGLang prefix caching", "02": "Gemma 3 on vLLM (LiteLLM route)", "03": "LangGraph Send() map-reduce", "04": "Open-weight 70B via vLLM"},
    "IDEA-10": {"01": "ClickHouse / Parquet fixtures", "02": "DSPy optimizer / open model", "03": "tree-sitter AST + ruff checks", "04": "Promptfoo / Inspect in GitHub Actions"},
}


_KEYWORD_EQUIVALENTS: List[tuple] = [
    (("openhands",), "OpenHands (MIT) + E2B sandbox"),
    (("model armor", "dlp"), "Llama Guard / NeMo Guardrails"),
    (("adk", "agent engine"), "LangGraph / CrewAI / AutoGen"),
    (("gemini", "vertex ai", "vertex"), "Gemma 3 / Llama 3.x on vLLM"),
    (("alloydb", "pgvector", "vector search"), "PostgreSQL + pgvector / Qdrant"),
    (("firestore",), "PostgreSQL / Redis checkpoints"),
    (("bigquery",), "ClickHouse / DuckDB / Parquet"),
    (("cloud trace", "opentelemetry", "logging", "monitoring"), "OpenTelemetry + Langfuse / Phoenix"),
    (("cloud run", "gke"), "Kubernetes / Knative"),
    (("cloud build", "artifact registry"), "GitHub Actions / Argo + Harbor"),
    (("kms", "secret"), "HashiCorp Vault / OpenBao"),
    (("iap", "identity", "wif", "iam"), "Keycloak / SPIFFE-SPIRE / OPA"),
    (("armor", "waf"), "Coraza / ModSecurity WAF"),
    (("workflows", "scheduler"), "Temporal / Argo Workflows"),
    (("evaluation", "eval", "judge"), "Promptfoo / DeepEval / Ragas"),
    (("terraform",), "OpenTofu"),
    (("a2a", "mcp"), "MCP + A2A open SDKs"),
    (("context cach", "kv "), "vLLM / SGLang prefix caching"),
]


def oss_equivalent_for(google_label: Optional[str]) -> str:
    """Return a concise open-source equivalent for a Google Cloud primitive label (keyword-based, deterministic)."""
    text = (google_label or "").lower()
    for keywords, equivalent in _KEYWORD_EQUIVALENTS:
        if any(k in text for k in keywords):
            return equivalent
    return "LangGraph / PostgreSQL / OpenTelemetry"


def oss_step_equivalent(item_id: str, step: str, google_label: Optional[str]) -> str:
    """Resolve the open-source equivalent for a dynamic step: explicit catalog field -> curated table -> keyword fallback."""
    curated = OSS_STEP_EQUIVALENTS.get(item_id, {}).get(str(step))
    return curated or oss_equivalent_for(google_label)


def pairing_rows_markdown() -> str:
    """Markdown table of the 12 Google Cloud <-> open-source pairings for READMEs."""
    rows = ["| Capability | Google Cloud | Open-Source Equivalent | Architecture Note |", "| :--- | :--- | :--- | :--- |"]
    for p in OSS_GOOGLE_PAIRINGS:
        rows.append(f"| **{p['capability']}** | {p['google']} | {p['oss']} | {p['note']} |")
    return "\n".join(rows)


def step_pairing_rows_markdown(item: Dict[str, Any]) -> str:
    """Markdown table pairing each dynamic step's Google Cloud primitive with its open-source equivalent."""
    steps = item.get("dynamic_steps") or []
    if not steps:
        return ""
    rows = ["| Step | Google Cloud Primitive | Open-Source Equivalent |", "| :--- | :--- | :--- |"]
    for st in steps:
        oss = st.get("oss_primitive") or oss_step_equivalent(item["id"], st["step"], st.get("gcp_primitive"))
        rows.append(f"| **{st['badge']}** — {st['title']} | `{st['gcp_primitive']}` | `{oss}` |")
    return "\n".join(rows)
