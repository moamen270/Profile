# Moamen Moustafa Basyoni

**C# Engineer | Code Analysis & LLM Evaluation**

Alexandria, Egypt · +20 102 786 8067 · mmoamen270@gmail.com
GitHub: github.com/moamen270

---

## Professional Summary

C# engineer whose current work sits at the intersection this role describes: reading unfamiliar code at scale, and judging what LLMs do with it. Built an AI code-documentation system combining Roslyn static analysis and code metrics with LLM interpretation, an automated pull-request review that comments line-by-line and checks implementations against their stated requirements, and a code graph spanning a 38-module application. Runs LLM evaluation and observability in production through LangSmith and LangFuse, with multi-model orchestration across OpenAI and OpenRouter. Three years of C# and .NET behind it, including extensive work extending and refactoring a large, unfamiliar legacy codebase.

---

## Professional Experience

### R&D Engineer — Code Analysis & AI Tooling · Andalusia Health Business Solution (AHBS)
**Dec 2023 – Present · Alexandria, Egypt**

**Code analysis and LLM evaluation**

- Built an **AI code-documentation system** combining **Roslyn** static analysis and code metrics with LLM interpretation — producing documentation carrying both a structural and a semantic view of the codebase.
- Built **automated pull-request review** integrated into Azure DevOps: opens threads, posts overall and **line-level comments**, and checks the implementation against the business requirements in the linked work item. This is, in practice, continuous assessment of code changes against intent.
- Built a **code graph spanning 38 modules** of a production application, mapping code to business capability.
- **LLM evaluation and observability** with LangSmith and LangFuse — prompt telemetry, token usage tracking, and comparison across models; **multi-model orchestration** over OpenAI and OpenRouter with model selection, rate limiting and cost control.
- Built five custom Model Context Protocol (MCP) servers, including a **database server** and a **Playwright** server used for AI-driven test analysis and automation.
- Applies guardrails, prompt-injection mitigation and human-in-the-loop review.

**C# / .NET engineering**

- Build and refactor services on **C#, ASP.NET Core and .NET 8/9/10**, with Entity Framework Core over SQL Server and PostgreSQL.
- Work extensively inside a **large, mature codebase that predated me** — modernized 5 core and 7+ additional modules from .NET Framework 4.5 / ASP.NET Core 2.2, including replacing a legacy MS DTC design with Temporal Saga orchestration. Reading unfamiliar code and forming a correct model of it quickly is the core skill.
- **Debugging and testing:** production issue triage and performance tuning; xUnit and pytest; a runtime rule engine benchmarked to a **45%** improvement with BenchmarkDotNet.
- **Git and Docker** daily — migrated source control from a legacy TFVC monolith to Azure DevOps Git multi-repo with a private NuGet feed, and deliver containerized CI/CD across Dev, Staging and Pre-Live.
- Conduct technical code reviews; mentored 25 engineers across 6 teams.

### Technical Partner (equity) — Trastain
**Feb 2025 – Aug 2025 · Cairo, Egypt (Remote) · Part-time**

- Built a booking platform from scratch, including RAG-based matching and multimodal AI search.
- **Remote collaboration** across time zones with a distributed founding team.

### Software Engineer — MYM (Make Your Miracle)
**Jun 2023 – Oct 2023 · Giza, Egypt**

- Backend systems for e-commerce and booking platforms, delivered end to end.

---

## Technical Skills

- **Languages:** C#, Python, SQL, TypeScript, JavaScript
- **C# / .NET:** ASP.NET Core, .NET 8/9/10, .NET Framework 4.5, Entity Framework Core, **Roslyn** (static analysis and metrics), xUnit, BenchmarkDotNet
- **Code analysis:** Roslyn-based static analysis, code graphs, automated PR review, implementation-versus-requirement checking, debugging and production triage
- **LLM evaluation & tooling:** LangSmith, LangFuse, prompt telemetry, multi-model orchestration (OpenAI, OpenRouter), model selection, Model Context Protocol (MCP), LangGraph, CrewAI, RAG, guardrails
- **AI-assisted development:** Claude Code (daily), GitHub Copilot, Codex, OpenCode
- **Tooling:** **Git**, GitHub, GitHub Actions, Azure DevOps, **Docker**, TFS/TFVC migration
- **Testing:** xUnit, pytest, pytest-asyncio, Playwright (via MCP-driven automation)

---

## Education

**B.Sc. Computer Engineering** — Behera Higher Institute (BHI), Alexandria, Egypt · 2023
Grade: B+ · GPA 3.2 / 4.0

## Publication & Languages

- *IoT-Enabled E-Prescription Management and Dispensing Machine Monitoring* — IEEE, 2024
- Arabic (Native) · English (B2, Upper Intermediate)

---
---

## ⚠️ NOT PART OF CV — Gaps to close before applying

**Overall fit: ~80%, and financially the most significant option in the pipeline.**

| Gap | Severity | Note |
|---|---|---|
| **3-month contract, not permanent** | **Decision, not a gap** | At $15–20/hr over 40 hrs, this pays multiples of his current salary — but it ends in 3 months with no security. Weigh against a permanent local role. It could also be run *alongside* notice elsewhere, or used as a bridge. |
| **4-hour PST overlap** | Medium | PST is 10 hours behind Egypt. A 4-hour overlap means working until roughly 2–4am Egyptian time, or a heavily shifted day. Confirm the exact window **before** accepting — this is the real cost of the role. |
| **Open-source repo navigation** | None — strength | He works daily in a large codebase he didn't write, and built a 38-module code graph to make sense of one. |
| **LLM performance assessment** | None — strength | Rare and directly held: LangSmith/LangFuse evaluation, multi-model comparison, and an automated PR reviewer that judges code against intent. |
| 2+ years C# | None | Comfortably met. |

**Why this is unusual:** most C# engineers applying will have the C# and none of the LLM-evaluation side; most AI people will have the evaluation side and no production C#. He has both, which is precisely what the role is.
