from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Prompt:
    content: str
    system: str | None = None

    def __str__(self) -> str:
        result = f"INSTRUCTION:\n\n{self.system}\n" if self.system is not None else ""
        result += self.content
        return result

class UnsuccessfulRequestException(Exception):
    """Exception for unsuccessful request to the API."""
    pass
    

class APIBase(ABC):
    def query(self, prompt: Prompt) -> str:
        """Analogue of __call__ method which throws a universal exception."""
        try:
            return self.__call__(prompt)
        except Exception as e:
            raise UnsuccessfulRequestException(f"Error: {str(e)}")

    @abstractmethod
    def __call__(self, prompt: Prompt) -> str:
        pass