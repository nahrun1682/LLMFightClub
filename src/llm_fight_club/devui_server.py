"""DevUI server for LLM Fight Club.

Provides a browser-based interface for interacting with all 4 LLM agents
and the multi-agent group chat workflow.
"""

from agent_framework.devui import serve

from llm_fight_club.agents.maf_agents import (
    create_claude_agent,
    create_gemini_agent,
    create_gpt_agent,
    create_grok_agent,
)
from llm_fight_club.workflows import create_fight_club_workflow


def main():
    """Launch DevUI server with all Fight Club agents and workflow."""
    print("=" * 60)
    print("LLM FIGHT CLUB - DevUI")
    print("=" * 60)
    print("Starting DevUI server...")
    print("Available entities:")
    print("  - GPT, Claude, Gemini, Grok (individual agents)")
    print("  - Fight Club (group chat workflow)")
    print("-" * 60)

    gpt = create_gpt_agent()
    claude = create_claude_agent()
    gemini = create_gemini_agent()
    grok = create_grok_agent()
    
    fight_club = create_fight_club_workflow()

    serve(
        entities=[gpt, claude, gemini, grok, fight_club],
        host="0.0.0.0",
        port=5000,
        auto_open=False,
    )


if __name__ == "__main__":
    main()
