from mychat.config import Settings

from .base import LLMProvider
from .ollama import OllamaLLMProvider
from .openai import OpenAILLMProvider


def create_llm_provider(provider: str | None = None, model: str | None = None) -> LLMProvider:
    settings = Settings()
    selected_provider = provider or settings.llm_provider
    if selected_provider.lower() == "ollama":
        return OllamaLLMProvider(model=model or settings.llm_model)
    elif selected_provider.lower() == "openai":
        return OpenAILLMProvider(model=model or settings.openai_model)
    else:
        raise ValueError(f"Unknown LLM provider: {selected_provider}")