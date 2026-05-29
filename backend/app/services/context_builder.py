from pathlib import Path
from typing import List

class ContextBuilder:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def build_context(self, paths: List[str]) -> str:
        context = []
        for path in paths:
            file_path = self.project_root / path
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                context.append(f"# File: {path}\n{content}")
        return "\n\n".join(context) if context else ""
