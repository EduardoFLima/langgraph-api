import json

from langchain.messages import HumanMessage
from langgraph.runtime import Runtime

from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.prompts.identify_ident_prompt import IntentSchema, get_system_prompt, wrap_user_prompt


def extract_conversation_history(messages) -> str:
    if messages is None:
        return ""

    return str(messages[:-1])


def identify_intent(model_client: ModelClientPort):
    def identify_intent_node(state: dict):
        dumped_user_context = json.dumps(state["user_context"]) if state.get("user_context") else "None"
        system_prompt = get_system_prompt(dumped_user_context)

        prompt = extract_prompt_from(state)
        conversation_history = extract_conversation_history(state.get("messages"))
        user_prompt = wrap_user_prompt(prompt, conversation_history)

        structured_response = model_client.send_prompt(system_prompt, user_prompt, IntentSchema)

        return {"path": structured_response["path"]}

    return identify_intent_node


def extract_prompt_from(state):
    message = state["messages"][-1]

    # Handle messages coming from chats service
    if isinstance(message, HumanMessage):
        prompt = message.content
    else:
        content = message.get("content")
        # Handle messages coming from langsmith studio's chat
        if isinstance(content, list):
            prompt = message["content"][0]["text"]
        else:
            # Handle messages coming from langsmith studio's graph
            prompt = message["content"]
    return prompt
