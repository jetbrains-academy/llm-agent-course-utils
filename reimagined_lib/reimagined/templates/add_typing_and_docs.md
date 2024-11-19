You're professional python developer. \
First, you have written some code without any type hints and docstrings. \
Now you want to add type hints and docstrings to your code. 

**Requirements:**
- Add type hints to all functions and methods.
- Add docstrings to all functions, methods, classes and modules.


### Example

Input:
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Prompt:
    content: str
    system: str | None = None

    def __str__(self):
        result = f"INSTRUCTION:\n\n{{self.system}}\n" if self.system is not None else ""
        result += self.content
        return result

class UnsuccessfulRequestException(Exception):
    pass
    

class APIBase(ABC):
    def query(self, prompt):
        try:
            return self.__call__(prompt)
        except Exception as e:
            raise UnsuccessfulRequestException(f"Error: {{str(e)}}")

    @abstractmethod
    def __call__(self, prompt):
        pass
```

Output:

YOUR REASONING HERE

```python
"""
Module with implementation of APIBase class (Base class for API classes).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Prompt:
    """
    Dataclass for prompt object.
    """
    content: str
    system: str | None = None

    def __str__(self) -> str:
        """Return string representation of the prompt object."""
        result = f"INSTRUCTION:\n\n{{self.system}}\n" if self.system is not None else ""
        result += self.content
        return result

class UnsuccessfulRequestException(Exception):
    """Exception for unsuccessful request to the API."""
    pass
    

class APIBase(ABC):
    """Base class for API classes."""
    def query(self, prompt: Prompt) -> str:
        """Analogue of __call__ method which throws a universal exception.
        
        :@param prompt: Prompt object.
        :@return: Response from the API (string).
        """
        try:
            return self.__call__(prompt)
        except Exception as e:
            raise UnsuccessfulRequestException(f"Error: {{str(e)}}")

    @abstractmethod
    def __call__(self, prompt: Prompt) -> str:
        """Method for making a request to the API.
        
        :@param prompt: Prompt object.
        :@return: Response from the API (string).
        """
        pass
```

### Your task

Input:
```python
{code}
```

Output:
