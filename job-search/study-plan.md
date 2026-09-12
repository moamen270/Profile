# Study Plan & Progress Tracker

Derived directly from **[gaps.md](gaps.md)** — same items, same leverage ranking, but organized as a
study sequence with real material and a checkbox per step. Check a box when you've actually watched
it **and** built the small project underneath it — watching alone doesn't close a gap; a demo that
survives an interview question does.

Videos below were found via web search on 2026-09-12, favoring well-known free-tutorial channels
(Traversy Media, Net Ninja, Web Dev Simplified, TechWorld with Nana, Hussein Nasser, freeCodeCamp-style
creators). Titles and channels are legitimate and current as of this search, but check the upload date
and skim the first two minutes before committing hours — framework versions move fast.

**When a gap closes:** check it here, check it in `gaps.md`, and update every CV/cover-letter note that
named it as absent.

---

## Phase 1 — Highest leverage, do these first

### [ ] 1. Angular (hands-on)
**Closes a named gap at:** Geidea, egabi Solutions, Raya Holding, TechLabs (preferred) — 4 applications, the single biggest blocker in the local .NET market.

- [Angular Crash Course — Traversy Media](https://www.youtube.com/watch?v=3dHNOWTI7H8) — project-based, components/services/HTTP/routing
- [Angular 101 Crash Course For Beginners (4 hrs, Angular 18)](https://www.youtube.com/watch?v=uWpgtcSxJ3E) — longer, more thorough on fundamentals + TypeScript
- [Learn Angular For Beginners and Advanced Devs (playlist)](https://www.youtube.com/playlist?list=PL9Plq6VIIT-MQ-3UJMZrlYoE7YNKUTFSx)

**Project:** a throwaway Angular app (one component, a form with data binding, one RxJS observable — an HTTP call is enough) talking to a small .NET Core Web API. Push it somewhere you can link to. **Est. 8-12 hours.**

### [ ] 2. React (hands-on)
**Closes a named gap at:** The Flex (the only real gap there), MTS, TechLabs (preferred) — 3 applications.

- [React Tutorial Full Course — Beginner to Pro (React 19, 2025)](https://www.youtube.com/watch?v=TtPXvEcE11E)
- [All React Hooks Explained — React Hooks Tutorial 2025](https://www.youtube.com/watch?v=xfKYYRE6-TQ) — useState/useEffect/custom hooks

**Project:** small React frontend (a form + a list view) against a FastAPI or .NET backend. **Est. 8-10 hours.**

### [ ] 3. pgvector / a dedicated vector store
**Closes a named gap at:** Mondia, Sana Commerce, Significa (preferred) — 3 applications, and the fastest fix on this whole list.

- [PGVECTOR — Vector Search in PostgreSQL Using pgvector: A Complete Tutorial](https://www.youtube.com/watch?v=wsBGpWBo0Ks)
- [Build Vector Search in .NET with Postgres and pgvector](https://www.youtube.com/watch?v=c_YZazjQrNs) — .NET-specific, worth prioritizing given your stack

**Project:** add embeddings + similarity search to a small RAG service on Postgres — reuse an existing project if you have one with document/chat data. **Est. ~1 day.**

---

## Phase 2 — Medium leverage, cheap to close

### [ ] 4. Apache Kafka
**Closes a named gap at:** Areeb Technology, Misbar Alkawn — 2 applications; RabbitMQ is your transferable base.

- [Apache Kafka Crash Course — Hussein Nasser](https://m.youtube.com/watch?v=cNFAP9OnJjo) — producers/consumers/topics/partitions, ride-sharing example
- [Apache Kafka Tutorial — Complete Crash Course for Beginners [2025]](https://www.youtube.com/watch?v=aOlDONHog50)

**Project:** none required — this is reading-depth, not a build. Be ready to explain partitions, consumer groups, and how it differs from RabbitMQ's model. **Est. 2-3 hours.**

### [ ] 5. Redis
**Closes a named gap at:** Thndr, MTS (preferred) — 2 applications.

- [Redis Crash Course — Web Dev Simplified](https://www.youtube.com/watch?v=jgpVdJB2sKQ) — installation, commands, lists/sets/hashes, Node.js example
- [Distributed Locks with Redis — official docs](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) — read this specifically for the idempotency-key angle Thndr cares about

**Project:** add Redis caching (or a simple distributed lock) to a sample service. **Est. 3-4 hours.**

### [ ] 6. Dapper
**Closes a named gap at:** Areeb Technology, Misbar Alkawn — 2 applications; you already use EF Core, so this is a fast add.

- [A Beginner's Guide to Dapper with .NET — Complete CRUD in a .NET 8 Web API](https://www.youtube.com/watch?v=hi1M-8LcjOw)
- [Learn Dapper in an Hour! (.NET Core)](https://www.youtube.com/watch?v=IVsN0WlufWc)

**Project:** a small repo comparing Dapper vs. EF Core query performance on the same table — doubles as an interview artifact. **Est. half a day.**

### [ ] 7. Kubernetes (concepts only — all named as "preferred", none required)
**Closes a named gap at:** Raya Holding, Areeb Technology (both preferred), noted absent at Jaheziya — 3 applications.

- [Kubernetes Tutorial for Beginners — FULL COURSE in 4 Hours (TechWorld with Nana)](https://www.youtube.com/watch?v=X48VuDVv0do)
- [Kubernetes Tutorial for Beginners — Learn K8s in 16 Minutes](https://www.youtube.com/watch?v=LwPG8_icN-E) — if you only have time for one short version

**Project (optional):** a local `kind` or `minikube` walkthrough — deploy one container, expose it, done. You already have Docker + Consul + Nginx gateway as the conceptual base, so this is about vocabulary, not new architecture thinking. **Est. 3-5 hours for the short path, a full evening for the long course.**

---

## Phase 3 — Role-specific, one-off (do only if that application is live)

### [ ] 8. AWS Bedrock — *Sana Commerce*
- [Amazon Bedrock Tutorial for Beginners — Full Console Walkthrough + Fundamentals](https://www.youtube.com/watch?v=ne7RDOiw1T4)
- [Amazon Bedrock for Beginners — From First Prompt to AI Agent](https://www.youtube.com/watch?v=FAgmR9VV0GQ)

Reading-depth only — your multi-model orchestration concepts (OpenAI/OpenRouter) transfer directly to how Bedrock exposes model access. **Est. 2 hours.**

### [ ] 9. .NET OpenTelemetry + Serilog — *Areeb Technology*
- [Getting Started With OpenTelemetry Tracing and ASP.NET Core](https://www.youtube.com/watch?v=g0G9M6AuTdo)
- [Implementing Distributed Tracing with OpenTelemetry in .NET Applications](https://www.youtube.com/watch?v=OX3FjaTl8jU)

**Project:** add Serilog + OTel tracing to a sample ASP.NET Core API — small, high-signal, reuses your LLM-observability instincts from LangSmith/LangFuse. **Est. half a day.**

### [ ] 10. WCF — *egabi Solutions*
- No strong dedicated crash-course video surfaced (WCF is legacy enough that most content is written, not video). [Microsoft Learn — SOAP and HTTP Endpoints in WCF](https://learn.microsoft.com/en-us/dotnet/framework/wcf/samples/soap-and-http-endpoints) is the most direct reference.

Reading-depth only — you're not claiming it, just need to be conversational about the binding/contract model. **Est. 1-2 hours.**

### [ ] 11. Node.js (production) — *Misr Technology Services*
- [Node.js and Express.js — Full Course](https://www.youtube.com/watch?v=Oe421EPjeBE)
- [Learn Node JS in 40 Minutes (Crash Course) — Express, CRUD APIs](https://www.youtube.com/watch?v=bqy1Sa6Ha7o) — if short on time

**Project:** a small Express API — enough to make it honestly discussable, not claimed as production experience. **Est. half a day.**

### [ ] 12. Microsoft Dynamics 365 Web API — *TechLabs London*
- [Dynamics 365 Integrations — Power Automate, APIs, Azure & Dataverse Explained](https://www.youtube.com/watch?v=Z_OSjEFYC_Q)

Reading-depth — your Microsoft Graph/SharePoint integration work is the same "REST/OData against a Microsoft platform" muscle. **Est. 2 hours.**

### [ ] 13. NopCommerce — *TechLabs London*
- [nopCommerce — .NET Developer Overview (From Zero to 60)](https://www.youtube.com/watch?v=B8Ni3yRrBMU)
- [The Architecture behind the nopCommerce eCommerce Platform](https://www.youtube.com/watch?v=6gLbizzSA9o)

It's ASP.NET Core-based and close to Onion Architecture — should feel familiar fast. **Est. 2-3 hours.**

### [ ] 14. MongoDB — *Misr Technology Services*
- [MongoDB Tutorial for Beginners — Full Course, Atlas, Compass, CLI & Node.js API (2026)](https://www.youtube.com/watch?v=p1NEtNmO33s)

**Project:** none required — document-model basics from a relational background is a quick conceptual jump. **Est. 2-3 hours.**

### [ ] 15. HashiCorp Vault — *Misr Technology Services*
- [HashiCorp Vault Tutorial for Beginners — FULL COURSE in 1 Hour](https://www.youtube.com/watch?v=ae72pKpXe-s)

You already have Consul KV (same vendor) — focus on what's Vault-specific (dynamic secrets, leases). **Est. 1 hour.**

### [ ] 16. Domain-Driven Design fundamentals — *Areeb Technology*
- [A Crash Course on Domain-Driven Design (ByteByteGo)](https://blog.bytebytego.com/p/a-crash-course-on-domain-driven-design) — written, but the clearest short overview found
- Amichai Mantinband's .NET-focused DDD content (search "Amichai Mantinband DDD" on YouTube — his channel is the best free .NET-specific source for this)

Reading-depth — Clean Architecture is your practical base; this is vocabulary (aggregates, bounded contexts, ubiquitous language). **Est. 2-3 hours.**

### [ ] 17. Semantic Kernel — *Significa*
- Search "Semantic Kernel AI Orchestration Devoxx" on YouTube for the Bruno Borges/John Oliver conference talk — the clearest free overview found, not linked directly here since search didn't return a stable direct URL.

LangGraph/CrewAI is your transferable base; this is the .NET-native equivalent. **Est. 2 hours.**

### [ ] 18. Dapr — *Misbar Alkawn*
- [Introduction to Dapr!](https://www.youtube.com/watch?v=EASb_r6vEoM)
- [.NET Microservices with DAPR](https://www.youtube.com/watch?v=TeHVd3UlfY8)

**Project:** run the official Dapr quickstarts locally; map service invocation/pub-sub/state/secrets to Consul + RabbitMQ, which you already know. **Est. 3-4 hours.**

### [ ] 19. Named testing libs (NSubstitute, Fluent Assertions) — *Edenred UAE*
- [Meet NSubstitute: The Best Way to Write Unit Tests](https://www.youtube.com/watch?v=YUxG19mDVG8)
- [How to write cleaner unit tests with Fluent Assertions in .NET Core](https://www.youtube.com/watch?v=b2zxl5zNjlA)

You already have xUnit — this is two library APIs, not a new testing philosophy. **Est. 1-2 hours.**

### [ ] 20. Firebase Auth — *Misbar Alkawn*
- Search "Firebase Authentication Crash Course" — several short (~30 min) options surfaced; pick whichever matches your frontend stack if you build a demo, otherwise skim one for the concepts.

Deep OIDC/OAuth2/JWT experience is the real base — this is a specific provider, not new territory. **Est. 1 hour.**

### [ ] 21. Linux environments — *Clover Infotech*
- [Linux Command for Programmers | Crash Course](https://www.youtube.com/watch?v=jUklCapWN5w)
- [Linux Terminal Crash Course — For Absolute Beginners](https://www.youtube.com/watch?v=hREnP0HslK8)

**Est. 2-3 hours** for baseline comfort — navigation, permissions, processes.

### [ ] 22. Event sourcing — *Lamdax*
- [Understanding Event Sourcing in ASP.NET Core C#](https://www.youtube.com/watch?v=EGYMNsI_Opo)
- [Event Sourcing for .NET Developers: From Zero to Implementation](https://www.youtube.com/watch?v=gvW9uJSFujA)

Know the distinction from Saga orchestration cold — that's the exact question this gap invites. **Est. 2-3 hours.**

### [ ] 23. Azure Service Bus — *Lamdax*
- [Get Started With Azure Service Bus: A Beginner's Guide!](https://www.youtube.com/watch?v=1l744A-psG4)

RabbitMQ is your transferable base — same pub/sub concepts, different product surface. **Est. 1-2 hours.**

### [ ] 24. AWS Lambda / serverless — *AWS-beyond-EC2/S3 structural gap*
- [AWS Serverless with AWS Lambda, API Gateway & EventBridge — Full Course for Beginners](https://www.youtube.com/watch?v=5rG-YgTHMC8)

**Project (optional):** one Lambda function behind API Gateway — enough to make "AWS-native serverless" a real answer, not just EC2/S3. **Est. half a day if you build it, 1-2 hours if reading only.**

### [ ] 25. Azure specialty services (APIM, Application Gateway, IoT Edge, Functions) — *Crossworkers Egypt*
- [Building a Serverless REST API With Azure Functions From Scratch](https://www.youtube.com/watch?v=3HZjmYohlgc)
- [Serverless APIs with Azure Functions and API Management](https://www.youtube.com/watch?v=6Z5qK9NTA3k)

Nice-to-have only, and Crossworkers is already applied — low priority unless it resurfaces in conversation. **Est. 2-3 hours reading-depth.**

---

## Not on this list, deliberately

- **Sitecore / Umbraco / Kentico CMS** (Significa, High severity) — real, substantial ramp-up, not a weekend fix. If Significa moves forward and gates on this, that's a decision point (invest seriously or accept the risk), not a checklist item.
- **WinForms / desktop development** (Clover Infotech) — no quick project manufactures real desktop-app experience. Not attempting a fix here; see `gaps.md` for why.

---

## Progress summary

Update this table as phases close:

| Phase | Items | Closed |
|---|---:|---:|
| 1 — Highest leverage | 3 | 0 / 3 |
| 2 — Medium leverage | 4 | 0 / 4 |
| 3 — Role-specific | 18 | 0 / 18 |
| **Total** | **25** | **0 / 25** |
