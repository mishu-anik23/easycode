from fastapi import APIRouter
from ..schemas.plan import PlanRequest, PlanResponse
from ..services.task_service import TaskService

router = APIRouter()
service = TaskService()

@router.post("/")
def plan(request: PlanRequest) -> PlanResponse:
    return PlanResponse(steps=service.create_task_list(request.goal))
