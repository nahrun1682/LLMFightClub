"""Tests for the Gemini agent."""

import pytest

from llm_fight_club.agents.gemini import GeminiAgent
from llm_fight_club.config import config


class TestGeminiAgent:
    """Tests for GeminiAgent class."""

    def test_agent_properties(self):
        agent = GeminiAgent(api_key="test-key")
        assert agent.name == "Gemini"
        assert "gemini" in agent.model

    def test_system_prompt_exists(self):
        agent = GeminiAgent(api_key="test-key")
        prompt = agent.system_prompt
        assert "Gemini" in prompt
        assert len(prompt) > 50

    @pytest.mark.asyncio
    async def test_respond_live(self, skip_if_no_google_key):
        """Test Gemini agent with real API call."""
        agent = GeminiAgent(api_key=config.google_api_key)
        response = await agent.respond("Say 'Hello' in one word.")

        print(f"\n[Gemini] Response: {response.content}")

        assert response.content is not None
        assert len(response.content) > 0
        assert response.agent_name == "Gemini"
