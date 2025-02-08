class Task:
    def __init__(self, title: str, description: str, priority: int, deadline: str):
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = "Pending"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status
        }