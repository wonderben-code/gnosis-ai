"""Claude API wrapper with retry, cost tracking, model fallback, and streaming."""

from __future__ import annotations

import random
import time
import json
from dataclasses import dataclass, field
from typing import Optional

import anthropic

from gnosis.config import Config


# Pricing per million tokens (approximate, as of April 2026)
PRICING = {
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-opus-4-20250514": {"input": 15.0, "output": 75.0},
    "claude-opus-4-6": {"input": 15.0, "output": 75.0},
}


@dataclass
class APIStats:
    """Track API usage across a session."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    errors: int = 0
    cost_usd: float = 0.0
    connection_failures: int = 0

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
    """Wrapper around the Anthropic Claude API with fallback and robust retry."""

    def __init__(self, config: Config):
        self.config = config
        self.client = anthropic.Anthropic(
            api_key=config.api_key,
            timeout=600.0,
            max_retries=2,  # SDK handles transient retries; we handle fallback
        )
        self.stats = APIStats()

    def query(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> str:
        """Send a query to Claude and return the text response.

        Uses streaming to avoid server disconnect on long responses.
        Falls back to alternate model on repeated connection failures.
        """
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

        # Try primary model, then fallback
        models_to_try = [model]
        if self.config.model_fallback and self.config.model_fallback != model:
            models_to_try.append(self.config.model_fallback)

        for model_idx, try_model in enumerate(models_to_try):
            kwargs["model"] = try_model
            last_error = None

            for attempt in range(self.config.max_retries):
                try:
                    # Use streaming to avoid server disconnect on long responses
                    text_parts = []
                    input_tokens = 0
                    output_tokens = 0

                    with self.client.messages.stream(**kwargs) as stream:
                        for event in stream:
                            if hasattr(event, 'type'):
                                if event.type == 'content_block_delta' and hasattr(event, 'delta'):
                                    if hasattr(event.delta, 'text'):
                                        text_parts.append(event.delta.text)

                        # Get final message for usage stats
                        final = stream.get_final_message()
                        input_tokens = final.usage.input_tokens
                        output_tokens = final.usage.output_tokens

                    text = "".join(text_parts)
                    self.stats.record(try_model, input_tokens, output_tokens)
                    return text

                except anthropic.RateLimitError:
                    wait = min(60, (2 ** attempt) + random.uniform(0.5, 1.5))
                    time.sleep(wait)
                    last_error = "rate_limit"

                except (anthropic.APIConnectionError, anthropic.APITimeoutError):
                    self.stats.errors += 1
                    self.stats.connection_failures += 1
                    last_error = "connection_error"
                    if attempt < self.config.max_retries - 1:
                        wait = min(30, (2 ** attempt) + random.uniform(1, 3))
                        time.sleep(wait)
                    # On last attempt, fall through to try fallback model

                except anthropic.APIError as e:
                    self.stats.errors += 1
                    last_error = str(e)
                    if attempt < self.config.max_retries - 1:
                        time.sleep(2 ** attempt)

            # If we get here, all retries for this model failed
            if model_idx < len(models_to_try) - 1:
                # Try fallback model
                continue
            else:
                raise RuntimeError(
                    f"API failed after trying {len(models_to_try)} model(s) "
                    f"with {self.config.max_retries} retries each: {last_error}"
                )

        raise RuntimeError(f"API failed: {last_error}")

    def query_json(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        max_tokens: int = 4096,
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
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass

            start = text.find("[")
            end = text.rfind("]") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass

            raise ValueError(
                f"Failed to parse JSON from API response. "
                f"Response starts with: {text[:200]}"
            )

    def query_deep(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
    ) -> str:
        """Query using the deep/powerful model (Opus)."""
        return self.query(
            prompt, system=system, model=self.config.model_deep, max_tokens=max_tokens
        )

    def query_deep_json(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
    ) -> dict | list:
        """Query deep model and parse as JSON."""
        return self.query_json(
            prompt, system=system, model=self.config.model_deep, max_tokens=max_tokens
        )
