from abc import ABC, abstractmethod
import ast
import inspect
import sys
import re



class BaseExtractor(ABC):
    def __init__(self, concatenation_type: str = "join"):
        assert concatenation_type in ["join", "first", "last"], "Invalid concatenation type. Must be one of 'join', 'first', 'last'."
        self.concatenation_type = concatenation_type

    @abstractmethod
    def extract_elements(self, text: str) -> list[str]:
        """Extract the content from the text."""
        pass

    def extract(self, text: str) -> str:
        elements = self.extract_elements(text)
        if self.concatenation_type == "join":
            return "\n\n".join(elements)
        elif self.concatenation_type == "first":
            return elements[0]
        elif self.concatenation_type == "last":
            return elements[-1]

class DefaultExtractor(BaseExtractor):
    """Extract the entire text."""
    def extract_elements(self, text: str) -> list[str]:
        return [text]

class ClassExtractor(BaseExtractor):
    """Extract classes from python code."""
    def extract_elements(self, text: str) -> list[str]:
        tree = ast.parse(text)
        lines = text.splitlines()

        class_snippets = [
            "\n".join(lines[node.lineno - 1: node.end_lineno])
            for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        ]
        return class_snippets

class BetweenTokensExtractor(BaseExtractor, ABC):
    """Extract text contained between two tokens."""
    @property
    @abstractmethod
    def begin_token(self) -> str:
        pass

    @property
    @abstractmethod
    def end_token(self) -> str:
        pass

    def extract_elements(self, text: str) -> list[str]:
        pattern = re.compile(
            rf"{re.escape(self.begin_token)}(.*?){re.escape(self.end_token)}",
            re.DOTALL
        )
        matches = pattern.findall(text)
        return [match.strip() for match in matches]

class DescriptionExtractor(BetweenTokensExtractor):
    """Extract descriptions from text."""
    @property
    def begin_token(self) -> str:
        return "START_DESC"
    
    @property
    def end_token(self) -> str:
        return "END_DESC"

class PythonCodeExtractor(BetweenTokensExtractor):
    """Extract python code from text."""
    @property
    def begin_token(self) -> str:
        return "```python"
    
    @property
    def end_token(self) -> str:
        return "```"
    
def __get_classes() -> list[tuple[str, type]]:
    current_module = sys.modules[__name__]
    classes = inspect.getmembers(current_module, inspect.isclass)
    return [(name, cls) for name, cls in classes if cls.__module__ == __name__]


def get_extractor_by_name(name: str) -> BaseExtractor:
    """Get the extractor by name."""
    classes = __get_classes()
    for class_name, cls in classes:
        if class_name.lower() == name.lower():
            return cls()
    raise ValueError(f"Extractor with name {name} not found.")