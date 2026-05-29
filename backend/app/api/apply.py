from fastapi import APIRouter
from ..schemas.common import ApplyResponse
from ..schemas.diff import DiffRequest

router = APIRouter()

@router.post("/")
def apply(request: DiffRequest) -> ApplyResponse:
    return ApplyResponse(status="applied")
