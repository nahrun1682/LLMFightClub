"""Group chat workflow for multi-agent discussion."""

from dataclasses import dataclass, field

from llm_fight_club.agents.base import AgentResponse, BaseAgent, Message


@dataclass
class GroupChatConfig:
    """Configuration for group chat."""

    max_rounds: int = 3
    include_orchestrator: bool = True


@dataclass
class GroupChatResult:
    """Result of a group chat session."""

    topic: str
    messages: list[Message] = field(default_factory=list)
    rounds_completed: int = 0


class GroupChat:
    """Orchestrates a group chat discussion among multiple agents."""

    def __init__(
        self,
        agents: list[BaseAgent],
        orchestrator: BaseAgent | None = None,
        config: GroupChatConfig | None = None,
    ):
        """Initialize group chat.

        Args:
            agents: List of participant agents.
            orchestrator: Optional orchestrator/facilitator agent.
            config: Group chat configuration.
        """
        self.agents = agents
        self.orchestrator = orchestrator
        self.config = config or GroupChatConfig()
        self.history: list[Message] = []

    async def run(self, topic: str) -> GroupChatResult:
        """Run the group chat discussion.

        Args:
            topic: The topic to discuss.

        Returns:
            GroupChatResult with all messages and metadata.
        """
        result = GroupChatResult(topic=topic)

        # Orchestrator opens the discussion
        if self.orchestrator and self.config.include_orchestrator:
            opening = await self._get_response(self.orchestrator, topic)
            self._add_message(opening, result)

        # Run rounds
        for round_num in range(self.config.max_rounds):
            await self._run_round(topic, result)
            result.rounds_completed += 1

        # Orchestrator wraps up
        if self.orchestrator and self.config.include_orchestrator:
            wrap_up_prompt = f"Topic: {topic}\nPlease summarize the discussion."
            closing = await self._get_response(self.orchestrator, wrap_up_prompt)
            self._add_message(closing, result)

        return result

    async def _run_round(self, topic: str, result: GroupChatResult) -> None:
        """Run a single round where each agent speaks once."""
        for agent in self.agents:
            # Build context from recent messages
            context = self._build_context(topic)
            response = await self._get_response(agent, context)
            self._add_message(response, result)

    async def _get_response(self, agent: BaseAgent, message: str) -> AgentResponse:
        """Get a response from an agent with history context."""
        return await agent.respond(message, history=self.history)

    def _add_message(self, response: AgentResponse, result: GroupChatResult) -> None:
        """Add a message to history and result."""
        msg = Message(
            role="assistant",
            content=response.content,
            name=response.agent_name,
        )
        self.history.append(msg)
        result.messages.append(msg)

    def _build_context(self, topic: str) -> str:
        """Build context message for agents."""
        if not self.history:
            return f"Topic: {topic}\nShare your thoughts on this topic."

        recent = self.history[-4:]  # Last 4 messages for context
        context_parts = [f"Topic: {topic}", "Recent discussion:"]
        for msg in recent:
            context_parts.append(f"- {msg.name}: {msg.content[:100]}...")
        context_parts.append("What are your thoughts?")

        return "\n".join(context_parts)
