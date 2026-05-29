from fastapi import APIRouter, HTTPException
from ..core.config import settings
from ..core.prompts import DIFF_PROMPT_TEMPLATE
from ..schemas.diff import DiffRequest, DiffResponse
from ..services.context_builder import ContextBuilder
from ..services.ollama_client import OllamaClient

router = APIRouter()
llm = OllamaClient()

@router.post("/")
def diff(request: DiffRequest) -> DiffResponse:
    if not request.files:
        raise HTTPException(status_code=400, detail="At least one file must be provided for diff generation.")

    builder = ContextBuilder(settings.project_root)
    context = builder.build_context(request.files)
    prompt = (
        f"{DIFF_PROMPT_TEMPLATE}\n\nGoal: {request.goal}\nFiles: {request.files}\n\nContext:\n{context}"
    )

    try:
        diff_text = llm.generate(prompt)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {exc}")

    return DiffResponse(diff=diff_text)
