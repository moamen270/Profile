"""Shared data models for the ATS engine.

Every stage of the universal pipeline (Hard filters -> Parse -> Normalize ->
Match -> Score/Rank -> Human review) exchanges these structures.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class DateRange:
    """Normalized date range. Months are 1-12; None means unparsed."""
    start: Optional[tuple[int, int]] = None      # (year, month)
    end: Optional[tuple[int, int]] = None
    raw: str = ""
    is_current: bool = False


@dataclass
class Contact:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    location: Optional[str] = None


@dataclass
class Experience:
    title: Optional[str] = None
    company: Optional[str] = None
    date_range: DateRange = field(default_factory=DateRange)
    bullets: list[str] = field(default_factory=list)
    raw: str = ""


@dataclass
class Education:
    degree: Optional[str] = None          # e.g. "bachelor", "master", "phd"
    raw_degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[int] = None


@dataclass
class Certification:
    name: str = ""
    acronym: Optional[str] = None
    raw: str = ""


@dataclass
class LayoutReport:
    """Diagnostics about how 'ATS-hostile' the source document is (research section 2)."""
    two_column: bool = False
    header_footer_text: list[str] = field(default_factory=list)
    tiny_fonts: int = 0
    table_like_lines: int = 0
    notes: list[str] = field(default_factory=list)


@dataclass
class ParsedResume:
    raw_text: str = ""
    sections: dict[str, str] = field(default_factory=dict)   # section name -> text
    contact: Contact = field(default_factory=Contact)
    experiences: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    skills: set[str] = field(default_factory=set)             # canonical skills
    skill_locations: dict[str, list[str]] = field(default_factory=dict)  # skill -> sections found in
    certifications: list[Certification] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    layout: Optional[LayoutReport] = None
    source_file: Optional[str] = None


@dataclass
class Qualification:
    """One basic/preferred qualification lifted from the JD (Workday 'Fit & Gap' / Ashby style)."""
    text: str
    kind: str = "basic"          # "basic" | "preferred"
    source: str = "jd"           # "jd" | "form"


@dataclass
class CriterionResult:
    qualification: Qualification
    status: str = "undecided"    # "met" | "not_met" | "undecided"
    evidence: str = ""
    method: str = "heuristic"    # "heuristic" | "llm"


@dataclass
class JobDescription:
    raw_text: str = ""
    title: Optional[str] = None
    required_skills: set[str] = field(default_factory=set)    # canonical
    preferred_skills: set[str] = field(default_factory=set)   # canonical
    qualifications: list[Qualification] = field(default_factory=list)
    min_years: Optional[int] = None
    education_level: Optional[str] = None
    education_field: Optional[str] = None
    location: Optional[str] = None
    remote_allowed: bool = False
    salary_ceiling: Optional[int] = None
    industry: Optional[str] = None
    keywords: dict[str, float] = field(default_factory=dict)  # term -> weight (matching/weighted_keywords)
    source_file: Optional[str] = None


@dataclass
class FilterResult:
    name: str
    passed: bool
    reason: str = ""
    category: str = "filter"     # "knockout" | "filter"


@dataclass
class MatchResult:
    technique: str
    score: float                 # 0..1
    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    evidence: Any = None
    notes: str = ""
    recommendation: str = ""     # actionable improvement hint ("" if n/a)


@dataclass
class FactorResult:
    name: str
    score: float                 # 0..1
    weight: float
    evidence: Any = None
    detail: str = ""
    recommendation: str = ""     # actionable improvement hint ("" if n/a)


@dataclass
class CriterionSummary:
    met: int = 0
    total: int = 0
    basic_met: int = 0
    basic_total: int = 0
    preferred_met: int = 0
    preferred_total: int = 0
    undecided: int = 0
    results: list[CriterionResult] = field(default_factory=list)


@dataclass
class ScoreResult:
    percentage: float = 0.0
    tier: str = ""
    grade: str = ""
    stars: dict[str, int] = field(default_factory=dict)       # dimension -> 0..3
    criteria: CriterionSummary = field(default_factory=CriterionSummary)
    match_composite: float = 0.0
    factor_composite: float = 0.0
    flags: list[str] = field(default_factory=list)


@dataclass
class CandidateRecord:
    """A candidate in a pool (for stack ranking / rediscovery)."""
    candidate_id: str
    name: str
    resume_path: Optional[str] = None
    parsed_resume: Optional[ParsedResume] = None
    form_answers: dict[str, Any] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)        # e.g. {"previous_stage": "offer", "group": "A"}


@dataclass
class RankedCandidate:
    rank: int
    candidate: CandidateRecord
    score: ScoreResult
    route: str = "review"        # review | needs_manual_review | rejected (knockout only)
    top_evidence: list[str] = field(default_factory=list)


@dataclass
class AnalysisReport:
    """Full output of one candidate run through the pipeline."""
    candidate: Optional[CandidateRecord] = None
    knockout: list[FilterResult] = field(default_factory=list)
    auto_rejected: bool = False
    parse_warnings: list[str] = field(default_factory=list)
    normalized_skills: set[str] = field(default_factory=set)
    inferred_capabilities: dict[str, list[str]] = field(default_factory=dict)
    stuffing_hits: list[tuple[str, int]] = field(default_factory=list)
    matchers: dict[str, MatchResult] = field(default_factory=dict)
    factors: list[FactorResult] = field(default_factory=list)
    scores: ScoreResult = field(default_factory=ScoreResult)
    fit_gap: dict[str, Any] = field(default_factory=dict)
    compliance: dict[str, Any] = field(default_factory=dict)
    recommendations: list[dict] = field(default_factory=list)   # {source, priority, audience, text}
    route: str = "review"
