# How ATS CV Scoring Actually Works — Complete Investigation

> Research compiled from vendor documentation (Oracle, Workday, Greenhouse, Lever, Ashby, iCIMS, SAP, Phenom, Eightfold), primary-source ATS platform research, parser vendors (Textkernel/Sovren, HireAbility, DaXtra, RChilli), LinkedIn official docs, and academic NLP papers (APJFNN, PJFCANN, BERT-based person-job fit).

---

## The Universal Pipeline

Every ATS follows this pipeline:

```
Hard filters → Parse → Normalize → Match → Score/Rank → Human review
```

**Critical finding:** most enterprise ATS do NOT compute a 0–100% score, and almost none auto-reject based on resume text. Instant rejections come from *form questions*, not resume analysis.

---

## 1. Hard Filters (Run BEFORE the CV Is Even Parsed)

- **Knockout / disqualification questions** — single-answer form questions (work authorization, license, salary ceiling, location, willingness to relocate). Wrong answer = instant auto-rejection.
  - Taleo: Disqualification Questions Library + Candidate Selection Workflow (CSW)
  - Greenhouse: "Auto-reject" rules (Yes/No, single-select, multi-select answers only)
  - Ashby: Global Auto-Reject Rules (with configurable email delay)
  - Workday: prescreening questionnaires
- **Salary expectations** above a preset ceiling
- **Minimum years of experience** answered on the form (not calculated from the CV)

---

## 2. CV Parsing & Structuring

### Parser engines

| Engine | Used by | Notes |
|---|---|---|
| Textkernel / Sovren | SAP SuccessFactors, Adecco, Manpower, Randstad | 2B+ docs/yr, 29 languages, HR-XML/JSON output |
| HireAbility ALEX | iCIMS | Grammar-based, context-aware, 50+ languages |
| DaXtra | Bullhorn | 150+ data fields |
| RChilli | Oracle Recruiting Cloud (add-on) | 40+ languages |
| In-house proprietary | Workday, Lever | Undisclosed internals |
| Fine-tuned LLMs + OpenAI | Greenhouse | Modular, task-specific models |

### What they extract

Contact info, employers, job titles, **date ranges (MM/YYYY preferred)**, education, degrees, skills, certifications. Output as HR-XML/JSON.

### Section detection

Dictionary of known headers. "Work Experience" works; "My Journey" fails. Keywords get assigned to the wrong category — or none at all.

### Failures that silently kill CVs

- Image-only / scanned PDFs (some OCR, some reject)
- Text in headers/footers (skipped entirely)
- Two-column layouts (interleaved garble)
- Tables (scramble chronology and company associations)
- Graphics, skill bars, photos (invisible)
- Dates placed before employer names (Taleo loses whole experience sections)
- Design-tool PDFs (Canva, Illustrator — text stored as graphical layers)
- Picklist field mapping bugs (SuccessFactors silent failures)
- Non-standard date formats (miscalculated tenure)
- ~30% of Workday applications flagged "unparseable" due to formatting errors

---

## 3. Entity Normalization — The Skills Taxonomy Layer

- **Skills ontologies / knowledge graphs**: Workday Skills Cloud (50,000+ canonical skills), Textkernel knowledge graph, Phenom ontologies. Maps "React.js / ReactJS / React library" → one canonical entity.
- **Synonym normalization**: "CPA" ↔ "Certified Public Accountant" (legacy Taleo *doesn't* do this — literal matching only).
- **Relationship inference**: Docker + Kubernetes → cloud infrastructure capability.
- **Unique concept counting, not frequency** — keyword stuffing gets zero extra weight in modern systems and can trigger spam detection (LinkedIn explicitly).

---

## 4. Matching Techniques (Full Sophistication Spectrum)

| Technique | How it works | Who uses it |
|---|---|---|
| Exact / literal string match | "project manager" ≠ "project management" | Legacy Taleo |
| Boolean search (recruiter-driven) | AND/OR/NOT queries over parsed fields; % of keywords found | All ATS |
| Word stemming | collaborate / collaborated / collaboration match | Lever |
| Fuzzy matching | Levenshtein distance ≤ 2 for typos and spelling variants | Most parsers |
| Weighted keyword scoring | Required keywords weighted 3–10× vs preferred; score = Σ(weighted matches) / Σ(weights) | Taleo ACE, most scoring engines |
| Skills-ontology matching | Normalize both CV & JD to taxonomy, compare entities | Workday, Phenom, Eightfold |
| Semantic embeddings | BERT/word2vec vectors for CV & JD, cosine similarity — "led cross-functional team" ≈ "project management" | Greenhouse, iCIMS, Eightfold |
| Semantic relationship clusters | Related-concept clusters ("stakeholder alignment" + "delivery optimization") score higher than one keyword repeated | Workday HiredScore |
| Ensemble ML / deep learning | Multiple models trained on 100M+ historical applications, learning what successful hires looked like | iCIMS, Eightfold, Phenom |
| LLM qualification evaluation | Extract each basic/preferred qualification from JD and evaluate individually against parsed CV, with natural-language explanations | Workday HiredScore "Fit & Gap", Lever Talent Fit, Ashby (up to 50 criteria, Meets/Does Not Meet/Undecided + evidence citations) |
| Academic models | APJFNN, PJFCANN (co-attention neural nets), BERT cross-encoders, graph-based fusion, learning-to-rank on application history | Research / newer startups |

---

## 5. Scoring & Ranking Output Formats

| Platform | Output | Details |
|---|---|---|
| **Taleo ACE** | Percentage + tiers | Points → % (points earned / total possible × 100). Tiers: ACE candidate / minimally qualified / other. ACE Star icon + threshold alerts (e.g., ≥75% or ≥3 of 5 assets) |
| **Workday HiredScore** | Letter grades A/B/C/D | All basic quals met = A/B; miss one = C/D; preferred quals differentiate A vs B. −57% recruiter screening time. LLM "Fit & Gap" with plain-language citations |
| **Greenhouse Talent Matching** | 5 tiers, 4 dots | Strong / Good / Partial / Limited / Needs manual review. Recruiter calibration: 4–6 core skills with weight sliders |
| **Lever** | No score | Green "✦ TALENT FIT" badge + Strengths / Areas-for-Clarification narrative |
| **Ashby** | Criteria Met % | e.g., "Meets 1 of 3" with clickable resume evidence citations |
| **Oracle Recruiting Cloud** | 0–3 stars | 4 dimensions: Profile, Education, Experience, Skills (Intelligent Matching) |
| **SAP SuccessFactors** | Stack ranking | Best → least fit using company skills framework (Joule AI); AI Units license required |
| **iCIMS Coalesce AI** | Role Fit score | Compatibility score + rank order; legally an AEDT, bias-audited |
| **Phenom Fit Score** | Dynamic grade | Skills, experience, title, location, engagement; explainable, continuously learning from outcomes |
| **Eightfold Match Score** | Match prediction | ML predicting candidate-to-requisition match; validated against post-hire retention; analyzes career trajectories |

---

## 6. Features / Factors Actually Scored

1. **Skill overlap** with JD (normalized, unique concepts)
2. **Years of experience** — calculated from parsed date ranges; recency-weighted (a skill used in your last 2 roles > same skill in 2016)
3. **Job title taxonomy match** — "Senior Product Manager" exact title + tenure beats title stuffing (heavy structural weight)
4. **Evidence-verified skills** — skills inside experience bullets with measurable outcomes > unaudited skills lists (Ashby/iCIMS explicitly)
5. **Education level & field** match
6. **Certifications / licenses** (both acronym and full form needed)
7. **Location** (distance / work authorization)
8. **Industry alignment**
9. **Career trajectory logic** (progression, tenure per role, company pedigree, employment gaps)
10. **Section placement** — keywords in Skills/Summary score higher than buried in old bullets (older systems)
11. **Competency self-ratings** — Taleo: proficiency (None→Expert) × years × last used × interest
12. **Engagement signals** — Phenom: email opens, chatbot interaction
13. **Historical success patterns** — what hired-and-succeeded people looked like (Eightfold, iCIMS)
14. **Rediscovery** — surfacing past applicants / "silver medalists" (Workday claims ~70% of reqs can be filled this way)

---

## 7. Beyond the CV — Adjacent Scoring Systems

- **LinkedIn Recruiter**: personalized relevance ranking (query match + searcher context + similar-search patterns + past search history); boolean filters; "Spotlights" (more likely to engage, top applicants); spam detection on keyword stuffing. Sourcing tools (SeekOut, hireEZ) add their own fit scores.
- **HireVue (video)**: transcribes answers, NLP/LLM maps text to competency models trained by IO psychologists; no facial analysis anymore; bands candidates Top/Middle/Bottom; bottom third often never watched; human scorecard uses BARS (Behaviorally Anchored Rating Scales) — measures communication, problem-solving, teamwork, drive, conscientiousness.
- **Gamified psychometrics** (pymetrics-style): neuroscience games → cognitive/emotional trait scores matched to a company's top performers.
- **Chatbot pre-screening** (Paradox/Mya/Phenom voice agents): conversational qualification, structured answers feed the ATS.
- **Coding / skills assessments** (HackerRank, Codility): scored tests integrated as pipeline stages.
- **Talent rediscovery & CRM scoring** — silver medalists, past applicants scored against new reqs.

---

## 8. Legal Constraints That Shape the Algorithms

- **NYC Local Law 144 / AEDT rules, California ADMT, EEOC**: any ranking tool must have annual independent bias audits, disparate-impact ratios, candidate disclaimers, opt-out (routing to "Needs manual review").
- **Human-in-the-loop is deliberate** — Greenhouse/Lever/iCIMS/Eightfold all design AI as *advisory prioritization*, never autonomous rejection, to avoid legal liability.
- **Bias guardrails**: Greenhouse blocks adding protected attributes as criteria and warns when a skill is a proxy for one; Lever anonymizes resumes (strips names, demographics, military status) before LLM processing; Phenom scores only job-relevant factors.

---

## 9. Key Myths vs. Reality

| Myth | Reality |
|---|---|
| "ATS rejects you below an 80% score" | No major ATS computes a single 0–100 score; third-party "ATS checkers" (Jobscan-style) simulate an algorithm that doesn't exist in enterprise software |
| "Keyword repetition boosts your score" | Modern systems count unique concepts, not density |
| "The AI reads and rejects your resume" | Rejection comes from knockout form questions; AI only sorts the queue |
| "Recruiters see the AI's verdict" | They see tiers/grades/badges + evidence citations, then decide in 5–10 seconds per CV |

---

## 10. Scoring Spectrum: Most → Least Automated

```
Taleo  >  SuccessFactors  >  iCIMS  >  Workday*  >  Greenhouse  >  Lever
(ACE +     (stack rank       (Role     (*with        (Talent        (no
req rank   with AI Units)    Fit       HiredScore)   Matching,      scoring)
+ disqual                      algo)                  opt-in)
questions)
```

## 11. Keyword Matching: Most Literal → Most Semantic

```
Taleo  >  Lever  >  Workday(base)  >  SuccessFactors  >  Greenhouse  >  iCIMS
(exact     (stemming  (keyword          (AI skills        (embedding    (ensemble ML
match      but no     only)             matching          semantic      semantic
only)      abbrevs)                      with AI Units)    matching)     relationships)
```

---

## Bottom Line

- **Legacy systems** (Taleo, BrassRing): literal keyword matching + weighted prescreening rules; genuinely auto-reject via disqualification questions.
- **Modern systems** (Workday+HiredScore, iCIMS Coalesce, Greenhouse, Ashby, Phenom, Eightfold): parse → normalize to skills taxonomies → semantic/embedding/LLM matching against JD qualifications → tiered ranking with explainability → human decides.

The real battle isn't beating a score — it's surviving parsing, passing knockout questions, and landing in the top tier of the recruiter's sorted queue.
