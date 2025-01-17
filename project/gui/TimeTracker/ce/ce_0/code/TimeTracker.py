import threading
import time
from Task import Task
from Alarm import Alarm

class TimeTracker:
    def __init__(self):
        self.tasks = []
        self.alarms = []

    def add_task(self, title: str, description: str):
        task_id = len(self.tasks) + 1
        task = Task(task_id, title, description)
        self.tasks.append(task)

    def start_timer(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if task:
            task.start()

    def set_alarm(self, time: str, message: str):
        alarm = Alarm(time, message)
        self.alarms.append(alarm)

    def generate_report(self) -> str:
        report = "Task Report:\n"
        for task in self.tasks:
            report += f"Task: {task.title}, Duration: {task.duration} seconds\n"
        return report

    def get_task_by_id(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None