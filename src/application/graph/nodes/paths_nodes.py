from langchain_core.messages import AIMessage


def path_a(state, runtime):
    save_history(state, runtime)

    return {"messages": [AIMessage("You will take the path_a !")]}


def path_b(state, runtime):
    save_history(state, runtime)

    return {"messages": [AIMessage("You will take the path_b !")]}


def unknown_path(state, runtime):
    save_history(state, runtime)

    return {
        "messages": [
            AIMessage("Apologies. Couldn't understand the path you want to take.")
        ]
    }


def save_history(state, runtime):
    user_id = runtime.context["user_id"] if "user_id" in runtime.context else None

    runtime.store.store_path_to_history(user_id, state["path"].value)