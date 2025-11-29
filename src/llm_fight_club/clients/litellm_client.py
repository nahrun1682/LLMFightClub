"""LiteLLM Chat Client for Microsoft Agent Framework."""

from collections.abc import AsyncIterable
from typing import Any

from agent_framework import ChatMessage, ChatResponse, ChatResponseUpdate
from litellm import acompletion


class LiteLLMChatClient:
    """Custom chat client that uses LiteLLM to support multiple LLM providers."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        **kwargs: Any,
    ):
        """Initialize LiteLLM chat client.

        Args:
            model: Model identifier (e.g., "openai/gpt-4o", "anthropic/claude-3-5-haiku")
            api_key: API key for the provider
            **kwargs: Additional LiteLLM parameters
        """
        self.model = model
        self.api_key = api_key
        self.default_kwargs = kwargs

    @property
    def additional_properties(self) -> dict[str, Any]:
        """Return additional properties for the client."""
        return {
            "model": self.model,
            "provider": self.model.split("/")[0] if "/" in self.model else "openai",
        }

    async def get_response(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Get a non-streaming response from LiteLLM."""
        litellm_messages = self._convert_messages(messages)

        params: dict[str, Any] = {
            "model": model or self.model,
            "messages": litellm_messages,
            **self.default_kwargs,
        }

        if self.api_key:
            params["api_key"] = self.api_key
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        response = await acompletion(**params)

        return self._convert_response(response)

    async def get_streaming_response(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[ChatResponseUpdate]:
        """Get a streaming response from LiteLLM."""
        litellm_messages = self._convert_messages(messages)

        params: dict[str, Any] = {
            "model": model or self.model,
            "messages": litellm_messages,
            "stream": True,
            **self.default_kwargs,
        }

        if self.api_key:
            params["api_key"] = self.api_key
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        response = await acompletion(**params)

        async for chunk in response:
            yield self._convert_streaming_chunk(chunk)

    def _convert_messages(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage],
    ) -> list[dict[str, str]]:
        """Convert Agent Framework messages to LiteLLM format."""
        if isinstance(messages, str):
            return [{"role": "user", "content": messages}]

        if isinstance(messages, ChatMessage):
            return [{"role": str(messages.role), "content": messages.text or ""}]

        if isinstance(messages, list):
            litellm_messages = []
            for msg in messages:
                if isinstance(msg, str):
                    litellm_messages.append({"role": "user", "content": msg})
                elif isinstance(msg, ChatMessage):
                    litellm_messages.append({
                        "role": str(msg.role),
                        "content": msg.text or "",
                    })
            return litellm_messages

        return []

    def _convert_response(self, litellm_response: Any) -> ChatResponse:
        """Convert LiteLLM response to Agent Framework ChatResponse."""
        content = litellm_response.choices[0].message.content or ""

        return ChatResponse(
            messages=[ChatMessage(role="assistant", text=content)],
            response_id=getattr(litellm_response, "id", None),
            model_id=getattr(litellm_response, "model", self.model),
        )

    def _convert_streaming_chunk(self, chunk: Any) -> ChatResponseUpdate:
        """Convert LiteLLM streaming chunk to Agent Framework format."""
        delta_content = ""
        if hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
            delta_content = chunk.choices[0].delta.content or ""

        return ChatResponseUpdate(
            text=delta_content,
            response_id=getattr(chunk, "id", None),
        )
