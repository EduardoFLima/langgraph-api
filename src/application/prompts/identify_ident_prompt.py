from functools import lru_cache
import json

from pydantic import BaseModel, Field

from src.application.graph.graph_state import Scenario


class IntentSchema(BaseModel):
    path: str = Field(description="The chosen path")
    scenario: Scenario = Field(description="Each path leads to a scenario")

@lru_cache
def get_system_prompt(previous_path: str) -> str:
    system_prompt = {
        "role": "You are a helpful attendant",
        "task": "Identify user intent and extract details on the path they want to go",
        "rules": {
            "path_a": {
                "description": "the path A",
                "keywords": ["first path", "path a", "go left", "first choice"],
            },
            "path_b": {
                "description": "the path B",
                "keywords": ["second path", "path b", "go right", "alternative"],
            },
            "unknown": {
                "description": "when the chosen path is unclear",
            },
        },
        "previous_path": previous_path,
        "extraction_instructions": {
            "path": "Extract the user intent from its prompt or from previous_path",
            "scenario": "Extract the scenario according to the chosen path or from previous_path"
        },
        "examples": [
            {
                "input": "I want the first path",
                "output": {
                    "path": "Path A",
                    "scenario": "path_a_scenario"
                },
            },
            {
                "input": "I want some alternative path",
                "output": {
                    "path": "Path B",
                    "scenario": "path_b_scenario"
                },
            },
            {
                "input": "How are you?",
                "output": {
                    "scenario": "unknown"
                },
            },
        ],
    }
    return json.dumps(system_prompt)


def wrap_user_prompt(prompt: str) -> str:
    user_prompt = {
        "request": prompt,
        "instructions": [
            "Carefully analyze the question to determine the user intent",
            "Extract all relevant details only from the user prompt",
            "Return only the fields that are present in the request",
            "Never infer or fabricate values"
        ],
    }

    return json.dumps(user_prompt)
