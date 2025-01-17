import json
from typing import List
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title: str, description: str, due_date: str, priority: str) -> None:
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def update_task(self, task_id: int, title: str, description: str, due_date: str, priority: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.title = title
                task.description = description
                task.due_date = due_date
                task.priority = priority
                self.save_tasks()
                break

    def complete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                break

    def search_tasks(self, keyword: str) -> List[Task]:
        return [task for task in self.tasks if keyword.lower() in task.title.lower()]

    def load_tasks(self) -> None:
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self) -> None:
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, indent=4)