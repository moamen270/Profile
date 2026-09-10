# Moamen Moustafa Basyoni

**Senior .NET Backend Developer | Monolith-to-Microservices, APIs & Distributed Systems**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend engineer with around three years maintaining and modernizing .NET services on a large enterprise codebase — decomposing a monolithic architecture into distributed services, designing API contracts and database boundaries, and keeping production systems healthy. Strong in C# with modern async patterns, .NET 8+, Entity Framework Core over PostgreSQL and SQL Server, and xUnit testing. Security-focused: built an OpenID Connect / OAuth2 identity server with JWT, applied OWASP-aware secure coding, and implemented PII masking. Runs CI/CD in Azure DevOps and builds event-driven communication with RabbitMQ behind a Consul-backed API gateway.

---

## Professional Experience

### .NET Backend Engineer — Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

- Contribute to an ongoing monolith-to-modern-architecture migration for the Andalusia hospital group (Egypt and Saudi Arabia) — decomposing legacy .NET Framework 4.5 / ASP.NET Core 2.2 modules into distributed services with Clean Architecture across 5 core and 7+ additional modules.
- Collaborate on architectural decisions: REST and gRPC API design, service and database boundaries, and inter-service communication patterns (improved 10+).
- Maintain and enhance backend services on modern .NET (8/9/10), writing clean, testable C# with async/await throughout for I/O-bound workloads.
- Design data access with Entity Framework Core over SQL Server and PostgreSQL.
- Build event-driven communication with RabbitMQ and long-running distributed transactions with Temporal Saga orchestration.
- Implemented an API gateway (Nginx) with Consul service discovery, health-aware load balancing, and parallel service versioning — cutting deployment downtime from 2 hours to 15 minutes.
- Implemented an OpenID Connect / OAuth2 identity server (OpenIddict) with JWT access and refresh tokens and scope- and claim-based authorization.
- Built a runtime business-rule engine, improving rule-execution performance by 45% (BenchmarkDotNet); troubleshoot production issues and optimize performance.
- Deliver CI/CD pipelines in Azure DevOps with multi-repository Git Flow and Docker across Dev, Staging, and Pre-Live environments.

### Backend Engineer — Trastain
**Feb 2025 – Aug 2025 · Cairo, Egypt (Remote) · Part-time · PropTech marketplace**

- Built a multi-feature marketplace backend from scratch — booking, policy enforcement, preference matching — with Stripe and Paymob payment integration (webhooks, HMAC verification).
- Automated build and deployment with GitHub Actions CI/CD to Azure Web Apps and Azure Static Web Apps.

### Software Engineer — MYM (Make Your Miracle)
**Jun 2023 – Oct 2023 · Giza, Egypt · SaaS / e-commerce / booking**

- Developed backend systems for e-commerce and booking platforms end-to-end; integrated payment gateways with webhook handling; deployed to Azure App Service.

---

## Technical Skills

- **Languages:** C#, SQL, Python, JavaScript, TypeScript
- **.NET & Backend:** .NET 8/9/10, ASP.NET Core, Minimal APIs, ASP.NET Core MVC, Entity Framework Core, modern async/await, REST APIs, gRPC
- **Architecture:** monolith-to-microservices decomposition, Clean Architecture, SOLID, Service-Oriented Architecture, Saga orchestration, API Gateway, event-driven architecture
- **Messaging & Distributed Systems:** RabbitMQ, Temporal, Consul (service discovery, health checks, KV)
- **Databases:** PostgreSQL, SQL Server, Neo4j
- **Security:** OpenID Connect (OIDC), OAuth2, OpenIddict, JSON Web Tokens (JWT), scope- and claim-based authorization, OWASP-aware secure coding
- **Testing & Performance:** xUnit, pytest, automated testing, BenchmarkDotNet, performance tuning
- **DevOps:** Azure DevOps (CI/CD pipelines), GitHub Actions, Git, Git Flow, Docker
- **AI-Assisted Development:** Claude Code, GitHub Copilot, Model Context Protocol (MCP)

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

**Overall fit: ~75%.** The monolith-to-microservices migration is the exact work Moamen is doing at AHBS — that's the headline match.

| Gap | Severity | Plan |
|---|---|---|
| **5+ years** vs ~3 | Medium | Offset with the direct migration parallel + API gateway (2h→15m) + identity server. |
| **Dapper** | Low | Uses EF Core. Half a day to learn; a small Dapper-vs-EF perf repo would cover it. |
| **Kafka** | Low | Has RabbitMQ (concept transfers). Read Kafka's partition/consumer-group model. |
| **Dapr** | Low-Medium | No Dapr. It sits on concepts Moamen knows (service invocation, pub/sub, state, secrets). Run the Dapr quickstarts locally; mention Consul + RabbitMQ as the equivalent building blocks he's used. |
| **Firebase auth** | Low | Has done OIDC/OAuth2/JWT deeply; Firebase Auth is a specific provider — quick to pick up. |

**Cover-note angle:** the migration parallel is unusually strong — open with it. Then messaging + API gateway + identity. Be honest about ~3 years; Dapr/Dapper/Kafka are all short ramps.
