# To submit — work down this list, apply yourself

Each folder in `job-application/<Company>/` has:
`Moamen_Basyoni_CV_<Company>.pdf/.docx` · `Moamen_Basyoni_Cover_Letter_<Company>.pdf/.docx` · `<Company>_Job_Description.md`

Use the **headline** (top of the cover letter) as your LinkedIn "message to hiring team" / email opener. Attach the CV; paste the letter body if there's a field.

Status: `ready` · `blocked` · `applied` · `assessment` · `video` · `closed` · `rejected` · `offer`

## 🔴 Do these first — already past the CV stage

| Company | Role | Status | Action |
|---|---|---|---|
| **Crossworkers Egypt** | Senior C# / .NET Core Developer | **assessment** | Assessment email still unopened. **Check whether it has expired** — invites usually last 3–7 days. Paste it to Claude either way. |
| **Raya Holding** | Software Development Specialist (.NET) | **video** | Record the ≤1-min English video. Script + delivery notes in `Raya Holding/Video_Script.md`. |

## 🟢 Ready to apply — full package built

Ordered by a mix of fit and how little competition there is.

| Pri | Company | Role | Fit | Apply link | Why now |
|---|---|---|---|---|---|
| 1 | **Müller's Solutions** | .NET Developer | 80% | [link](https://www.linkedin.com/jobs/view/4451349192) | **Lowest friction in the batch** — no framework gap, experience bar matches, "first 25 applicants". Send today. |
| 2 | **Thndr** | Senior Backend Engineer, Money Movements | 82% | [link](https://www.linkedin.com/jobs/view/4440558721) | Best overall match. Distributed-correctness + payments. **"Why Thndr?" answer ready in `Thndr/Thndr_Application_Questions.md`.** |
| 3 | **Mondia** | Agentic AI Engineer | 75% | [link](https://www.linkedin.com/jobs/view/4443361159) | "First 25 applicants" and requires Claude Code experience you have. **Build the pgvector sample first.** |
| 4 | **egabi Solutions** | Sr. Backend Software Developer | 75% | [link](https://www.linkedin.com/jobs/view/4205393694) | "First 25 applicants", backend-titled, legacy estate suits your modernization work. |
| 5 | **Crossing Hurdles** | Senior C# Engineer (remote, $15–20/hr) | 80% | [link](https://www.linkedin.com/jobs/view/4463832136) | Biggest financial lever. **Decide on the 3-month term and confirm the PST overlap window before accepting.** |
| 6 | **Geidea** | .NET Developer (Mid-Level) | 78% | [link](https://www.linkedin.com/jobs/view/4465035998) | Experience bar matches exactly; payments company. |
| 7 | **The Flex** | Software Engineer | 78% | [link](https://www.linkedin.com/jobs/view/4429158770) | PropTech = Trastain. Alexandria, remote-first. **Two essay questions you must write yourself — they explicitly forbid AI. Source material in `The Flex/The_Flex_Application_Questions.md`.** |
| 8 | **Sana Commerce** | Software Engineer — AI | 76% | [link](https://www.linkedin.com/jobs/view/4462431384) | Your AI stack, in Alexandria. Same pgvector sample helps. |
| 9 | **Raya CX** | Full Stack Developer (.NET) | 75% | [link](https://www.linkedin.com/jobs/view/4436886553) | No frontend-framework gap. Different entity from Raya Holding. |

## ✅ Applied — awaiting response

| Company | Role | Fit | Applied |
|---|---|---|---|
| TechLabs London | Senior .NET Developer | 80% | 2026-09-10 |
| Areeb Technology | Senior .NET Developer | 75% | 2026-09-10 |
| Misr Technology Services | Senior Software Developer | 72% | 2026-09-10 |
| Significa | Senior Backend Developer | 70% | 2026-09-10 |
| PaxeraHealth | Senior .NET Developer | 85% | earlier |
| SSC HR Solutions | Senior Backend Engineer .NET | 70% | earlier |

## ⚫ Closed

| Company | Role | Note |
|---|---|---|
| Misbar Alkawn | Senior .NET Backend Developer | Posting ~1 year old, not accepting. Package kept in case it reposts. |

## Skill tasks that unblock multiple applications

- [ ] **pgvector sample** — add embeddings + similarity search to a small RAG service on Postgres. Closes a named gap at **Mondia** and **Sana Commerce**. About a day.
- [ ] **Learn Angular properly** — hands-on, enough to pass a component/RxJS exercise. It is a requirement in 7 of the last 32 postings reviewed and is currently your biggest blocker in the local .NET market. Highest-return effort available.
- [ ] **React + FastAPI sample** — would unblock **The Flex** and strengthen MTS.

## Interview prep by company

- **Thndr** — idempotency, exactly-once vs at-least-once, compensating transactions, reconciliation after partial failure. Know precisely why MS DTC failed on .NET Core 2.2 and what Saga bought.
- **Geidea / egabi / Raya Holding** — expect a live Angular question. Answer honestly: you directed the migration, you don't write Angular.
- **Mondia / Sana Commerce** — cross-encoder re-ranking; AWS Bedrock's model-access and invocation model.
- **egabi** — WCF binding/contract model (don't claim it, but know what it is).
- **Raya CX** — English-heavy screen. Rehearse describing the architecture work out loud.
- **TechLabs London** — NopCommerce and the Dynamics 365 Web API.
