from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from src.application.ports.outbound.model_client_port import ModelClientPort

def summarize(model_client: ModelClientPort):
    def summarize_node(state: dict, runtime):
        messages = state.get("messages")
        shrunk_messages = messages[-6:]

        path = state["path"]
        user_id = runtime.context["user_id"] if runtime.context else None

        runtime.store.put(
            namespace=("preferences", "paths"),
            key=user_id,
            value={"preferred_path": path.value}
        )

        return {
            "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *shrunk_messages
            ]
        }

    return summarize_node
