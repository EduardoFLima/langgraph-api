from langgraph.graph import END, START, StateGraph

from src.domain.graph.graph_state import GraphState
from src.domain.graph.nodes.identify_intent_node import identify_intent


def create_graph():

    agent_builder = StateGraph(GraphState)

    agent_builder.add_node("identify_intent", identify_intent)

    agent_builder.add_edge(START, "identify_intent")
    agent_builder.add_edge("identify_intent", END)

    return agent_builder.compile()
