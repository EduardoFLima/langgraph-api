from enum import Enum
import operator

from langchain.messages import AnyMessage
from typing_extensions import Annotated, TypedDict


class Scenario(Enum):
    PATH_A = "path_a_scenario"
    PATH_B = "path_b_scenario"


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    scenario: Scenario
