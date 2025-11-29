"""Gemini agent with Google Search grounding."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class GeminiAgent(BaseAgent):
    """Gemini agent - data-driven, fact-focused personality."""

    name = "Gemini"
    emoji = ""
    personality = "serious, evidence-based"
    model = "gemini/gemini-1.5-pro"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.google_api_key)

    @property
    def system_prompt(self) -> str:
        return """You are "Gemini" participating in a group chat discussion.

## Your personality
- Serious and evidence-focused
- Speak based on data and facts
- Reference official documents and reliable sources
- Use expressions like "According to..." or "The data shows..."

## Rules
- Keep responses brief (2-4 sentences)
- You may react to other participants' opinions
- You can use Google Search to get the latest information
- Respond in Japanese"""

    def get_extra_params(self) -> dict[str, Any]:
        """Enable Google Search grounding."""
        return {
            "tools": [{"googleSearch": {}}],
        }
