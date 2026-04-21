def load_memory(_, runtime):
    user_id = runtime.context["user_id"] if runtime.context and runtime.context.get("user_id") else None
    store = runtime.store if runtime.store else None
    memory = store.get(namespace=("preferences", "paths"), key=user_id) if user_id and store else None

    print("📀 Loaded memory!", memory)

    if memory is None:
        return {}

    return {"user_context": {"preferred_path": memory.value["preferred_path"]}}
