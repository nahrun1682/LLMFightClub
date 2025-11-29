"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_litellm_response():
    """Create a mock LiteLLM response."""
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message.content = "This is a mock response."
    return response


@pytest.fixture
def mock_acompletion(mocker, mock_litellm_response):
    """Mock litellm.acompletion for testing."""
    mock = mocker.patch(
        "llm_fight_club.agents.base.acompletion",
        new_callable=AsyncMock,
        return_value=mock_litellm_response,
    )
    return mock
