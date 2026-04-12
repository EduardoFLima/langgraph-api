
from langchain.messages import HumanMessage

from src.domain.graph.factory import graph
from src.domain.ports.chat_service_port import ChatServicePort


class ChatService(ChatServicePort):

    def chat(self, question: str) -> str:
        messages = [HumanMessage(question)]

        result = graph.invoke({"messages": messages })

        last_message = result["messages"][-1].content

        return last_message
