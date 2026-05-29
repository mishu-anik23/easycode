from fastapi import APIRouter
from ..core.config import settings
from ..schemas.search import SearchRequest, SearchResponse
from ..services.search_service import SearchService

router = APIRouter()
service = SearchService(settings.project_root)

@router.post("/")
def search(request: SearchRequest) -> SearchResponse:
    results = service.search(request.query)
    return SearchResponse(results=results)
