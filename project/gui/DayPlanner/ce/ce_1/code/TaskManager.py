import os
from typing import List
from Task import Task

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, name: str, priority: str, category: str, start_time: str, end_time: str) -> None:
        new_task = Task(name, priority, category, start_time, end_time)
        self.tasks.append(new_task)
        self.save_tasks()

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    name, priority, category, start_time, end_time = line.strip().split('|')
                    task = Task(name, priority, category, start_time, end_time)
                    self.tasks.append(task)

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.name}|{task.priority}|{task.category}|{task.start_time}|{task.end_time}\n")