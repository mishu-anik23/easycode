from pydantic import BaseModel

class ApplyResponse(BaseModel):
    status: str

class IndexResponse(BaseModel):
    status: str
    files: int
