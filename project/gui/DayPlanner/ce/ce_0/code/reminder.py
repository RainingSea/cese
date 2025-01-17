import os

class Reminder:
    def __init__(self, task_id: int, time: str):
        self.task_id = task_id
        self.time = time

    def set_reminder(self):
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.task_id}|{self.time}\n")

    @staticmethod
    def get_reminders() -> list:
        if not os.path.exists('reminders.txt'):
            return []
        with open('reminders.txt', 'r') as file:
            reminders = [line.strip().split('|') for line in file.readlines()]
        return reminders