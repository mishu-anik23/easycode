from fastapi import APIRouter
from ..schemas.common import IndexResponse

router = APIRouter()

@router.post("/")
def index() -> IndexResponse:
    return IndexResponse(status="indexed", files=0)
