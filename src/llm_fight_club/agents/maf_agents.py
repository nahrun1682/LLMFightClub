"""MAF-based agents for LLM Fight Club."""

from agent_framework import ChatAgent

from llm_fight_club.clients import LiteLLMChatClient
from llm_fight_club.config import config
from llm_fight_club.prompts import get_system_prompt


def create_gpt_agent() -> ChatAgent:
    """Create GPT agent using MAF ChatAgent."""
    client = LiteLLMChatClient(
        model="openai/gpt-4o",
        api_key=config.openai_api_key,
    )
    return ChatAgent(
        chat_client=client,
        name="GPT",
        instructions=get_system_prompt("gpt"),
        description="Balanced and neutral perspective, good at summarizing",
    )


def create_claude_agent() -> ChatAgent:
    """Create Claude agent using MAF ChatAgent."""
    client = LiteLLMChatClient(
        model="anthropic/claude-3-5-haiku-20241022",
        api_key=config.anthropic_api_key,
    )
    return ChatAgent(
        chat_client=client,
        name="Claude",
        instructions=get_system_prompt("claude"),
        description="Thoughtful and critical, questions assumptions",
    )


def create_gemini_agent() -> ChatAgent:
    """Create Gemini agent using MAF ChatAgent."""
    client = LiteLLMChatClient(
        model="gemini/gemini-2.0-flash",
        api_key=config.google_api_key,
    )
    return ChatAgent(
        chat_client=client,
        name="Gemini",
        instructions=get_system_prompt("gemini"),
        description="Evidence-based, references data and facts",
    )


def create_grok_agent() -> ChatAgent:
    """Create Grok agent using MAF ChatAgent."""
    client = LiteLLMChatClient(
        model="xai/grok-2-latest",
        api_key=config.xai_api_key,
    )
    return ChatAgent(
        chat_client=client,
        name="Grok",
        instructions=get_system_prompt("grok"),
        description="Provocative and edgy, knows X/Twitter trends",
    )


def create_orchestrator_client() -> LiteLLMChatClient:
    """Create orchestrator chat client for GroupChatBuilder manager."""
    return LiteLLMChatClient(
        model="openai/gpt-4o-mini",
        api_key=config.openai_api_key,
    )


def create_all_agents() -> list[ChatAgent]:
    """Create all participant agents."""
    return [
        create_gpt_agent(),
        create_claude_agent(),
        create_gemini_agent(),
        create_grok_agent(),
    ]
