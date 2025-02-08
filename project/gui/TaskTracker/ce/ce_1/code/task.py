class Task:
    def __init__(self, id: int, title: str, description: str, due_date: str, priority: str):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False