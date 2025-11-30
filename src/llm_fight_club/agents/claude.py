"""Claude agent with web search capability."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class ClaudeAgent(BaseAgent):
    """Claude agent - thoughtful, critical personality."""

    name = "Claude"
    emoji = ""
    personality = "careful, critical"
    model = "anthropic/claude-3-5-haiku-20241022"
    prompt_name = "claude"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.anthropic_api_key)

    def get_extra_params(self) -> dict[str, Any]:
        """Extra parameters for Claude."""
        return {}
