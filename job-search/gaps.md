# Gap & Missing-Skill Tracker

Every gap noted in a built CV's "NOT PART OF CV" section, pulled into one place — plus a couple of
items that only ever showed up as a `pipeline.md` review note, flagged as such, for roles where no
full package was built. Ranked by **leverage** — how many applications it affects × how severe it
was called in the worst case — not just by severity in isolation, since a "Low" gap that recurs
five times is worth more than a "High" gap that shows up once.

Check a box when a fix is actually built and verified working, not just started.

## Skill gaps worth closing

| Done | Gap | Appears in (severity) | Roles affected | Action |
|---|---|---|---|---|
| [ ] | **Angular (hands-on)** | Geidea (High), egabi (Medium-High), Raya Holding (Medium), TechLabs (Low) | 4 built packages, plus named in 7 of the 32 postings reviewed in Batch 4 — the single biggest blocker in the local .NET market | Build a throwaway Angular + .NET Core API (a component, data binding, basic RxJS) before any technical round. Highest-return item on this list. |
| [ ] | **React (hands-on)** | The Flex (High — the only real gap there), MTS (Medium), TechLabs (Low, preferred) | 3 built packages | Small React + FastAPI/.NET backend app. |
| [ ] | **pgvector / a dedicated vector store** | Mondia (Medium), Sana Commerce (Medium), Significa (Low-Medium, preferred) | 3 built packages | Add embeddings + similarity search to a small RAG service on Postgres. About a day; closes all three at once. |
| [ ] | **Apache Kafka** | Areeb (Low-Medium), Misbar Alkawn (Low) | 2 | Read the log/partition/consumer-group model; RabbitMQ experience is the transferable base — mention it. |
| [ ] | **Redis** | Thndr (Low), MTS (Low, preferred) | 2 | Add to a sample service; read up on caching, distributed locks, and idempotency keys. |
| [ ] | **Dapper** | Areeb (Low), Misbar Alkawn (Low) | 2 | Half a day — a small Dapper-vs-EF-Core query-performance comparison repo covers it. |
| [ ] | **Kubernetes** | Raya Holding (Low, preferred), Areeb (Low, preferred), noted absent everywhere at Jaheziya | 3, all preferred not required | Optional local `kind`/`minikube` walkthrough. Docker + Consul + Nginx gateway experience covers the concepts in interview. |
| [ ] | **AWS Bedrock** | Sana Commerce (Medium) | 1 | Read the model-access and invocation docs — multi-model orchestration via OpenAI/OpenRouter transfers directly. |
| [ ] | **.NET OpenTelemetry + Serilog** | Areeb (Medium) | 1 | Add Serilog + OTel tracing to a sample ASP.NET Core API — small, high-signal, and you already have LLM observability (LangSmith/LangFuse) as the conceptual base. |
| [ ] | **WCF** | egabi (Medium) | 1 | Read the binding/contract model. Legacy SOAP-era .NET — don't claim it, just be conversational; your .NET Framework 4.5 modernization work is the adjacent evidence. |
| [ ] | **Node.js (production)** | MTS (Medium, required) | 1 | Not currently claimed at all. A small Express API would make it discussable. |
| [ ] | **Microsoft Dynamics 365 Web API** | TechLabs London (Medium) | 1 | Read the Web API basics — Microsoft Graph/SharePoint integration is the same "integrate with a Microsoft platform via API" muscle. |
| [ ] | **NopCommerce** | TechLabs London (Medium) | 1 | Skim the architecture docs (it's ASP.NET Core-based) — e-commerce backend work at MYM/Trastain is transferable context. |
| [ ] | **MongoDB** | MTS (Low-Medium) | 1 | Document-model basics; quick pickup from a relational background. |
| [ ] | **HashiCorp Vault** | MTS (Low, preferred) | 1 | Already has Consul KV (same vendor, adjacent problem) — read what's Vault-specific. |
| [ ] | **Domain-Driven Design fundamentals** | Areeb (Low) | 1 | Reading only — aggregates, bounded contexts, ubiquitous language vocabulary. Clean Architecture work is the practical base. |
| [ ] | **Semantic Kernel** | Significa (Low, preferred) | 1 | Read the planner/plugin model — LangGraph/CrewAI is the transferable base; it's the .NET-native equivalent. |
| [ ] | **Dapr** | Misbar Alkawn (Low-Medium) | 1 | Run the quickstarts locally; map to Consul + RabbitMQ as the equivalent building blocks already used. |
| [ ] | **Event sourcing** | Lamdax (Medium) | 1 | Has pub/sub (RabbitMQ) solidly; event sourcing specifically (event store as source of truth, replay) isn't documented. Saga orchestration is adjacent, not identical — know the distinction, don't blur it. |
| [ ] | **Azure Service Bus** | Lamdax (Low) | 1 | Has RabbitMQ — same messaging concepts, different product. Quick to pick up if it comes up. |
| [ ] | **Azure specialty/PaaS services** (API Management, Application Gateway, IoT Edge, Azure Functions) | Crossworkers Egypt (Low-Medium, nice-to-have) | 1 | Named explicitly in the JD. Documented Azure experience is App Service, Blob Storage, Azure SQL, Static Web Apps, and DevOps — all managed compute/storage/CI, not these serverless/networking-specialty services. The Nginx API gateway work is the closest conceptual analog to Application Gateway; AKS overlaps with the Kubernetes row above. Read the docs for the rest — no hands-on claim to make yet. |
| [ ] | **AWS beyond EC2/S3** (Lambda, managed RDS, ECS/EKS, CloudFormation/IaC) | Flagged in the Digital Zone review (Low-Medium; no CV built — "stack is AWS, he's Azure") | 1 (pipeline note only) | Documented AWS experience is EC2 + S3 (self-managed) and messaging — real, but narrower than a JD asking for AWS-native serverless or managed-service depth. Distinct from the Azure row above: this is "both clouds, but each one's depth is in different places" rather than a single missing service. Worth a small Lambda or managed-RDS side project if AWS-heavy roles keep coming up. |
| [ ] | **Named testing libs (NSubstitute, Fluent Assertions)** | Edenred UAE (Minor) | 1 | Has xUnit already (a direct hit on the same line) — these two are a quick pickup if it comes up. |
| [ ] | **Firebase Auth** | Misbar Alkawn (Low) | 1 | Quick pickup — deep OIDC/OAuth2/JWT experience is the base; Firebase Auth is just a specific provider. |
| [ ] | **Linux environments** | Clover Infotech (Gap) | 1 | Basic ops familiarity. Low effort, currently Windows/IIS-centric. |
| [ ] | **Jenkins / Jira / Confluence (named tools)** | Clover Infotech (Minor) | 1 | Has Azure DevOps Pipelines + Boards equivalents — this is a tool-name gap, not a skill gap. |
| [ ] | **Native AOT** | Areeb (Very low, preferred) | 1 | One paragraph of reading; publish an AOT console app if there's time. |
| [ ] | **Sitecore / Umbraco / Kentico CMS** | Significa (High, required) | 1 | Genuine gap with zero experience. ASP.NET Core-based, so a real ramp-up is at least plausible, but this is the one item on this list that isn't a weekend fix. |
| — | **WinForms / desktop development** | Clover Infotech (Real gap) | 1 | No plan here deliberately — all experience is web/backend, and there's no quick project that manufactures real desktop-app experience. If this turns out to be a large share of daily work there, that's a genuine mismatch, not a gap to close. |

## Structural gaps — not closable by learning, tracked so the pattern is visible

These show up repeatedly but aren't a study-list item — they're either about time served, geography, or a genuine domain that only actual work in it would close.

| Gap | Appears in | Note |
|---|---|---|
| **Years of experience (~3 vs 4–8 asked, one case at 6+)** | Areeb (5+, "expert-level"), Significa (5+), Sana Commerce (4+), MTS (5+), Misbar Alkawn (5+), Raya Holding (4+), **Lamdax (6+, the hardest bar seen yet)** | Not fixable except by time. Every cover letter counters with scope/depth evidence instead of claiming years. Worth watching — if this keeps costing screens, the fix is skewing the search toward lower experience floors, which Batches 5–6 already started doing (Edenred 3–7, Jaheziya 3–8, Clover Infotech 3–6, Hire Feed 3+). Lamdax is a deliberate exception — applied anyway because the identity-stack match (OpenIddict/JWT) is unusually specific. |
| **"Senior" in the title vs an IC track record** | Thndr and others | Same shape as the years gap — countered with scope, never claimed outright. |
| **Financial / regulated domain (banking, settlement, reconciliation)** | Thndr (Medium) | No banking background. Payments integration (Stripe/Paymob, webhook/HMAC) is the closest adjacent evidence; only real exposure closes this one. |
| **English screen weight** | Raya CX (Medium — "the real filter") | B2 (upper intermediate) is documented honestly. Not something to close before applying — just something to prepare for by rehearsing technical explanations out loud. |
| **Visa sponsorship unconfirmed** | Jaheziya, Edenred UAE | Neither posting states it. A screening question, not a skill gap. |
| **4-hour PST overlap** | Crossing Hurdles | Logistics, not a skill — confirm the exact window before accepting if it moves forward. |

## Study plan

**[job-search/study-plan.md](study-plan.md)** turns this table into an actual sequence — real
YouTube material per item, time estimates, and the small project that proves each one, organized in
the same leverage order as above.

## How to use this

- **Before building a new CV package**, check whether the JD's gaps are already on this list — if so, reuse the wording and severity rather than re-deriving it.
- **When a fix actually gets built** (e.g., the pgvector sample), check the box here, update every CV/cover-letter note that named the gap, and note the closed gap in `pipeline.md`'s skill-tasks section.
- **Ranking logic:** items are ordered by recurrence first, severity second — Angular and React sit at the top because they're both frequent *and* severe, not because either alone would justify the position.
