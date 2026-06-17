from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    project_id: str
    query: str
    search_source: str = "local"

class SearchResponse(BaseModel):
    results: List[str]

class FolderSearchRequest(BaseModel):
    project_id: str
    query: str
    folder_path: Optional[str] = None
    auth_token: Optional[str] = None

class FolderSearchResponse(BaseModel):
    results: List[str]
    source: str
    error: Optional[str] = None

class AuthUrlResponse(BaseModel):
    auth_url: str
