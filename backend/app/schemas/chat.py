from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    project_id: str
    message: str
    selected_files: Optional[List[str]] = []
    mode: Optional[str] = "chat"

class ChatResponse(BaseModel):
    reply: str
    used_context: List[str]
    tokens: int
