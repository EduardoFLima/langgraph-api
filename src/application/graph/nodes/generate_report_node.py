from langchain_core.tools import BaseTool
from langgraph.runtime import Runtime

from src.application.graph.message_extractor import extract_conversation_history
from src.application.ports.outbound.model_client_port import ModelClientPort
from src.application.prompts.report_prompt import get_system_prompt, get_user_prompt
from src.config import Settings


def generate_report(settings: Settings, model_client: ModelClientPort, tools: list[BaseTool]):
    async def generate_report_node(state: dict, runtime: Runtime):
        should_generate_report = runtime.context["should_generate_report"] if "should_generate_report" in runtime.context else None

        if not should_generate_report:
            return state

        user_id = runtime.context["user_id"] if "user_id" in runtime.context else None
        system_prompt = get_system_prompt(user_id, settings.reports_dir)

        conversation_history = extract_conversation_history(state.get("messages"))
        user_prompt = get_user_prompt(conversation_history)

        await model_client.send_prompt_with_tools(system_prompt, user_prompt, tools)

        return state

    return generate_report_node
