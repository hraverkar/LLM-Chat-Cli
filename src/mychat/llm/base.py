from abc import ABC, abstractmethod
from collections.abc import Iterator

class LLMProvider(ABC):
    @abstractmethod
    def stream(self, messages: list[dict[str, str]]) -> Iterator[str]:
        """Stream a response for the given conversation messages."""
        raise NotImplementedError("Subclasses must implement the stream method.")