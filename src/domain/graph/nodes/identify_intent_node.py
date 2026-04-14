from langchain.messages import HumanMessage

from src.domain.ports.model_client_port import ModelClientPort
from src.domain.prompts.identify_ident_prompt import IntentSchema, get_system_prompt, wrap_user_prompt


def identify_intent(model_client: ModelClientPort):
    def identify_intent_node(state: dict):
        prompt = extract_prompt_from(state)

        system_prompt = get_system_prompt()
        user_prompt = wrap_user_prompt(prompt)

        structured_response = model_client.send_prompt(system_prompt, user_prompt, IntentSchema)

        return {"scenario": structured_response["scenario"]}

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