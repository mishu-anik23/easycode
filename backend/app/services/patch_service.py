import re
from pathlib import Path
from typing import Dict, List, Optional

from ..core.config import settings

HUNK_HEADER_RE = re.compile(r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? \+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@")

class PatchService:
    def validate_diff(self, diff_text: str) -> bool:
        return diff_text.strip().startswith("--- ")

    def _parse_diff(self, diff_text: str) -> List[Dict]:
        files = []
        current = None
        for line in diff_text.splitlines():
            if line.startswith("--- "):
                current = {"old_path": line[4:].strip(), "new_path": None, "hunks": []}
                files.append(current)
            elif line.startswith("+++ ") and current is not None:
                current["new_path"] = line[4:].strip()
            elif line.startswith("@@") and current is not None:
                match = HUNK_HEADER_RE.match(line)
                if match:
                    current["hunks"].append({
                        "old_start": int(match.group("old_start")),
                        "old_count": int(match.group("old_count") or 1),
                        "new_start": int(match.group("new_start")),
                        "new_count": int(match.group("new_count") or 1),
                        "lines": [],
                    })
            elif current is not None and current["hunks"]:
                current["hunks"][-1]["lines"].append(line)
        return files

    def _apply_hunk(self, original_lines: List[str], hunk: Dict) -> List[str]:
        old_index = hunk["old_start"] - 1
        result = []
        original_index = old_index

        for line in hunk["lines"]:
            if line.startswith(" "):
                if original_index < len(original_lines):
                    result.append(original_lines[original_index])
                original_index += 1
            elif line.startswith("-"):
                original_index += 1
            elif line.startswith("+"):
                result.append(line[1:])
            else:
                result.append(line)

        return original_lines[:old_index] + result + original_lines[original_index:]

    def apply_diff(self, diff_text: str) -> bool:
        if not self.validate_diff(diff_text):
            return False

        parsed = self._parse_diff(diff_text)
        if not parsed:
            return False

        for file_change in parsed:
            new_path = file_change.get("new_path")
            if not new_path:
                return False
            normalized = new_path.replace("b/", "", 1) if new_path.startswith("b/") else new_path
            target_path = settings.project_root / normalized
            file_exists = target_path.exists()
            original_lines: List[str] = []
            if file_exists:
                original_lines = target_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for hunk in file_change["hunks"]:
                original_lines = self._apply_hunk(original_lines, hunk)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text("\n".join(original_lines) + ("\n" if original_lines else ""), encoding="utf-8")

        return True
