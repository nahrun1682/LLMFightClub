"""DevUI server for LLM Fight Club.

Provides a browser-based interface for interacting with all 4 LLM agents.
"""

from agent_framework.devui import serve

from llm_fight_club.agents.maf_agents import (
    create_claude_agent,
    create_gemini_agent,
    create_gpt_agent,
    create_grok_agent,
)


def main():
    """Launch DevUI server with all Fight Club agents."""
    print("=" * 60)
    print("LLM FIGHT CLUB - DevUI")
    print("=" * 60)
    print("Starting DevUI server...")
    print("Open your browser to interact with the agents!")
    print("-" * 60)

    gpt = create_gpt_agent()
    claude = create_claude_agent()
    gemini = create_gemini_agent()
    grok = create_grok_agent()

    serve(
        entities=[gpt, claude, gemini, grok],
        host="0.0.0.0",
        port=5000,
        auto_open=False,
    )


if __name__ == "__main__":
    main()
