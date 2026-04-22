from enum import Enum

from langgraph.graph import MessagesState


class Path(Enum):
    PATH_A = "path_a"
    PATH_B = "path_b"
    UNKNOWN = "unknown_path"


class State(MessagesState):
    user_context: dict
    path: Path
