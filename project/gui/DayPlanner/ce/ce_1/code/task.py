class Task:
    def __init__(self, task_description: str, priority: int, category: str, time_slot: str):
        self.task_description = task_description
        self.priority = priority
        self.category = category
        self.time_slot = time_slot