from fastapi import APIRouter, HTTPException
from ..schemas.common import ApplyResponse
from ..schemas.diff import DiffRequest
from ..services.patch_service import PatchService

router = APIRouter()
service = PatchService()

@router.post("/")
def apply(request: DiffRequest) -> ApplyResponse:
    if not request.diff:
        raise HTTPException(status_code=400, detail="Missing diff payload.")

    success = service.apply_diff(request.diff)
    if not success:
        raise HTTPException(status_code=400, detail="Diff validation or application failed.")

    return ApplyResponse(status="applied")
