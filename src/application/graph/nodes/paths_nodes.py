from langchain_core.messages import AIMessage

from src.application.ports.outbound.path_history_port import PathHistoryPort


def path_a(path_history_repo: PathHistoryPort):
    def path_a_node(state, runtime):
        save_history(state, runtime, path_history_repo)
        return {"messages": [AIMessage("You will take the path_a !")]}
    return path_a_node


def path_b(path_history_repo: PathHistoryPort):
    def path_b_node(state, runtime):
        save_history(state, runtime, path_history_repo)
        return {"messages": [AIMessage("You will take the path_b !")]}
    return path_b_node


def unknown_path(path_history_repo: PathHistoryPort):
    def unknown_path_node(state, runtime):
        save_history(state, runtime, path_history_repo)
        return {
            "messages": [
                AIMessage("Apologies. Couldn't understand the path you want to take.")
            ]
        }
    return unknown_path_node


def save_history(state, runtime, path_history_repo: PathHistoryPort):
    user_id = runtime.context["user_id"] if "user_id" in runtime.context else None

    if user_id:
        path_history_repo.store_path_to_history(user_id, state["path"].value)
