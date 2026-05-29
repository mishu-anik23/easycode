from fastapi import APIRouter, HTTPException
from ..core.config import settings
from ..core.prompts import CHAT_PROMPT_TEMPLATE
from ..schemas.chat import ChatRequest, ChatResponse
from ..services.context_builder import ContextBuilder
from ..services.ollama_client import OllamaClient

router = APIRouter()
chat_client = OllamaClient()

@router.post("/")
def chat(request: ChatRequest) -> ChatResponse:
    selected_files = request.selected_files or []
    builder = ContextBuilder(settings.project_root)
    context = builder.build_context(selected_files)
    prompt = f"{CHAT_PROMPT_TEMPLATE}\n\nGoal: {request.message}\n\nContext:\n{context}\n\nReply with a concise answer."

    try:
        reply = chat_client.generate(prompt)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {exc}")

    tokens = len(reply.split())
    return ChatResponse(reply=reply, used_context=selected_files, tokens=tokens)
