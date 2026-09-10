#!/usr/bin/env python
"""CV evaluation: simulate a company's deterministic ATS scoring of a CV.

The AI never decides whether a CV fits the job — this script mimics applying
to a company and getting its score back. Both scoring techniques always run
(there is no technique selection); the response is always three fields:

    1. TF-IDF scoring      deterministic lexical scoring (ats-engine-tfidf)
    2. Embedding scoring   semantic sentence-transformer scoring
                           (ats-engine-transformer)
    3. Overall score       the mean of the two scores

Both techniques share the SAME parsing layer (the bundled engines' identical
ats/parsing packages): the CV PDF and the JD markdown are parsed identically
for every technique. Improvement directions are deterministic engine
recommendations, never AI opinion.

The full source of both evaluation engines is bundled inside this skill
(engines/), so the script is completely self-contained: it does not depend on
any external copy of the two projects. The engines' optional LLM
qualification evaluation activates only if LLM_API_KEY / OPENAI_API_KEY is
set in the environment (deterministic heuristics otherwise).

Usage:
    python cv_review.py --resume cv.pdf --jd job.md
    python cv_review.py --resume cv.pdf --jd job.md --json -         (JSON to stdout)
    python cv_review.py --resume cv.pdf --jd job.md --json out.json   (JSON to file)

Exit codes: 0 ok | 1 bad input | 2 no engine found | 3 analysis failure
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]      # .../skills/cv-review
BUNDLED_ENGINES = SKILL_DIR / "engines"             # engines bundled inside the skill

ENGINE_DIRS = {"tfidf": "ats-engine-tfidf", "transformer": "ats-engine-transformer"}
OUTPUT_KEYS = {"tfidf": "tfidf", "transformer": "embedding"}

DISCLAIMER = (
    "Scores are deterministic engine estimates simulating what a company's ATS "
    "would compute (TF-IDF lexical vs embedding semantic). A gap between them "
    "shows how sensitive the match is to semantic interpretation; they are not "
    "real-world ATS numbers."
)


# ------------------------------------------------------------------ engines
def find_engines() -> dict[str, Path]:
    """Locate the bundled engine project dirs.

    The complete source of both engine projects lives inside this skill:
    engines/ats-engine-tfidf and engines/ats-engine-transformer. No external
    copy of the projects is ever used.
    """
    found: dict[str, Path] = {}
    for key, name in ENGINE_DIRS.items():
        candidate = (BUNDLED_ENGINES / name).resolve()
        if candidate.is_dir() and (candidate / "ats" / "pipeline.py").exists():
            found[key] = candidate
    return found


def strip_markdown(text: str) -> str:
    """Markdown -> plain text, tuned for the engines' JD parser.

    Headings become plain heading lines, emphasis/link/code syntax is removed,
    fenced-code content is kept (tech stacks matter for matching), list markers
    are normalized to '- '.
    """
    text = text.replace("\r\n", "\n")
    text = re.sub(r"```[a-zA-Z0-9_+-]*\n?", "", text)              # fenced code (keep content)
    text = re.sub(r"`([^`\n]*)`", r"\1", text)                      # inline code
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)               # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)            # links -> link text
    # Headings -> "Heading:" lines. Deleting the '#' alone left them
    # indistinguishable from prose, so the JD parser never saw a section
    # boundary and every requirement fell into one bucket. A trailing colon is
    # the plain-text heading convention the engines' parser already keys on.
    text = re.sub(r"^ {0,3}#{1,6}[ \t]*(.+?)[ \t]*:?[ \t]*$", r"\1:", text, flags=re.M)
    text = re.sub(r"^(\s*)>\s?", r"\1", text, flags=re.M)           # blockquotes
    text = re.sub(r"^(\s*)[*+][ \t]+", r"\1- ", text, flags=re.M)  # * / + bullets -> -
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)                  # bold **
    text = re.sub(r"(?<!\w)__([^_]+)__(?!\w)", r"\1", text)          # bold __
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)       # italic *
    text = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", text)         # italic _
    text = re.sub(r"~~([^~]+)~~", r"\1", text)                      # strikethrough
    text = re.sub(r"^ {0,3}[-*_][ \t]*[-*_ \t]+$", "", text, flags=re.M)  # horizontal rules
    text = re.sub(r"</?[a-zA-Z][^<>]*>", " ", text)                 # html tags
    text = re.sub(r"^\s*\|(.+)\|\s*$", r" \1 ", text, flags=re.M)   # table rows -> text
    text = re.sub(r"[ \t]+\n", "\n", text)                          # trailing spaces
    text = re.sub(r"\n{3,}", "\n\n", text)                          # collapse blank lines
    return text.strip() + "\n"


def analyze_with_engine(engine_key: str, engine_dir: Path, resume: Path, jd_text: str):
    """Run one engine's pipeline. Returns (key, report | None, error | None).

    Each engine's `ats` package is imported in isolation (sys.modules purged
    between runs) so both engines can coexist in one process.
    """
    engine_dir_str = str(engine_dir)
    if engine_dir_str not in sys.path:
        sys.path.insert(0, engine_dir_str)
    for module_name in [m for m in sys.modules if m == "ats" or m.startswith("ats.")]:
        del sys.modules[module_name]
    try:
        pipeline_mod = importlib.import_module("ats.pipeline")
        pipeline = pipeline_mod.ATSPipeline(llm=pipeline_mod.LLMClient(api_key=None))
        jd = pipeline_mod.parse_job_description(jd_text)
        report = pipeline.analyze(resume, jd)
        return engine_key, report, None
    except Exception as exc:  # noqa: BLE001
        return engine_key, None, f"{type(exc).__name__}: {exc}"


# ------------------------------------------------------------------ scoring
def criteria_snapshot(report) -> dict:
    c = report.scores.criteria
    return {
        "met": c.met,
        "total": c.total,
        "undecided": c.undecided,
        "basic_met": c.basic_met,
        "basic_total": c.basic_total,
        "preferred_met": c.preferred_met,
        "preferred_total": c.preferred_total,
    }


def engine_scores(report) -> dict:
    """One engine's report -> score card (engine-native outputs, 0-100 percentage).

    Includes the full scoring breakdown: every matcher score (exact, stemming,
    fuzzy, weighted keywords, ontology, semantic_embedding — the TF-IDF or
    transformer backend, relationship clusters, co-attention, graph fusion,
    cross-encoder, boolean) and every weighted factor.
    """
    s = report.scores
    return {
        "score": round(s.percentage, 1),
        "tier": s.tier,
        "grade": s.grade,
        "stars": s.stars,
        "criteria": criteria_snapshot(report),
        "match_composite": round(s.match_composite, 3),
        "factor_composite": round(s.factor_composite, 3),
        "matchers": {name: round(m.score, 3) for name, m in report.matchers.items()},
        "factors": [
            {"name": f.name, "score": round(f.score, 3), "weight": f.weight}
            for f in report.factors
        ],
    }


def fit_gap_snapshot(report) -> dict:
    fit = report.fit_gap or {}
    return {
        "badge": fit.get("badge"),
        "strengths": list(fit.get("strengths", [])),
        "areas_for_clarification": list(fit.get("areas_for_clarification", [])),
    }


# -------------------------------------------------------------------- main
def build_payload(resume_path: Path, jd_path: Path, engines: dict[str, Path],
                  results: list, errors: list) -> dict:
    scores = {OUTPUT_KEYS[key]: engine_scores(report) for key, report in results}
    available = [scores[key] for key in ("tfidf", "embedding") if key in scores]
    overall = round(sum(s["score"] for s in available) / len(available), 1) if available else 0.0
    first_report = results[0][1]
    return {
        "resume": str(resume_path),
        "jd": str(jd_path),
        "engines_used": [ENGINE_DIRS[key] for key, _ in results],
        "engine_paths": {OUTPUT_KEYS[key]: str(engines[key]) for key, _ in results},
        "engine_errors": [{"engine": ENGINE_DIRS[e["engine"]], "error": e["error"]} for e in errors],
        "scores": {key: scores[key] for key in ("tfidf", "embedding") if key in scores},
        "overall_score": overall,
        "criteria": criteria_snapshot(first_report),
        "fit_gap": fit_gap_snapshot(first_report),
        "parse_warnings": list(first_report.parse_warnings),
        "recommendations": list(first_report.recommendations)[:5],
        "disclaimer": DISCLAIMER,
    }


def render(payload: dict) -> None:
    line = "=" * 74
    print(line)
    print("CV EVALUATION (simulated company scoring)")
    print(line)
    print(f"resume  : {payload['resume']}")
    print(f"jd      : {payload['jd']}")
    print(f"engines : {', '.join(payload['engines_used']) or '(none)'}")
    for err in payload["engine_errors"]:
        print(f"skipped : {err['engine']} ({err['error'][:60]})")
    print()
    labels = [("tfidf", "TF-IDF scoring"), ("embedding", "Embedding scoring")]
    for key, label in labels:
        s = payload["scores"].get(key)
        if s is None:
            continue
        details = f"tier: {s['tier']}"
        if s.get("grade"):
            details += f", grade: {s['grade']}"
        print(f"{label:<20}: {s['score']:5.1f} / 100  ({details})")
    print("-" * 74)
    print(f"{'Overall score':<20}: {payload['overall_score']:5.1f} / 100  (mean of both scores)")
    print()
    criteria = payload["criteria"]
    if criteria and criteria.get("total"):
        print(f"criteria: meets {criteria['met']} of {criteria['total']} "
              f"({criteria['undecided']} undecided)")
    if payload["parse_warnings"]:
        print(f"parse warnings ({len(payload['parse_warnings'])}):")
        for warning in payload["parse_warnings"][:4]:
            print(f"  ! {warning}")
    if payload["recommendations"]:
        print("improvement directions (deterministic, engine-derived):")
        for rec in payload["recommendations"]:
            print(f"  [{rec['priority']}] {rec['text'][:100]}")
    print()
    print(DISCLAIMER)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="CV evaluation: TF-IDF scoring + embedding scoring + overall score")
    parser.add_argument("--resume", required=True, help="CV file (PDF/DOCX/TXT)")
    parser.add_argument("--jd", required=True, help="job description file (Markdown or text)")
    parser.add_argument("--json", help="write JSON report to file ('-' for stdout)")
    args = parser.parse_args()

    resume_path = Path(args.resume)
    jd_path = Path(args.jd)
    if not resume_path.exists():
        print(f"ERROR: resume not found: {resume_path}", file=sys.stderr)
        return 1
    if not jd_path.exists():
        print(f"ERROR: JD file not found: {jd_path}", file=sys.stderr)
        return 1
    jd_text = strip_markdown(jd_path.read_text(encoding="utf-8", errors="replace"))

    engines = find_engines()
    if not engines:
        print(
            "ERROR: bundled engines not found.\n"
            f"Looked for {' / '.join(ENGINE_DIRS.values())} inside the skill's engines/ "
            "directory.\nThe skill installation is damaged - restore the engines/ folder "
            "inside .opencode/skills/cv-review/.",
            file=sys.stderr,
        )
        return 2

    results: list[tuple[str, object]] = []
    errors: list[dict] = []
    for key in ("tfidf", "transformer"):
        if key not in engines:
            continue
        engine_key, report, error = analyze_with_engine(key, engines[key], resume_path, jd_text)
        if report is None:
            errors.append({"engine": engine_key, "error": str(error)})
        else:
            results.append((engine_key, report))

    if not results:
        print(f"ERROR: all engines failed: {errors}", file=sys.stderr)
        return 3

    payload = build_payload(resume_path, jd_path, engines, results, errors)
    render(payload)
    if args.json:
        if args.json == "-":
            print(json.dumps(payload, indent=2, default=str))
        else:
            Path(args.json).write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
            print(f"\nJSON written to {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
