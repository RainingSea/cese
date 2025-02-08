class Task:
    def __init__(self, title: str, description: str, due_date: str, priority: str):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = 'in progress'

    def mark_complete(self) -> None:
        self.status = 'complete'

    def update_details(self, description: str, due_date: str, priority: str) -> None:
        self.description = description
        self.due_date = due_date
        self.priority = priority