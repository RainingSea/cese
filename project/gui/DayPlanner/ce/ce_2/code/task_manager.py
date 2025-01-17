import json
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title: str, category: str, priority: int, time_slot: str):
        task = Task(title, category, priority, time_slot)
        self.tasks.append(task)

    def load_tasks(self) -> list:
        try:
            with open('tasks.json', 'r') as file:
                task_data = json.load(file)
                self.tasks = [Task(**task) for task in task_data]
        except FileNotFoundError:
            self.tasks = []
        return self.tasks

    def save_tasks(self):
        task_data = [{'title': task.title, 'category': task.category, 'priority': task.priority, 'time_slot': task.time_slot} for task in self.tasks]
        with open('tasks.json', 'w') as file:
            json.dump(task_data, file, indent=4)

    def get_reminders(self) -> list:
        # Placeholder for reminder logic, returning all tasks for now
        return self.tasks