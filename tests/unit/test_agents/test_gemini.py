"""Tests for the Gemini agent."""

import pytest

from llm_fight_club.agents.gemini import GeminiAgent


class TestGeminiAgent:
    """Tests for GeminiAgent class."""

    def test_agent_properties(self):
        agent = GeminiAgent(api_key="test-key")
        assert agent.name == "Gemini"
        assert agent.model == "gemini/gemini-1.5-pro"

    def test_system_prompt_exists(self):
        agent = GeminiAgent(api_key="test-key")
        prompt = agent.system_prompt
        assert "Gemini" in prompt
        assert len(prompt) > 50

    def test_extra_params_includes_google_search(self):
        agent = GeminiAgent(api_key="test-key")
        params = agent.get_extra_params()
        assert "tools" in params
        assert {"googleSearch": {}} in params["tools"]

    @pytest.mark.asyncio
    async def test_respond_with_mock(self, mock_acompletion):
        agent = GeminiAgent(api_key="test-key")
        response = await agent.respond("Test question")

        assert response.content == "This is a mock response."
        assert response.agent_name == "Gemini"

        # Verify Google Search tool was passed
        call_args = mock_acompletion.call_args
        assert "tools" in call_args.kwargs
        assert {"googleSearch": {}} in call_args.kwargs["tools"]
