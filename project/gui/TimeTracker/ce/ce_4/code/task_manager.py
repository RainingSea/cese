import os
import datetime
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def create_task(self, title: str, description: str) -> None:
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def start_timer(self, task_id: int) -> None:
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].start()

    def set_alarm(self, task_id: int, time: str) -> None:
        # Alarm feature is not implemented yet
        pass

    def generate_report(self) -> str:
        report = "Task Report:\n"
        for task in self.tasks:
            report += f"{task.title}: {task.duration} seconds\n"
        return report

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description, duration = line.strip().split('|')
                    task = Task(title, description)
                    task.duration = float(duration)
                    self.tasks.append(task)

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.description}|{task.duration}\n")