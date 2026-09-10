"""Section 7 — Chatbot pre-screening (Paradox/Mya/Phenom voice agents).

Research: "conversational qualification, structured answers feed the ATS."
This module converts a knockout questionnaire into a conversational flow and
collects structured answers. With an LLM configured it can paraphrase/re-ask;
without one it walks the script exactly like a rule-based bot.

API:
    ChatbotPrescreen(questions).ask(qid) -> str
    ChatbotPrescreen.submit(qid, answer) -> None
    ChatbotPrescreen.results(knockout_module) -> list[FilterResult]
"""
from __future__ import annotations

from ..hard_filters.knockout_questions import evaluate_knockout, is_auto_rejected, run_knockouts
from ..llm_client import LLMClient
from ..models import FilterResult


class ChatbotPrescreen:
    """Scripted conversational pre-screen over knockout questions."""

    def __init__(self, questions: list[dict], llm: LLMClient | None = None) -> None:
        self.questions = questions
        self.llm = llm if (llm and llm.available) else None
        self.answers: dict[str, object] = {}
        self._index = 0

    def next_question(self) -> dict | None:
        if self._index >= len(self.questions):
            return None
        return self.questions[self._index]

    def submit(self, answer) -> FilterResult:
        """Submit an answer for the current question; returns pass/fail result."""
        question = self.questions[self._index]
        self.answers[question.get("id", f"q{self._index}")] = answer
        result = evaluate_knockout(question=question, answer=answer)
        self._index += 1
        return result

    def results(self) -> list[FilterResult]:
        return run_knockouts(self.questions, self.answers)

    def auto_rejected(self) -> bool:
        return is_auto_rejected(self.results())

    def _paraphrase(self, question_text: str) -> str:
        """LLM paraphrase of the scripted question (falls back to script)."""
        if self.llm and self.llm.available:
            reply = self.llm.chat(
                "Rephrase this screening question in one friendly sentence. Output only the question.",
                question_text,
            )
            if reply:
                return reply.strip()
        return question_text


if __name__ == "__main__":
    questions = [
        {"id": "auth", "type": "yes_no", "pass_values": [True], "category": "knockout"},
        {"id": "years", "type": "number", "min": 3, "category": "knockout"},
    ]
    bot = ChatbotPrescreen(questions)
    while True:
        q = bot.next_question()
        if q is None:
            break
        print("BOT:", q.get("id"))
        bot.submit(True if q["type"] == "yes_no" else 5)
    print("auto-rejected:", bot.auto_rejected())
