"""GPT agent with web search capability."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class GPTAgent(BaseAgent):
    """GPT agent - balanced, summarizing personality."""

    name = "GPT"
    emoji = ""
    personality = "balanced, neutral"
    model = "openai/gpt-4o"
    prompt_name = "gpt"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.openai_api_key)

    def get_extra_params(self) -> dict[str, Any]:
        """Extra parameters for GPT."""
        return {}
