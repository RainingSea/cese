from user import User
from task import Task

class DataStore:
    def load_users(self) -> list[User]:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def save_user(self, user: User) -> None:
        user.save()

    def load_tasks(self, username: str) -> list[Task]:
        tasks = []
        try:
            with open('tasks.txt', 'r') as f:
                for line in f:
                    user, description, due_date = line.strip().split(',')
                    if user == username:
                        tasks.append(Task(user, description, due_date))
        except FileNotFoundError:
            pass
        return tasks

    def save_task(self, task: Task) -> None:
        task.save()

    def remove_task(self, task: Task) -> None:
        tasks = self.load_tasks(task.username)
        tasks = [t for t in tasks if t.description != task.description]
        with open('tasks.txt', 'w') as f:
            for t in tasks:
                f.write(f"{t.username},{t.description},{t.due_date}\n")