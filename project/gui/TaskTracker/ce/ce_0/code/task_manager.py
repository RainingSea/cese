import os
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks(self, file_path: str) -> None:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    title, description, due_date, priority, status = line.strip().split(',')
                    task = Task(title, description, due_date, priority)
                    if status == 'Complete':
                        task.mark_complete()
                    self.tasks.append(task)

    def save_tasks(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            for task in self.tasks:
                file.write(task.to_string() + '\n')

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def update_task(self, index: int, task: Task) -> None:
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task

    def mark_task_complete(self, index: int) -> None:
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()

    def search_tasks(self, keyword: str) -> list[Task]:
        return [task for task in self.tasks if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]