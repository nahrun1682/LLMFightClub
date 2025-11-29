"""Tests for the Grok agent."""

import pytest

from llm_fight_club.agents.grok import GrokAgent
from llm_fight_club.config import config


class TestGrokAgent:
    """Tests for GrokAgent class."""

    def test_agent_properties(self):
        agent = GrokAgent(api_key="test-key")
        assert agent.name == "Grok"
        assert "grok" in agent.model

    def test_system_prompt_exists(self):
        agent = GrokAgent(api_key="test-key")
        prompt = agent.system_prompt
        assert "Grok" in prompt
        assert len(prompt) > 50

    @pytest.mark.asyncio
    async def test_respond_live(self, skip_if_no_xai_key):
        """Test Grok agent with real API call."""
        agent = GrokAgent(api_key=config.xai_api_key)
        response = await agent.respond("Say 'Hello' in one word.")

        assert response.content is not None
        assert len(response.content) > 0
        assert response.agent_name == "Grok"
