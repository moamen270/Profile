"""Section 2 — OCR fallback for scanned / image-only PDFs.

Research: "Image-only / scanned PDFs — some OCR, some reject." We try pytesseract
(pdf2image needs the poppler binary; tesseract needs the tesseract binary).
If either binary or package is missing we return ok=False with a clear message —
graceful degradation, never a crash.

API:
    ocr_pdf(path) -> OcrResult(ok, text, warning)
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OcrResult:
    ok: bool = False
    text: str = ""
    warnings: list[str] = field(default_factory=list)


def ocr_pdf(path: str, dpi: int = 200, language: str = "eng") -> OcrResult:
    try:
        import pytesseract  # noqa: PLC0415
        from pdf2image import convert_from_path  # noqa: PLC0415
    except ImportError as exc:
        return OcrResult(
            ok=False,
            warnings=[f"OCR dependencies missing ({exc}). Install: pip install pytesseract pdf2image "
                      "+ tesseract & poppler binaries"],
        )
    try:
        pages = convert_from_path(path, dpi=dpi)
        text = "\n".join(pytesseract.image_to_string(page, lang=language) for page in pages)
        if not text.strip():
            return OcrResult(ok=False, warnings=["OCR produced no text — document may be blank/graphics-only"])
        return OcrResult(ok=True, text=text)
    except Exception as exc:  # noqa: BLE001
        return OcrResult(
            ok=False,
            warnings=[f"OCR failed: {type(exc).__name__}: {exc}. "
                      "Image-only PDFs often get silently dropped by real ATS."],
        )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = ocr_pdf(sys.argv[1])
        print("ok:", result.ok)
        for warning in result.warnings:
            print("warning:", warning)
        print(result.text[:1000])
    else:
        print("usage: python ocr_extractor.py <scanned.pdf>")
