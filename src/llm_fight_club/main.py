"""LLM Fight Club - Multi-LLM Group Chat System.

A group chat where GPT, Claude, Gemini, and Grok debate topics together.
"""

import argparse
import asyncio
import sys
from typing import Sequence

from llm_fight_club.agents import (
    ClaudeAgent,
    GeminiAgent,
    GPTAgent,
    GrokAgent,
    Message,
    OrchestratorAgent,
)
from llm_fight_club.config import config


class GroupChat:
    """Orchestrates a group chat discussion between multiple LLM agents."""

    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.participants = [
            GPTAgent(),
            ClaudeAgent(),
            GeminiAgent(),
            GrokAgent(),
        ]
        self.history: list[Message] = []

    async def run(self, topic: str, rounds: int = 3) -> None:
        """Run a group chat discussion on the given topic.

        Args:
            topic: The topic to discuss.
            rounds: Number of discussion rounds (each participant speaks once per round).
        """
        missing = config.validate()
        if missing:
            print(f"Error: Missing API keys: {', '.join(missing)}")
            print("Please set the required environment variables.")
            sys.exit(1)

        print("\n" + "=" * 60)
        print("LLM FIGHT CLUB")
        print("=" * 60)
        print(f"\nTopic: {topic}\n")
        print("-" * 60)

        opening = await self.orchestrator.start_discussion(topic)
        print(f"\n[Facilitator]: {opening}\n")
        self.history.append(Message(role="assistant", content=opening, name="Facilitator"))

        for round_num in range(1, rounds + 1):
            print(f"\n{'='*20} Round {round_num} {'='*20}\n")

            for agent in self.participants:
                try:
                    context = self._build_context(topic)
                    response = await agent.respond(context, history=self.history)

                    print(f"[{agent.name}]: {response.content}\n")
                    print("-" * 40)

                    self.history.append(
                        Message(
                            role="assistant",
                            content=response.content,
                            name=agent.name,
                        )
                    )
                except Exception as e:
                    print(f"[{agent.name}]: (Error: {e})\n")
                    print("-" * 40)

        print(f"\n{'='*20} Summary {'='*20}\n")
        summary = await self.orchestrator.wrap_up(self.history)
        print(f"[Facilitator]: {summary}\n")
        print("=" * 60)

    def _build_context(self, topic: str) -> str:
        """Build context message for the next participant."""
        if not self.history:
            return f"Discuss this topic: {topic}"

        recent = self.history[-3:] if len(self.history) > 3 else self.history
        context_parts = [f"Topic: {topic}", "", "Recent discussion:"]
        for msg in recent:
            context_parts.append(f"[{msg.name}]: {msg.content}")
        context_parts.append("")
        context_parts.append("Please share your perspective on this topic, responding to what others have said.")
        return "\n".join(context_parts)


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
        default=3,
        help="Number of discussion rounds (default: 3)",
    )

    parsed = parser.parse_args(args)

    chat = GroupChat()
    asyncio.run(chat.run(parsed.topic, rounds=parsed.rounds))


if __name__ == "__main__":
    main()
