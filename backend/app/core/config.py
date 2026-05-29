from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    project_id: str = "easycode"
    database_url: str = "sqlite:///./easycode.db"
    ollama_url: str = "http://127.0.0.1:11434"
    model_name: str = "qwen2.5-coder-7b"
    project_root: Path = Path.cwd()

    class Config:
        env_file = ".env"

settings = Settings()
