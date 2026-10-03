from .base import LLMProvider
from .ollama import OllamaLLMProvider
from .openai import OpenAILLMProvider


def create_llm_provider(provider_name: str, model: str = None) -> LLMProvider:
    if provider_name.lower() == "ollama":
        return OllamaLLMProvider(model=model or 'llama3.2:latest')
    elif provider_name.lower() == "openai":
        return OpenAILLMProvider(model=model or 'gpt-4o')
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")