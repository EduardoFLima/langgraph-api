from langchain.messages import AIMessage

from src.domain.graph.graph_state import Scenario


def identify_intent(state: dict):

    return {"scenario": Scenario.PATH_A}
