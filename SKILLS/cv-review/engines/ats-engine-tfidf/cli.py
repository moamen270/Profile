"""Command-line interface for the ATS engine.

Commands:
    parse <resume>                     parsing debug + layout diagnostics
    analyze <resume> --jd <jd>         full pipeline report for one candidate
    rank <resumes_dir> --jd <jd>       stack-rank a candidate pool
    knockout --config <json> --answers <json>   run the knockout questionnaire
    jd <jd_file>                       JD structuring debug
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ats.llm_client import LLMClient
from ats.models import CandidateRecord
from ats.pipeline import ATSPipeline
from ats.parsing.jd_parser import parse_job_description


def _load_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _load_jd(path: str):
    return parse_job_description(_load_text(path))


def cmd_parse(args) -> int:
    pipeline = ATSPipeline()
    parsed = pipeline.parse_resume(args.resume)
    print(f"=== PARSE: {Path(args.resume).name} ===")
    print(f"contact: {parsed.contact}")
    print(f"sections: {sorted(parsed.sections)}")
    print(f"experiences: {len(parsed.experiences)}")
    for experience in parsed.experiences:
        print(f"  - {experience.title} @ {experience.company} [{experience.date_range.raw}] "
              f"({len(experience.bullets)} bullets)")
    print(f"education: {[(e.degree, e.field) for e in parsed.education]}")
    print(f"certifications: {[c.acronym for c in parsed.certifications]}")
    print(f"skills ({len(parsed.skills)}): {sorted(parsed.skills)}")
    if parsed.layout:
        print(f"layout: two_column={parsed.layout.two_column} "
              f"header_footer={len(parsed.layout.header_footer_text)} "
              f"table_lines={parsed.layout.table_like_lines}")
    if parsed.warnings:
        print("warnings:")
        for warning in parsed.warnings:
            print(f"  ! {warning}")
    return 0


def cmd_jd(args) -> int:
    jd = _load_jd(args.jd_file)
    print(f"=== JD: {args.jd_file} ===")
    print(f"title: {jd.title}")
    print(f"min_years: {jd.min_years}")
    print(f"education: {jd.education_level} in {jd.education_field}")
    print(f"location: {jd.location} (remote={jd.remote_allowed})")
    print(f"salary ceiling: {jd.salary_ceiling}")
    print(f"industry: {jd.industry}")
    print(f"required skills: {sorted(jd.required_skills)}")
    print(f"preferred skills: {sorted(jd.preferred_skills)}")
    print(f"qualifications ({len(jd.qualifications)}):")
    for qualification in jd.qualifications:
        print(f"  [{qualification.kind}] {qualification.text}")
    return 0


def cmd_analyze(args) -> int:
    pipeline = ATSPipeline(LLMClient())
    jd = _load_jd(args.jd)
    form_answers = json.loads(Path(args.answers).read_text()) if args.answers else None
    report = pipeline.analyze(args.resume, jd, form_answers,
                              candidate=CandidateRecord("c1", Path(args.resume).stem))

    print(f"=== ANALYSIS: {Path(args.resume).name} vs {args.jd} ===")

    print("\n-- Stage 1: Hard filters (knockout) --")
    if report.auto_rejected:
        for result in report.knockout:
            print(f"  {'PASS' if result.passed else 'FAIL'} {result.name}: {result.reason}")
        print("  >>> AUTO-REJECTED (knockout form question) — pipeline stops here")
        return 0
    print("  no knockout failures" if report.knockout else "  no form answers — filters skipped")

    print(f"\n-- Stage 2: Parse ({len(report.parse_warnings)} warnings) --")
    for warning in report.parse_warnings:
        print(f"  ! {warning}")

    print("\n-- Stage 3: Normalize --")
    print(f"  canonical skills: {sorted(report.normalized_skills)}")
    for capability, evidence in report.inferred_capabilities.items():
        print(f"  capability: {capability} <- {evidence}")
    if report.stuffing_hits:
        print(f"  STUFFING: {report.stuffing_hits}")

    print("\n-- Stage 4: Match --")
    for technique, result in report.matchers.items():
        print(f"  {technique:22} {result.score:6.1%}  {result.notes[:60]}")

    print("\n-- Stage 5: Factors --")
    for factor in sorted(report.factors, key=lambda f: -f.weight):
        print(f"  {factor.name:26} {factor.score:6.1%} (w={factor.weight}) {factor.detail[:70]}")

    scores = report.scores
    print("\n-- Stage 5: Scores --")
    print(f"  Percentage:      {scores.percentage}%")
    print(f"  Tier:            {scores.tier}")
    print(f"  Grade:           {scores.grade}")
    print(f"  Stars:           {scores.stars}")
    print(f"  Criteria:        Meets {scores.criteria.met} of {scores.criteria.total} "
          f"({scores.criteria.undecided} undecided)")
    print(f"  Composites:      match={scores.match_composite} factor={scores.factor_composite}")
    print(f"  Fit narrative:   badge={report.fit_gap.get('badge')}")
    for strength in report.fit_gap.get("strengths", []):
        print(f"    + {strength}")
    for area in report.fit_gap.get("areas_for_clarification", []):
        print(f"    ? {area}")

    print("\n-- Stage 6: Route --")
    print(f"  {report.route.upper()}" + ("  (undecided criteria -> human review)" if report.route != "review" else ""))

    print("\n-- Recommendations (beyond the score) --")
    for rec in report.recommendations:
        marker = {"high": "!!", "medium": " +", "low": " +"}[rec["priority"]]
        print(f"  [{rec['priority']:6}] {rec['audience']:<9} ({rec['source']}): {rec['text']}")
    if not report.recommendations:
        print("  none — profile aligns with the job description")
    return 0


def cmd_rank(args) -> int:
    pipeline = ATSPipeline(LLMClient())
    jd = _load_jd(args.jd)
    resumes = sorted(Path(args.resumes_dir).glob("*.txt"))
    candidates = [CandidateRecord(path.stem, path.stem.replace("_", " ").title(), resume_path=str(path))
                  for path in resumes]
    if not candidates:
        print(f"no .txt resumes found in {args.resumes_dir}")
        return 1
    ranked = pipeline.rank_pool(candidates, jd)

    print(f"=== STACK RANK: {len(candidates)} candidates vs {args.jd} ===")
    for entry in ranked:
        print(f"  #{entry.rank} {entry.candidate.name:20} {entry.score.percentage:5.1f}%  "
              f"{entry.score.tier:20} {entry.score.grade}  route={entry.route}")
    return 0


def cmd_knockout(args) -> int:
    from ats.hard_filters.knockout_questions import is_auto_rejected, run_knockouts

    config = json.loads(Path(args.config).read_text())
    answers = json.loads(Path(args.answers).read_text())
    results = run_knockouts(config.get("questions", []), answers)
    print("=== KNOCKOUT QUESTIONNAIRE ===")
    for result in results:
        print(f"  {'PASS' if result.passed else 'FAIL'} {result.name}: {result.reason}")
    print("auto-rejected:", is_auto_rejected(results))
    return 0 if not is_auto_rejected(results) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="ATS scoring engine (TF-IDF backend)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("parse", help="parse a resume and show diagnostics")
    p.add_argument("resume")
    p.set_defaults(func=cmd_parse)

    p = sub.add_parser("jd", help="show structured JD")
    p.add_argument("jd_file")
    p.set_defaults(func=cmd_jd)

    p = sub.add_parser("analyze", help="full pipeline report")
    p.add_argument("resume")
    p.add_argument("--jd", required=True)
    p.add_argument("--answers", help="JSON file with form answers (knockouts)")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("rank", help="stack-rank a pool of .txt resumes")
    p.add_argument("resumes_dir")
    p.add_argument("--jd", required=True)
    p.set_defaults(func=cmd_rank)

    p = sub.add_parser("knockout", help="run knockout questionnaire")
    p.add_argument("--config", required=True)
    p.add_argument("--answers", required=True)
    p.set_defaults(func=cmd_knockout)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
