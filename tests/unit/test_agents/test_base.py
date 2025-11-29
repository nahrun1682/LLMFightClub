"""Tests for the base agent class."""

import pytest

from llm_fight_club.agents.base import AgentResponse, BaseAgent, Message


class ConcreteAgent(BaseAgent):
    """Concrete implementation for testing."""

    name = "TestAgent"
    emoji = ""
    model = "test/model"
    prompt_name = "gemini"  # Use existing YAML for testing


class TestMessage:
    """Tests for Message dataclass."""

    def test_message_creation(self):
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.name is None

    def test_message_with_name(self):
        msg = Message(role="assistant", content="Hi", name="Agent1")
        assert msg.name == "Agent1"


class TestAgentResponse:
    """Tests for AgentResponse dataclass."""

    def test_response_creation(self):
        response = AgentResponse(content="Test", agent_name="Agent")
        assert response.content == "Test"
        assert response.agent_name == "Agent"
        assert response.raw_response is None


class TestBaseAgent:
    """Tests for BaseAgent class."""

    def test_agent_initialization(self):
        agent = ConcreteAgent(api_key="test-key")
        assert agent.api_key == "test-key"
        assert agent.name == "TestAgent"

    def test_agent_repr(self):
        agent = ConcreteAgent()
        assert repr(agent) == " TestAgent"

    def test_system_prompt_loads_from_yaml(self):
        agent = ConcreteAgent()
        prompt = agent.system_prompt
        assert "Gemini" in prompt
        assert len(prompt) > 50

    def test_get_extra_params_default(self):
        agent = ConcreteAgent()
        assert agent.get_extra_params() == {}

    def test_get_api_key_param_with_key(self):
        agent = ConcreteAgent(api_key="test-key")
        assert agent.get_api_key_param() == {"api_key": "test-key"}

    def test_get_api_key_param_without_key(self):
        agent = ConcreteAgent()
        assert agent.get_api_key_param() == {}

    def test_build_messages_simple(self):
        agent = ConcreteAgent()
        messages = agent._build_messages("Hello")

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "Gemini" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"

    def test_build_messages_with_history(self):
        agent = ConcreteAgent()
        history = [
            Message(role="user", content="First message"),
            Message(role="assistant", content="First response", name="Agent1"),
        ]
        messages = agent._build_messages("New message", history)

        assert len(messages) == 4
        assert messages[1]["content"] == "First message"
        assert messages[2]["content"] == "[Agent1]: First response"

    @pytest.mark.asyncio
    async def test_respond(self, mock_acompletion):
        agent = ConcreteAgent(api_key="test-key")
        response = await agent.respond("Test question")

        assert response.content == "This is a mock response."
        assert response.agent_name == "TestAgent"
        mock_acompletion.assert_called_once()

    @pytest.mark.asyncio
    async def test_respond_with_history(self, mock_acompletion):
        agent = ConcreteAgent(api_key="test-key")
        history = [Message(role="user", content="Previous")]
        response = await agent.respond("New question", history)

        assert response.content == "This is a mock response."
        call_args = mock_acompletion.call_args
        messages = call_args.kwargs["messages"]
        assert len(messages) == 3  # system + history + new message
