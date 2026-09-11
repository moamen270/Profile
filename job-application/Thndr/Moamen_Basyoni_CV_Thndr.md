# Moamen Moustafa Basyoni

**Backend Engineer | Distributed Systems, Correctness & Payments**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend engineer with around three years building distributed services in both C# / .NET Core and Python, on a large enterprise platform where correctness under partial failure is the hard requirement. Replaced a legacy distributed-transaction design with Temporal Saga orchestration, built event-driven communication with RabbitMQ, and designed data access over PostgreSQL and SQL Server. Direct payments experience — Stripe and Paymob integration with webhook processing and HMAC signature verification for payment events. Comfortable owning a service end to end: design, implementation, deployment, and production troubleshooting.

---

## Professional Experience

### R&D Engineer — Backend & Distributed Systems · Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

- Replaced a legacy MS DTC distributed-transaction design — which forced the entire system onto a single shared database — with **Temporal Saga orchestration**, giving long-running, recoverable transactions across service boundaries. Improved 10+ inter-service interaction patterns.
- Built event-driven communication with **RabbitMQ**, and designed REST and gRPC API contracts before implementation.
- Designed data access with Entity Framework Core over **SQL Server and PostgreSQL**.
- Built **Python** services with FastAPI (Pydantic v2, async/await, dependency injection) and Flask, with SQLAlchemy 2.0 and Alembic migrations, tested with pytest and pytest-asyncio.
- Implemented an **OpenID Connect / OAuth2 identity server** (OpenIddict) with JWT access and refresh tokens and scope- and claim-based authorization; applied OWASP-aware secure coding and PII masking.
- Implemented service discovery and dynamic routing with Consul behind an Nginx API gateway with health-aware load balancing and parallel service versioning — cutting deployment downtime from 2 hours to 15 minutes.
- Built a runtime Business Rule Engine for injected business logic, improving rule-execution performance by **45%** (measured with BenchmarkDotNet).
- Modernized modules from .NET Framework 4.5 / ASP.NET Core 2.2 toward modern .NET (8/9/10) with Clean Architecture, across 5 core and 7+ additional modules.
- Migrated source control from a legacy TFS/TFVC monolith to Azure DevOps Git multi-repo with a private NuGet feed; delivered CI/CD pipelines across Dev, Staging, and Pre-Live.
- Troubleshoot production issues and performance-tune live services.

### Technical Partner (equity) — Trastain
**Feb 2025 – Aug 2025 · Cairo, Egypt (Remote) · Part-time · PropTech**

- Built a short-term rental booking platform from scratch, including **transaction security for booking execution**.
- Integrated **Stripe and Paymob** payment gateways; implemented **webhook processing with HMAC signature verification** for payment events.
- Developed RAG-based and multimodal AI search (image, location, or natural-language description).
- Automated build and deployment with GitHub Actions CI/CD to Azure Web Apps and Azure Static Web Apps.

### Software Engineer — MYM (Make Your Miracle)
**Jun 2023 – Oct 2023 · Giza, Egypt · Software house — e-commerce & booking**

- Built backend systems for e-commerce and booking platforms (hotel, gym/fitness, and other reservation systems), end to end from requirements through deployment and support.
- Integrated payment gateways (Stripe, Paymob) with webhook handling; deployed to Azure App Service.

---

## Technical Skills

- **Languages:** C#, Python, SQL, JavaScript, TypeScript
- **Backend:** ASP.NET Core, Minimal APIs, .NET 8/9/10, Entity Framework Core, FastAPI, Flask, SQLAlchemy, Pydantic, REST APIs, gRPC, Webhooks
- **Distributed Systems:** Temporal (Saga orchestration), RabbitMQ, MassTransit, Consul (service discovery, health checks, KV), API gateway, event-driven architecture, async/await concurrency
- **Databases:** PostgreSQL, SQL Server, Neo4j
- **Payments & Integrations:** Stripe, Paymob, webhook processing, HMAC signature verification, third-party API integration
- **Security:** OpenID Connect (OIDC), OAuth2, OpenIddict, JWT, scope- and claim-based authorization, OWASP-aware coding, PII masking
- **Cloud & DevOps:** Azure (App Service, Blob, SQL, Static Web Apps), AWS (EC2, S3), Docker, Azure DevOps CI/CD, GitHub Actions, Git
- **Testing & Performance:** pytest, pytest-asyncio, xUnit, BenchmarkDotNet, performance tuning
- **AI Engineering:** Model Context Protocol (MCP), LangGraph, CrewAI, RAG, GraphRAG, multi-model orchestration (OpenAI, OpenRouter)

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

**Overall fit: ~82% — the strongest match in the current pipeline.**

| Gap | Severity | Note |
|---|---|---|
| **"Senior" in the title** vs ~3 years IC | Medium | Not claimable. The Saga/DTC migration, identity server, and gateway work are the counterweight — that is senior-scope work. Expect the years question. |
| **Redis** | Low | Not claimed. Has RabbitMQ and Consul KV; Redis is a short ramp. Read up on its use for caching, locks and idempotency keys before interview. |
| **Financial systems domain** | Medium | No banking/settlement/reconciliation background. Closest real evidence is Stripe/Paymob integration, webhook + HMAC verification, and transaction security at Trastain. Be honest that the domain is new and the distributed-correctness problem is not. |
| Kubernetes | Low | Not asked here. Not claimed anywhere. |

**Interview prep:** they will probe correctness — idempotency, exactly-once vs at-least-once delivery, reconciliation after partial failure, and compensating transactions. The Temporal Saga work is the right story; be ready to explain *why* the old MS DTC single-database approach failed and what Saga bought.
