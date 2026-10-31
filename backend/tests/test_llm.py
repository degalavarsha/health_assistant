from types import SimpleNamespace

import pytest

from app.core.config import Settings
from app.services import llm


def _settings(**kw) -> Settings:
    return Settings(_env_file=None, **kw)


def test_missing_key_raises():
    with pytest.raises(llm.LLMError):
        llm.chat([{"role": "user", "content": "hi"}], settings=_settings(llm_api_key=""))


def test_returns_text(monkeypatch):
    fake = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
        create=lambda **kw: SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="hello"))]))))
    monkeypatch.setattr(llm, "_client", lambda s: fake)
    assert llm.chat([{"role": "user", "content": "hi"}], settings=_settings(llm_api_key="k")) == "hello"
