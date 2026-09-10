# Moamen Moustafa Basyoni

**Senior Backend Developer | .NET, APIs & AI-Integrated Systems**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend developer with around three years building and maintaining backend systems and web applications on C#, ASP.NET Core (including MVC), and modern .NET, with strong REST API design, third-party API and platform integrations, SOLID principles, and OWASP-aware secure coding. Daily user of AI development tools (Claude Code, GitHub Copilot) and a builder of AI-integrated backends: LLM API integration and multi-model orchestration (OpenAI, OpenRouter), retrieval-augmented generation (RAG and GraphRAG), agent workflows with LangGraph and CrewAI, and internal Model Context Protocol (MCP) servers. Contributes to architecture decisions and mentors engineers.

---

## Professional Experience

### Senior Backend Developer — Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

- Develop and maintain backend systems and web applications on C#, ASP.NET Core and ASP.NET Core MVC for the Andalusia hospital group across Egypt and Saudi Arabia.
- Design and implement REST APIs and services across distributed modules; build integrations with third-party platforms and APIs (Microsoft Graph / SharePoint, payment providers).
- Participate in architecture and technical design decisions; modernized legacy modules onto modern .NET with Clean Architecture across 5 core and 7+ additional modules.
- Apply SOLID and OWASP-aware secure coding; implemented an OpenID Connect / OAuth2 identity server (OpenIddict) with JWT and scope-/claim-based authorization.
- Build AI-integrated backend tooling: LLM API integration and multi-model orchestration (OpenAI, OpenRouter), RAG and GraphRAG systems (Neo4j), LangGraph and CrewAI agent workflows, internal MCP servers, and automated code-review pipelines — with observability (LangSmith, LangFuse), guardrails, and cost optimization.
- Deliver with Docker and CI/CD (Azure DevOps); mentor engineers through an 8-session onboarding program reaching 25 engineers across 6 teams.

### Backend Engineer — Trastain
**Feb 2025 – Aug 2025 · Cairo, Egypt (Remote) · Part-time · PropTech marketplace**

- Built a PropTech marketplace backend from scratch with booking, policy enforcement, and RAG-based preference matching.
- Integrated Stripe and Paymob payment gateways with webhook processing and HMAC signature verification.
- Automated build and deployment with GitHub Actions CI/CD to Azure Web Apps and Azure Static Web Apps.

### Software Engineer — MYM (Make Your Miracle)
**Jun 2023 – Oct 2023 · Giza, Egypt · SaaS / e-commerce / booking**

- Developed backend systems for e-commerce and booking platforms end-to-end; integrated payment gateways with webhook handling; deployed to Azure App Service.

---

## Technical Skills

- **Languages:** C#, SQL, Python, JavaScript, TypeScript
- **.NET & Backend:** ASP.NET Core, ASP.NET Core MVC, Minimal APIs, .NET 8/9/10, Entity Framework Core, REST APIs, gRPC, Webhooks
- **Architecture & Practices:** SOLID, Clean Architecture, Microservices, Service-Oriented Architecture, OWASP-aware secure coding, API design
- **AI Integration:** LLM API integration & multi-model orchestration (OpenAI, OpenRouter), Model Context Protocol (MCP), LangGraph, CrewAI, RAG, GraphRAG, prompt engineering, guardrails, human-in-the-loop; observability with LangSmith and LangFuse
- **AI-Assisted Development:** Claude Code, GitHub Copilot, Codex
- **Databases & Retrieval:** SQL Server, PostgreSQL, Neo4j, Elasticsearch, semantic search / contextual retrieval
- **Identity & Security:** OpenID Connect (OIDC), OAuth2, OpenIddict, JSON Web Tokens (JWT)
- **Messaging & Distributed Systems:** RabbitMQ, Temporal, Consul, event-driven architecture
- **DevOps & Cloud:** Docker, Azure DevOps (CI/CD), GitHub Actions, Git, Azure Web Apps / App Service / Static Web Apps
- **Integrations:** Microsoft Graph APIs, SharePoint, Stripe, Paymob, webhooks, HMAC signature verification

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

**Overall fit: ~70%.** The AI/preferred section is an exceptional match — being "comfortable with Claude / Claude Code" is *required* and you're well past that. Two real gaps: the CMS requirement and the 5-year bar.

| Gap | Severity | Plan |
|---|---|---|
| **Sitecore / Umbraco / Kentico CMS** (required) | High — it's a hard requirement | Zero experience. Umbraco is the fastest on-ramp: it's open-source, ASP.NET Core-based, free to run locally. Spin up an Umbraco site, build a small custom section/API, push it. Even a weekend of this lets you say "built a proof-of-concept Umbraco site" honestly instead of nothing. |
| **5+ years** vs ~3 | Medium | Offset with the AI-integration depth (few candidates have MCP + multi-model orchestration + RAG in production) and architecture work. |
| **Vector databases** (pgvector, Qdrant, Pinecone) — preferred | Low-Medium | You have Elasticsearch + Neo4j + semantic search but not a dedicated vector DB. pgvector is a Postgres extension — add embeddings + similarity search to a sample RAG service this week; you already run Postgres. |
| **Semantic Kernel** (preferred) | Low | You use LangGraph / CrewAI. Read Semantic Kernel's planner/plugin model; it's the .NET-native equivalent — build a tiny SK console agent to have a concrete reference. |
| ASP.NET **MVC** (they say "MVC" not just Core) | Very low | You have ASP.NET Core MVC — fine. If they mean legacy .NET Framework MVC 5, you have .NET Framework 4.5 experience too. |

**Cover-note angle:** lead with the AI-integrated backend work — you are exactly the "backend engineer who is fluent with LLM APIs, agents, and Claude Code" they're describing in the preferred section, and that's rare. Be honest that CMS (Umbraco) would be ramp-up, and mention the POC if you build one.
