"""Grok agent with X (Twitter) live search."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class GrokAgent(BaseAgent):
    """Grok agent - provocative, edgy personality with X/Twitter access."""

    name = "Grok"
    emoji = ""
    personality = "provocative, edgy"
    model = "xai/grok-2-latest"
    prompt_name = "grok"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.xai_api_key)

    def get_extra_params(self) -> dict[str, Any]:
        """Extra parameters for Grok."""
        return {}
