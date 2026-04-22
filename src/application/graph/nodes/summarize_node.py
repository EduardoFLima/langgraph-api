from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from src.application.ports.outbound.model_client_port import ModelClientPort


def summarize(model_client: ModelClientPort):
    def summarize_node(state: dict):
        messages = state.get("messages")
        shrunk_messages = messages[-6:]

        return {
            "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *shrunk_messages
            ]
        }

    return summarize_node
