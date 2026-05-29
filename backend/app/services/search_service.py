from pathlib import Path
from typing import List

class SearchService:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def search(self, query: str) -> List[str]:
        query_lower = query.lower().strip()
        if not query_lower:
            return []

        results: List[str] = []
        for path in self.project_root.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if query_lower in line.lower():
                    results.append(f"{path.relative_to(self.project_root)}:{line_no}: {line.strip()}")
                    if len(results) >= 50:
                        return results
        return results
