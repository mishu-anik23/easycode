from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    project_id: str
    query: str

class SearchResponse(BaseModel):
    results: List[str]
