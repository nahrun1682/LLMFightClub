"""Orchestrator agent for managing group chat flow."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent, Message
from llm_fight_club.config import config


class OrchestratorAgent(BaseAgent):
    """Orchestrator agent - facilitates and manages discussion flow."""

    name = "Facilitator"
    emoji = ""
    personality = "facilitator"
    model = "azure/gpt-4o-mini"
    prompt_name = "orchestrator"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.azure_openai_api_key)

    def get_api_key_param(self) -> dict[str, str]:
        """Return Azure OpenAI specific parameters."""
        params = {}
        if self.api_key:
            params["api_key"] = self.api_key
        if config.azure_openai_endpoint:
            params["api_base"] = config.azure_openai_endpoint
        return params

    def get_extra_params(self) -> dict[str, Any]:
        """No extra params for orchestrator."""
        return {}

    async def start_discussion(self, topic: str) -> str:
        """Generate an opening message for the discussion."""
        response = await self.respond(
            f"Start a discussion on the following topic: {topic}"
        )
        return response.content

    async def wrap_up(self, history: list) -> str:
        """Generate a summary/wrap-up message."""
        response = await self.respond(
            "Please summarize the discussion.",
            history=[Message(**h) if isinstance(h, dict) else h for h in history],
        )
        return response.content
