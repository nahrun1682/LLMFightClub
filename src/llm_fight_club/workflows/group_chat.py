"""MAF-based group chat workflow for LLM Fight Club."""

from collections.abc import Callable
from typing import Any

from agent_framework import (
    ChatMessage,
    InMemoryCheckpointStorage,
    MagenticBuilder,
    MagenticAgentMessageEvent,
    MagenticOrchestratorMessageEvent,
    MagenticFinalResultEvent,
)

from llm_fight_club.agents import (
    create_all_agents,
    create_orchestrator_client,
)
from llm_fight_club.prompts import get_system_prompt


def create_fight_club_workflow():
    """Create a Fight Club workflow for DevUI registration.
    
    Returns:
        A MagenticBuilder workflow that can be registered with DevUI.
    """
    orchestrator_client = create_orchestrator_client()
    agents = create_all_agents()
    participants = {agent.name: agent for agent in agents}
    orchestrator_instructions = get_system_prompt("orchestrator")
    
    checkpoint_storage = InMemoryCheckpointStorage()
    
    workflow = (
        MagenticBuilder()
        .with_standard_manager(
            chat_client=orchestrator_client,
            instructions=orchestrator_instructions,
            max_round_count=10,
            max_stall_count=5,
        )
        .participants(**participants)
        .with_checkpointing(checkpoint_storage)
        .build()
    )
    
    return workflow


class FightClubGroupChat:
    """Multi-LLM group chat orchestrated by MAF."""

    def __init__(
        self,
        max_rounds: int = 10,
        on_message: Callable[[str, str], None] | None = None,
    ):
        """Initialize group chat.

        Args:
            max_rounds: Maximum discussion rounds
            on_message: Callback when an agent sends a message
        """
        self.max_rounds = max_rounds
        self.on_message = on_message
        self._messages: list[dict[str, Any]] = []

    async def run(self, topic: str) -> str:
        """Run a group discussion on the given topic.

        Args:
            topic: The topic to discuss

        Returns:
            Final synthesized answer from the discussion
        """
        orchestrator_client = create_orchestrator_client()
        agents = create_all_agents()

        participants = {agent.name: agent for agent in agents}

        orchestrator_instructions = get_system_prompt("orchestrator")

        task_message = ChatMessage(
            role="user",
            text=f"トピック: {topic}\n\n参加者全員でこのトピックについて議論してください。",
        )
        
        workflow = (
            MagenticBuilder()
            .with_standard_manager(
                chat_client=orchestrator_client,
                instructions=orchestrator_instructions,
                max_round_count=self.max_rounds,
                max_stall_count=3,
            )
            .participants(**participants)
            .start_with_message(task_message)
        )

        final_result = ""
        
        async for event in workflow.run_stream():
            if isinstance(event, MagenticAgentMessageEvent):
                agent_id = getattr(event, 'agent_id', 'Agent')
                msg = event.message
                content = msg.text if msg else ""
                self._messages.append({
                    "agent": agent_id,
                    "content": content,
                })
                if self.on_message and content:
                    self.on_message(agent_id, content)

            elif isinstance(event, MagenticOrchestratorMessageEvent):
                msg = event.message
                content = msg.text if msg else ""
                if content:
                    self._messages.append({
                        "agent": "Orchestrator",
                        "content": content,
                    })
                    if self.on_message:
                        self.on_message("Orchestrator", content)
            
            elif isinstance(event, MagenticFinalResultEvent):
                msg = event.message
                if msg:
                    final_result = msg.text or ""

        return final_result or "議論が終了しました。"

    @property
    def conversation_history(self) -> list[dict[str, Any]]:
        """Return the conversation history."""
        return self._messages


async def run_fight_club(
    topic: str,
    max_rounds: int = 10,
    on_message: Callable[[str, str], None] | None = None,
) -> str:
    """Convenience function to run a Fight Club discussion.

    Args:
        topic: The topic to discuss
        max_rounds: Maximum discussion rounds
        on_message: Callback when an agent sends a message

    Returns:
        Final synthesized answer from the discussion
    """
    chat = FightClubGroupChat(max_rounds=max_rounds, on_message=on_message)
    return await chat.run(topic)
