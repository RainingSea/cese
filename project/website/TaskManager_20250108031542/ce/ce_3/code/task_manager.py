from user import User
from task import Task

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
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def add_task(self, username: str, description: str, due_date: str):
        new_task = Task(description, due_date)
        new_task.save_task(username)

    def get_tasks(self, username: str) -> list:
        return Task.load_tasks(username)

    def delete_task(self, username: str, task_index: int):
        Task.remove_task(username, task_index)