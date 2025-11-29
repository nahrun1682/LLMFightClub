"""LLM Fight Club - Multi-LLM Group Chat System.

A group chat where GPT, Claude, Gemini, and Grok debate topics together,
orchestrated by Microsoft Agent Framework (MAF).
"""

import argparse
import asyncio
import sys
from typing import Sequence

from llm_fight_club.config import config
from llm_fight_club.workflows import FightClubGroupChat


def print_message(agent: str, content: str) -> None:
    """Print a message from an agent."""
    print(f"\n[{agent}]: {content}")
    print("-" * 40)


async def run_discussion(topic: str, max_rounds: int) -> None:
    """Run a group chat discussion on the given topic.

    Args:
        topic: The topic to discuss.
        max_rounds: Maximum discussion rounds.
    """
    missing = config.validate()
    if missing:
        print(f"Error: Missing API keys: {', '.join(missing)}")
        print("Please set the required environment variables.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("LLM FIGHT CLUB")
    print("Powered by Microsoft Agent Framework (MAF)")
    print("=" * 60)
    print(f"\nTopic: {topic}\n")
    print("-" * 60)

    chat = FightClubGroupChat(
        max_rounds=max_rounds,
        on_message=print_message,
    )

    try:
        result = await chat.run(topic)

        print(f"\n{'='*20} Final Summary {'='*20}\n")
        print(result)
        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\nError during discussion: {e}")
        sys.exit(1)


def main(args: Sequence[str] | None = None) -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="LLM Fight Club - Watch AIs debate!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "topic",
        type=str,
        help="The topic for the AIs to discuss",
    )
    parser.add_argument(
        "--rounds",
        "-r",
        type=int,
        default=5,
        help="Maximum discussion rounds (default: 5)",
    )

    parsed = parser.parse_args(args)

    asyncio.run(run_discussion(parsed.topic, max_rounds=parsed.rounds))


if __name__ == "__main__":
    main()
