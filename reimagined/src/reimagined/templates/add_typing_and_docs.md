You're professional Python developer. You know that type hints and docstrings are crucial for the code readability and maintainability. \
First, you have written some code with some omitting type hints and docstrings. \
Now you want to add type hints and docstrings to your code. 

**Requirements:**
- Add type hints to all _defined_ functions and methods.
    * Note: the _defined_ function is one starting with `def`, _defined_ class is one starting with `class`.
- Add docstrings to all _defined_ functions, methods, classes and modules.
    * Note: if docstring is already present, you might add to its content, but SAVE the existing content.
- Don't change the code logic at all.
    - For example, don't remove existing imports or change their order.
- Add required imports if needed (e.g. `from typing import List`, `import torch`).

**Notes:**
- You can remove unnecessary comments


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
        
        :param prompt: Prompt object.
        :return: Response from the API (string).
        :raises: UnsuccessfulRequestException.
        """
        try:
            return self.__call__(prompt)
        except Exception as e:
            raise UnsuccessfulRequestException(f"Error: {{str(e)}}")

    @abstractmethod
    def __call__(self, prompt: Prompt) -> str:
        """Method for making a request to the API.
        
        :param prompt: Prompt object.
        :return: Response from the API (string).
        """
        pass
```

Input:
```python
class RNNLanguageModel(nn.Module, BaseLanguageModel):
    def __init__(self, tokens, emb_size=16, hid_size=256):
        """ 
        Build a recurrent language model.
        You are free to choose anything you want, but the recommended architecture is
        - token embeddings
        - one or more LSTM/GRU layers with hid size
        - linear layer to predict logits
        
        :note: if you use nn.RNN/GRU/LSTM, make sure you specify batch_first=True
         With batch_first, your model operates with tensors of shape [batch_size, sequence_length, num_units]
         Also, please read the docs carefully: they don't just return what you want them to return :)
        """
        super().__init__() # initialize base class to track sub-layers, trainable variables, etc.
        
        # YOUR CODE - create layers/variables/etc
        n_tokens = len(tokens)
        self.tokens = tokens

        self.emb = nn.Embedding(n_tokens, emb_size)
        self.gru = nn.GRU(input_size=emb_size, hidden_size=hid_size, batch_first=True)
        self.lin = nn.Linear(hid_size, n_tokens)
```

Output:

YOUR REASONING HERE

```python
class RNNLanguageModel(nn.Module, BaseLanguageModel):
    def __init__(self, tokens, emb_size=16, hid_size=256):
        """ 
        Build a recurrent language model.
        You are free to choose anything you want, but the recommended architecture is
        - token embeddings
        - one or more LSTM/GRU layers with hid size
        - linear layer to predict logits
        
        :param tokens: List of tokens.
        :param emb_size: Size of the embedding layer.
        :param hid_size: Size of the hidden layer.
        :note: if you use nn.RNN/GRU/LSTM, make sure you specify batch_first=True
         With batch_first, your model operates with tensors of shape [batch_size, sequence_length, num_units]
         Also, please read the docs carefully: they don't just return what you want them to return :)
        """
        super().__init__() # initialize base class to track sub-layers, trainable variables, etc.
        
        # YOUR CODE - create layers/variables/etc
        n_tokens = len(tokens)
        self.tokens = tokens

        self.emb = nn.Embedding(n_tokens, emb_size)
        self.gru = nn.GRU(input_size=emb_size, hidden_size=hid_size, batch_first=True)
        self.lin = nn.Linear(hid_size, n_tokens)
```

### Your task

**Reminder:**
Don't change the code logic at all.
- Don't change the imports
- Don't shorten or remove the existing docstrings
- Sometimes, docsting is well written, and there's no need to add anything

**HIGHLY IMPORTANT:** The existing docstrings content might be **only** extended, not replaced or removed.
It's crucially important to keep the existing docstrings content. You fail in case you don't keep it.


Input:
```python
{code}
```

Output:


