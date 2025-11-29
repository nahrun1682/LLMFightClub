"""Pytest configuration and fixtures."""

import pytest

from llm_fight_club.config import config


@pytest.fixture
def api_keys():
    """Provide API keys from config for live testing."""
    return {
        "openai": config.openai_api_key,
        "anthropic": config.anthropic_api_key,
        "google": config.google_api_key,
        "xai": config.xai_api_key,
    }


@pytest.fixture
def skip_if_no_openai_key():
    """Skip test if OpenAI API key is not set."""
    if not config.openai_api_key:
        pytest.skip("OPENAI_API_KEY not set")


@pytest.fixture
def skip_if_no_anthropic_key():
    """Skip test if Anthropic API key is not set."""
    if not config.anthropic_api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")


@pytest.fixture
def skip_if_no_google_key():
    """Skip test if Google API key is not set."""
    if not config.google_api_key:
        pytest.skip("GOOGLE_API_KEY not set")


@pytest.fixture
def skip_if_no_xai_key():
    """Skip test if xAI API key is not set."""
    if not config.xai_api_key:
        pytest.skip("XAI_API_KEY not set")
