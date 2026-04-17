from langchain.messages import HumanMessage

from src.application.ports.chat_port import ChatServicePort


class ChatService(ChatServicePort):

    def __init__(self, graph):
        self._graph = graph

    def chat(self, thread_id: str, question: str) -> dict:
        messages = [HumanMessage(question)]

        result = self._graph.invoke(
            {"messages": messages},
            {
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        last_message = result["messages"][-1].content

        return {
            "answer": last_message,
            "scenario": result.get("scenario")
        }
