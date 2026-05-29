class PatchService:
    def validate_diff(self, diff_text: str) -> bool:
        return diff_text.startswith("--- ")

    def apply_diff(self, diff_text: str) -> bool:
        # Stub: Use git apply or a safe parser in production
        return self.validate_diff(diff_text)
