from typing import List
from Task import Task

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []

    def load_tasks(self, file_name: str) -> None:
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    title, description, due_date, priority, status = line.strip().split('|')
                    self.tasks.append(Task(title, description, due_date, priority, status))
        except FileNotFoundError:
            print(f"File {file_name} not found. Starting with an empty task list.")

    def save_tasks(self, file_name: str) -> None:
        with open(file_name, 'w') as file:
            for task in self.tasks:
                file.write(task.to_string() + '\n')

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def update_task(self, index: int, task: Task) -> None:
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task

    def delete_task(self, index: int) -> None:
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def search_tasks(self, keyword: str) -> List[Task]:
        return [task for task in self.tasks if keyword.lower() in task.title.lower()]