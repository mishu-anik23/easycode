from typing import List


def parse_unified_diff(diff_text: str) -> List[str]:
    return [line for line in diff_text.splitlines() if line.startswith(("+", "-", "@@"))]
