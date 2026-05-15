from langchain_core.tools import BaseTool
from langgraph.runtime import Runtime

from config import Settings
from src.application.graph.message_extractor import extract_conversation_history
from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.prompts.report_prompt import get_system_prompt, get_user_prompt


def generate_report(settings: Settings, model_client: ModelClientPort, tools: list[BaseTool]):
    async def generate_report_node(state: dict, runtime: Runtime):
        user_id = runtime.context["user_id"] if "user_id" in runtime.context else None
        system_prompt = get_system_prompt(user_id, settings.reports_dir)

        conversation_history = extract_conversation_history(state.get("messages"))
        user_prompt = get_user_prompt(conversation_history)

        await model_client.send_prompt_with_tools(system_prompt, user_prompt, tools)

        return state

    return generate_report_node
