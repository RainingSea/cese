import os
from user import User

class TaskManager:
    def __init__(self):
        self.users = {}
        self.tasks = {}

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    self.users[username] = User(username, password, email)

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password},{user.email}\n")

    def load_tasks(self, username: str) -> list:
        if username not in self.tasks:
            self.tasks[username] = []
            if os.path.exists(f'tasks_{username}.txt'):
                with open(f'tasks_{username}.txt', 'r') as file:
                    self.tasks[username] = [line.strip().split(',') for line in file]
        return self.tasks[username]

    def save_tasks(self, username: str) -> None:
        with open(f'tasks_{username}.txt', 'w') as file:
            for task in self.tasks[username]:
                file.write(f"{task[0]},{task[1]}\n")

    def add_task(self, username: str, task_description: str, due_date: str) -> None:
        self.tasks[username].append([task_description, due_date])
        self.save_tasks(username)

    def remove_task(self, username: str, task_index: int) -> None:
        if 0 <= task_index < len(self.tasks[username]):
            del self.tasks[username][task_index]
            self.save_tasks(username)

    def register_user(self, username: str, password: str, email: str) -> None:
        self.users[username] = User(username, password, email)
        self.save_users()

    def authenticate_user(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username].password == password