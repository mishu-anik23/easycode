from fastapi import APIRouter
from ..schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply="This is a stub response.", used_context=request.selected_files or [], tokens=0)
