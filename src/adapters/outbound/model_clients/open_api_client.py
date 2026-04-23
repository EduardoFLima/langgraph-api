from typing import TypeVar

from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.application.ports.outbound.model_client_port import ModelClientPort
from src.config import Settings

T = TypeVar("T")

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
                "order": "arcee-ai",
                "models": self._settings.models,
                "provider": self._settings.provider,
            },
        )

    def send_prompt(
            self, system_prompt: str, user_prompt: str, response_format: type[T]
    ) -> T:
        agent = create_agent(
            model=self._client, tools=[], response_format=response_format
        )

        print("\n⌛...calling the agent...")

        try:
            data = agent.invoke(
                {"messages": [SystemMessage(system_prompt), HumanMessage(user_prompt)]}
            )

            last_ai_message = data["messages"][-2]

            if last_ai_message is not None and isinstance(last_ai_message, AIMessage):
                print(
                    f"\nℹ️ Got a response. The model used was {last_ai_message.response_metadata["model_name"]}",
                )

            structured_response = data.get("structured_response")

            if structured_response is not None:
                return structured_response


        except Exception as e:
            answer = "An error occurred when calling the llm provider"
            print(f"{answer}:", e)

        return None
