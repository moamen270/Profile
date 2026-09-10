# Moamen Moustafa Basyoni

**Senior .NET Developer | Distributed Backend & AI-Integrated Systems**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend engineer with around three years building enterprise .NET systems — designing REST and gRPC APIs from specification, operating resilient distributed services with asynchronous messaging (RabbitMQ) and Temporal Saga orchestration, and modernizing legacy modules onto contemporary .NET (8/9/10) with Clean Architecture and SOLID. Strong in C#, ASP.NET Core, Entity Framework Core over SQL Server and PostgreSQL, OAuth2 / OpenID Connect / JWT, and asynchronous and concurrent programming. Builds AI-integrated backend tooling: internal Model Context Protocol (MCP) servers, automated code-review pipelines, and multi-model LLM orchestration. Runs technical code reviews and mentors engineers.

---

## Professional Experience

### .NET Backend Engineer — Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

- Build enterprise backend systems on modern .NET (8/9/10) for the Andalusia hospital group across Egypt and Saudi Arabia, designing REST and gRPC API contracts before implementation.
- Create resilient distributed services with fault-tolerant asynchronous messaging (RabbitMQ) and long-running distributed transactions via Temporal Saga orchestration, improving 10+ inter-service interaction patterns.
- Integrate legacy systems with modern platforms — migrated modules from .NET Framework 4.5 / ASP.NET Core 2.2 toward modern .NET with Clean Architecture and SOLID across 5 core and 7+ additional modules.
- Design efficient data access with Entity Framework Core and LINQ over SQL Server and PostgreSQL.
- Built a runtime Business Rule Engine for injected business logic, improving rule-execution performance by 45% (measured with BenchmarkDotNet).
- Implemented an identity/authentication server with OpenID Connect and OAuth2 (OpenIddict), JWT access/refresh tokens, and scope- and claim-based authorization.
- Built internal Model Context Protocol (MCP) servers, automated code-review / pull-request analysis tooling, and multi-model LLM orchestration (OpenAI, OpenRouter) with observability (LangSmith, LangFuse), guardrails, token budgeting, and cost optimization.
- Conduct technical code reviews and mentor engineers; led an 8-session onboarding program reaching 25 engineers across 6 teams.

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
- **.NET & Backend:** ASP.NET Core, Minimal APIs, ASP.NET Core MVC, .NET 8/9/10, .NET Aspire, Entity Framework Core, LINQ, REST APIs, gRPC, Webhooks
- **Architecture & Practices:** Clean Code, SOLID, Design Patterns, Clean Architecture, Microservices, Service-Oriented Architecture, Saga orchestration, spec-first API design, technical code review
- **Distributed Systems & Messaging:** RabbitMQ, Temporal, Consul (service discovery, health checks, KV), event-driven architecture, asynchronous & concurrent programming (async/await)
- **Databases:** SQL Server, PostgreSQL, Neo4j, Elasticsearch
- **Identity & Security:** OpenID Connect (OIDC), OAuth2, OpenIddict, JSON Web Tokens (JWT), OWASP-aware secure coding, scope- and claim-based authorization
- **Observability:** LangSmith, LangFuse, prompt telemetry, token & cost monitoring
- **Testing & Performance:** pytest, pytest-asyncio, automated testing, BenchmarkDotNet, performance tuning
- **DevOps:** Docker, Azure DevOps (CI/CD), GitHub Actions, Git, Git Flow
- **AI Engineering:** Model Context Protocol (MCP), LangGraph, CrewAI, RAG, GraphRAG, multi-model orchestration (OpenAI, OpenRouter), prompt engineering, guardrails, human-in-the-loop

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

**Overall fit: ~75%.** Rare positive: their preferred quals explicitly name **MCP + prompt engineering**, which almost no other .NET applicant will have. The risk is the "5+ years / expert-level" framing.

| Gap | Severity | Plan |
|---|---|---|
| **5+ years + "expert-level" C#/ASP.NET Core** vs ~3 | High | Not closable. Counter with depth artifacts: identity server, Saga orchestration, rule engine (45%), API gateway (2h→15m). Let the cover note say "~3 years, but here's the scope." Recruiter may still filter — accept that risk. |
| **Dapper** | Low | You use EF Core + LINQ. Dapper is a half-day to learn; build a small repo comparing Dapper vs EF Core query perf and link it. |
| **OpenTelemetry for .NET** + Serilog | Medium | You have LLM observability (LangSmith/LangFuse) but not .NET OTel/Serilog specifically. Add Serilog + OpenTelemetry tracing to a sample ASP.NET Core API this week — small, high-signal. |
| **Apache Kafka** | Low-Medium | You have RabbitMQ (transferable). Read Kafka's log/partition/consumer-group model; note RabbitMQ experience. |
| **Domain-Driven Design** (fundamentals) | Low | You do Clean Architecture; read up on aggregates/bounded contexts/ubiquitous language so you can speak DDD vocabulary. |
| **Kubernetes** (preferred) | Low | Docker + Consul + Nginx gateway experience; optional local k8s demo. |
| Native AOT (preferred) | Very low | One paragraph of reading; publish an AOT console app if time. |

**Cover-note angle:** open with the MCP servers, automated code review, and multi-model orchestration — position yourself as the .NET engineer who already builds the AI tooling they list as "nice to have." Then the resilient-distributed-systems work (RabbitMQ + Temporal Saga). Be upfront about ~3 years.
