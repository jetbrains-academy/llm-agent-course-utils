import re
from ..api.base import Prompt

class Prompter:
    """Class to create a prompt based on a template."""
    def __init__(self, template: str) -> None:
        self.template = template
        self.vars = self._get_template_vars()
    
    def _get_template_vars(self) -> list:
        """Get the variables in the template."""
        # return re.findall(r"\{(\w+)\}", self.template)
        return re.findall(r"[^\{]\{(\w+)\}[^\}]", self.template)
    
    def _check_params(self, **params) -> None:
        """Check if all the variables are present in the parameters."""
        missing_params = [var for var in self.vars if var not in params]
        if missing_params:
            raise ValueError(f"Missing parameters: {missing_params}")
        
        extra_params = [param for param in params if param not in self.vars]
        if extra_params:
            raise ValueError(f"Extra parameters: {extra_params}")

    def prompt(self, **params) -> Prompt:
        """Create a prompt based on the template.

        Raises ValueError if any of the variables are missing or if there are extra parameters.
        """
        self._check_params(**params)
        content = self.template.format(**params) 
        return Prompt(content=content)
