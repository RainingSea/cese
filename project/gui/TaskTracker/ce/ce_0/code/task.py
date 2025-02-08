class Task:
    def __init__(self, title: str, description: str, due_date: str, priority: str):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = 'Incomplete'

    def to_string(self) -> str:
        return f"{self.title},{self.description},{self.due_date},{self.priority},{self.status}"

    def mark_complete(self) -> None:
        self.status = 'Complete'