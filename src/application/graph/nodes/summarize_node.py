from langchain_core.messages import RemoveMessage, HumanMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.prompts.summarize_prompt import get_system_prompt, wrap_user_prompt, SummarizeSchema


def summarize(model_client: ModelClientPort):
    def summarize_node(state: dict, runtime):
        messages = state.get("messages")

        conversation_history = [("User: " if isinstance(message, HumanMessage) else "AI: ") + message.content
                                for message in messages]

        system_prompt = get_system_prompt()
        user_prompt = wrap_user_prompt(conversation_history)

        structured_response = model_client.send_prompt(system_prompt, user_prompt, SummarizeSchema)
        preferred_path = structured_response.preferred_path

        shrunk_messages = messages[-6:]

        user_id = runtime.context["user_id"] if runtime.context else None
        runtime.store.put(
            namespace=("preferences", "paths"),
            key=user_id,
            value={"preferred_path": preferred_path.value}
        )

        return {
            "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *shrunk_messages
            ],
            "preferred_path": preferred_path
        }

    return summarize_node
