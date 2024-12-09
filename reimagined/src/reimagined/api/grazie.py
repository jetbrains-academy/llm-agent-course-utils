from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient, RequestFailedException
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from grazie.api.client.profiles import Profile

from .base import Prompt, APIBase


class GrazieApi(APIBase):
    """Grazie API handler."""
    TEMPERATURE = 0.6
    MODEL_FAMILIES_SUPPORTING_SYSTEM = {
        "openai",
        "gpt",
    }

    def __init__(self, token: str, model: str) -> None:
        """Initializes the API.
        :@param token: Grazie API token.
        :@param model: Name of model to use.
        :@param supports_system: Whether the model supports system messages.
        """
        self.client = GrazieApiGatewayClient(
            grazie_agent=GrazieAgent(name="Rodion.Khvorostov", version="dev"),
            url=GrazieApiGatewayUrls.STAGING,
            auth_type=AuthType.USER,
            grazie_jwt_token=token
        )
        self.model_profile = Profile.get_by_name(model)
        self.supports_system = any(family in model for family in self.MODEL_FAMILIES_SUPPORTING_SYSTEM)

    def __call__(self, prompt: Prompt) -> str:
        """Returns generated text."""
        if self.supports_system:
            chat = ChatPrompt().add_system(prompt.system).add_user(prompt.content)
        else:
            chat = ChatPrompt().add_user(str(prompt))

        res = self.client.chat(
            chat=chat,
            profile=self.model_profile,
            parameters={
                LLMParameters.Temperature: Parameters.FloatValue(self.TEMPERATURE)
            }
        )

        return res.content
