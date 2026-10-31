"""Provider-neutral chat client for OpenAI-compatible endpoints (Groq, Ollama, ...).

Switch providers with LLM_PROVIDER / LLM_BASE_URL / LLM_API_KEY / LLM_MODEL in
.env; no code changes. Free tiers are rate limited, so transient errors are
retried with backoff and everything else is surfaced as LLMError.
"""
import logging
import time

from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from app.core.config import Settings, get_settings

log = logging.getLogger(__name__)


class LLMError(RuntimeError):
    pass


def _client(s: Settings) -> OpenAI:
    if not s.llm_api_key:
        raise LLMError("LLM_API_KEY is not set")
    return OpenAI(base_url=s.llm_base_url, api_key=s.llm_api_key, max_retries=0, timeout=60)


def chat(messages: list[dict], *, settings: Settings | None = None,
         json_mode: bool = False, max_attempts: int = 3) -> str:
    """Send messages, return the assistant text. Retries rate limits and 5xx."""
    s = settings or get_settings()
    client = _client(s)
    kwargs: dict = dict(model=s.llm_model, messages=messages,
                        max_tokens=s.llm_max_tokens, temperature=s.llm_temperature)
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content or ""
        except (RateLimitError, APIConnectionError) as e:
            err = e
        except APIStatusError as e:
            if e.status_code < 500:
                raise LLMError(f"LLM request rejected ({e.status_code})") from None
            err = e
        if attempt == max_attempts:
            raise LLMError("LLM unavailable after retries") from err
        delay = 2 ** attempt
        log.warning("LLM call failed (%s); retry %d/%d in %ds",
                    type(err).__name__, attempt, max_attempts, delay)
        time.sleep(delay)
    raise LLMError("unreachable")
