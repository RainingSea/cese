import json
from typing import List

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

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks(self) -> None:
        try:
            with open('tasks.txt', 'r') as file:
                self.tasks = [Task(**json.loads(line.strip())) for line in file.readlines()]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(json.dumps(task.to_dict()) + '\n')

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save_tasks()

    def update_task_status(self, title: str, status: str) -> None:
        for task in self.tasks:
            if task.title == title:
                task.status = status
                break
        self.save_tasks()

    def get_tasks(self) -> List[Task]:
        return self.tasks