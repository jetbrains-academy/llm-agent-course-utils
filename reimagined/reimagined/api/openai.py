import openai

from .base import Prompt, APIBase


class OpenAIApi(APIBase):
    def __init__(self, model: str, token: str | None = None) -> None:
        """Initializes the API.
        :param model: Name of model to use.
        :param token: OpenAI API token. If None, the token will be read from the OPENAI_API_KEY environment variable.
        """
        self.model = model
        self.client = openai.OpenAI(api_key=token)

    def __call__(self, prompt: Prompt) -> str:
        """Returns generated text."""
        messages = []
        if prompt.system is not None:
            messages.append({"role": "system", "content": prompt.system})
        messages.append({"role": "user", "content": prompt.content})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        # Return the response content from the OpenAI API
        return response.choices[0].message.content
