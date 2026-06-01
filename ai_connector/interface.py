from abc import ABC, abstractmethod
from typing import List

class AIProvider(ABC):
    @abstractmethod
    def message(self, prompt: str) -> str:
        raise NotImplementedError()
    @abstractmethod
    def chatml_message(self, prompt: str) -> List[any]:
        raise NotImplementedError()
