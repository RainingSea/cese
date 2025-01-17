import json

class Task:
    def __init__(self, title: str, description: str, priority: int, assignee: str, deadline: str):
        self.title = title
        self.description = description
        self.priority = priority
        self.assignee = assignee
        self.deadline = deadline
        self.status = "Pending"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "assignee": self.assignee,
            "deadline": self.deadline,
            "status": self.status
        }

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**task) for task in tasks_data]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def create_task(self, title: str, description: str, priority: int, assignee: str, deadline: str):
        new_task = Task(title, description, priority, assignee, deadline)
        self.tasks.append(new_task)
        self.save_tasks('tasks.txt')

    def update_task_status(self, task_id: int, status: str):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].status = status
            self.save_tasks('tasks.txt')

    def get_all_tasks(self) -> list:
        return [task.to_dict() for task in self.tasks]