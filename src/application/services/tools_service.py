import logging

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.callbacks import CallbackContext, Callbacks
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.types import LoggingMessageNotificationParams

from application.tools.fs_tool import get_fs_tool
from application.tools.get_path_history_tool import get_path_history

logger = logging.getLogger(__name__)


# Define your handler
async def on_logging_message(
        params: LoggingMessageNotificationParams,
        context: CallbackContext,
):
    """Handle log messages from MCP servers."""
    logger.info(f"[{context.server_name}] {params.level}: {params.data}")


async def get_all_mcp_tools(reports_dir) -> list[BaseTool]:
    client = MultiServerMCPClient(
        {
            **get_fs_tool(reports_dir)
        },
        callbacks=Callbacks(
            on_logging_message=on_logging_message,
        ),
    )

    tools = await client.get_tools()

    return tools + [get_path_history]
