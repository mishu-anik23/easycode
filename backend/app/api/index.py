from pathlib import Path
from fastapi import APIRouter
from ..core.config import settings
from ..schemas.index import IndexRequest, IndexResponse
from ..services.repo_indexer import RepoIndexer

router = APIRouter()

@router.post("/")
def index(request: IndexRequest = None) -> IndexResponse:
    project_root = settings.project_root
    if request and request.project_path:
        project_root = request.project_path.resolve()

    indexer = RepoIndexer(project_root)
    files = indexer.index()
    return IndexResponse(status="indexed", files=len(files))
