"""Section 6 — factor tests."""
from __future__ import annotations

from ats.factors.career_trajectory import career_trajectory_factor, career_gaps
from ats.factors.certification_match import certification_match_factor
from ats.factors.education_match import education_match_factor
from ats.factors.evidence_verified_skills import evidence_verified_factor
from ats.factors.location_match import location_match_factor
from ats.factors.skill_overlap import skill_overlap_factor
from ats.factors.years_experience import skill_recency_score, total_years, years_experience_factor
from ats.models import DateRange, Education, Experience, JobDescription, ParsedResume
from tests.conftest import make_resume


class TestSkillOverlap:
    def test_overlap(self):
        result = skill_overlap_factor(
            {"python", "sql", "docker"}, {"python", "sql", "kubernetes"}, {"kafka"}
        )
        assert 0.4 < result.score < 0.8
        assert "kubernetes" in result.evidence["required_missing"]

    def test_perfect(self):
        result = skill_overlap_factor({"python"}, {"python"})
        assert result.score == 1.0


class TestYearsExperience:
    def test_total_years(self):
        resume = make_resume()
        from ats.factors.years_experience import total_years

        assert total_years(resume, today=(2026, 9)) > 5

    def test_meets_requirement(self):
        resume = make_resume()
        result = years_experience_factor(resume, 3)
        assert result.score == 1.0

    def test_below_minimum(self):
        resume = make_resume(experiences=[
            Experience(title="Eng", date_range=DateRange(start=(2024, 1), is_current=True))
        ])
        result = years_experience_factor(resume, 5)
        assert result.score < 0.8

    def test_recency_weighting(self):
        from ats.factors.years_experience import recency_weight

        assert recency_weight(0) > recency_weight(1) > recency_weight(3)


class TestEvidenceVerified:
    def test_demonstrated_beats_listed(self):
        resume = make_resume(
            sections={"skills": "python, sql, kubernetes"},
            experiences=[Experience(
                title="Eng",
                date_range=DateRange(start=(2020, 1), is_current=True),
                bullets=["Cut latency 40% with python and docker"],
            )],
        )
        result = evidence_verified_factor(resume, {"python", "sql", "kubernetes"})
        assert "python" in result.evidence["demonstrated"]
        assert "kubernetes" in result.evidence["listed_only"]
        assert 0.3 < result.score < 0.8


class TestEducation:
    def test_meets(self):
        resume = make_resume()
        jd = JobDescription(education_level="bachelor")
        assert education_match_factor(resume, jd).score == 1.0

    def test_below(self):
        resume = make_resume()
        jd = JobDescription(education_level="master")
        assert education_match_factor(resume, jd).score < 1.0


class TestCertification:
    def test_acronym_or_full(self):
        from ats.factors.certification_match import certification_match_factor

        resume = make_resume(raw_text="Has PMP and Certified Public Accountant")
        jd = JobDescription(raw_text="Requires Certified Public Accountant or PMP")
        result = certification_match_factor(resume, jd.raw_text)
        assert result.score == 1.0

    def test_missing_cert(self):
        from ats.factors.certification_match import certification_match_factor

        resume = make_resume(raw_text="No certifications yet")
        jd = JobDescription(raw_text="Requires PMP certification")
        assert certification_match_factor(resume, jd.raw_text).score == 0.0


class TestLocation:
    def test_match(self):
        resume = make_resume()
        jd = JobDescription(location="Austin, TX")
        assert location_match_factor(resume, jd).score == 1.0

    def test_remote(self):
        resume = make_resume()
        jd = JobDescription(location="Anywhere", remote_allowed=True)
        assert location_match_factor(resume, jd).score == 1.0


class TestCareerTrajectory:
    def test_progression(self):
        resume = make_resume(experiences=[
            Experience(title="Senior Engineer", date_range=DateRange(start=(2020, 1), is_current=True)),
            Experience(title="Engineer", date_range=DateRange(start=(2017, 1), end=(2019, 12))),
        ])
        result = career_trajectory_factor(resume)
        assert "progression" in result.detail

    def test_gap_detection(self):
        resume = make_resume(experiences=[
            Experience(title="Engineer", date_range=DateRange(start=(2020, 1), end=(2020, 6))),
            Experience(title="Engineer", date_range=DateRange(start=(2022, 1), end=(2023, 1))),
        ])
        assert career_gaps_safe(resume)  # 2020-07 .. 2020-12 = 6+ month gap


def career_gaps_safe(resume):
    from ats.factors.career_trajectory import career_gaps

    return career_gaps(resume.experiences)


class TestYearsExperienceFactor:
    def test_calculation(self):
        resume = make_resume()
        result = years_experience_factor(resume, 3)
        assert result.score == 1.0
