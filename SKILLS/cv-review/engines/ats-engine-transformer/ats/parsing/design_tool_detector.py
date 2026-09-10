"""Section 2 — Design-tool PDF & graphics-heavy detection.

Research failures: "Design-tool PDFs (Canva, Illustrator — text stored as
graphical layers)" and "Graphics, skill bars, photos (invisible)".

Reads the PDF's own metadata (Creator/Producer) and counts embedded images —
a Canva/Illustrator export or an image-heavy resume predicts garbled parsing
in most ATS.

API:
    inspect_pdf(path_or_bytes) -> DesignReport(design_tool, image_count, notes)
"""
from __future__ import annotations

import io
from dataclasses import dataclass, field

DESIGN_TOOLS = ["canva", "illustrator", "indesign", "figma", "sketch", "photoshop", "inkscape"]

IMAGE_HEAVY_THRESHOLD = 5


@dataclass
class DesignReport:
    design_tool: str | None = None
    image_count: int = 0
    text_chars: int = 0
    notes: list[str] = field(default_factory=list)


def _metadata_producer(reader) -> str:
    try:
        metadata = reader.metadata or {}
        return str(metadata.get("/Producer", "")) + " " + str(metadata.get("/Creator", ""))
    except Exception:  # noqa: BLE001
        return ""


def _count_images(reader) -> int:
    """Count /Image XObjects across pages (best-effort, never raises)."""
    total = 0
    for page in reader.pages:
        try:
            resources = page.get("/Resources", {}) or {}
            xobjects = resources.get("/XObject", {}) or {}
            for _name, ref in xobjects.items():
                obj = ref.get_object()
                if obj.get("/Subtype") == "/Image":
                    total += 1
        except Exception:  # noqa: BLE001
            continue
    return total


def inspect_pdf(source) -> DesignReport:
    """Inspect a PDF path or bytes for design-tool origin + graphics density."""
    report = DesignReport()
    try:
        from pypdf import PdfReader  # noqa: PLC0415

        stream = io.BytesIO(source) if isinstance(source, (bytes, bytearray)) else open(source, "rb")
        try:
            reader = PdfReader(stream)
            producer = _metadata_producer(reader).lower()
            for tool in DESIGN_TOOLS:
                if tool in producer:
                    report.design_tool = tool
                    report.notes.append(
                        f"Produced with {tool} — text may be stored as graphical layers; "
                        "ATS parsers often extract nothing or garble it"
                    )
                    break
            report.image_count = _count_images(reader)
            if report.image_count >= IMAGE_HEAVY_THRESHOLD:
                report.notes.append(
                    f"{report.image_count} embedded images detected — graphics/skill bars/photos "
                    "are invisible to ATS parsers"
                )
            report.text_chars = sum(len(page.extract_text() or "") for page in reader.pages[:3])
        finally:
            try:
                if hasattr(stream, "close"):
                    stream.close()
            except Exception:  # noqa: BLE001
                pass
    except Exception as exc:  # noqa: BLE001
        report.notes.append(f"design-tool inspection failed: {type(exc).__name__}: {exc}")
    return report


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = inspect_pdf(sys.argv[1])
        print("design_tool:", result.design_tool)
        print("images:", result.image_count)
        print("text_chars (first 3 pages):", result.text_chars)
        for note in result.notes:
            print("!", note)
    else:
        print("usage: python design_tool_detector.py <file.pdf>")
