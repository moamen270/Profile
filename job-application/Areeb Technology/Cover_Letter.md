# Cover Letter — Areeb Technology (Senior .NET Developer)

**Headline** — _LinkedIn note to the hiring team / email opener:_

> The .NET engineer who already builds the AI tooling on your "nice to have" list — internal Model Context Protocol servers, multi-model LLM orchestration, automated code review — on top of resilient distributed systems (RabbitMQ, Temporal Saga) and hands-on legacy-to-modern .NET migration.

---

Moamen Moustafa Basyoni
Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com · github.com/moamen270

Dear Hiring Team,

I'm applying for the Senior .NET Developer role. Two things in your description line up unusually well with my work: the resilient distributed systems with asynchronous messaging, and the AI preferences — Model Context Protocol and prompt engineering. I do both today at Andalusia Health Business Solution.

On distributed systems and modernization:

- I design REST and gRPC API contracts before implementation and build fault-tolerant asynchronous messaging with RabbitMQ, plus long-running distributed transactions via Temporal Saga orchestration — improving 10+ inter-service interaction patterns.
- I integrate legacy systems with modern platforms: I've migrated modules from .NET Framework 4.5 / ASP.NET Core 2.2 toward modern .NET with Clean Architecture across 5 core and 7+ additional modules, and built a runtime business-rule engine that improved rule-execution performance by 45% (BenchmarkDotNet).
- Security: an OpenID Connect / OAuth2 identity server (OpenIddict) with JWT access and refresh tokens, scope- and claim-based authorization, and OWASP-aware secure coding.
- Data access with Entity Framework Core and LINQ over SQL Server and PostgreSQL, with .NET Aspire in the same codebase.

On AI: I've built internal MCP servers, an automated code-review and pull-request analysis pipeline, and multi-model orchestration across OpenAI and OpenRouter with observability, guardrails, and cost controls. This is production work, not experimentation.

To be straightforward: I'm at roughly three years rather than five, and my structured-logging has been LLM-side (LangSmith, LangFuse) rather than Serilog and OpenTelemetry in .NET — I'm adding both to a sample service now. I believe the depth of the distributed-systems and modernization work speaks to the level.

I'd welcome a conversation.

Best regards,
Moamen Basyoni

---
---

## NOT PART OF LETTER — notes

### Selling-point map
- **What the company needs (from the JD):** an experienced .NET backend engineer for enterprise, high-throughput systems — resilient distributed services, async messaging, spec-first APIs, legacy-to-modern integration, code reviews, mentoring. Explicitly values MCP + prompt engineering and .NET Aspire in the preferred list.
- **Lead selling point(s):** AI / agentic engineering (MCP, multi-model orchestration, automated code review) + distributed-systems architecture (RabbitMQ, Temporal Saga) → headline + para 1.
- **Supporting:** legacy modernization ("integrate legacy systems with contemporary platforms" is a JD responsibility — the 5-core/7-module migration + 45% rule engine); identity/security; .NET Aspire.
- **What makes this CV different here:** almost no .NET applicant combines real distributed-systems depth with production MCP / multi-model / automated-code-review work. That intersection is the whole pitch.
- **Deliberately NOT emphasized:** healthcare domain (not relevant), payments, full-stack/front-end, greenfield product ownership.

### Gaps
- "Expert-level / 5+ years" is a real filter risk. Letter is honest about ~3 years and counters with depth. Recruiter may still screen out — acceptable.
- Serilog/OpenTelemetry and Dapper are minor; letter commits to the OTel sample. Kafka not mentioned (RabbitMQ covers the concept). Kubernetes not mentioned (Docker + Consul cover the ground).
