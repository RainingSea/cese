class Task:
    def __init__(self, id: int, title: str, description: str, assigned_to: str, deadline: str, progress: str, priority: str):
        self.id = id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.deadline = deadline
        self.progress = progress
        self.priority = priority