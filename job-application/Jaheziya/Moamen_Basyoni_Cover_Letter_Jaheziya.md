# Cover Letter — Jaheziya (Backend Developer, .NET)

**Headline** — _LinkedIn note to the hiring team / email opener:_

> A backend engineer who's replaced a legacy distributed-transaction design with Saga orchestration and built the identity, API gateway, and service-discovery layer around it — with production experience on both Azure and AWS, which covers your "Azure or AWS" line either way.

---

Moamen Moustafa Basyoni
Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com · github.com/moamen270

Dear Hiring Team,

I'm applying for the Backend Developer (.NET) role. Your requirements line up closely with what I actually build day to day: C#, ASP.NET Core, RESTful APIs, and SQL Server, with clean and scalable architecture as the explicit standard rather than an afterthought.

At Andalusia, I've spent the last two years modernizing a large healthcare platform's backend: replacing a legacy MS DTC distributed-transaction workaround — which had forced the entire system onto a single shared database — with Temporal Saga orchestration, and building the surrounding distributed-systems infrastructure myself: an OIDC/OAuth2 identity server, Consul-based service discovery, and an Nginx API gateway whose parallel-versioning design cut deployment downtime from two hours to fifteen minutes. In parallel, I migrated our source control from a TFVC monolith to Azure DevOps Git multi-repo, decomposing project-level coupling across the codebase.

On your preferred list: I've worked across **both** Azure (App Service, Blob Storage, managed SQL, Static Web Apps) and AWS (EC2, S3), evaluating and delivering on whichever fit the project. I use Docker daily, and I've built CI/CD pipelines on Azure DevOps and GitHub Actions from scratch more than once.

I'm comfortable relocating to Abu Dhabi for the right role, and would appreciate clarity on visa sponsorship for candidates outside the UAE as part of the process.

I'd welcome the chance to discuss how I could contribute to your team.

Best regards,
Moamen Basyoni

---
---

## NOT PART OF LETTER — notes

### Selling-point map
- **What the company needs (from the JD):** 3–8 yrs .NET backend — C#, .NET/.NET Core, ASP.NET Core, REST APIs, SQL Server, clean/scalable architecture, Git. Preferred: Azure or AWS, microservices, CI/CD, Docker.
- **Lead selling point(s):** distributed-systems architecture (Saga orchestration, identity server, API gateway, service discovery) + dual-cloud experience → headline + para 2/3.
- **Supporting:** legacy modernization, CI/CD ownership, Docker, quantified wins (87.5% downtime cut).
- **Deliberately NOT emphasized:** AI/agentic engineering, frontend modernization — not asked for; would dilute a pure-backend pitch.
- **What makes this CV different here:** most backend applicants will have one cloud; he has both, plus a concrete example of the distributed-systems work the JD only asks for in the abstract.

### Gaps
- Visa sponsorship for non-UAE hires isn't stated in the posting — raised directly and honestly in the letter rather than assumed either way.
- Docker experience is real but not deep production container-orchestration ownership — don't overstate if it comes up live.

### Interview prep
- Be ready to explain precisely why MS DTC failed on .NET Core and what Saga bought — this is the CV's central claim.
- Expect questions on RESTful API design principles and SQL Server schema/performance work given the JD's emphasis on "scalable application architecture."
