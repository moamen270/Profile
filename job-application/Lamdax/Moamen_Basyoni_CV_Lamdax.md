# Moamen Moustafa Basyoni

**Backend Developer | .NET Core, Distributed Systems & Identity**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend engineer building production .NET Core services around exactly the problem set this role describes: microservices, event-driven communication, and authentication/authorization infrastructure. Designed and built an OIDC/OAuth2 identity server on OpenIddict with JWT access/refresh tokens — the same identity stack named in this posting — plus RabbitMQ-based event-driven communication and a Temporal Saga replacement for a legacy distributed-transaction design. Roughly three years of production experience against the six asked for here; the scope of that work is what I'd ask to be judged on.

---

## Professional Experience

### R&D Engineer — Backend, Distributed Systems & AI Engineering
**Andalusia Health Business Solution (AHBS)** · Alexandria, Egypt · Dec 2023 – Present

- Designed and built an **identity/authentication server** using **OpenIddict**, issuing **JWT access and refresh tokens** with scope-based and claim-based authorization — the same identity technology named in this role's stack.
- Implemented **event-driven communication with RabbitMQ**, and replaced a legacy MS DTC distributed-transaction workaround with **Temporal Saga orchestration**, improving 10+ inter-service interaction patterns.
- Built and maintain services in **C#, ASP.NET Core (.NET 8/9/10)** with **Entity Framework Core** over **SQL Server** and PostgreSQL, applying **Clean Architecture** and SOLID principles.
- Built a **Consul**-based service discovery layer and an **Nginx API gateway** with parallel service versioning, cutting deployment downtime from 2 hours to 15 minutes (87.5%).
- Optimized a runtime business-rule engine to a **45%** performance improvement, measured with BenchmarkDotNet — direct evidence of high-throughput service tuning.
- Modernized 5 core + 7 additional modules off legacy .NET Framework 4.5, working inside a large, mature distributed codebase.
- Migrated source control from a TFVC monolith to Azure DevOps Git multi-repo; established CI/CD pipelines across Dev, Staging and Pre-Live.

### Technical Partner (equity) — Trastain
**Cairo, Egypt (Remote)** · Feb 2025 – Aug 2025

- Built a booking platform from scratch, including transaction security work for booking execution and payment webhook processing with HMAC signature verification.

### Software Engineer — MYM (Make Your Miracle)
**Giza, Egypt** · Jun 2023 – Oct 2023

- Built backend systems for e-commerce and booking platforms, delivered end to end.

---

## Technical Skills

- **Languages:** C#, Python, SQL, TypeScript, JavaScript
- **.NET / Backend:** C#, .NET Core, .NET 8/9/10, ASP.NET Core, Entity Framework Core, gRPC, REST APIs
- **Databases:** SQL Server, PostgreSQL
- **Distributed Systems & Messaging:** Temporal (Saga orchestration), **RabbitMQ** (event-driven / pub-sub), gRPC, MassTransit
- **Identity & Security:** **OpenIddict**, **JWT** (access/refresh tokens), OAuth2, OpenID Connect, scope- and claim-based authorization
- **Architecture:** Clean Architecture, Microservices, Distributed Systems, SOLID, Business Rule Engines
- **Service Discovery & Gateway:** Consul, Nginx API Gateway, dynamic routing, load balancing
- **Performance:** BenchmarkDotNet, high-throughput service tuning, async/await concurrency
- **DevOps & Version Control:** Git, Azure DevOps Pipelines, GitHub Actions, CI/CD automation, Docker
- **Cloud:** Azure (App Service, Blob Storage, SQL, DevOps), AWS (EC2, S3)
- **AI-Assisted Development:** Claude Code, GitHub Copilot

---

## Education

**B.Sc. Computer Engineering** — Behera Higher Institute (BHI), Alexandria, Egypt · 2023
Grade: B+ · GPA 3.2 / 4.0

## Publication & Languages

- *IoT-Enabled E-Prescription Management and Dispensing Machine Monitoring* — IEEE, 2024
- Arabic (Native) · English (B2, Upper Intermediate)

---
---

## ⚠️ NOT PART OF CV — Gaps and fit notes

**Overall fit: ~72%, weighted down almost entirely by one hard number.** The technical overlap is unusually precise — this is a reach application, not a comfortable one.

| Gap | Severity | Note |
|---|---|---|
| **6+ years hands-on .NET Core/C#; he's at ~3** | **High — the real risk** | Not closable, not fudgeable. This is a harder bar than any other role in the pipeline (most ask 3-8). Countered the only honest way available: naming the exact identity/messaging stack overlap (OpenIddict, JWT, RabbitMQ) as evidence the *depth* is there even if the *years* aren't. Expect this to be a hard screen at some companies and a non-issue at others — worth trying given how rare the stack match is. |
| **Event sourcing** | Medium | JD asks for "pub/sub, event sourcing" as a pair. He has pub/sub (RabbitMQ) solidly; event sourcing specifically (event store as source of truth, replay) isn't documented — Saga orchestration is adjacent (both deal with distributed state over time) but isn't the same pattern. Don't claim it; be ready to discuss the distinction. |
| **Kafka** | Low-Medium | Already tracked in `gaps.md` — RabbitMQ is the transferable base. |
| **Azure Service Bus** | Low | Has RabbitMQ, not Azure Service Bus specifically — same messaging concepts, different product. |
| **Contractor, not permanent** | Decision, not a gap | Matches the "biggest financial lever" logic already applied to Crossing Hurdles. No rate stated — ask early. |

### Selling-point map
- **What the company needs:** 6+ yrs .NET Core/C#, deep microservices/distributed-systems expertise, event-driven architecture, EF Core + SQL Server, auth frameworks (JWT/OAuth2/OIDC), SOLID, high-throughput optimization.
- **Lead selling point(s):** the identity/auth stack is a near-literal match — **OpenIddict and JWT are named in the JD and are things he actually built**, not adjacent technologies. This is the rare case where the exact product names line up, not just the category.
- **Supporting:** Temporal Saga (distributed-systems depth beyond the JD's own ask), RabbitMQ event-driven work, quantified performance wins (45%, 87.5%).
- **Deliberately NOT emphasized:** AI/agentic work — off-message for a pure backend infrastructure role.
- **What makes this CV different here:** most applicants who clear the 6-year bar won't have this specific an identity-stack match; most applicants with this stack match won't clear 6 years. He's betting the specificity of the match outweighs the years gap.
