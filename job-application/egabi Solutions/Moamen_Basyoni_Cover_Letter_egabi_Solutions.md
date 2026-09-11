# Cover Letter — egabi Solutions (Sr. Backend Software Developer)

**Headline** — _LinkedIn note to the hiring team / email opener:_

> Backend developer working daily in both a large legacy .NET Framework estate and modern .NET Core — Onion architecture, CQRS, EF Core over SQL Server — with a track record of modernizing mature codebases rather than only building new ones.

---

Moamen Moustafa Basyoni
Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com · github.com/moamen270

Dear Hiring Team,

I'm applying for the Sr. Backend Software Developer role. Two parts of your description match my day job closely: the architecture you list as desirable, and working across both legacy .NET and .NET Core.

On architecture — I build with **Onion and layered architecture, CQRS**, Repository and Dependency Injection, applying SOLID throughout, on **C#, ASP.NET Core and .NET 8/9/10** with **Entity Framework Core over SQL Server**. Specifics:

- Built a runtime business-rule engine for injected business logic that improved rule-execution performance by **45%**, measured with BenchmarkDotNet.
- Designed REST and gRPC API contracts before implementation, improving 10+ inter-service interaction patterns.
- Implemented an OpenID Connect / OAuth2 identity server with JWT and scope-based authorization.
- Built the distributed layer: RabbitMQ messaging, Consul service discovery, and an API gateway with health-aware load balancing that cut deployment downtime from two hours to fifteen minutes.

On legacy — a large part of my work is inside a **mature .NET Framework 4.5 and ASP.NET Core 2.2 codebase**, extending and refactoring it while modernizing it. I've migrated 5 core and 7+ additional modules to modern .NET, and replaced a legacy MS DTC distributed-transaction design — which had forced the whole system onto one shared database — with Temporal Saga orchestration. I also moved source control off a legacy TFS/TFVC monolith to Azure DevOps Git with a private NuGet feed. I'm comfortable in old code, which in my experience is a larger part of senior backend work than job descriptions usually admit.

Two things to be straight about. I haven't worked with **WCF** — my legacy exposure is .NET Framework application and data code rather than SOAP services, though that's the same era and I'd pick it up quickly. And on **Angular**: I directed our frontend migration to it, setting the architecture and overseeing delivery, but I wasn't the hands-on Angular developer. Given this is a backend role I hope that's the right side of the line, but I'd rather say so now.

I'd welcome the chance to discuss.

Best regards,
Moamen Basyoni

---
---

## NOT PART OF LETTER — notes

### Selling-point map
- **What the company needs (from the JD):** a 3–5 year **backend** developer — C#, ASP.NET, .NET Core, SQL Server, EF, JavaScript, Angular, WCF; CQRS and N-Tier/Onion desirable.
- **Lead selling point(s):** backend depth with layered/Onion + CQRS, plus **legacy modernization credibility** — WCF signals an older estate, so being genuinely comfortable in .NET Framework code is the differentiator → headline + paras 2–3.
- **Supporting:** quantified wins (45%, 2h→15m); identity/OAuth2; distributed infrastructure; TFVC→Git migration; code review and mentoring.
- **What makes this CV different here:** most candidates pitch greenfield. This JD (WCF, N-Tier) describes a mature estate — modernization experience is worth more here than novelty.
- **Deliberately NOT emphasized:** AI/agentic work, healthcare domain, payments, cloud specifics.

### Gaps
- **WCF** — not held, stated openly, with the adjacent legacy experience offered honestly.
- **Angular** — direction not hands-on, stated openly; the role being backend-titled should make it secondary, but flag it rather than hide it.
- 3–5 years: he's at the bottom of the band. Fine.

### Priority
"Be among the first 25 applicants" — low competition. Worth sending early.
