import os
from typing import List
from task import Task

class TaskManager:
    def __init__(self) -> None:
        self.tasks = []
        self.load_tasks()

    def create_task(self, title: str, description: str) -> None:
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description)
        self.tasks.append(new_task)
        self.save_tasks()

    def set_timer(self, task_id: int, duration: int) -> None:
        task = self.get_task_by_id(task_id)
        if task:
            task.set_timer(duration)
            self.save_tasks()

    def set_alarm(self, task_id: int, time: str) -> None:
        task = self.get_task_by_id(task_id)
        if task:
            task.set_alarm(time)
            self.save_tasks()

    def generate_report(self) -> str:
        report = "Task Report:\n"
        for task in self.tasks:
            report += f"ID: {task.id}, Title: {task.title}, Timer: {task.timer}, Alarm: {task.alarm}\n"
        return report

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description = line.strip().split('|')
                    self.create_task(title, description)

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.description}\n")

    def get_task_by_id(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None