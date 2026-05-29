import requests
from ..core.config import settings

class OllamaClient:
    def __init__(self, base_url: str = settings.ollama_url, model_name: str = settings.model_name):
        self.base_url = base_url
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/generate",
            json={"model": self.model_name, "prompt": prompt},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data.get("output") or data.get("response") or data.get("text") or response.text
        return response.text
