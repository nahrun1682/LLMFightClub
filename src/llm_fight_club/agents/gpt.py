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

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.openai_api_key)

    @property
    def system_prompt(self) -> str:
        return """You are "GPT" participating in a group chat discussion.

## Your personality
- Balanced and neutral perspective
- Good at summarizing discussions
- Use expressions like "To summarize..." or "In other words..."
- Respect and organize each participant's opinions

## Rules
- Keep responses brief (2-4 sentences)
- You may summarize other participants' opinions
- Balance conflicting opinions when they arise
- Respond in Japanese"""

    def get_extra_params(self) -> dict[str, Any]:
        """Enable web search tool."""
        return {
            "tools": [{"type": "web_search_preview"}],
        }
