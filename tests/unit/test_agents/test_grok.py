"""Tests for the Grok agent."""

import pytest

from llm_fight_club.agents.grok import GrokAgent


class TestGrokAgent:
    """Tests for GrokAgent class."""

    def test_agent_properties(self):
        agent = GrokAgent(api_key="test-key")
        assert agent.name == "Grok"
        assert agent.model == "xai/grok-beta"

    def test_system_prompt_exists(self):
        agent = GrokAgent(api_key="test-key")
        prompt = agent.system_prompt
        assert "Grok" in prompt
        assert len(prompt) > 50

    def test_extra_params_includes_search(self):
        agent = GrokAgent(api_key="test-key")
        params = agent.get_extra_params()
        assert "search_parameters" in params
        assert params["search_parameters"]["mode"] == "on"
        assert "x" in params["search_parameters"]["sources"]
        assert "web" in params["search_parameters"]["sources"]

    @pytest.mark.asyncio
    async def test_respond_with_mock(self, mock_acompletion):
        agent = GrokAgent(api_key="test-key")
        response = await agent.respond("Test question")

        assert response.content == "This is a mock response."
        assert response.agent_name == "Grok"

        # Verify search parameters were passed
        call_args = mock_acompletion.call_args
        assert "search_parameters" in call_args.kwargs
        assert call_args.kwargs["search_parameters"]["mode"] == "on"
