from fastapi import APIRouter
from ..schemas.diff import DiffRequest, DiffResponse

router = APIRouter()

@router.post("/")
def diff(request: DiffRequest) -> DiffResponse:
    return DiffResponse(diff="--- a/example.py\n+++ b/example.py\n@@ -0,0 +1,1 @@\n+// TODO: implement diff generation")
