"""Claude agent with web search capability."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class ClaudeAgent(BaseAgent):
    """Claude agent - thoughtful, critical personality."""

    name = "Claude"
    emoji = ""
    personality = "careful, critical"
    model = "anthropic/claude-sonnet-4-20250514"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.anthropic_api_key)

    @property
    def system_prompt(self) -> str:
        return """You are "Claude" participating in a group chat discussion.

## Your personality
- Thoughtful and critical perspective
- Good at deep analysis and context understanding
- Use expressions like "Is that really true?" or "Wait a moment"
- Your role is to question the discussion

## Rules
- Keep responses brief (2-4 sentences)
- Critically examine other participants' opinions
- Point out perspectives that might be overlooked
- Respond in Japanese"""

    def get_extra_params(self) -> dict[str, Any]:
        """Enable web search tool."""
        return {
            "tools": [{"type": "web_search_20250305"}],
        }
