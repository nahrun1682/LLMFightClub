"""Tests for the Claude agent."""

import pytest

from llm_fight_club.agents.claude import ClaudeAgent
from llm_fight_club.config import config


class TestClaudeAgent:
    """Tests for ClaudeAgent class."""

    def test_agent_properties(self):
        agent = ClaudeAgent(api_key="test-key")
        assert agent.name == "Claude"
        assert "anthropic" in agent.model

    def test_system_prompt_exists(self):
        agent = ClaudeAgent(api_key="test-key")
        prompt = agent.system_prompt
        assert "Claude" in prompt
        assert len(prompt) > 50

    @pytest.mark.asyncio
    async def test_respond_live(self, skip_if_no_anthropic_key):
        """Test Claude agent with real API call."""
        agent = ClaudeAgent(api_key=config.anthropic_api_key)
        response = await agent.respond("Say 'Hello' in one word.")

        assert response.content is not None
        assert len(response.content) > 0
        assert response.agent_name == "Claude"
