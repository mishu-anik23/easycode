from pathlib import Path
from typing import List

class RepoIndexer:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def index(self) -> List[str]:
        return [str(path.relative_to(self.project_root)) for path in self.project_root.rglob("*.py")]
