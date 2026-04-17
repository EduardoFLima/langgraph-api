from fastapi import APIRouter, Cookie

from src.adapters.inbound.api.schemas import (
    ChatRequest,
    ChatResponse,
)
from src.dependencies import ChatServiceDep

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def receive_question(request: ChatRequest, service: ChatServiceDep, thread_id: str = Cookie(None)):
    
    chat_response = service.chat(thread_id, request.question)

    return ChatResponse(answer=chat_response.get("answer"), scenario=chat_response.get("scenario") )
