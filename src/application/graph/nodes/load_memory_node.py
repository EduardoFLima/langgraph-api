import logging

logger = logging.getLogger(__name__)


def load_memory(_, runtime):
    user_id = runtime.context["user_id"] if "user_id" in runtime.context else None
    store = runtime.store if runtime.store else None

    memory = store.get_preferred_path(user_id)  if user_id else None

    logger.info("📀 Loaded memory! %s", memory)

    if memory is None:
        return {}

    return {"user_context": {"preferred_path": memory.value["preferred_path"]}}
