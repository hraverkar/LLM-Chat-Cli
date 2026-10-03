import os
from collections.abc import Iterator
from openai import OpenAI, api_key
from .base import LLMProvider

class OpenAILLMProvider(LLMProvider):
    def __init__(self, model: str = 'gpt-4o'):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def stream(self, messages: list[dict]) -> Iterator[str]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )

        for chunk in response:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield content