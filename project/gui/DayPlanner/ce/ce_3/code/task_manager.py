import os
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_name: str) -> None:
        self.tasks = [task for task in self.tasks if task.name != task_name]
        self.save_tasks()

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.name},{task.priority},{task.category},{task.time_slot}\n")

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    name, priority, category, time_slot = line.strip().split(',')
                    self.tasks.append(Task(name, int(priority), category, time_slot))