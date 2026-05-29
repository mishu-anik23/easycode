from fastapi import APIRouter
from ..schemas.plan import PlanRequest, PlanResponse

router = APIRouter()

@router.post("/")
def plan(request: PlanRequest) -> PlanResponse:
    return PlanResponse(steps=["Inspect current codebase", "Draft plan steps", "Review with user"])
