"""The one place that calls a model.

The composition gives a model two texts, the instruction and the material, and gets one text
back. Any service with a chat completions address of the common kind can be used, for
example OpenRouter. The settings come from the environment:

``SKILLCARD_API_KEY``   the key of the service. For OpenRouter, ``OPENROUTER_API_KEY`` is
                        read when it is not set
``SKILLCARD_MODEL``     the name of the model at that service
``SKILLCARD_API_BASE``  the address of the service

Without a key no model is called. The key is read from the environment only. It is never
written to a file, a log or a card.
"""

from __future__ import annotations

import http.client
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from skillcard import net

DEFAULT_MODEL = "deepseek/deepseek-v4.1-flash-1017"
DEFAULT_BASE = "https://openrouter.ai/api/v1"
SECONDS = 900
LARGEST_ANSWER_TOKENS = 64_000


@dataclass
class Model:
    """A model at a service. Calling it sends one request and returns the answer."""

    name: str
    base: str
    key: str = field(repr=False)

    def __call__(self, instruction: str, material: str) -> dict:
        """Return the text of the answer with the model that gave it and the tokens used."""
        body = {
            "model": self.name,
            "messages": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": material},
            ],
            "temperature": 0,
            "max_tokens": LARGEST_ANSWER_TOKENS,
            "response_format": {"type": "json_object"},
        }
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        request = urllib.request.Request(
            f"{self.base.rstrip('/')}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with net.open_request(request, SECONDS) as response:
                answer = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            try:
                said = error.read(2000).decode("utf-8", "replace")
            except (OSError, http.client.HTTPException):
                said = "no message"
            raise RuntimeError(f"the model service answered HTTP {error.code}, {said}") from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as error:
            raise RuntimeError(f"the model service did not answer, {error}") from None
        except ValueError:
            raise RuntimeError("the model service did not answer with JSON") from None
        try:
            choice = answer["choices"][0]
            text = choice["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise RuntimeError(f"the model service gave no answer, {str(answer)[:500]}") from None
        if choice.get("finish_reason") == "length":
            raise RuntimeError("the answer of the model was cut off before it ended")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("the answer of the model is empty")
        return {
            "text": text,
            "model": answer.get("model") or self.name,
            "provider": answer.get("provider") or "not stated",
            "usage": answer.get("usage") or {},
        }


def from_environment() -> Model | None:
    """Return the model the environment names, or ``None`` when no key is set.

    ``OPENROUTER_API_KEY`` is only used for OpenRouter itself, so that the key of one service
    is never sent to another.
    """
    base = os.environ.get("SKILLCARD_API_BASE") or DEFAULT_BASE
    key = os.environ.get("SKILLCARD_API_KEY")
    if not key and urlsplit(base).hostname == urlsplit(DEFAULT_BASE).hostname:
        key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return None
    return Model(name=os.environ.get("SKILLCARD_MODEL") or DEFAULT_MODEL, base=base, key=key)
