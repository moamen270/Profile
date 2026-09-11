# Moamen Moustafa Basyoni

**AI Engineer | Agentic Systems, MCP & RAG in Production**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

R&D engineer building agentic AI systems in production, not prototypes. Designs and ships LLM tooling: five custom Model Context Protocol servers, multi-agent workflows with LangGraph and CrewAI, retrieval-augmented generation and GraphRAG pipelines, and multi-model orchestration across OpenAI and OpenRouter with observability, guardrails, and cost controls. Python backend on FastAPI and Flask with async, Pydantic v2, SQLAlchemy 2.0 and pytest, over PostgreSQL. Uses Claude Code daily as a core part of how work gets delivered, and has built the tooling that lets a whole engineering organization do the same.

---

## Professional Experience

### R&D Engineer — AI & Backend Platform · Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

**Agentic systems & LLM tooling**

- Built **five custom Model Context Protocol (MCP) servers** — Azure DevOps (work items, test plans, suites, cases), Figma, XMind, Playwright, and a database server for schema inspection and read-only querying — and surfaced them to the organization through a custom Azure DevOps extension.
- Developed **multi-agent workflows with LangGraph and CrewAI**, including cyclic agent workflows and tool/function calling.
- Implemented **multi-model orchestration** across OpenAI and OpenRouter, with model selection, rate limiting, token budgeting, and cost optimization; managed the OpenRouter organization (model access, provider configuration, usage monitoring).
- Built **RAG and GraphRAG pipelines** on Neo4j — a policy-retrieval knowledge graph, a code-to-business development knowledge graph, and a PII-masked organizational memory graph — plus semantic search and contextual retrieval.
- **LLM observability** with LangSmith and LangFuse; prompt telemetry, guardrails, prompt-injection mitigation, and human-in-the-loop review.

**AI products**

- **Mail AI assistant** with a chat interface, delivered for C-level and managerial users.
- **Assessment chat** generating multiple-choice and essay quizzes and scoring submitted answers, for the HR and L&D teams.
- **Clinic booking chat** for the Customer Experience team.
- **AI code documentation** combining Roslyn static analysis and code metrics with LLM interpretation.

**AI across the delivery lifecycle**

- AI-assisted requirements analysis and user-story authoring grounded in a business GraphRAG knowledge base; automated story quality scoring and Use Case Point weighting.
- **AI pull-request review** on Azure DevOps — opens threads, posts overall and line-level comments, and checks the implementation against the business requirements in the linked user story.
- Code graph spanning the full application — **38 modules** — for code-to-business traceability.
- AI-supported test generation and Playwright-driven test automation.

**Python & platform engineering**

- Python services with **FastAPI** (Pydantic v2, async/await, dependency injection) and **Flask**, with **SQLAlchemy 2.0** and Alembic migrations over **PostgreSQL** and SQL Server; async HTTP with httpx and asyncio.
- Testing with **pytest and pytest-asyncio**; CI/CD pipelines in Azure DevOps across Dev, Staging, and Pre-Live; Docker.
- OAuth2 / OpenID Connect with JWT for internal service access (FastAPI Security and a .NET identity server).

### Technical Partner (equity) — Trastain
**Feb 2025 – Aug 2025 · Cairo, Egypt (Remote) · Part-time · PropTech**

- Developed **RAG-based property matching** and **multimodal AI search** — image, location, or natural-language description as the query.
- Ran the competitor and market analysis that shaped the product, then built the platform from scratch.
- Deployed via GitHub Actions CI/CD to Azure.

### Software Engineer — MYM (Make Your Miracle)
**Jun 2023 – Oct 2023 · Giza, Egypt**

- Backend systems for e-commerce and booking platforms, delivered end to end.

---

## Technical Skills

- **Languages:** Python, C#, SQL, TypeScript, JavaScript
- **Python:** FastAPI, Flask, SQLAlchemy (Core + ORM 2.0), Pydantic v2, Alembic, asyncio, httpx, aiohttp, pytest, pytest-asyncio, Poetry / uv / pip
- **Agentic AI:** Model Context Protocol (MCP) — five servers built, LangGraph, CrewAI, LangChain, tool/function calling, multi-agent systems, cyclic agent workflows, human-in-the-loop
- **Retrieval:** RAG, GraphRAG, Neo4j, semantic search, contextual retrieval, query expansion, Elasticsearch, multimodal retrieval
- **LLMOps:** LangSmith, LangFuse, prompt telemetry, token usage tracking, cost optimization, model selection, multi-model orchestration (OpenAI, OpenRouter), rate limiting, guardrails, prompt-injection mitigation, PII masking
- **AI-assisted development:** **Claude Code (daily)**, GitHub Copilot, Codex, OpenCode
- **Databases:** PostgreSQL, SQL Server, Neo4j
- **Backend & Infra:** ASP.NET Core, REST, gRPC, RabbitMQ, Temporal, Docker, Azure (App Service, Blob, SQL), AWS (EC2, S3), Azure DevOps CI/CD, GitHub Actions, Git

---

## Education

**B.Sc. Computer Engineering** — Behera Higher Institute (BHI), Alexandria, Egypt · 2023
Grade: B+ · GPA 3.2 / 4.0

## Publication & Languages

- *IoT-Enabled E-Prescription Management and Dispensing Machine Monitoring* — IEEE, 2024
- Arabic (Native) · English (B2, Upper Intermediate)

---
---

## ⚠️ NOT PART OF CV — Gaps to close before applying

**Overall fit: ~75%, and unusually low competition — "be among the first 25 applicants".**

| Gap | Severity | Note |
|---|---|---|
| **4+ years professional *Python*** | High — the one hard filter | Python is ~2 years, alongside C#. Total engineering experience is ~3 years. Not claimable. Counter with the depth and production status of the agentic work, which is what the role is actually about. |
| **pgvector** | Medium | Named explicitly in the JD. Has PostgreSQL, Neo4j, Elasticsearch, semantic search — but **no pgvector project**. Do not claim it. This is a genuine weekend fix: add embeddings + similarity search to a small RAG service on Postgres and it becomes real. |
| **6+ months Claude Code** | None — this is a strength | Daily user, and has built MCP tooling *for* it. Most applicants will not clear this bar. Lead with it. |
| Re-ranking in RAG pipelines | Low | Has ingestion, embeddings, retrieval, contextual retrieval and query expansion. Read up on cross-encoder re-ranking specifically. |

**Recommendation:** build the pgvector sample **before** applying — it is the only gap that is both named in the JD and closable in a day. Then this becomes one of the strongest applications in the pipeline.
