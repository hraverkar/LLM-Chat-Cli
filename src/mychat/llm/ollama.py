from collections.abc import Iterator

from openai import OpenAI
from .base import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self, model: str = 'llama3.2:latest',
                 base_url: str = "http://localhost:11434/v1",
                 api_key: str = "ollama"):
        self.model = model
        self.client = OpenAI(base_url=base_url, api_key=api_key)


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