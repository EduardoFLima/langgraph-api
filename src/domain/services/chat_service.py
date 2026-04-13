
from langchain.messages import HumanMessage

from src.domain.ports.chat_service_port import ChatServicePort


class ChatService(ChatServicePort):

    def __init__(self, graph):
        self._graph = graph

    def chat(self, question: str) -> dict:
        messages = [HumanMessage(question)]

        result = self._graph.invoke({"messages": messages })

        last_message = result["messages"][-1].content

        return {
            "answer": last_message,
            "scenario": result.get("scenario")
        }
