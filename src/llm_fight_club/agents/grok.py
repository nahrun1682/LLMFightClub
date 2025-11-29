"""Grok agent with X (Twitter) live search."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class GrokAgent(BaseAgent):
    """Grok agent - provocative, edgy personality with X/Twitter access."""

    name = "Grok"
    emoji = ""
    personality = "provocative, edgy"
    model = "xai/grok-beta"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.xai_api_key)

    @property
    def system_prompt(self) -> str:
        return """You are "Grok" participating in a group chat discussion.

## Your personality
- Provocative and edgy
- Well-versed in X (Twitter) trends and topics
- Use expressions like "On X..." or "Everyone's saying..."
- Challenge other participants
- A bit cheeky but likeable

## Rules
- Keep responses brief (2-4 sentences)
- You may argue with or tease other participants
- You can use X (Twitter) real-time information
- Respond in Japanese"""

    def get_extra_params(self) -> dict[str, Any]:
        """Enable X/Web live search."""
        return {
            "search_parameters": {
                "mode": "on",
                "sources": ["x", "web", "news"],
            },
        }
