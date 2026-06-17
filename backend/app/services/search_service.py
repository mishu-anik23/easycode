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

    def search_folder(self, folder_path: str, query: str) -> List[str]:
        """Search for code in a local folder"""
        query_lower = query.lower().strip()
        if not query_lower or not folder_path:
            return []

        results: List[str] = []
        folder = Path(folder_path)
        
        if not folder.exists():
            return []

        # Search in common code file extensions
        extensions = ["*.py", "*.js", "*.ts", "*.tsx", "*.jsx", "*.java", "*.cpp", "*.c", "*.go", "*.rs", "*.rb"]
        
        for ext in extensions:
            for path in folder.rglob(ext):
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                for line_no, line in enumerate(text.splitlines(), start=1):
                    if query_lower in line.lower():
                        results.append(f"{path.relative_to(folder)}:{line_no}: {line.strip()}")
                        if len(results) >= 50:
                            return results
        
        return results
