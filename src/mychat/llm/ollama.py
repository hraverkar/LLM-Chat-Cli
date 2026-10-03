from collections.abc import Iterator

from openai import OpenAI

from mychat.config import Settings
from .base import LLMProvider


class OllamaLLMProvider(LLMProvider):
    def __init__(self, model: str | None = None):
        self.model = model or Settings().llm_model
        self.client = OpenAI(base_url=Settings().ollama_host, api_key=Settings().ollama_api_key)


    def stream(self, messages: list[dict]) -> Iterator[str]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=Settings().llm_temperature,
            stream=True
        )

        for chunk in response:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield content