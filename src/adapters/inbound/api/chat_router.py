from fastapi import APIRouter, Cookie, Response

from src.adapters.inbound.api.schemas import (
    ChatRequest,
    ChatResponse,
)
from src.dependencies import ChatServiceDep

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def receive_question(request: ChatRequest,
                     response: Response,
                     service: ChatServiceDep,
                     thread_id: str = Cookie(None)):
    chat_response = service.chat(thread_id, request.question)

    response.set_cookie("thread_id", chat_response.get("thread_id"))

    return ChatResponse(answer=chat_response.get("answer"), path=str(chat_response.get("path")))
