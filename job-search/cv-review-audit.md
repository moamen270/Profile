# cv-review skill — scores, accuracy check, and audit

Run 2026-09-10 · engines: `ats-engine-tfidf` + `ats-engine-transformer` (sentence-transformers all-MiniLM-L6-v2)
Runner: `node job-search/review-cvs.mjs` → `cv-scores.json` / `cv-scores.md`
Env: `.venv-cvreview` (Python 3.11 + scikit-learn, sentence-transformers, torch, pypdf, python-docx)

---

## 1. Scores

| Company | TF-IDF | Embedding | **Overall** | Tier/grade | Criteria met | Badge |
|---|---:|---:|---:|---|---|---|
| Significa | 72.6 | 77.0 | **74.8** | Good / C | 18/21 (3 undecided) | TALENT FIT |
| PaxeraHealth | 72.3 | 74.6 | **73.4** | Good / C | 0/0 ⚠️ | TALENT FIT |
| Misr Technology Services | 69.2 | 73.0 | **71.1** | Good / C | 23/25 (2 undecided) | TALENT FIT |
| TechLabs London | 68.1 | 72.9 | **70.5** | Good / C | 12/13 (1 undecided) | TALENT FIT |
| Misbar Alkawn | 65.0 | 69.2 | **67.1** | Good / C | 13/13 | TALENT FIT |
| Raya Holding | 64.1 | 68.4 | **66.2** | Good / C | 17/20 (3 undecided) | TALENT FIT |
| Crossworkers Egypt | 62.2 | 65.6 | **63.9** | Fair / D | 0/0 ⚠️ | NO BADGE |
| SSC HR Solutions | 61.2 | 63.6 | **62.4** | Fair / D | 0/0 ⚠️ | NO BADGE |
| Areeb Technology | 56.4 | 60.9 | **58.6** | Fair / D | 14/17 (3 undecided) | NO BADGE |

Embedding scores every CV 2–4 points above TF-IDF — a consistent offset, not a per-CV signal.

---

## 2. Accuracy check — my fit % vs the engine

**Method note:** I could not produce a fresh blind estimate, because I had already seen the engine's
numbers by the time the comparison was requested. Instead this compares the **fit % recorded in
`pipeline.md` / `applications.json` days earlier, before this skill existed** — a genuine
held-out prediction.

| Company | My fit % | Engine | Gap |
|---|---:|---:|---:|
| Significa | 70 | 74.8 | **+4.8** |
| Misr Technology Services | 72 | 71.1 | −0.9 |
| SSC HR Solutions | 70 | 62.4 | −7.6 |
| Misbar Alkawn | 75 | 67.1 | −7.9 |
| Raya Holding | 75 | 66.2 | −8.8 |
| TechLabs London | 80 | 70.5 | −9.5 |
| PaxeraHealth | 85 | 73.4 | −11.6 |
| Areeb Technology | 75 | 58.6 | −16.4 |
| Crossworkers Egypt | 85 | 63.9 | **−21.1** |

- **Mean gap −8.8** (I am systematically optimistic), **mean absolute error 9.8**
- **Range −21.1 → +4.8 (spread 25.9)**
- **Spearman rank correlation ≈ 0.13** — essentially no agreement on *ordering*

### Is the engine "accurate"?

It is **precise but measuring a different construct**, so neither number is wrong — they answer
different questions:

| | My fit % | Engine score |
|---|---|---|
| Measures | can Moamen do this job, and would a human shortlist him | how lexically/semantically similar this CV text is to this JD text |
| Sees | seniority gaps, location, domain fit, career trajectory, market context | tokens, taxonomy skills, section structure |
| Blind to | ATS parsing, keyword coverage | that 3 yrs vs 5 yrs is negotiable; that healthcare depth transfers |

The two biggest disagreements show this clearly:

- **Crossworkers (mine 85, engine 63.9).** I scored the *human* fit high — the JD's "AI tools and
  agentic workflows" and distributed-systems asks map onto Moamen's strongest work. The engine
  scored it low because that JD has no bullet characters, so **zero qualifications parsed** and the
  keyword overlap is thin.
- **Areeb (mine 75, engine 58.6).** Same story inverted: the MCP/prompt-engineering overlap that
  makes this application distinctive is in the JD's *preferred* section, which the engine
  (see §3) misreads as hard requirements and then penalizes for Kafka/Kubernetes gaps.

**Verdict:** use the engine for what it is good at — keyword coverage, parse health, missing-term
detection. Do **not** use it to rank which jobs to pursue. The rank correlation of 0.13 means
following its ordering would have deprioritized Crossworkers, the one application that has already
produced a real response.

---

## 3. Skill audit — defects found

### 🔴 D1. The JD parser cannot read Markdown headings (highest impact)

`jd_parser._is_heading()` accepts a heading only if it is ALL-CAPS, ends with `:`, or exactly
matches a known phrase. A Markdown heading like `## Preferred qualifications` matches none of
these — the `##` prefix is never stripped.

Consequence, verified on the Raya JD:

| | required skills | preferred skills |
|---|---|---|
| As-is (`## Preferred qualifications`) | **16** — incl. kubernetes, docker, microservices, agile, devops | **0** |
| Same JD with colon headings | 9 | **5** — kubernetes, docker, microservices, agile, devops |

Because `_classify_skills` falls back to `required = all_skills` when no required section is found,
**every nice-to-have becomes a hard requirement**. This is the direct cause of the false
recommendations:

- Raya: *"Required skill 'kubernetes' is missing"* — Kubernetes is in Raya's **preferred** list
- Significa: *"Required skill 'aws' is missing"* — the JD says "Azure **or** AWS", **preferred**
- Areeb: Kafka / Kubernetes flagged as unmet requirements — both **preferred**

`preferred_total` is **0 on all 9 runs**, which is the tell.

This contradicts SKILL.md, which states the JD is *"Markdown, as written on the company's website"*.

### 🔴 D2. Silent total parse failure on prose JDs

`extract_qualifications()` only accepts lines starting with a bullet glyph (`•-*–◦‣·`) or `1.`/`1)`.
Three JDs copied from job boards have no bullet characters → **0 qualifications extracted**, yet the
pipeline still emits a confident badge from zero evidence:

- PaxeraHealth — 0/0 criteria → **"TALENT FIT"**
- Crossworkers — 0/0 criteria → "NO BADGE"
- SSC HR Solutions — 0/0 criteria → "NO BADGE"

No warning is raised. A 0/0 criteria run should be a loud error, not a badge.

**Measured impact of D1+D2** — same CVs, JDs normalized (md heading → colon heading, indented lines → bullets):

| Company | as-is | normalized | Δ | criteria before → after |
|---|---:|---:|---:|---|
| SSC HR Solutions | 62.4 | 52.6 | **−9.8** | 0/0 → 27/41 |
| Crossworkers | 63.9 | 58.8 | **−5.1** | 0/0 → 9/16 |
| Raya Holding | 66.2 | 68.5 | +2.3 | 17/20 → 17/20 |
| Significa | 74.8 | 76.2 | +1.4 | 18/21 → 18/21 |
| Areeb | 58.6 | 59.4 | +0.8 | 14/17 → 14/17 |

**The same CV and JD score up to 10 points apart purely on JD text formatting.** That sensitivity is
undocumented and makes cross-application comparison unsound.

### 🟠 D3. Inapplicable matchers are scored as 0 and dragged into the mean

`score_combiner.combine_matchers()` is documented as *"missing matchers ignored"* but filters with
`if 0.0 <= m.score <= 1.0` — which **includes** 0.0. It cannot distinguish "not applicable" from
"genuinely zero".

`boolean` returns `0.000` on 8 of 9 runs and `1.000` on the 9th — it is a pass/fail flag being
averaged into a similarity mean. Excluding spurious zeros: **+2.9 to +3.7 points** (Areeb, Misbar,
MTS, Raya, TechLabs).

### 🟠 D4. Two matchers carry no discriminative signal

Across all 9 CVs, in the TF-IDF engine:

- `co_attention` — **0.954 → 0.993** (saturated at ceiling)
- `semantic_embedding` — **0.120 → 0.279** (pinned near floor)

Both are averaged with equal weight alongside matchers spanning 0.2–0.99. The floored
`semantic_embedding` is why *"Rewrite the summary/experience language toward the job description's
vocabulary"* fires on **all 9** applications — a recommendation that never varies carries no
information.

### 🟡 D5. SKILL.md documents the wrong path

```
python .opencode/skills/cv-review/scripts/cv_review.py …
```

The skill actually lives at `SKILLS/cv-review/`. It is also not under `.claude/skills/`, so Claude
Code will not auto-discover it — it has to be invoked manually.

### 🟡 D6. Undeclared runtime cost

`compatibility` says "Requires Python 3.11+ with scikit-learn and sentence-transformers". It does
not mention that `sentence-transformers` pulls **torch (~2.5 GB)**. The bundled `__pycache__` is
cpython-313 while the stated floor is 3.11.

### ✅ What the skill gets right

- **Parse-health warnings are genuinely useful and were correct** — see §4.
- Missing-keyword detection is accurate and every suggestion is correctly hedged with *"if truthful"*.
- *"Calculated experience is below the JD minimum"* fires correctly (~3 yrs vs 4–5 asked).
- Deterministic and reproducible; identical scores across two runs.
- Honest disclaimer that these are simulated, not real ATS numbers.
- Running both a lexical and a semantic backend is the right design.

---

## 4. Real problems it found in our CVs

Every one of the 9 CVs produced the same three parse warnings — these are artefacts of the
`build-cvs.mjs` pandoc + wkhtmltopdf output, not of any single CV:

1. **"Text found in page header/footer region"** — the name + contact block sits in the zone many
   parsers discard. Risk: contact details dropped.
2. **"Table-like content detected"** — the `**Label:** value` skills lines read as tabular.
3. **"Unrecognized section headers: PUBLICATION & LANGUAGES"** — a non-standard heading, so that
   content may be misrouted. (Appears on the 6 CVs I generated; absent from the 3 originals.)

Worth fixing in the CV template regardless of what one thinks of the scoring.

---

## 5. Recommended changes before using this for new CVs

Priority order:

1. **Fix D1** — strip leading `#{1,6}\s*` in `_is_heading()` before matching, and match headings by
   *substring* rather than exact equality. One-line-ish change, largest accuracy gain.
2. **Fix D2** — raise a hard warning (or non-zero exit) when `criteria.total == 0`, and suppress the
   fit badge. Optionally accept indented plain lines as list items.
3. **Fix D3** — have matchers return `None` / `not_applicable` instead of `0.0`, and filter those out.
4. **Recalibrate D4** — drop or down-weight `co_attention`; investigate why the TF-IDF backend's
   `semantic_embedding` is floored; suppress recommendations that fire on 100% of runs.
5. **Fix D5/D6** — correct the path in SKILL.md, move the skill to `.claude/skills/cv-review/`, and
   document the torch download.
6. **Until 1–3 are fixed, normalize JDs on the way in** (md headings → colon headings, indented
   lines → bullets) so scores are comparable across applications.

## 6. How to use it in the workflow

**Use it for:** parse health, missing-keyword coverage, formatting fixes — as a *pre-submission
lint* on a CV we have already decided to send.

**Do not use it for:** deciding which jobs to apply to, or ranking applications. Rank correlation
with considered human judgement is ~0.13.

**Never** action a "required skill missing" recommendation without checking the JD yourself —
until D1 is fixed, many of those skills are preferred, not required, and `profile.md` §14 forbids
adding anything untruthful regardless of what the engine asks for.
