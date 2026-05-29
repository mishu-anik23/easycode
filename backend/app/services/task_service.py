from typing import List

class TaskService:
    def create_task_list(self, goal: str) -> List[str]:
        return [
            f"Review project goal: {goal}",
            "Generate draft plan steps",
            "Validate with user",
        ]
