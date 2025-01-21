import os

class TaskManager:
    def __init__(self):
        self.username = None
        self.users = {}
        self.tasks = {}

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username]['password'] == password:
            self.username = username
            self.load_tasks()
            return True
        return False

    def add_task(self, task_description: str, due_date: str) -> bool:
        if self.username is None:
            return False
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {'description': task_description, 'due_date': due_date}
        self.save_tasks()
        return True

    def remove_task(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False

    def get_tasks(self) -> list:
        return self.tasks.values()

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = {'password': password, 'email': email}

    def load_tasks(self) -> None:
        if self.username and os.path.exists(f'tasks_{self.username}.txt'):
            with open(f'tasks_{self.username}.txt', 'r') as file:
                for line in file:
                    task_id, description, due_date = line.strip().split('|')
                    self.tasks[int(task_id)] = {'description': description, 'due_date': due_date}

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, data in self.users.items():
                file.write(f"{username}|{data['password']}|{data['email']}\n")

    def save_tasks(self) -> None:
        if self.username:
            with open(f'tasks_{self.username}.txt', 'w') as file:
                for task_id, data in self.tasks.items():
                    file.write(f"{task_id}|{data['description']}|{data['due_date']}\n")