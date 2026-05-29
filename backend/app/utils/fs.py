from pathlib import Path
from typing import Optional


def safe_read_text(path: Path, encoding: str = "utf-8") -> Optional[str]:
    if not path.exists():
        return None
    return path.read_text(encoding=encoding)
