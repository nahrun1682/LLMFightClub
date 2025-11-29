"""Tests for the Claude agent."""

import pytest

from llm_fight_club.agents.claude import ClaudeAgent


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

    def test_extra_params_includes_web_search(self):
        agent = ClaudeAgent(api_key="test-key")
        params = agent.get_extra_params()
        assert "tools" in params
        assert any("web_search" in str(t) for t in params["tools"])

    @pytest.mark.asyncio
    async def test_respond_with_mock(self, mock_acompletion):
        agent = ClaudeAgent(api_key="test-key")
        response = await agent.respond("Test question")

        assert response.content == "This is a mock response."
        assert response.agent_name == "Claude"

        # Verify web search tool was passed
        call_args = mock_acompletion.call_args
        assert "tools" in call_args.kwargs
