"""Shared fixtures for the ATS engine test suite."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ats.models import (  # noqa: E402
    Contact,
    DateRange,
    Education,
    Experience,
    JobDescription,
    ParsedResume,
)
from ats.parsing.jd_parser import parse_job_description  # noqa: E402

SAMPLES = PROJECT_ROOT / "samples"
JD_BACKEND = SAMPLES / "jobs" / "jd_backend_engineer.txt"
JD_MARKETING = SAMPLES / "jobs" / "jd_marketing_manager.txt"
RESUME_BACKEND = SAMPLES / "resumes" / "jane_doe_backend.txt"
RESUME_MARKETING = SAMPLES / "resumes" / "bob_smith_marketing.txt"
RESUME_DATA = SAMPLES / "resumes" / "priya_patel_data.txt"
RESUME_STUFFING = SAMPLES / "resumes" / "stuffy_stuffing.txt"


@pytest.fixture(scope="session")  # noqa: F821
def jd_backend() -> JobDescription:
    return parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")  # noqa: F821
def jd_marketing() -> JobDescription:
    return parse_job_description(JD_MARKETING.read_text(encoding="utf-8"))


def make_resume(**overrides) -> ParsedResume:
    resume = ParsedResume(
        raw_text="Engineer with python and docker. Cut latency 40%.",
        sections={
            "skills": "python, docker, kubernetes",
            "experience": "01/2020 - Present Engineer at Acme\n- Cut latency 40% with python",
        },
        contact=Contact(name="Test Person", email="t@x.com", location="Austin, TX"),
        experiences=[
            Experience(
                title="Senior Engineer",
                company="Acme",
                date_range=DateRange(start=(2020, 1), is_current=True),
                bullets=["Cut latency 40% with python and docker"],
            )
        ],
        education=[Education(degree="bachelor", field="Computer Science")],
        skills={"python", "docker", "kubernetes"},
    )
    for key, value in overrides.items():
        setattr(resume, key, value)
    return resume
