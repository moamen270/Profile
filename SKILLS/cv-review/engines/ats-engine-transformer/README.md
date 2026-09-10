# ats-engine-transformer

Full implementation of the researched ATS universal pipeline in Python —
**one file per method**, organized by research section. This variant uses
**sentence-transformers (all-MiniLM-L6-v2) + cosine similarity** for the
semantic-matching tier (~90MB model download on first run). The sister project
`ats-engine-tfidf` implements the identical API with scikit-learn TF-IDF
vectors (zero downloads, deterministic, faster).

```
Hard filters → Parse → Normalize → Match → Score/Rank → Human review
```

## Install & run

```powershell
pip install -r requirements.txt
python cli.py analyze samples\resumes\jane_doe_backend.txt --jd samples\jobs\jd_backend_engineer.txt
python cli.py rank samples\resumes --jd samples\jobs\jd_backend_engineer.txt
python cli.py parse samples\resumes\priya_patel_data.txt
python cli.py jd samples\jobs\jd_backend_engineer.txt
python cli.py knockout --config data\knockout_config.json --answers samples\answers_jane.json
```

## Mapping: research section → files

### §1 Hard filters (run BEFORE parsing; the ONLY auto-reject path) — `ats/hard_filters/`
| File | Research point |
|---|---|
| `knockout_questions.py` | Taleo CSW / Greenhouse Auto-reject / Ashby rules (yes_no, single/multi-select, number) |
| `salary_ceiling.py` | salary expectation above preset ceiling = instant reject |
| `min_years_form.py` | min years taken from the FORM, never calculated from the CV |
| `work_authorization.py` | work authorization / sponsorship knockout |
| `location_filter.py` | location + willingness-to-relocate knockout |

### §2 CV parsing & structuring — `ats/parsing/`
| File | Research point |
|---|---|
| `pdf_extractor.py` / `docx_extractor.py` / `txt_extractor.py` | text extraction with positioned words (pypdf) |
| `ocr_extractor.py` | image-only / scanned PDFs (pytesseract; graceful fallback) |
| `layout_diagnostics.py` | two-column layouts, header/footer text, tables — the silent CV killers |
| `design_tool_detector.py` | Canva/Illustrator/design-tool PDFs + embedded-image density (graphics are invisible to ATS) |
| `section_detector.py` | headers dict; "Work Experience" works, "My Journey" flagged |
| `contact_extractor.py` | contact info |
| `date_parser.py` | MM/YYYY normalization, "Present", tenure months |
| `experience_extractor.py` | employers/titles/date-ranges/bullets; tolerates dates before employer names |
| `education_extractor.py` | degrees/fields/institutions |
| `skills_extractor.py` | taxonomy-driven skills (variation → canonical) |
| `certifications_extractor.py` | certs — acronym AND full form |
| `jd_parser.py` | JD structuring: required/preferred skills, min years, qualifications list |

### §3 Entity normalization — `ats/normalization/`
| File | Research point |
|---|---|
| `taxonomy.py` | skills taxonomy / canonical entities (Workday Skills Cloud style) |
| `synonym_normalizer.py` | CPA ↔ Certified Public Accountant (legacy Taleo fails here) |
| `acronym_expander.py` | k8s → Kubernetes inline expansion |
| `relationship_inference.py` | Docker + Kubernetes → cloud infrastructure capability |
| `unique_concepts.py` | unique-concept counting; keyword-stuffing detection |

### §4 Matching spectrum — `ats/matching/`
| File | Research point |
|---|---|
| `exact_match.py` | literal matching (legacy Taleo) |
| `boolean_search.py` | AND/OR/NOT with parens + quoted phrases |
| `stemmer.py` | Lever stemming (collaborate/collaborated/collaboration) |
| `fuzzy_match.py` | Levenshtein ≤ 2, pure Python |
| `weighted_keywords.py` | Taleo ACE weighted scoring, section-boosted keywords |
| `ontology_match.py` | taxonomy entity comparison (Workday/Phenom) |
| `embedding_match.py` | ★ **sentence-transformers + cosine (this project)** / TF-IDF (sister `ats-engine-tfidf`) |
| `relationship_clusters.py` | related-concept clusters (Workday HiredScore) |
| `llm_qualification.py` | per-qualification Fit & Gap with evidence citations; "undecided" without API key |
| `co_attention.py` | academic co-attention alignment (APJFNN/PJFCANN-inspired, deterministic) |
| `graph_fusion.py` | personalized-PageRank skill-graph fusion (academic graph-based fit) |
| `cross_encoder.py` | pairwise interaction re-ranking (BERT cross-encoder pattern) |
| `learning_to_rank.py` | learning-to-rank over historical application outcomes (pure-Python logistic ranker) |

### §5 Scoring output formats — `ats/scoring/`
| File | Platform |
|---|---|
| `percentage_score.py` | Taleo ACE points → %, tiers, asset thresholds |
| `tier_classifier.py` | Greenhouse 5 tiers + recruiter calibration |
| `letter_grades.py` | Workday HiredScore A/B/C/D |
| `criteria_met.py` | Ashby "Meets X of Y" + undecided tracking |
| `star_rating.py` | Oracle 0-3 stars, 4 dimensions |
| `stack_rank.py` | SuccessFactors pool ranking |
| `fit_gap_report.py` | Lever TALENT FIT badge + narrative |
| `score_combiner.py` | ensemble blend (matchers 55% / factors 45%) + stuffing penalty |

### §6 Scored factors (one file each) — `ats/factors/`
`skill_overlap.py` · `years_experience.py` (recency-weighted) · `title_match.py` ·
`evidence_verified_skills.py` · `education_match.py` · `certification_match.py` ·
`location_match.py` · `industry_alignment.py` · `career_trajectory.py` (gaps,
progression, tenure) · `section_placement.py` · `competency_ratings.py` (Taleo
proficiency model) · `engagement_signals.py` (Phenom) · `historical_patterns.py`
(Eightfold)

### §7 Adjacent systems — `ats/adjacent/`
`rediscovery.py` (silver medalists) · `skills_assessment.py` (pipeline-stage
quizzes) · `chatbot_prescreen.py` (conversational knockouts) ·
`video_interview.py` (HireVue-style transcript competency scoring,
Top/Middle/Bottom bands, BARS anchors) · `psychometrics.py` (pymetrics-style
trait benchmark matching) · `sourcing_rank.py` (LinkedIn Recruiter personalized
relevance: query match + team context + similar-search + history - spam penalty)

### §8 Legal compliance — `ats/compliance/`
`anonymizer.py` (Lever: strip PII/demographics/military before LLM) ·
`bias_audit.py` (4/5ths disparate-impact rule, LL144/AEDT) ·
`human_review_router.py` (AI never rejects; opt-out → manual review) ·
`protected_attribute_guard.py` (Greenhouse-style: blocks/warns on
protected-attribute proxies in JDs)

### Pipeline & review
`ats/pipeline.py` (orchestrator) · `ats/review/review_queue.py` (tiered
recruiter queue) · `ats/models.py` (shared dataclasses) · `ats/llm_client.py`
(optional OpenAI-compatible adapter)

## LLM mode (optional)

```powershell
$env:LLM_API_KEY = "sk-..."
$env:LLM_BASE_URL = "https://api.openai.com/v1"   # or any OpenAI-compatible endpoint
$env:LLM_MODEL = "gpt-4o-mini"
```

Without a key, LLM-based criteria return **"undecided"** (Ashby behavior) and
route to human review — never a fabricated rejection.

## Tests

```powershell
python -m pytest tests -q          # 138 tests
```

The semantic-embedding test downloads all-MiniLM-L6-v2 from HuggingFace on
first run (cached afterwards).

## Notes
- OCR requires the [tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  and poppler binaries on Windows; the engine degrades gracefully without them.
- Research note: real enterprise ATS do NOT compute a single 0-100 score —
  this engine provides one because consumers expect it, but the honest outputs
  are the tiers, grades, stars, and criteria counts.
