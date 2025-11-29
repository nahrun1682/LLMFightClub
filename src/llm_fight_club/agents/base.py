"""Base agent class for all LLM agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from litellm import acompletion


@dataclass
class Message:
    """A message in the conversation."""

    role: str
    content: str
    name: str | None = None


@dataclass
class AgentResponse:
    """Response from an agent."""

    content: str
    agent_name: str
    raw_response: Any = None


class BaseAgent(ABC):
    """Base class for all LLM agents."""

    name: str = "Agent"
    emoji: str = ""
    personality: str = ""
    model: str = ""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        pass

    def get_extra_params(self) -> dict[str, Any]:
        return {}

    def get_api_key_param(self) -> dict[str, str]:
        if self.api_key:
            return {"api_key": self.api_key}
        return {}

    async def respond(
        self,
        message: str,
        history: list[Message] | None = None,
    ) -> AgentResponse:
        messages = self._build_messages(message, history)

        params = {
            "model": self.model,
            "messages": messages,
            **self.get_api_key_param(),
            **self.get_extra_params(),
        }

        response = await acompletion(**params)
        content = response.choices[0].message.content

        return AgentResponse(
            content=content,
            agent_name=self.name,
            raw_response=response,
        )

    def _build_messages(
        self,
        message: str,
        history: list[Message] | None = None,
    ) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": self.system_prompt}]

        if history:
            for msg in history:
                msg_dict = {"role": msg.role, "content": msg.content}
                if msg.name:
                    msg_dict["content"] = f"[{msg.name}]: {msg.content}"
                messages.append(msg_dict)

        messages.append({"role": "user", "content": message})
        return messages

    def __repr__(self) -> str:
        return f"{self.emoji} {self.name}"
