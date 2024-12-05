from .base import Prompt, APIBase
# from .grazie import GrazieApi  # TO-DO: Uncomment this line after implementing Grazie API
from .openai import OpenAIApi

def get_api_class_by_name(name: str) -> OpenAIApi:
    """Get the API by name."""
    api_cls = {
        # "grazie": GrazieApi,  # TO-DO: Uncomment this line after implementing Grazie API
        "openai": OpenAIApi,
    }
    return api_cls[name]
