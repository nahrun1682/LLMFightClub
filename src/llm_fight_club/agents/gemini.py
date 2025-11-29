"""Gemini agent with Google Search grounding."""

from typing import Any

from llm_fight_club.agents.base import BaseAgent
from llm_fight_club.config import config


class GeminiAgent(BaseAgent):
    """Gemini agent - data-driven, fact-focused personality."""

    name = "Gemini"
    emoji = ""
    personality = "serious, evidence-based"
    model = "gemini/gemini-2.0-flash"
    prompt_name = "gemini"

    def __init__(self, api_key: str | None = None):
        super().__init__(api_key or config.google_api_key)

    def get_extra_params(self) -> dict[str, Any]:
        """Extra parameters for Gemini."""
        return {}
