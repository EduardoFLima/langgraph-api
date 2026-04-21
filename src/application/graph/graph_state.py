import operator
from enum import Enum

from langchain.messages import AnyMessage
from typing_extensions import Annotated, TypedDict


class Path(Enum):
    PATH_A = "path_a"
    PATH_B = "path_b"
    UNKNOWN = "unknown_path"


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_context: dict
    path: Path
