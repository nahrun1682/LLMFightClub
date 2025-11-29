"""Configuration and environment variable loading."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration from environment variables."""

    # Google Gemini
    google_api_key: str = ""

    # xAI Grok
    xai_api_key: str = ""

    # Anthropic Claude
    anthropic_api_key: str = ""

    # OpenAI GPT (also used for Orchestrator)
    openai_api_key: str = ""

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            xai_api_key=os.getenv("XAI_API_KEY", ""),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        )

    def validate(self) -> list[str]:
        """Validate that required API keys are set.

        Returns:
            List of missing configuration keys.
        """
        missing = []
        if not self.google_api_key:
            missing.append("GOOGLE_API_KEY")
        if not self.xai_api_key:
            missing.append("XAI_API_KEY")
        if not self.anthropic_api_key:
            missing.append("ANTHROPIC_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        return missing


config = Config.from_env()
