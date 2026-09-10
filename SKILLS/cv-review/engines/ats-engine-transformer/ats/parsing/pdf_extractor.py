"""Section 2 — PDF text extraction (pypdf).

Collects both plain text and positioned words (text, x, y, font_size) so that
layout_diagnostics can detect two-column layouts / headers / footers — the
silent CV killers from the research.

API:
    extract_pdf(path_or_bytes) -> PdfExtraction(text, words, n_pages, warnings)
"""
from __future__ import annotations

import io
from dataclasses import dataclass, field

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


@dataclass
class PositionedWord:
    text: str
    x: float
    y: float          # PDF coordinate, origin bottom-left
    font_size: float


@dataclass
class PdfExtraction:
    text: str = ""
    words: list[PositionedWord] = field(default_factory=list)
    page_sizes: list[tuple[float, float]] = field(default_factory=list)  # (width, height) per page
    n_pages: int = 0
    warnings: list[str] = field(default_factory=list)


def extract_pdf(source) -> PdfExtraction:
    """Extract text + positioned chunks from a PDF file path or bytes."""
    if PdfReader is None:
        return PdfExtraction(warnings=["pypdf not installed — run: pip install pypdf"])
    result = PdfExtraction()
    try:
        stream = io.BytesIO(source) if isinstance(source, (bytes, bytearray)) else open(source, "rb")
    except OSError as exc:
        result.warnings.append(f"Cannot open PDF: {exc}")
        return result
    try:
        reader = PdfReader(stream)
        texts: list[str] = []
        for page in reader.pages:
            box = page.mediabox
            result.page_sizes.append((float(box.width), float(box.height)))
            chunks: list[tuple[str, float, float, float]] = []

            def visitor(text, cm, tm, font_dict, font_size, chunks=chunks):
                if text and text.strip():
                    chunks.append((text, tm[4], tm[5], font_size or 0.0))

            page_text = page.extract_text(visitor_text=visitor) or ""
            texts.append(page_text)
            for raw_text, x, y, size in chunks:
                for piece in raw_text.split("\n"):
                    piece = piece.strip()
                    if piece:
                        result.words.append(PositionedWord(piece, x, y, size))
        result.text = "\n".join(texts).strip()
        if not result.text.strip():
            result.warnings.append(
                "No extractable text — likely a scanned/image-only PDF (try OCR). "
                "Some ATS reject these outright."
            )
    except Exception as exc:  # noqa: BLE001
        result.warnings.append(f"PDF extraction failed: {type(exc).__name__}: {exc}")
    finally:
        try:
            if hasattr(stream, "close"):
                stream.close()
        except Exception:  # noqa: BLE001
            pass
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        extraction = extract_pdf(sys.argv[1])
        print(extraction.text[:1500])
        print("warnings:", extraction.warnings)
    else:
        print("usage: python pdf_extractor.py <file.pdf>")
