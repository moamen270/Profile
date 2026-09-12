# Cover Letter — Lamdax (Senior Backend .NET Core Developer)

**Headline** — _LinkedIn/Workable note to the hiring team or email opener:_

> Your stack names OpenIddict and JWT specifically — I designed and built an identity server on exactly that stack, plus RabbitMQ event-driven communication and a Temporal Saga replacement for a legacy distributed-transaction design. Three years, not six, but the depth is real.

---

Moamen Moustafa Basyoni
Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com · github.com/moamen270

Dear Hiring Team,

I'm applying for the Senior Backend .NET Core Developer role. I want to be upfront about the one number that doesn't match: you're asking for 6+ years, and I have roughly three. I'm applying anyway because the technical overlap is unusually specific, and I'd rather let that speak than not try.

You name OpenIddict and JWT in your stack. I designed and built an identity/authentication server on exactly that combination — OpenIddict issuing JWT access and refresh tokens with scope- and claim-based authorization — at Andalusia, a healthcare platform serving hospitals across Egypt and Saudi Arabia. On event-driven architecture, I implemented RabbitMQ-based communication and replaced a legacy MS DTC distributed-transaction workaround with Temporal Saga orchestration, improving 10+ inter-service interaction patterns. I don't have production event-sourcing experience specifically — pub/sub, yes; an event store as source of truth, no — and I'd rather say that plainly than imply otherwise.

On the rest of the stack: C#, ASP.NET Core, Entity Framework Core over SQL Server, Consul-based service discovery, and an Nginx API gateway that cut deployment downtime by 87.5%. A runtime rule engine I optimized runs 45% faster, measured with BenchmarkDotNet — direct evidence of the high-throughput tuning work you're asking about.

I'd welcome a conversation, including about the contract structure and rate.

Best regards,
Moamen Basyoni

---
---

## NOT PART OF LETTER — notes

### Selling-point map
- **What the company needs:** 6+ yrs .NET Core/C#, microservices/distributed systems, event-driven architecture, EF Core + SQL Server, JWT/OAuth2/OIDC, SOLID, high-throughput optimization.
- **Lead selling point(s):** literal product-name match on identity stack (OpenIddict + JWT) — headline + para 2.
- **Supporting:** Temporal Saga, RabbitMQ, quantified performance wins.
- **Deliberately NOT emphasized:** AI/agentic engineering — off-message here.
- **What makes this different:** the years gap is real and named upfront rather than danced around — the letter's credibility rests on being straight about the one thing that doesn't fit.

### Gaps
- 6+ years vs ~3 — the central risk, addressed head-on in paragraph 1 rather than buried.
- Event sourcing specifically not claimed — pub/sub is, and the letter draws that line explicitly.
- No rate/salary stated in the posting — raised directly since it's a contractor role.

### Interview prep
- Be ready to explain the distinction between Saga orchestration and true event sourcing if asked — the letter already flags this, so it shouldn't come as a surprise question.
- Expect deep technical probing on OpenIddict/JWT internals given how specifically it's named — this is the strongest card, make sure it holds up under detail.
