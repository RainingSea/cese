import json
from Task import Task
from User import User
from Notification import Notification

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.users = []
        self.load_tasks()
        self.load_users()

    def load_tasks(self):
        try:
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description, priority, deadline, status = line.strip().split('|')
                    task = Task(title, description, int(priority), deadline)
                    task.status = status
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.description}|{task.priority}|{task.deadline}|{task.status}\n")

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def assign_task(self, task_title: str, user_email: str):
        for task in self.tasks:
            if task.title == task_title:
                task.status = f"Assigned to {user_email}"
                self.save_tasks()
                break

    def update_task_status(self, task_title: str, status: str):
        for task in self.tasks:
            if task.title == task_title:
                task.status = status
                self.save_tasks()
                break

    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    name, email = line.strip().split('|')
                    user = User(name, email)
                    self.users.append(user)
        except FileNotFoundError:
            pass

    def get_notifications(self) -> list[str]:
        notifications = []
        try:
            with open('notifications.txt', 'r') as file:
                for line in file:
                    message, date = line.strip().split('|')
                    notification = Notification(message, date)
                    notifications.append(notification.to_dict())
        except FileNotFoundError:
            pass
        return notifications