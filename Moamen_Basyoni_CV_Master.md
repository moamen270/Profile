# Moamen Moustafa Basyoni

**R&D Engineer — Backend, Distributed Systems, AI & Platform Engineering**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com · github.com/moamen270

---

## Professional Summary

Software engineer with roughly three years of production experience spanning enterprise .NET backend development, distributed-systems architecture, and applied AI/agentic engineering, plus a Python backend practice built alongside the .NET work. Currently an R&D Engineer at a healthcare software company with a two-part mandate: build AI-integrated products and AI tooling across the full software delivery lifecycle, and work with the platform architect to modernize and maintain a large legacy estate. That combination produced an unusual breadth for the experience level — replacing a distributed-transaction design that had forced an entire platform onto a shared database, building an internal AI-driven SDLC automation platform surfaced through a custom Azure DevOps extension, and directing a frontend migration off a legacy Vue/AngularJS stack — alongside earlier work building a PropTech marketplace from scratch as a technical equity partner, and e-commerce/booking platforms as a first job out of university. Comfortable working in both C#/.NET and Python, across Azure and AWS, and in a regulated domain (healthcare). This document is the full profile; a CV tailored to a specific role selects and reorders from it rather than using all of it at once.

## Areas of Expertise

- Enterprise .NET backend development (C#, ASP.NET Core, Entity Framework Core)
- Python backend development (FastAPI, Flask, SQLAlchemy, Pydantic v2, async)
- Distributed systems & microservices architecture
- Legacy system modernization (.NET Framework → modern .NET; monolith → multi-repo; MS DTC → Saga)
- Agentic AI & LLM engineering (RAG, GraphRAG, multi-agent systems, MCP)
- AI-driven software delivery lifecycle (SDLC) automation
- Identity & security engineering (OIDC/OAuth2)
- API gateway, service discovery & event-driven messaging
- Payments & third-party integrations (Stripe, Paymob, webhooks/HMAC)
- Cross-cloud infrastructure (Azure and AWS)
- Healthcare / regulated-domain systems (HMIS)
- Technical enablement, mentoring & instruction

---

## Technical Skills

**Languages:** C#, Python, SQL, JavaScript, TypeScript

**.NET & Backend:** .NET 8/9/10, .NET Framework 4.5, ASP.NET Core (MVC & Minimal APIs), Entity Framework Core, .NET Aspire, REST APIs, gRPC, Webhooks, XML processing

**Python Backend:** FastAPI, Flask, SQLAlchemy (Core + ORM 2.0), Pydantic v2, Alembic, async Python (asyncio, httpx, aiohttp), OpenAPI, pytest / pytest-asyncio, Poetry / uv / pip

**Distributed Systems & Messaging:** Temporal (Saga orchestration), RabbitMQ, MassTransit, gRPC, event-driven architecture, MS DTC → Saga migration

**Architecture:** Clean Architecture, Microservices, Service-Oriented Architecture, Layered Architecture, Business Rule Engines, API Gateway architecture, Reverse Proxy architecture

**API Gateway & Networking:** Nginx, YARP Reverse Proxy, load balancing, dynamic routing, health-aware routing, SSL termination, response caching

**Identity & Security:** OpenID Connect, OAuth2, OpenIddict, JWT (access/refresh tokens), scope-based and claim-based authorization, OWASP-aware coding, PII masking

**Service Discovery & Configuration:** Consul (service discovery, health checks, Consul Template, Consul KV), dynamic service registration/deregistration, centralized configuration

**Databases:** SQL Server, PostgreSQL (relational) · Neo4j (graph)

**Search & Retrieval:** GraphRAG, contextual retrieval, query expansion, semantic search, Elasticsearch

**AI & Agentic Systems:** LangGraph, CrewAI, LangChain, Model Context Protocol (MCP) — five custom MCP servers built (Azure DevOps, Figma, XMind, Playwright, database); RAG and GraphRAG; multimodal search and retrieval (image, location, and natural-language query); multi-agent and cyclic agent workflows; tool/function calling

**LLMOps & Observability:** LangSmith, LangFuse, OpenRouter organization management, OpenAI organization management, token usage tracking, cost optimization, model selection / multi-model orchestration

**AI Security & Guardrails:** prompt-injection mitigation, LLM policy enforcement, human-in-the-loop review, PII masking, rate limiting, token budgeting, prompt telemetry

**Web / Frontend:** JavaScript, TypeScript, jQuery, Ajax, HTML, CSS, XML. **Angular** — working knowledge; directed a migration to it as the target frontend architecture, not a hands-on production Angular developer. **Vue 3 / AngularJS / PrimeNG** — familiarity from the same migration (legacy and target stacks), not development experience. **React** — working proficiency, self-assessed, no documented production project. Micro-frontend / shell architecture — architectural direction, not implementation.

**Payments & Integrations:** Stripe, Paymob, webhook processing, HMAC signature verification, Google Sheets API (two-way), Google Drive API, Microsoft Graph / SharePoint, SMS and email notification providers

**DevOps & Version Control:** Azure DevOps (cloud & on-premise, Pipelines, Artifacts, custom extension development), GitHub Actions, CI/CD automation, TFS/TFVC → Git migration, monolithic repo → multi-repository decomposition, Git Flow, Docker, private NuGet feed, private npm feed

**Cloud & Hosting:** **Azure** — App Service (Web Apps), Blob Storage, Azure SQL, Static Web Apps, DevOps Pipelines/Artifacts. **AWS** — EC2, S3, messaging services (SMS/email notifications). Cross-cloud evaluation and cost optimization; IIS hosting.

**AI-Assisted Development Tools:** Claude Code (daily), GitHub Copilot, Codex, OpenCode

**Performance:** BenchmarkDotNet, performance tuning, legacy system modernization

**Training & Instruction:** .NET, Generative AI, AI Agents — delivered through Andalusia Academy

---

## Professional Experience

### R&D Engineer — Backend, Distributed Systems & AI Engineering
**Andalusia Health Business Solution (AHBS)** · Alexandria, Egypt · December 2023 – Present
*Healthcare / HMIS, serving the Andalusia hospital group in Egypt and Saudi Arabia · 5-developer delivery team · Agile Scrum on Azure DevOps*

The role carries two mandates: building AI-integrated products and AI tooling across the software delivery lifecycle, and working with the platform architect to analyze, modernize, and maintain the core platform — then implementing, reviewing, deploying, and supporting that plan alongside the development team as a senior developer.

**AI & R&D Engineering**
- Built five custom Model Context Protocol (MCP) servers (Azure DevOps, Figma, XMind, Playwright, database), surfaced to the organization through a custom Azure DevOps extension so the whole AI toolchain runs inside one platform.
- Built an AI-driven Software Delivery Lifecycle (SDLC) automation program: AI-assisted requirements analysis and user-story authoring grounded in a business GraphRAG knowledge base, automated story-quality scoring, Use Case Point (UCP) story weighting, AI-generated bug reports and test cases, and an automated pull-request reviewer that opens threads, posts overall and line-level comments, and checks implementations against the business requirements in the linked work item.
- Built a code graph spanning 38 modules of the production application for code-to-business traceability, an AI code-documentation system combining Roslyn static analysis and code metrics with LLM interpretation, and a documentation portal with an embedded AI assistant.
- Delivered internal AI products for specific business functions: a mail AI assistant for C-level and managerial users, an assessment chat that generates and scores multiple-choice/essay quizzes for HR and Learning & Development, and a conversational clinic-booking assistant for the Customer Experience team.
- Built RAG and GraphRAG systems on Neo4j, including a policies knowledge base and a PII-masked organizational memory graph; built LangGraph workflows and CrewAI multi-agent pipelines; implemented multi-model orchestration across OpenAI and OpenRouter with observability via LangSmith and LangFuse.
- Managed OpenRouter organization infrastructure — model access, provider configuration, usage/cost monitoring, and rate limiting/token budgeting.
- Applied AI guardrails: prompt-injection mitigation, human-in-the-loop review, and PII masking.

**System Modernization Program** (with the platform architect)
- Analyzed a platform running .NET Framework 4.5 and ASP.NET Core 2.2 side by side, with distributed transactions handled through a custom MS DTC workaround that forced the entire system onto a single shared database, and source control on one monolithic TFVC repository on a legacy TFS server.
- Replaced the MS DTC workaround with **Temporal Saga orchestration**, improving 10+ inter-service communication patterns.
- Migrated source control from legacy TFS/TFVC to Azure DevOps Git, decomposed the monolith into multiple Git repositories, and stood up a private NuGet feed for shared packages.
- Modernized 5 core and 7+ additional modules off the legacy stack, applying Clean Architecture.
- Designed the target architecture — gRPC for inter-service communication, MassTransit messaging, service discovery, centralized configuration with secret management, an OIDC/OAuth2 identity server, and an API gateway — and implemented an identity server (OpenIddict, JWT, scope/claim-based authorization), Consul-based service discovery/dynamic routing/centralized configuration, and an Nginx API gateway with parallel service versioning that cut deployment downtime from **2 hours to 15 minutes (87.5%)**.
- Containerization (Docker and Kubernetes) is planned and deliberately deferred until the work above is complete and stable — **not yet implemented**.

**Frontend Modernization — technical direction** *(not hands-on development)*
- Defined and directed the migration from a monolithic Vue 3 shell embedding multiple AngularJS applications through iframes, to a single modern Angular shell application on PrimeNG, split into multiple repositories distributed through a private Azure DevOps npm feed.
- This was a planning and oversight role — setting the target architecture and directing delivery; hands-on Angular development was not part of this work.

**Backend & Platform Engineering**
- Built and maintained server-rendered and API-driven web applications using ASP.NET Core MVC and Minimal APIs, with JavaScript/jQuery/Ajax front-end behavior and XML-based data exchange, hosted on IIS.
- Developed internal Python services: FastAPI (Pydantic v2, dependency injection, async/await, OAuth2 JWT security) for LLM service orchestration; Flask (blueprints, extensions) for legacy-system integration and data processing; SQLAlchemy Core and ORM 2.0 (async sessions, Alembic migrations); asyncio/httpx for external API communication; pytest and pytest-asyncio for test coverage; batch data-transformation pipelines.
- Built a runtime business-rule engine, improving execution performance by **45%** (measured with BenchmarkDotNet).
- Implemented AABB-aligned international blood-transfusion workflows for the Blood Bank module, reaching a **98%** compliance score, alongside Supply Chain, Bed Management, and Hospital Structure modules.
- Established Azure DevOps CI/CD pipelines across Dev, Staging, and Pre-Live for both backend and frontend projects, on multi-repository Git Flow.
- Mentored and onboarded **25 engineers across 6 teams** over **8 sessions** on architecture and AI-assisted development.

---

### Technical Partner (equity) — Trastain
**Cairo, Egypt (Remote)** · Part-time · February 2025 – August 2025

Joined a friend's early-stage company as technical partner, compensated in equity rather than salary, on a PropTech / short-term-rental marketplace.

- Analyzed existing short-term-rental platforms (Airbnb and similar), identified that the Airbnb model is not culturally aligned with the Egyptian, wider Middle Eastern, and Muslim market, and wrote the product case for a differently-shaped alternative — the platform's culture-fit matching and policy features exist because of this analysis.
- Built the resulting vacation/short-term-rental booking platform from scratch: shared-property booking, culture-fit/preference matching, and policy enforcement.
- Developed RAG-based AI property matching with actionable booking recommendations, and **multimodal AI search** — users can search by image, by location, or by natural-language description.
- Handled transaction security for booking execution; integrated Stripe and Paymob payment gateways with webhook processing and HMAC signature verification.
- Built GitHub Actions CI/CD pipelines deploying backend services to Azure Web Apps and the frontend to Azure Static Web Apps.

---

### Software Engineer — MYM (Make Your Miracle)
**Giza, Egypt** · June 2023 – October 2023

First role after graduating, at a client-project software house delivering SaaS / e-commerce / booking systems.

- Developed backend systems for e-commerce and booking platforms across several client domains, including hotel booking, gym/fitness booking, and other reservation systems.
- Worked end to end on client delivery: requirements analysis, implementation, deployment, and support.

---

### Freelance / Independent Client Work
**With a small partner group** · Side work alongside employment

An attempt to formalize freelance client work into a company (branding, web presence, an intake process) — the company was not fully established, but client delivery was real, for small offices and training centres.

- Built **Vortex**, a management system for a children's programming and robotics training centre: course materials and programme structure, instructor session logging with management approval/denial, a management report calculating instructor pay from approved sessions, two-way Google Sheets integration against the centre's existing sheets, and a Google Drive-powered public gallery of the centre's work on the landing page.
- Evaluated **Azure vs. AWS** per project and chose based on delivery speed and cost: Azure managed services (Blob Storage, App Service, managed SQL, Static Web Apps) for fast MVP delivery with no self-managed servers; AWS EC2/S3 self-managed infrastructure for later projects. Replaced a cloud SMS notification service with a local Egyptian provider, cutting messaging cost.
- Integrated Stripe and Paymob payment gateways with webhook processing and HMAC signature verification.
- Built GitHub Actions CI/CD workflows deploying to Azure Web Apps and Azure Static Web Apps.

---

## Notable Projects & Initiatives

| Project | Description | Result / Evidence |
|---|---|---|
| AI-Driven SDLC Automation Program | AI + MCP tooling across requirements, design, QA and development, surfaced through a custom Azure DevOps extension | End-to-end delivery-lifecycle automation |
| Application Code Graph | Code graph spanning the full application | 38 modules mapped |
| AI Pull-Request Review | Opens threads, overall + line-level comments, checks implementation against linked business requirements | Automated code and requirements review |
| Custom MCP Servers | Azure DevOps, Figma, XMind, Playwright, and database MCP servers | Reusable AI tooling across the SDLC |
| Mail AI Assistant / Assessment Chat / Clinic Booking Chat | Internal AI products for C-level, HR/L&D, and CX teams respectively | Delivered to production users |
| Distributed Transactions | Temporal Saga orchestration replacing a custom MS DTC workaround | 10+ service communication patterns improved |
| System Modernization | Legacy .NET Framework 4.5 / ASP.NET Core 2.2 → modern .NET, Clean Architecture | 5 core + 7+ additional modules |
| Source Control Migration | Legacy TFS/TFVC monolith → Azure DevOps Git multi-repo + private NuGet feed | Project coupling broken across repositories |
| Frontend Modernization (direction) | Vue 3 shell with iframed AngularJS → modern Angular shell on PrimeNG, split into repos | Monolithic frontend decomposed |
| Deployment Infrastructure | API Gateway with parallel service versioning | Downtime reduced 2h → 15m (87.5%) |
| Business Rule Engine | Runtime-injected business logic | 45% performance improvement |
| Blood Bank Module | AABB-aligned international transfusion workflows | 98% compliance score |
| Team Onboarding Program | Architecture and AI-assisted development training | 25 engineers across 6 teams, 8 sessions |
| Trastain Booking Platform | Built from scratch as technical equity partner; RAG matching + multimodal AI search | 0→1 product build, market analysis to launch |
| Vortex | Training-centre management system with approval workflow and Google Sheets/Drive integration | Freelance client delivery |

---

## Education

**B.Sc. Computer Engineering** — Behera Higher Institute (BHI), Alexandria, Egypt
Graduated 2023 · GPA 3.2/4.0 (B+)

## Publication

*IoT-Enabled E-Prescription Management and Dispensing Machine Monitoring* — IEEE, 2024

## Languages

Arabic (Native) · English (B2, Upper Intermediate)

---
---

## ⚠️ NOT PART OF CV — usage notes

**What this document is.** A single CV representing the complete profile — every documented role, project, and skill — rather than a version tailored and trimmed to one job description. It exists to answer "what has this person actually done," not to pass a specific ATS screen.

**When to use it:**
- Sharing the full picture with a recruiter or contact who explicitly wants it.
- A personal portfolio/LinkedIn "featured" attachment.
- A reference source when drafting a new tailored CV for a specific application.

**When not to use it:** for an actual job application. It is long by design and unfocused for any single JD's keyword scan. Use a `job-application/<Company>/Moamen_Basyoni_CV_<Company>.md` tailored version instead — built per §14/§14b/§14c of `profile.md`.

**Truthfulness rules applied here are identical to the tailored CVs** (`profile.md` §5 and §14): Angular is claimed only as technical direction, never hands-on; React is working proficiency with no project; Vue 3/AngularJS/PrimeNG are context, not development experience; no invented seniority ("Senior"/"Lead"/etc. not used); Trastain and MYM titles are the same truthful functional descriptors used elsewhere, since exact titles at those two are undocumented (`profile.md` §13).

**Regeneration:** if `profile.md` changes materially, re-derive this file from it rather than hand-patching, to avoid drift between the two.
