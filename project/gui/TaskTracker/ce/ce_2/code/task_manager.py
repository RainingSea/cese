import os
from tasks import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description, due_date, priority, status = line.strip().split('|')
                    task = Task(title, description, due_date, priority)
                    task.status = status
                    self.tasks.append(task)

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.description}|{task.due_date}|{task.priority}|{task.status}\n")

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, task: Task) -> None:
        for idx, existing_task in enumerate(self.tasks):
            if existing_task.title == task.title:
                self.tasks[idx] = task
                break
        self.save_tasks()

    def search_tasks(self, query: str) -> list[Task]:
        return [task for task in self.tasks if query.lower() in task.title.lower()]

    def get_categories(self) -> list[str]:
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                return [line.strip() for line in file]
        return []