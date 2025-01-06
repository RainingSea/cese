from user import User

class TaskManager:
    def __init__(self):
        self.users = {}
        self.tasks = {}

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    self.users[username] = User(username, password, email)
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password},{user.email}\n")

    def load_tasks(self, username: str) -> list:
        try:
            with open(f'tasks_{username}.txt', 'r') as file:
                return [line.strip().split(',') for line in file]
        except FileNotFoundError:
            return []

    def save_tasks(self, username: str) -> None:
        with open(f'tasks_{username}.txt', 'w') as file:
            for task in self.tasks.get(username, []):
                file.write(f"{task[0]},{task[1]}\n")

    def add_task(self, username: str, task_description: str, due_date: str) -> None:
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append((task_description, due_date))
        self.save_tasks(username)

    def remove_task(self, username: str, task_index: int) -> None:
        if username in self.tasks and 0 <= task_index < len(self.tasks[username]):
            self.tasks[username].pop(task_index)
            self.save_tasks(username)

    def register_user(self, username: str, password: str, email: str) -> None:
        if username not in self.users:
            new_user = User(username, password, email)
            self.users[username] = new_user
            self.save_users()

    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user.password == password