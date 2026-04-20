from langchain.messages import AIMessage
from langgraph.graph import END, START, StateGraph

from src.application.ports.outbound.memory_port import MemoryPort
from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.graph.graph_state import GraphState, Path
from src.application.graph.nodes.identify_intent_node import identify_intent


def load_memory(_, runtime):
    user_id = runtime.context["user_id"] if runtime.context else None
    store = runtime.store if runtime.store else None
    memory = store.get(namespace=("preferences", "paths"), key=user_id) if user_id and store else None

    print("📀 Loaded memory!", memory)

    if memory is None:
        return {}

    return {"user_context": {"preferred_path": memory.value["preferred_path"]}}



def path_a(state: dict, runtime):
    ai_message = AIMessage("you got here in path_a !")

    store_path(runtime, state)

    return {"messages": [ai_message]}

def path_b(state: dict, runtime):
    ai_message = AIMessage("you got here in path_b !")

    store_path(runtime, state)

    return {"messages": [ai_message]}


def store_path(runtime, state):
    user_id = runtime.context["user_id"] if runtime.context else None
    path = state["path"]

    runtime.store.put(
        namespace=("preferences", "paths"),
        key=user_id,
        value={"preferred_path": path.value}
    )


def path_condition(state: dict):
    path = state["path"]
    match path:
        case Path.PATH_A:
            return "path_a"
        case Path.PATH_B:
            return "path_b"
        case _:
            return "path_failure"


def get_graph_definition(model_client: ModelClientPort, memory_saver: MemoryPort):
    agent_builder = StateGraph(GraphState)

    agent_builder.add_node("load_memory", load_memory)
    agent_builder.add_node("identify_intent", identify_intent(model_client))
    agent_builder.add_node("path_a", path_a)
    agent_builder.add_node("path_b", path_b)

    agent_builder.add_edge(START, "load_memory")
    agent_builder.add_edge("load_memory", "identify_intent")
    agent_builder.add_conditional_edges(
        "identify_intent",
        path_condition,
        {"path_a": "path_a", "path_b": "path_b", "path_failure": END},
    )
    agent_builder.add_edge("path_a", END)
    agent_builder.add_edge("path_b", END)

    return agent_builder.compile(
        checkpointer=memory_saver.get_checkpointer(),
        store=memory_saver.get_store()
    )
