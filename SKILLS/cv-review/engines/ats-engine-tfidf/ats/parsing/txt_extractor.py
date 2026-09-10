"""Section 2 — Plain text extraction (.txt).

API:
    extract_txt(path_or_text) -> TxtExtraction(text, warnings)
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TxtExtraction:
    text: str = ""
    warnings: list[str] = field(default_factory=list)


def extract_txt(source) -> TxtExtraction:
    result = TxtExtraction()
    try:
        if isinstance(source, str) and "\n" in source:
            result.text = source
        else:
            with open(source, encoding="utf-8", errors="replace") as handle:
                result.text = handle.read()
        if not result.text.strip():
            result.warnings.append("Text file is empty")
    except OSError as exc:
        result.warnings.append(f"Cannot read text file: {exc}")
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print(extract_txt(sys.argv[1]).text[:800])
    else:
        print("usage: python txt_extractor.py <file.txt>")
