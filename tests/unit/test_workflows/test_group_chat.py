"""Tests for the group chat workflow."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from llm_fight_club.agents.base import AgentResponse, BaseAgent, Message
from llm_fight_club.workflows.group_chat import (
    GroupChat,
    GroupChatConfig,
    GroupChatResult,
)


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    prompt_name = "gemini"

    def __init__(self, name: str, response: str):
        super().__init__()
        self.name = name
        self._mock_response = response

    async def respond(self, message: str, history=None) -> AgentResponse:
        return AgentResponse(
            content=self._mock_response,
            agent_name=self.name,
        )


class TestGroupChatConfig:
    """Tests for GroupChatConfig."""

    def test_default_config(self):
        config = GroupChatConfig()
        assert config.max_rounds == 3
        assert config.include_orchestrator is True

    def test_custom_config(self):
        config = GroupChatConfig(max_rounds=5, include_orchestrator=False)
        assert config.max_rounds == 5
        assert config.include_orchestrator is False


class TestGroupChatResult:
    """Tests for GroupChatResult."""

    def test_default_result(self):
        result = GroupChatResult(topic="Test topic")
        assert result.topic == "Test topic"
        assert result.messages == []
        assert result.rounds_completed == 0


class TestGroupChat:
    """Tests for GroupChat workflow."""

    @pytest.fixture
    def mock_agents(self):
        return [
            MockAgent("Gemini", "Data shows..."),
            MockAgent("Grok", "On X, everyone says..."),
            MockAgent("Claude", "Wait, is that true?"),
            MockAgent("GPT", "To summarize..."),
        ]

    @pytest.fixture
    def mock_orchestrator(self):
        return MockAgent("Facilitator", "Let's discuss...")

    def test_initialization(self, mock_agents):
        chat = GroupChat(agents=mock_agents)
        assert len(chat.agents) == 4
        assert chat.orchestrator is None
        assert chat.config.max_rounds == 3

    def test_initialization_with_orchestrator(self, mock_agents, mock_orchestrator):
        chat = GroupChat(agents=mock_agents, orchestrator=mock_orchestrator)
        assert chat.orchestrator is not None
        assert chat.orchestrator.name == "Facilitator"

    @pytest.mark.asyncio
    async def test_run_without_orchestrator(self, mock_agents):
        config = GroupChatConfig(max_rounds=2, include_orchestrator=False)
        chat = GroupChat(agents=mock_agents, config=config)

        result = await chat.run("Test topic")

        assert result.topic == "Test topic"
        assert result.rounds_completed == 2
        # 4 agents * 2 rounds = 8 messages
        assert len(result.messages) == 8

    @pytest.mark.asyncio
    async def test_run_with_orchestrator(self, mock_agents, mock_orchestrator):
        config = GroupChatConfig(max_rounds=1)
        chat = GroupChat(
            agents=mock_agents,
            orchestrator=mock_orchestrator,
            config=config,
        )

        result = await chat.run("Test topic")

        assert result.rounds_completed == 1
        # 1 opening + 4 agents * 1 round + 1 closing = 6 messages
        assert len(result.messages) == 6
        # First message from orchestrator
        assert result.messages[0].name == "Facilitator"
        # Last message from orchestrator
        assert result.messages[-1].name == "Facilitator"

    @pytest.mark.asyncio
    async def test_all_agents_speak_in_round(self, mock_agents):
        config = GroupChatConfig(max_rounds=1, include_orchestrator=False)
        chat = GroupChat(agents=mock_agents, config=config)

        result = await chat.run("Test topic")

        agent_names = [msg.name for msg in result.messages]
        assert "Gemini" in agent_names
        assert "Grok" in agent_names
        assert "Claude" in agent_names
        assert "GPT" in agent_names

    @pytest.mark.asyncio
    async def test_history_is_maintained(self, mock_agents):
        config = GroupChatConfig(max_rounds=2, include_orchestrator=False)
        chat = GroupChat(agents=mock_agents, config=config)

        await chat.run("Test topic")

        # History should contain all messages
        assert len(chat.history) == 8

    @pytest.mark.asyncio
    async def test_messages_have_correct_structure(self, mock_agents):
        config = GroupChatConfig(max_rounds=1, include_orchestrator=False)
        chat = GroupChat(agents=mock_agents, config=config)

        result = await chat.run("Test topic")

        for msg in result.messages:
            assert isinstance(msg, Message)
            assert msg.role == "assistant"
            assert msg.name is not None
            assert msg.content is not None
