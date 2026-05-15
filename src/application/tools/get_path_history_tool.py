import logging

from langchain_core.tools import tool

from src.application.ports.outbound.path_history_port import PathHistoryPort

logger = logging.getLogger(__name__)


def make_get_path_history_tool(path_history_repo: PathHistoryPort):
    @tool
    def get_path_history(runtime) -> list[dict]:
        """Search path history for given user"""

        try:
            user_id = runtime.context["user_id"] if "user_id" in runtime.context else None
            return path_history_repo.get_path_history(user_id)

        except Exception as e:
            logger.error("\n❌ Error while executing get_path_history tool: %s", e)
            return []

    return get_path_history
