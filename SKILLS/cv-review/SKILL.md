---
name: cv-review
description: Evaluate a CV/resume (PDF) against a job description (Markdown) by SIMULATING a company's deterministic ATS scoring — the response is always three fields: TF-IDF scoring, embedding (transformer) scoring, and the overall score (mean of both), plus deterministic improvement directions. Use when the user provides a CV and a job description and asks for an evaluation score, a CV review, a resume score, what a company's ATS would say, or how well the CV matches the job.
license: MIT
compatibility: Fully self-contained — both engine projects and the research doc are bundled inside this skill (engines/, references/). Requires Python 3.11+ with scikit-learn and sentence-transformers. Optional LLM (qualification checks) via LLM_API_KEY.
metadata:
  version: "2.1"
  bundled-engines: engines/ats-engine-tfidf, engines/ats-engine-transformer
  research-source: references/ats-cv-scoring-research.md
---

# CV Review — Simulated Company Scoring

**The AI never decides whether the CV fits the job and never chooses a scoring
technique.** The AI's only job is to run the deterministic script — mimicking
applying to the company and getting its score back. Both techniques always run;
the response is always the same three fields:

1. **TF-IDF scoring** — deterministic lexical scoring (`engines/ats-engine-tfidf`)
2. **Embedding scoring** — semantic sentence-transformer scoring (`engines/ats-engine-transformer`)
3. **Overall score** — the mean of the two scores

## The process (three layers)

1. **Parsing layer (shared by both techniques).** The CV (PDF) is parsed into a
   structured resume and the JD (Markdown, as written on the company's website)
   into a structured job description. Both techniques use the SAME parser
   (the engines' `ats/parsing` packages are byte-identical), so both scores see
   identical candidate data.
2. **Scoring layer.** TF-IDF (lexical) and embedding (semantic) always both
   run — company X may score the CV lexically, company Y semantically; the
   three fields cover every case.
3. **Improvement layer.** Deterministic, engine-generated directions (which
   skills need evidence, what to rewrite, formatting fixes) — never AI opinion.

## Workflow

- [ ] 1. Get the CV file path (PDF preferred) from the user. Get the job
      description: a Markdown file path, or pasted text — save pasted text to a
      temp `.md` file first (e.g. `%TEMP%\jd.md`).
- [ ] 2. Execute only the script (no ad-hoc analysis code, no technique flags —
      there is nothing to choose):

```powershell
python .opencode/skills/cv-review/scripts/cv_review.py --resume <cv.pdf> --jd <job.md> --json -
```

- [ ] 3. Report the three fields exactly: **TF-IDF scoring**, **embedding
      scoring**, **overall score** (mean). Frame them as "here is what the
      company's scoring system would return", not as your own judgment.
- [ ] 4. The `--json -` output also carries the full scoring breakdown per
      engine (every matcher score — including `semantic_embedding`, which
      differs between the TF-IDF and transformer backends — and every weighted
      factor), `engine_paths` proving which bundled code ran, criteria
      coverage, fit & gap, parse warnings, and the deterministic improvement
      directions — use them to explain *why* the scores are what they are.
- [ ] 5. If one engine was skipped (missing dependency), say so and report that
      the overall score covers only the available engine.

## Output template

```markdown
## CV Evaluation: <resume> vs <job>

| Field | Score |
|---|---|
| TF-IDF scoring | X / 100 (tier <tier>, grade <grade>) |
| Embedding scoring | Y / 100 (tier <tier>, grade <grade>) |
| **Overall score** | **Z / 100** (mean of both) |

**Criteria coverage**: Meets X of Y qualifications (Z undecided)
**Parse health**: clean / N warnings (summarize the top ones)

### Improvement directions (deterministic, engine-derived)
1. <from the script's recommendations list>

<one-line note: TF-IDF is lexical, embedding is semantic; a gap between them
shows how interpretation-sensitive the match is. These are simulated engine
scores, not real-world ATS numbers.>
```

## Scoring components (all bundled in this skill)

Parsing the PDF and the JD is only the first layer — the scoring itself lives here:

| Component | File |
|---|---|
| **TF-IDF scoring** (lexical backend: TF-IDF vectors + cosine) | `engines/ats-engine-tfidf/ats/matching/embedding_match.py` |
| **Embedding scoring** (semantic backend: sentence-transformers all-MiniLM-L6-v2) | `engines/ats-engine-transformer/ats/matching/embedding_match.py` |
| Optional LLM qualification checks (fit & gap; active only with `LLM_API_KEY`) | `engines/*/ats/matching/llm_qualification.py`, `engines/*/ats/scoring/fit_gap_report.py` |
| Matcher ensemble (both engines): exact, stemming, fuzzy, weighted keywords, ontology, relationship clusters, co-attention, graph fusion, cross-encoder, boolean | `engines/*/ats/matching/*.py` |
| Weighted factors (skills, experience, education, title, certifications...) | `engines/*/ats/factors/*.py` |
| Composite 0-100 percentage (the score the script reports) | `engines/*/ats/scoring/score_combiner.py` |
| Tier / letter grade / stars / criteria | `engines/*/ats/scoring/{tier_classifier,letter_grades,star_rating,criteria_met}.py` |
| Shared parsing layer (identical in both engines) | `engines/*/ats/parsing/` |
| End-to-end pipeline orchestration | `engines/*/ats/pipeline.py` |

## Gotchas

- **Never write ad-hoc code that imports `ats`** (e.g. `from ats.pipeline import
  ATSPipeline`). The engine packages are NOT pip-installed — they only resolve
  inside their own engine directories, so such imports fail with
  `ModuleNotFoundError: ats` anywhere else. Always execute
  `scripts/cv_review.py` (it handles the import isolation itself). Direct
  engine use is only via running its `cli.py` as a script.
- **First transformer-engine run downloads the ~90MB all-MiniLM-L6-v2 model**
  (cached afterwards). A slow first run is normal; don't kill it.
- **Scanned/image PDFs** degrade to parse warnings (OCR needs tesseract +
  poppler binaries). Surface the warnings — they're candidate-actionable.
- **Optional LLM**: without `LLM_API_KEY`/`OPENAI_API_KEY` runs are fully
  deterministic; unverifiable qualification checks come back "undecided" —
  expected behavior, not an error. With a key set, the engines call it for
  qualification evaluation (slower runs).
- **Knockouts dominate in reality**: real ATS auto-reject only via form
  questions, never resume text. If the user mentions screening questions
  (authorization, salary, location), note that they can reject regardless of
  the scores here.
- **Missing engine dependency**: if `sentence-transformers` (or
  `scikit-learn`) isn't installed, that engine is skipped with a `skipped:`
  note and the overall score covers the remaining engine — mention it.
- **Exit codes**: 0 ok | 1 input file missing | 2 no engine found (the bundled
  engines/ folder is missing or damaged — restore it) | 3 all engines failed.
- **Self-contained**: the skill bundles both engine projects under `engines/`
  and the research under `references/`. The engines can also be used directly
  (`python engines/ats-engine-tfidf/cli.py ...`) or tested (`pytest` inside
  either engine folder).
