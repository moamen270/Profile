# Moamen Moustafa Basyoni

**R&D Engineer — Backend & Distributed Systems**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend engineer with roughly three years of production C#/.NET experience, building RESTful APIs and event-driven, distributed backend services. Currently replacing a legacy distributed-transaction design with Temporal Saga orchestration and building the API gateway and service-discovery layer around it — direct experience with the event-driven and distributed-systems patterns this role values. Also brings hands-on payments integration (Stripe, Paymob, webhook/HMAC verification), which overlaps with fintech-style correctness requirements even though the employer wasn't a fintech itself.

---

## Professional Experience

### R&D Engineer — Backend, Distributed Systems & AI Engineering
**Andalusia Health Business Solution (AHBS)** · Alexandria, Egypt · Dec 2023 – Present

- Build and maintain RESTful APIs and services with **C#, ASP.NET Core (.NET 8/9/10)** and **Entity Framework Core** over **SQL Server** and PostgreSQL.
- Replaced a legacy MS DTC distributed-transaction workaround with **Temporal Saga orchestration**, improving 10+ inter-service interaction patterns — direct experience with distributed, event-driven correctness problems.
- Implemented **event-driven communication with RabbitMQ**, a **Consul**-based service-discovery layer, and an **Nginx API gateway** with parallel service versioning, cutting deployment downtime from 2 hours to 15 minutes (87.5%).
- Designed and built an **OIDC/OAuth2 identity server** (OpenIddict, JWT, scope/claim-based authorization).
- Modernized 5 core + 7 additional modules off legacy .NET Framework 4.5, applying Clean Architecture and modern coding standards.
- Test coverage with **xUnit**; a runtime business-rule engine benchmarked to a 45% performance improvement with BenchmarkDotNet.
- Migrated source control from a TFVC monolith to **Azure DevOps Git multi-repo**; established CI/CD pipelines across Dev, Staging and Pre-Live.

### Technical Partner (equity) — Trastain
**Cairo, Egypt (Remote)** · Feb 2025 – Aug 2025

- Integrated **Stripe and Paymob** payment gateways for booking transactions, with webhook processing and **HMAC signature verification** — direct payments/fintech-adjacent integration experience.
- Handled transaction security for booking execution on a platform built from scratch.

### Software Engineer — MYM (Make Your Miracle)
**Giza, Egypt** · Jun 2023 – Oct 2023

- Built backend systems for e-commerce and booking platforms, delivered end to end.

### Freelance / Independent Client Work

- Integrated Stripe/Paymob payments with webhook/HMAC verification; delivered on both Azure and AWS depending on project needs.

---

## Technical Skills

- **Languages:** C#, Python, SQL, TypeScript, JavaScript
- **.NET / Backend:** C#, .NET Core, .NET 6+/8/9/10, ASP.NET Core, Entity Framework Core, RESTful APIs, gRPC
- **Databases:** SQL Server, PostgreSQL
- **Distributed Systems & Messaging:** Temporal (Saga orchestration), RabbitMQ, MassTransit, gRPC, event-driven architecture
- **Architecture:** Clean Architecture, Microservices, Service-Oriented Architecture, Distributed Systems
- **Service Discovery & Gateway:** Consul, Nginx API Gateway, dynamic routing, load balancing
- **Identity & Security:** OpenID Connect, OAuth2, OpenIddict, JWT, scope/claim-based authorization
- **Payments & Integrations:** Stripe, Paymob, webhook processing, HMAC signature verification
- **Testing:** xUnit, BenchmarkDotNet, pytest
- **Cloud:** Azure (App Service, Blob Storage, SQL, DevOps) and AWS (EC2, S3) — basic-to-solid exposure on both
- **DevOps & Version Control:** Git, Azure DevOps Pipelines, GitHub Actions, CI/CD automation, Docker
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

**Overall fit: ~85%.** Strong match — every required item is a direct hit, and two of the three preferred signals (event-driven/microservices/distributed systems) are his strongest documented work.

| Gap | Severity | Note |
|---|---|---|
| **"Fintech industry background" (preferred)** | Minor | He hasn't worked *at* a fintech company, but has built real payments integrations (Stripe, Paymob, webhook/HMAC) — framed honestly as adjacent experience, not fintech employment, in the cover letter. |
| **NSubstitute, Fluent Assertions** | Minor | Not documented — he has xUnit (a direct hit on the same preferred line) but hasn't used these two specific libraries by name. Don't claim them; they're easy to pick up if it comes up. |
| **3–7 years asked; he's at ~3** | None | Within range, at the low end — normal for a wide band. |
| **Location: Dubai, work model unstated** | Decision, not a gap | Matches the widened Gulf search. Confirm onsite/hybrid/remote and visa sponsorship at screening — neither is stated in the posting. |

### Selling-point map
- **What the company needs:** 3–7 yrs backend — C#/.NET Core, REST APIs, EF, SQL. Preferred: fintech background, xUnit-family testing, event-driven/microservices/distributed systems.
- **Lead selling point(s):** distributed-systems/event-driven architecture (Saga, RabbitMQ, Consul, API gateway) — this is the strongest, most specific preferred signal and it's a direct, deep match.
- **Supporting:** payments integration (adjacent to "fintech industry"), xUnit testing, dual-cloud exposure.
- **Deliberately NOT emphasized:** AI/agentic engineering, frontend — not asked for.
- **What makes this CV different here:** most 3–7 yr backend candidates will have REST/EF/SQL; few will have actually replaced a production distributed-transaction system with Saga orchestration, which is exactly what "event-driven architectures... distributed systems" is gesturing at in the abstract.
