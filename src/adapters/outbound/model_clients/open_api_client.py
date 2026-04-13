from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config import Settings
from src.domain.ports.model_client_port import ModelClientPort


class OpenAPIClient(ModelClientPort):

    def __init__(self, settings: Settings):
        self._settings = settings

        self._client = ChatOpenAI(
            api_key=self._settings.openrouter_api_key,
            model=self._settings.models[0],
            temperature=self._settings.temperature,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": self._settings.http_referer,
                "X-Title": self._settings.x_title,
            },
            extra_body={
                "order":"arcee-ai",
                "models": self._settings.models,
                "provider": self._settings.provider,
            },
        )

    def send_prompt(self, prompt):
        print("this is the key:", self._settings.open_router_api_key)
