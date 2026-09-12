# Moamen Moustafa Basyoni

**Backend Developer | .NET, Distributed Systems & Cloud**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

Backend .NET engineer with roughly three years of production experience building and modernizing RESTful services, distributed systems, and enterprise database applications in C#, ASP.NET Core, and SQL Server. Works comfortably across both Azure and AWS, with hands-on Docker and CI/CD delivery. Currently modernizing a large healthcare platform: replacing a legacy distributed-transaction design with Temporal Saga orchestration, decomposing a TFVC monolith into Git microservices repositories, and building the identity, API gateway, and service-discovery infrastructure around it. Comfortable relocating for the right role.

---

## Professional Experience

### R&D Engineer — Backend, Distributed Systems & AI Engineering
**Andalusia Health Business Solution (AHBS)** · Alexandria, Egypt · Dec 2023 – Present

- Build and maintain server-rendered and API-driven applications with **ASP.NET Core** (MVC and Minimal APIs) and **Entity Framework Core** over **SQL Server** and PostgreSQL, following **Clean Architecture**.
- Modernized **5 core + 7 additional modules** off legacy .NET Framework 4.5 / ASP.NET Core 2.2, and replaced a custom MS DTC distributed-transaction workaround — which had forced the whole platform onto one shared database — with **Temporal Saga orchestration**, improving 10+ inter-service interaction patterns.
- Designed and built distributed-systems infrastructure: an **OIDC/OAuth2 identity server** (OpenIddict, JWT, scope/claim-based authorization), **Consul**-based service discovery and dynamic routing, and an **Nginx API gateway** with parallel service versioning that cut deployment downtime from 2 hours to 15 minutes (87.5%).
- Migrated source control from a legacy TFVC monolith to **Azure DevOps Git multi-repository** delivery with a private NuGet feed, breaking project-level coupling across services.
- Built a runtime **business-rule engine**, improving execution performance by 45% (measured with BenchmarkDotNet).
- Established **CI/CD pipelines** on Azure DevOps across Dev, Staging and Pre-Live environments; work daily with **Git** and **Docker**.
- Conduct technical code reviews and mentor engineers on architecture and modernization practices.

### Technical Partner (equity) — Trastain
**Cairo, Egypt (Remote)** · Feb 2025 – Aug 2025

- Built a booking platform from scratch on C#/.NET, including secure payment transaction handling (Stripe, Paymob) with webhook processing and HMAC signature verification.
- Deployed to **Azure Web Apps** and **Azure Static Web Apps** via GitHub Actions CI/CD.

### Software Engineer — MYM (Make Your Miracle)
**Giza, Egypt** · Jun 2023 – Oct 2023

- Built backend systems for e-commerce and booking platforms, delivered end to end from requirements through deployment and support.

### Freelance / Independent Client Work

- Evaluated **Azure vs. AWS** per project and delivered on both: Azure managed services (App Service, Blob Storage, managed SQL, Static Web Apps) for fast MVP delivery, and **AWS EC2/S3** self-managed infrastructure for later projects, including a cost-driven migration off a cloud SMS provider.
- Built GitHub Actions CI/CD pipelines and integrated Stripe/Paymob payments with webhook/HMAC verification.

---

## Technical Skills

- **Languages:** C#, Python, SQL, TypeScript, JavaScript
- **.NET / Backend:** ASP.NET Core, ASP.NET Core MVC, Minimal APIs, .NET 8/9/10, .NET Framework 4.5, Entity Framework Core, REST APIs, gRPC, Webhooks
- **Databases:** Microsoft SQL Server, PostgreSQL
- **Architecture:** Clean Architecture, Microservices, Service-Oriented Architecture, Distributed Systems, Business Rule Engines, API Gateway Architecture
- **Distributed Systems & Messaging:** Temporal (Saga orchestration), RabbitMQ, MassTransit, gRPC
- **Identity & Security:** OpenID Connect, OAuth2, OpenIddict, JWT, scope- and claim-based authorization
- **Service Discovery:** Consul (service discovery, health checks, Consul Template, Consul KV)
- **Cloud:** **Azure** (App Service, Blob Storage, SQL, Static Web Apps, DevOps) and **AWS** (EC2, S3, messaging) — evaluated and delivered on both
- **DevOps & Version Control:** Git, Git Flow, **Docker**, Azure DevOps Pipelines, GitHub Actions, CI/CD automation, TFVC → Git migration
- **Performance:** BenchmarkDotNet, performance tuning, legacy system modernization
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

**Overall fit: ~82%.** One of the cleanest matches in the pipeline — every required qualification is directly met, and the preferred list (Azure **or** AWS, microservices, CI/CD, Docker) is fully covered by having *both* clouds rather than one.

| Gap | Severity | Note |
|---|---|---|
| **3–8 years asked; he's at ~3** | None | He's within the stated range, at the low end, which is normal for a 3–8 yr band rather than a stretch. |
| **Onsite, Abu Dhabi — relocation** | Decision, not a gap | Matches the widened search parameters (Gulf with visa sponsorship is explicitly in scope). Visa sponsorship isn't stated in the posting — **confirm during screening** whether Jaheziya sponsors work visas for hires from outside the UAE; this is standard for many UAE employers but not universal. |
| **Docker** | Minor | He has hands-on Docker but not deep production container-orchestration ownership (Kubernetes is explicitly not implemented anywhere in his experience — don't imply otherwise if asked). |
| **No frontend framework required** | None — strength | Pure backend role. No Angular/React gap to manage here, unlike most of the rest of the pipeline. |
| **AI/agentic work** | Not required | Not mentioned in the JD; correctly left off this CV entirely rather than diluting the backend pitch. |

### Selling-point map
- **What the company needs:** 3–8 yrs .NET backend — C#, .NET/.NET Core, ASP.NET Core, REST APIs, SQL Server, clean/scalable architecture, Git. Preferred: Azure or AWS, microservices, CI/CD, Docker.
- **Lead selling point(s):** distributed-systems architecture (Saga, identity server, API gateway, service discovery) + **both** major clouds, which directly overshoots the "Azure or AWS" preferred line.
- **Supporting:** legacy modernization (5+7 modules, MS DTC → Saga), CI/CD ownership, Docker, quantified wins (87.5% downtime reduction, 45% rule-engine improvement).
- **Deliberately NOT emphasized:** AI/agentic engineering, frontend modernization — neither is asked for; would dilute a pure-backend pitch.
- **What makes this CV different here:** most backend candidates will have one cloud; he has both, plus a live example of exactly the kind of distributed-systems work ("scalable application architecture") the JD asks for in the abstract.
