"""Section 2 — parsing tests."""
from __future__ import annotations

from ats.parsing.contact_extractor import extract_contact
from ats.parsing.date_parser import normalize_date, parse_date, parse_date_range, range_to_months
from ats.parsing.docx_extractor import extract_docx
from ats.parsing.education_extractor import extract_education
from ats.parsing.certifications_extractor import extract_certifications
from ats.parsing.experience_extractor import extract_experiences
from ats.parsing.section_detector import detect_sections
from ats.parsing.skills_extractor import build_variation_map, find_skills, load_taxonomy
from ats.parsing.jd_parser import parse_job_description
from tests.conftest import JD_BACKEND, RESUME_BACKEND, RESUME_DATA


class TestDateParser:
    def test_mm_slash_yyyy(self):
        assert parse_date("01/2020") == (2020, 1)

    def test_month_name(self):
        assert parse_date("Jan 2020") == (2020, 1)
        assert parse_date("SEPTEMBER 2019") == (2019, 9)

    def test_year_only(self):
        assert parse_date("2020") == (2020, 1)

    def test_range(self):
        rng = parse_date_range("01/2020 - 12/2022")
        assert rng.start == (2020, 1) and rng.end == (2022, 12)

    def test_present(self):
        rng = parse_date_range("2020 - Present")
        assert rng.is_current and rng.end is None

    def test_normalize(self):
        assert normalize_date((2020, 3)) == "03/2020"

    def test_tenure_months(self):
        rng = parse_date_range("Jan 2018 – Dec 2019")
        assert range_to_months(rng) == 23


class TestSections:
    def test_known_headers(self):
        sections, unknown = detect_sections(
            ["SUMMARY", "text", "WORK EXPERIENCE", "job text", "SKILLS", "python"]
        )
        assert "summary" in sections and "experience" in sections and "skills" in sections
        assert sections["skills"] == "python"

    def test_unknown_header_flagged(self):
        sections, unknown = detect_sections(["MY JOURNEY", "some story", "SKILLS", "python"])
        assert "MY JOURNEY" in unknown
        assert "some story" not in sections.get("skills", "")


class TestContact:
    def test_all_fields(self):
        lines = [
            "Jane Doe",
            "jane.doe@gmail.com | (512) 555-0134",
            "linkedin.com/in/janedoe",
            "Austin, TX 78701",
        ]
        contact = extract_contact(lines)
        assert contact.name == "Jane Doe"
        assert contact.email == "jane.doe@gmail.com"
        assert contact.phone == "(512) 555-0134"
        assert contact.location == "Austin, TX"


class TestExperience:
    def test_extraction_from_sample(self):
        text = RESUME_BACKEND.read_text(encoding="utf-8")
        from ats.parsing.experience_extractor import extract_experiences

        experiences = extract_experiences(text)
        assert len(experiences) == 3
        assert experiences[0].title == "Senior Backend Engineer"
        assert experiences[0].date_range.is_current
        assert len(experiences[0].bullets) >= 3


class TestEducation:
    def test_degrees(self):
        text = "EDUCATION\nM.S. Computer Science, University of Texas, 2019\nB.Tech IT - IIT Delhi, 2015"
        education = extract_education(text)
        assert {ed.degree for ed in education} == {"master", "bachelor"}
        assert any(ed.institution == "University of Texas" for ed in education)


class TestCerts:
    def test_acronym_and_full_form(self):
        certs = extract_certifications("PMP and Certified Public Accountant and CKA")
        acronyms = {c.acronym for c in certs}
        assert {"PMP", "CPA", "CKA"} <= acronyms


class TestSkills:
    def test_variation_mapping(self):
        variation_map = build_variation_map(load_taxonomy())
        found = find_skills("Skilled in ReactJS, k8s and Postgres", variation_map)
        assert {"react", "kubernetes", "sql"} <= found

    def test_taxonomy_loads(self):
        taxonomy = load_taxonomy()
        assert "python" in taxonomy["skills"]


class TestJDParser:
    def test_backend_jd(self):
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        assert jd.title and "Backend" in jd.title
        assert jd.min_years == 5
        assert {"python", "sql", "docker", "kubernetes", "aws"} <= jd.required_skills
        assert {"kafka", "terraform"} <= jd.preferred_skills
        assert jd.education_level == "bachelor"
        assert jd.salary_ceiling == 150000
        assert jd.industry == "fintech"
        assert len(jd.qualifications) >= 8
        assert any(q.kind == "preferred" for q in jd.qualifications)

    def test_remote_detection(self):
        jd = parse_job_description("Requirements:\n- python\nRemote friendly team")
        assert jd.remote_allowed

    def test_extract_qualifications_only_list_items(self):
        from ats.parsing.jd_parser import extract_qualifications

        jd_text = "Header prose\n\nREQUIREMENTS\n- Strong Python skills required\n- SQL experience\n\nProse footer."
        quals = extract_qualifications(jd_text)
        assert all("Prose" not in q.text for q in quals)
        assert len(quals) == 2


class TestDocx:
    def test_missing_file_warning(self):
        result = extract_docx_safe()
        assert result.warnings


def extract_docx_safe():
    from ats.parsing.docx_extractor import extract_docx

    return extract_docx("no_such_file.docx")


class TestPdf:
    def test_missing_file_warning(self):
        from ats.parsing.pdf_extractor import extract_pdf

        result = extract_pdf("definitely_missing.pdf")
        assert result.warnings and not result.text
