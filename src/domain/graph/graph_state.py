import operator

from langchain.messages import AnyMessage
from typing_extensions import Annotated, TypedDict


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
