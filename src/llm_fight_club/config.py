"""Configuration and environment variable loading."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration from environment variables."""

    # Azure OpenAI (Orchestrator)
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment_name: str = "gpt-4o-mini"

    # Google Gemini
    google_api_key: str = ""

    # xAI Grok
    xai_api_key: str = ""

    # Anthropic Claude
    anthropic_api_key: str = ""

    # OpenAI GPT
    openai_api_key: str = ""

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            azure_openai_deployment_name=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"
            ),
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
        if not self.azure_openai_api_key:
            missing.append("AZURE_OPENAI_API_KEY")
        if not self.azure_openai_endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
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
