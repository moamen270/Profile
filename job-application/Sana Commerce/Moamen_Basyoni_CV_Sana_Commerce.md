# Moamen Moustafa Basyoni

**AI Engineer | RAG, Agents & LLMOps on Production Backends**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Engineer building LLM systems on production web backends — retrieval-augmented generation and GraphRAG pipelines, multi-agent workflows with LangGraph, CrewAI and LangChain, and five custom Model Context Protocol servers, all running inside a live enterprise platform rather than as prototypes. Operates them properly: LLM observability with LangSmith and LangFuse, multi-model orchestration across OpenAI and OpenRouter with model selection, token budgeting and cost control, plus guardrails, prompt-injection mitigation and PII masking. Backed by three years of backend and system design in ASP.NET Core and Python/FastAPI across Azure and AWS.

---

## Professional Experience

### R&D Engineer — AI & Backend Platform · Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

**Retrieval & agents**

- Built **RAG and GraphRAG pipelines** on Neo4j — a policy-retrieval knowledge graph, a code-to-business development knowledge graph over a 38-module application, and a PII-masked organizational memory graph — with semantic search, contextual retrieval and query expansion, plus Elasticsearch.
- Developed **multi-agent workflows with LangGraph, CrewAI and LangChain**, including cyclic workflows, tool/function calling and human-in-the-loop review.
- Built **five custom Model Context Protocol (MCP) servers** (Azure DevOps, Figma, XMind, Playwright, database), surfaced organization-wide through a custom Azure DevOps extension.
- Developed **multimodal retrieval** — query by image, location or natural-language description (Trastain).

**LLMOps & monitoring**

- **LLM observability with LangSmith and LangFuse**, including prompt telemetry and token usage tracking.
- **Multi-model orchestration** across OpenAI and OpenRouter — model selection, provider configuration, rate limiting, token budgeting and cost optimization; managed the OpenRouter organization.
- AI safety: guardrails, prompt-injection mitigation, human-in-the-loop, PII masking.

**Backend & system design**

- Web backends on **ASP.NET Core** and **Python/FastAPI** (Pydantic v2, async/await, SQLAlchemy 2.0, pytest) over PostgreSQL and SQL Server.
- Distributed system design — Temporal Saga orchestration, RabbitMQ messaging, Consul service discovery, an API gateway that cut deployment downtime from 2 hours to 15 minutes, and REST/gRPC contracts across 10+ improved interaction patterns.
- Modernized 5 core and 7+ additional modules from .NET Framework 4.5 to modern .NET with Clean Architecture.

**Shipped AI products**

- Mail AI assistant (C-level and managerial users); assessment system generating and scoring quizzes for HR and L&D; clinic booking assistant for the CX team; AI code documentation combining Roslyn static analysis with LLM interpretation.

**Cloud**

- **Azure** — App Service, Blob Storage, managed SQL, Static Web Apps, DevOps CI/CD. **AWS** — EC2, S3, messaging services. Evaluated both and chose per project; cut messaging spend by moving off a cloud SMS provider.

### Technical Partner (equity) — Trastain
**Feb 2025 – Aug 2025 · Cairo, Egypt (Remote) · Part-time · PropTech**

- Built the platform from scratch, including **RAG-based matching and multimodal AI search**.
- Ran the competitor and market analysis behind the product.

### Software Engineer — MYM (Make Your Miracle)
**Jun 2023 – Oct 2023 · Giza, Egypt**

- Backend systems for e-commerce and booking platforms, delivered end to end.

---

## Technical Skills

- **AI / LLM:** LangChain, LangGraph, CrewAI, Model Context Protocol (MCP), RAG, GraphRAG, multimodal retrieval, agents, tool/function calling, prompt engineering
- **LLMOps:** LangSmith, LangFuse, prompt telemetry, token usage tracking, cost optimization, model selection, multi-model orchestration (OpenAI, OpenRouter), rate limiting, guardrails, prompt-injection mitigation, PII masking
- **Retrieval & data:** Neo4j, Elasticsearch, PostgreSQL, SQL Server, semantic search, contextual retrieval, query expansion
- **Languages:** Python, C#, SQL, TypeScript, JavaScript
- **Backend:** FastAPI, Flask, SQLAlchemy 2.0, Pydantic v2, pytest, ASP.NET Core, Minimal APIs, REST, gRPC, microservices, Clean Architecture
- **Cloud & DevOps:** AWS (EC2, S3), Azure (App Service, Blob, SQL, Static Web Apps), Docker, Azure DevOps CI/CD, GitHub Actions, Git
- **AI-assisted development:** Claude Code (daily), GitHub Copilot, Codex

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

**Overall fit: ~76% — and it's in Alexandria, which matters.**

| Gap | Severity | Note |
|---|---|---|
| **4+ years web engineering** | Medium-High | ~3 years. Not claimable. The counterweight is that his AI work is production-grade and unusually broad for the level. |
| **AWS Bedrock** | Medium | Named explicitly. He has AWS (EC2, S3) and multi-model orchestration via OpenAI/OpenRouter, but **not Bedrock**. Do not claim it. Read the Bedrock model-access and invocation model before interview — the orchestration concepts transfer directly. |
| **Vector stores** | Medium | Named explicitly. Has Neo4j, Elasticsearch, semantic search and contextual retrieval — but **no dedicated vector store** (pgvector/Qdrant/Pinecone). Same fix as the Mondia application: one pgvector sample closes it for both. |
| MS Foundry / Cloudflare Agents | Low | Niche and unlikely to be a hard filter. Don't claim; mention the equivalent orchestration experience. |

**Note:** the pgvector sample would strengthen **both** this and the Mondia application. Build it once.
