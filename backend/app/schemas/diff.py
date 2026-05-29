from pydantic import BaseModel
from typing import List, Optional

class DiffRequest(BaseModel):
    project_id: str
    goal: str
    files: Optional[List[str]] = []
    diff: Optional[str] = None

class DiffResponse(BaseModel):
    diff: str
