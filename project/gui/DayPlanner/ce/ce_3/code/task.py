class Task:
    def __init__(self, name: str, priority: int, category: str, time_slot: str) -> None:
        self.name = name
        self.priority = priority
        self.category = category
        self.time_slot = time_slot