import requests
import json
from ..core.config import settings

class OllamaClient:
    def __init__(self, base_url: str = settings.ollama_url, model_name: str = settings.model_name):
        self.base_url = base_url
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """Generate text using Ollama API"""
        try:
            # Use the correct Ollama API endpoint
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60,
            )
            response.raise_for_status()
            
            data = response.json()
            # Ollama returns response in the "response" field
            if isinstance(data, dict):
                return data.get("response") or data.get("output") or data.get("text") or str(data)
            return str(data)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Please ensure Ollama is running: ollama serve"
            ) from e
        except requests.exceptions.HTTPError as e:
            if "404" in str(e):
                raise RuntimeError(
                    f"Model '{self.model_name}' not found in Ollama. "
                    f"Pull it with: ollama pull {self.model_name}"
                ) from e
            raise RuntimeError(f"Ollama error: {str(e)}") from e

    def list_models(self) -> list:
        """List available models in Ollama"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            models = [model.get("name") for model in data.get("models", [])]
            return models
        except Exception as e:
            return []

    def health_check(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
