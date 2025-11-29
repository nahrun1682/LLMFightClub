"""Tests for the GPT agent."""

import pytest

from llm_fight_club.agents.gpt import GPTAgent
from llm_fight_club.config import config


class TestGPTAgent:
    """Tests for GPTAgent class."""

    def test_agent_properties(self):
        agent = GPTAgent(api_key="test-key")
        assert agent.name == "GPT"
        assert "openai" in agent.model

    def test_system_prompt_exists(self):
        agent = GPTAgent(api_key="test-key")
        prompt = agent.system_prompt
        assert "GPT" in prompt
        assert len(prompt) > 50

    @pytest.mark.asyncio
    async def test_respond_live(self, skip_if_no_openai_key):
        """Test GPT agent with real API call."""
        agent = GPTAgent(api_key=config.openai_api_key)
        response = await agent.respond("どう？今日の調子は？")

        print(f"\n[GPT] Response: {response.content}")

        assert response.content is not None
        assert len(response.content) > 0
        assert response.agent_name == "GPT"
