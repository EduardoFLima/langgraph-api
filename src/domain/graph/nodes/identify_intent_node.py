from langchain.messages import AIMessage

from src.domain.graph.graph_state import Scenario
from src.domain.ports.model_client_port import ModelClientPort


def identify_intent(model_client: ModelClientPort):
    def identify_intent_node(state: dict):

        prompt = state["messages"][-1].content

        model_client.send_prompt(prompt)

        return {"scenario": Scenario.PATH_A}

    return identify_intent_node
