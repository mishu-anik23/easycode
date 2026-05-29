from pydantic import BaseModel
from typing import List

class PlanRequest(BaseModel):
    project_id: str
    goal: str

class PlanResponse(BaseModel):
    steps: List[str]
