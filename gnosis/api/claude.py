"""Claude API wrapper with retry, cost tracking, and model selection."""

from __future__ import annotations

import time
import json
from dataclasses import dataclass, field
from typing import Optional

import anthropic

from gnosis.config import Config


# Pricing per million tokens (approximate, as of April 2026)
PRICING = {
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
    "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
}


@dataclass
class APIStats:
    """Track API usage across a session."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    errors: int = 0
    cost_usd: float = 0.0

    def record(self, model: str, input_tokens: int, output_tokens: int):
        self.calls += 1
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        pricing = PRICING.get(model, {"input": 10.0, "output": 50.0})
        self.cost_usd += (
            input_tokens * pricing["input"] / 1_000_000
            + output_tokens * pricing["output"] / 1_000_000
        )


class ClaudeAPI:
    """Wrapper around the Anthropic Claude API."""

    def __init__(self, config: Config):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)
        self.stats = APIStats()

    def query(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> str:
        """Send a query to Claude and return the text response."""
        if model is None:
            model = self.config.model_fast

        # Cost guard
        if self.stats.cost_usd >= self.config.max_cost_usd:
            raise RuntimeError(
                f"Cost limit reached: ${self.stats.cost_usd:.2f} "
                f"(max: ${self.config.max_cost_usd:.2f})"
            )

        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }
        if system:
            kwargs["system"] = system

        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                response = self.client.messages.create(**kwargs)
                text = response.content[0].text
                self.stats.record(
                    model,
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                )
                return text
            except anthropic.RateLimitError:
                wait = (2 ** attempt) + 1
                time.sleep(wait)
                last_error = "rate_limit"
            except anthropic.APIError as e:
                self.stats.errors += 1
                last_error = str(e)
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

        raise RuntimeError(f"API failed after {self.config.max_retries} retries: {last_error}")

    def query_json(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        max_tokens: int = 8192,
    ) -> dict | list:
        """Query Claude and parse the response as JSON."""
        full_prompt = (
            prompt
            + "\n\nRespond with valid JSON only. No markdown fencing, no explanation — just the JSON."
        )

        text = self.query(full_prompt, system=system, model=model, max_tokens=max_tokens)

        # Strip markdown fencing if present
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json) and last line (```)
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        return json.loads(text)

    def query_deep(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 8192,
    ) -> str:
        """Query using the deep/powerful model (Opus)."""
        return self.query(
            prompt, system=system, model=self.config.model_deep, max_tokens=max_tokens
        )

    def query_deep_json(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 8192,
    ) -> dict | list:
        """Query deep model and parse as JSON."""
        return self.query_json(
            prompt, system=system, model=self.config.model_deep, max_tokens=max_tokens
        )
