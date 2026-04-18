from datetime import datetime

from langchain.messages import HumanMessage

from src.application.ports.inbound.chat_use_case import ChatUseCase

def resolve_thread_id(thread_id: str) -> str:
    if thread_id is None:
        thread_id = str(datetime.now())
        print("thread_id was null ❌, generated one 🔨", thread_id)
    else:
        print("got an existing thread_id ✅", thread_id)
    return thread_id


class ChatService(ChatUseCase):

    def __init__(self, graph):
        self._graph = graph

    def chat(self, thread_id: str, question: str) -> dict:
        print(f"\n\n===== received a message =====\nmessage:{question}\n")

        messages = [HumanMessage(question)]

        thread_id = resolve_thread_id(thread_id)

        result = self._graph.invoke(
            {"messages": messages},
            {
                "configurable": {
                    "thread_id": thread_id
                },
                "context": { "userId": "actualUserId" }
            }
        )

        last_message = result["messages"][-1].content
        scenario = result.get("scenario").value

        print("✅ The resulting scenario was:", scenario)

        return {
            "answer": last_message,
            "scenario": scenario,
            "thread_id": thread_id
        }
