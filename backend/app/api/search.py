from fastapi import APIRouter
from ..core.config import settings
from ..schemas.search import SearchRequest, SearchResponse, FolderSearchRequest, FolderSearchResponse, AuthUrlResponse
from ..services.search_service import SearchService
from ..services.cloud_search_service import CloudSearchService

router = APIRouter()
service = SearchService(settings.project_root)
cloud_service = CloudSearchService()

@router.post("/")
def search(request: SearchRequest) -> SearchResponse:
    results = service.search(request.query)
    return SearchResponse(results=results)

@router.post("/folder/local")
def search_folder_local(request: FolderSearchRequest) -> FolderSearchResponse:
    """Search for code files in a local folder"""
    results = service.search_folder(request.folder_path, request.query)
    return FolderSearchResponse(results=results, source="local")

@router.post("/folder/google-drive")
def search_folder_google_drive(request: FolderSearchRequest) -> FolderSearchResponse:
    """Search for code files in Google Drive"""
    try:
        results = cloud_service.search_google_drive(request.query, request.auth_token)
        return FolderSearchResponse(results=results, source="google_drive")
    except Exception as e:
        return FolderSearchResponse(results=[], source="google_drive", error=str(e))

@router.post("/folder/dropbox")
def search_folder_dropbox(request: FolderSearchRequest) -> FolderSearchResponse:
    """Search for code files in Dropbox"""
    try:
        results = cloud_service.search_dropbox(request.query, request.auth_token)
        return FolderSearchResponse(results=results, source="dropbox")
    except Exception as e:
        return FolderSearchResponse(results=[], source="dropbox", error=str(e))
