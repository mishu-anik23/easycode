from fastapi import APIRouter
from ..schemas.search import SearchRequest, SearchResponse

router = APIRouter()

@router.post("/")
def search(request: SearchRequest) -> SearchResponse:
    return SearchResponse(results=["Stub search result for query: " + request.query])
