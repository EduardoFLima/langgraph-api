from fastapi import APIRouter

from src.adapters.inbound.api.schemas import (
    ChatRequest,
    ChatResponse,
)
from src.dependencies import ChatServiceDep

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def receive_question(request: ChatRequest, service: ChatServiceDep):
    
    chat_response = service.chat(request.question)

    return ChatResponse(answer=chat_response.get("answer"), scenario=chat_response.get("scenario") )
