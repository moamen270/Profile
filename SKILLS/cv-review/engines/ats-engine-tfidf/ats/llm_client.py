"""Optional LLM adapter (research section 4: LLM qualification evaluation).

Provider-agnostic, OpenAI-compatible chat-completions client driven by env vars:

    LLM_API_KEY    (required to activate)
    LLM_BASE_URL   (default: https://api.openai.com/v1)
    LLM_MODEL      (default: gpt-4o-mini)

Without LLM_API_KEY the client is "unavailable"; LLM-based methods degrade
gracefully to heuristic mode and criteria come back "undecided" (exactly the
Ashby behavior research describes) instead of crashing.
"""
from __future__ import annotations

import json
import os
from typing import Any, Optional

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


class LLMClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.base_url = (base_url or os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")
        self.timeout = timeout
        self.last_error: Optional[str] = None

    @property
    def available(self) -> bool:
        return bool(self.api_key) and requests is not None

    def chat(self, system: str, user: str, json_mode: bool = False) -> Optional[str]:
        """Single chat completion. Returns None (with last_error set) on any failure."""
        if not self.available:
            self.last_error = "LLM not configured (set LLM_API_KEY / install requests)"
            return None
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"content": user, "role": "user"},
            ],
            "temperature": 0.0,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001 - degrade gracefully by design
            self.last_error = f"{type(exc).__name__}: {exc}"
            return None

    def chat_json(self, system: str, user: str) -> Optional[dict]:
        raw = self.chat(system, user, json_mode=True)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            start, end = raw.find("{"), raw.rfind("}")
            if start >= 0 and end > start:
                try:
                    return json.loads(raw[start : end + 1])
                except json.JSONDecodeError:
                    self.last_error = "LLM returned unparseable JSON"
        return None


if __name__ == "__main__":
    client = LLMClient()
    print("LLM available:", client.available)
    if client.available:
        print(client.chat("Answer in one word.", "What is 2+2?"))
    else:
        print("Running in deterministic mode; LLM criteria will be 'undecided'.")
