from user import User
from task import Task
from flask import session

class TaskManager:
    def __init__(self):
        self.users = User.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def add_task(self, description: str, due_date: str):
        username = session['username']
        task = Task(description, due_date)
        task.save_task(username)

    def remove_task(self, task_index: int):
        username = session['username']
        task = Task("", "")
        task.remove_task(username, task_index)

    def get_tasks(self) -> list:
        username = session['username']
        task = Task("", "")
        return task.load_tasks(username)