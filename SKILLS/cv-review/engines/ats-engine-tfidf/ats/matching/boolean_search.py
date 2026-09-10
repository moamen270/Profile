"""Section 4 — Boolean search (recruiter-driven AND/OR/NOT queries).

Used by all ATS. Supports parentheses, quoted phrases, and NOT.
Example:  ("project manager" OR scrum) AND agile NOT marketing

API:
    evaluate(query, text) -> bool
    matched_terms(query, text) -> set[str]
"""
from __future__ import annotations

import re

_TOKEN_RE = re.compile(r'\(|\)|"[^"]*"|[^\s()"]+')
_STOP = {"and", "or", "not"}


def _tokenize(query: str) -> list[str]:
    return [t for t in _TOKEN_RE.findall(query) if t.strip()]


def _term_hit(term: str, text_lower: str) -> bool:
    term = term.strip().lower()
    if term.startswith('"') and term.endswith('"') and len(term) > 2:
        return term[1:-1] in text_lower
    return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text_lower) is not None


class _Parser:
    def __init__(self, tokens: list[str], text_lower: str) -> None:
        self.tokens = tokens
        self.pos = 0
        self.text = text_lower

    def parse(self) -> bool:
        value = self.expr()
        return bool(value)

    def expr(self) -> bool:
        value = self.term()
        while self.peek() and self.peek().lower() == "or":
            self.next_token()
            rhs = self.term()
            value = value or rhs
        return value

    def term(self) -> bool:
        value = self.factor()
        while self.peek() and (self.peek().lower() == "and" or self.peek() not in (")",) and self.peek().lower() != "or"):
            if self.peek().lower() == "and":
                self.next_token()
            rhs = self.factor()
            value = value and rhs
        return value

    def factor(self) -> bool:
        token = self.next_token()
        if token is None:
            return True
        if token == "(":
            value = self.expr()
            if self.peek() == ")":
                self.next_token()
            return value
        if token.lower() == "not":
            return not self.factor()
        return _term_hit(token, self.text)

    def peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next_token(self) -> str | None:
        token = self.peek()
        if token is not None:
            self.pos += 1
        return token


def evaluate(query: str, text: str) -> bool:
    parser = _Parser(_TOKEN_RE.findall(query), text.lower())
    return parser.parse()


def matched_terms(query: str, text: str) -> set[str]:
    text_lower = text.lower()
    return {
        token.lower().strip('"')
        for token in _TOKEN_RE.findall(query)
        if token.lower() not in _STOP and token not in ("(", ")") and _term_hit(token, text_lower)
    }


if __name__ == "__main__":
    q = '("project manager" OR scrum) AND agile NOT marketing'
    resume = "Agile scrum master with PMP."
    print(evaluate(q, "Agile scrum master with PMP"))     # True
    print(evaluate(q, "Agile marketer"))                  # False
    print(sorted(matched_terms(q, "Agile scrum master with PMP")))
