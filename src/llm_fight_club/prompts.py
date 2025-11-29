"""Prompt loader for YAML-based prompt management."""

from pathlib import Path

import yaml


PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def load_prompt(agent_name: str) -> dict:
    """Load prompt configuration for an agent from YAML.

    Args:
        agent_name: Name of the agent (e.g., 'gemini', 'grok')

    Returns:
        Dictionary with prompt configuration.
    """
    yaml_path = PROMPTS_DIR / f"{agent_name}.yaml"

    if not yaml_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_system_prompt(agent_name: str) -> str:
    """Get the system prompt for an agent.

    Args:
        agent_name: Name of the agent (e.g., 'gemini', 'grok')

    Returns:
        System prompt string.
    """
    config = load_prompt(agent_name)
    return config.get("system_prompt", "")
