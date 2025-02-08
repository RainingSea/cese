from datetime import datetime
from typing import List
from task import Task

class TaskManager:
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, title: str, description: str) -> None:
        new_task = Task(title, description)
        self.tasks.append(new_task)
        self.save_tasks()

    def start_timer(self, task_id: int) -> None:
        # Placeholder for starting timer logic
        pass

    def set_alarm(self, task_id: int, time: datetime) -> None:
        # Placeholder for setting alarm logic
        pass

    def generate_report(self) -> str:
        report = ""
        for task in self.tasks:
            report += f"{task.title} | {task.description} | {task.duration} | {task.timestamp}\n"
        return report

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as f:
            for task in self.tasks:
                f.write(f"{task.title}|{task.description}|{task.duration}|{task.timestamp}\n")

    def load_tasks(self) -> None:
        try:
            with open('tasks.txt', 'r') as f:
                for line in f:
                    title, description, duration, timestamp = line.strip().split('|')
                    task = Task(title, description)
                    task.duration = float(duration)
                    task.timestamp = datetime.fromisoformat(timestamp)
                    self.tasks.append(task)
        except FileNotFoundError:
            pass