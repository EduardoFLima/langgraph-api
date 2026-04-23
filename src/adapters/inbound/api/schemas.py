from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    path: str
    preferred_path: str
    messages: list[str]
