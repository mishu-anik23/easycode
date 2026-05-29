from pydantic import BaseModel
from pathlib import Path
from typing import Optional

class IndexRequest(BaseModel):
    project_path: Optional[Path] = None

class IndexResponse(BaseModel):
    status: str
    files: int
