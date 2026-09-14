# LinkedIn Profile Rewrite

Drafted from `profile.md` — same truthfulness rules as every CV in this repo: no invented seniority,
Angular/React stay out of the hands-on skills claims, R&D Engineer stays the official Experience-entry
title (verifiable) but doesn't lead the public headline (unfamiliar label — see `profile.md` §14).

Copy-paste each section directly into LinkedIn. Character counts are LinkedIn's actual limits.

---

## Headline (220 characters max)

LinkedIn's headline is the single highest-visibility piece of text on the whole profile — it's what
shows in every search result and every comment you leave. Three options, same idea at different
lengths:

**Option A — 118 characters (recommended: leaves room, reads clean)**
> Backend Engineer | .NET, Python & Distributed Systems | AI/Agentic Engineering | Legacy Modernization | Azure & AWS

**Option B — 156 characters (more keyword coverage for recruiter search)**
> Backend Engineer (.NET & Python) building distributed systems and production AI/agentic tooling | Healthcare platform modernization | Azure & AWS

**Option C — 91 characters (shortest, punchiest)**
> Backend Engineer | .NET + Python, Distributed Systems, AI/Agentic Engineering, Azure/AWS

**Why not "R&D Engineer" here:** this is the exact headline problem already documented for AHBS —
most recruiters skimming search results don't know what R&D Engineer means, and your current
headline compounds it with "Mid," which reads as a qualifier working against you rather than for
you. The Experience section below still uses the real title (see the AHBS entry) — LinkedIn doesn't
have the same background-check stakes as a CV field, but a functional headline still does more work
than an unfamiliar label at the top of the page.

---

## About (2,600 characters max — this draft is ~1,850, leaving room to personalize)

> I'm a backend engineer with about three years of production experience spanning enterprise .NET,
> a growing Python practice, and applied AI/agentic engineering — three things that don't usually
> show up together this early in a career.
>
> At Andalusia Health Business Solution (AHBS), my role has two parts. First, I work with our
> platform architect to modernize and maintain a large healthcare platform serving hospitals across
> Egypt and Saudi Arabia — I replaced a legacy distributed-transaction design (MS DTC, unsupported on
> .NET Core) with Temporal Saga orchestration, built the identity server and API gateway
> infrastructure around it, and migrated our source control from a TFVC monolith to Azure DevOps Git
> multi-repo. An API gateway change I designed cut deployment downtime from two hours to fifteen
> minutes.
>
> Second, I build AI tooling across the whole software delivery lifecycle: five custom MCP servers
> (Azure DevOps, Figma, XMind, Playwright, database), an automated pull-request reviewer that checks
> implementations against linked requirements, a code graph spanning 38 modules for code-to-business
> traceability, and internal AI products — a mail assistant for managers, an assessment chat for HR
> and L&D, a booking assistant for our CX team. All of it surfaces through a custom Azure DevOps
> extension so it lives inside the platform our teams already use, not as a separate demo.
>
> I also ran a 25-engineer, 6-team onboarding program on architecture and AI-assisted development,
> and I use Claude Code daily — which gives me a practical, not theoretical, sense of where these
> tools help and where they quietly fail.
>
> Before AHBS: I joined a friend's PropTech startup, Trastain, as technical partner on equity — did
> the market analysis (the Airbnb model doesn't fit the Egyptian/Muslim market, and the product's
> culture-fit matching exists because of that finding), then built the platform from scratch,
> including multimodal AI search. Before that, backend work on e-commerce and booking platforms at
> MYM, my first role after graduating in Computer Engineering.
>
> Stack: C#, ASP.NET Core, .NET 8-10, Entity Framework Core, Python (FastAPI, Flask, SQLAlchemy),
> PostgreSQL, SQL Server, RabbitMQ, Temporal, Consul, Neo4j, LangGraph, CrewAI, Azure and AWS.
>
> Open to backend, AI/agentic engineering, and platform roles — Egypt, the Gulf, or remote.

---

## Experience

### AHBS (Andalusia Health Business Solution)
**Position title field:** `R&D Engineer — Backend, Distributed Systems & AI Engineering`
*(The real title, AHBS verifies this with HR — the descriptor after the dash is a LinkedIn-standard
way to add context, not a substitution. See `profile.md` §14.)*
**Dates:** December 2023 – Present · **Location:** Alexandria, Egypt

> Two-part mandate: build AI-integrated products and tooling across the software delivery lifecycle,
> and work with the platform architect to modernize and maintain the core platform alongside the
> development team.
>
> **Platform modernization**
> • Replaced a legacy MS DTC distributed-transaction design — unsupported on .NET Core and worked
>   around by forcing every service onto one shared database — with Temporal Saga orchestration,
>   improving 10+ inter-service interaction patterns.
> • Designed and built an OIDC/OAuth2 identity server (OpenIddict, JWT), Consul-based service
>   discovery, and an Nginx API gateway with parallel service versioning — cut deployment downtime
>   from 2 hours to 15 minutes (87.5%).
> • Modernized 5 core + 7 additional modules off legacy .NET Framework 4.5, applying Clean
>   Architecture.
> • Migrated source control from a TFVC monolith to Azure DevOps Git multi-repo with a private
>   NuGet feed.
>
> **AI & R&D**
> • Built five custom MCP servers (Azure DevOps, Figma, XMind, Playwright, database) surfaced
>   through a custom Azure DevOps extension.
> • Built an AI-driven SDLC automation program: AI-assisted requirements/user-story authoring
>   grounded in a business GraphRAG, automated story-quality scoring, and an AI PR reviewer that
>   checks implementations against linked business requirements with line-level comments.
> • Delivered internal AI products: a mail assistant (C-level/managerial), an assessment chat
>   (HR/L&D), and a clinic-booking assistant (CX).
> • Built RAG and GraphRAG systems on Neo4j; LangGraph workflows and CrewAI multi-agent pipelines;
>   multi-model orchestration across OpenAI and OpenRouter with LangSmith/LangFuse observability.
>
> **Enablement**
> • Designed and ran a 25-engineer, 6-team, 8-session onboarding program on architecture and
>   AI-assisted development.
> • Directed the technical migration from a Vue 3/AngularJS shell to a modern Angular shell
>   architecture — architecture and delivery oversight, not hands-on Angular development.

---

### Trastain
**Position title field:** `Technical Partner (equity)`
**Dates:** February 2025 – August 2025 · **Location:** Cairo, Egypt (Remote) · Part-time

> Joined a friend's early-stage PropTech company as technical partner, compensated in equity.
> • Analyzed existing short-term-rental platforms and identified that the Airbnb model doesn't fit
>   the Egyptian/Middle Eastern/Muslim market — wrote the product case for an alternative; the
>   platform's culture-fit matching and policy features exist because of this analysis.
> • Built the resulting booking platform from scratch: shared-property booking, RAG-based property
>   matching, and multimodal AI search (image, location, or natural-language query).
> • Integrated Stripe and Paymob with webhook processing and HMAC signature verification.

---

### MYM (Make Your Miracle)
**Position title field:** `Software Engineer`
**Dates:** June 2023 – October 2023 · **Location:** Giza, Egypt

> First role after graduating, at a client-project software house.
> • Built backend systems for e-commerce and booking platforms — hotel, gym/fitness, and other
>   reservation domains — end to end: requirements, implementation, deployment, support.

---

## Skills (top ~20, pin the first 3)

Pin these three first — they're the ones worth being endorsed for and the ones recruiters search on:
1. **ASP.NET Core**
2. **Distributed Systems**
3. **C#**

Full list to add:

C#, ASP.NET Core, .NET Core, Entity Framework Core, Python, FastAPI, Microservices, Distributed
Systems, RESTful APIs, RabbitMQ, PostgreSQL, SQL Server, Azure, AWS, Docker, CI/CD, Git, OAuth 2.0,
LangChain, Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP)

**Deliberately left off:** Angular, React. LinkedIn skill endorsements read as a proficiency claim to
anyone who sees them, and the CV rule (`profile.md` §5) is explicit that neither is hands-on
production experience. If you want them discoverable for search without implying expertise, add
them low in the About section prose instead ("comfortable directing Angular migrations, working
proficiency in React") rather than as an endorsable skill tag.

---
---

## ⚠️ NOT PART OF THE PROFILE — notes

### What I couldn't check
LinkedIn blocks automated page loads (HTTP 999). I don't have visibility into your current profile
photo, cover banner, full About text, or Skills list — the only real data point was your public
headline, surfaced via web search: **"Mid R&D Engineer - Andalusia Health Egypt."** That's flagged
above; everything else needs you to paste the text or share the images directly for a full review.

### Photo/banner review — general guidance until I can see yours
- **Profile photo:** solo headshot, front-facing or slight angle, plain or softly blurred background,
  good even lighting, business-casual or better. Smiling reads as more approachable than neutral for
  a candidate actively job-hunting.
- **Cover banner:** the most commonly wasted piece of real estate on LinkedIn. A plain color or a
  simple graphic naming your focus area (e.g. ".NET · Distributed Systems · AI Engineering") reads
  more intentional than the default LinkedIn background or a generic stock photo. Given you're
  actively applying, this is worth 15 minutes in Canva if it's currently the default.

### Where the master CV and this draft diverge
The Master CV (`Moamen_Basyoni_CV_Master.md`) is denser and reads like a document. This is written
for LinkedIn's format and audience — more first-person, more narrative in the About section, and the
Experience bullets are longer than any CV would carry since LinkedIn readers expect the full record,
not a filtered one.
