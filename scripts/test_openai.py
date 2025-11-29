"""OpenAI connection test script."""

import asyncio
import os
import sys

from dotenv import load_dotenv
from litellm import acompletion


async def test_openai():
    """Test OpenAI connection with LiteLLM."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not found in .env")
        sys.exit(1)

    print("Testing OpenAI connection...")
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")

    try:
        response = await acompletion(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in Japanese"}],
            api_key=api_key,
        )

        content = response.choices[0].message.content
        print(f"\nSuccess! Response:\n{content}")

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_openai())
