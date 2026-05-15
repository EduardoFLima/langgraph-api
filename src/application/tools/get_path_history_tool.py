import logging

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

logger = logging.getLogger(__name__)


@tool
def get_path_history(runtime: ToolRuntime) -> list[dict]:
    """Search path history for given user"""

    try:

        user_id = runtime.context["user_id"] if "user_id" in runtime.context else None
        search_items = runtime.store.get_path_history(user_id)

        path_history = [item.value for item in search_items]

        return path_history

    except Exception as e:
        logger.error("\n❌ Error while executing get_path_history tool: %s", e)
