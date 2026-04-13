from src.domain.ports.model_client_port import ModelClientPort
from src.domain.prompts.identify_ident_prompt import IntentSchema, get_system_prompt, wrap_user_prompt


def identify_intent(model_client: ModelClientPort):
    def identify_intent_node(state: dict):

        prompt = state["messages"][-1].content

        system_prompt = get_system_prompt()
        user_prompt = wrap_user_prompt(prompt)

        structured_response = model_client.send_prompt(system_prompt, user_prompt, IntentSchema)

        return {"scenario": structured_response["scenario"]}

    return identify_intent_node
