from user import User
from task import Task
from datastore import DataStore

class TaskManager:
    def __init__(self, data_store: DataStore):
        self.data_store = data_store
        self.users = self.data_store.load_users()

    def register_user(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        user = User(username, password, email)
        self.data_store.save_user(user)
        self.users.append(user)
        return True

    def login(self, username: str, password: str) -> bool:
        user = next((u for u in self.users if u.username == username), None)
        if user and user.validate_password(password):
            return True
        return False

    def add_task(self, username: str, description: str, due_date: str) -> None:
        task = Task(username, description, due_date)
        self.data_store.save_task(task)

    def remove_task(self, username: str, task_description: str) -> None:
        task = Task(username, task_description, '')
        self.data_store.remove_task(task)

    def get_tasks(self, username: str) -> list[Task]:
        return self.data_store.load_tasks(username)