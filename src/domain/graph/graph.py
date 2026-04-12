from langchain.messages import AIMessage
from langgraph.graph import END, START, StateGraph

from src.domain.graph.graph_state import GraphState, Scenario
from src.domain.graph.nodes.identify_intent_node import identify_intent
from src.domain.ports.model_client_port import ModelClientPort


def path_a(state: dict):
    ai_message = AIMessage("you got here in path_a ! good.")

    return {"messages": [ai_message]}


def path_b(state: dict):
    return state


def path_condition(state: dict):
    scenario = state["scenario"]
    match scenario:
        case Scenario.PATH_A:
            return "path_a"
        case Scenario.PATH_B:
            return "path_b"
        case _:
            return "path_failure"


def get_graph_definition(model_client: ModelClientPort):

    agent_builder = StateGraph(GraphState)

    agent_builder.add_node("identify_intent", identify_intent(model_client))
    agent_builder.add_node("path_a", path_a)
    agent_builder.add_node("path_b", path_b)

    agent_builder.add_edge(START, "identify_intent")
    agent_builder.add_conditional_edges(
        "identify_intent",
        path_condition,
        {"path_a": "path_a", "path_b": "path_b", "path_failure": END},
    )
    agent_builder.add_edge("path_a", END)
    agent_builder.add_edge("path_b", END)

    return agent_builder.compile()
