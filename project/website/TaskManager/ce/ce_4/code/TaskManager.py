from FileHandler import FileHandler

class TaskManager:
    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email
        self.file_handler = FileHandler()

    def register(self, username: str, password: str, email: str) -> bool:
        users = self.file_handler.read_from_file('users.txt')
        for user in users:
            if user.split(',')[0] == username:
                return False  # User already exists
        self.file_handler.write_to_file('users.txt', f"{username},{password},{email}")
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.file_handler.read_from_file('users.txt')
        for user in users:
            if user.split(',')[0] == username and user.split(',')[1] == password:
                return True
        return False

    def add_task(self, task_description: str, due_date: str) -> bool:
        tasks = self.file_handler.read_from_file(f'tasks_{self.username}.txt')
        self.file_handler.write_to_file(f'tasks_{self.username}.txt', f"{task_description},{due_date}")
        return True

    def remove_task(self, task_description: str) -> bool:
        tasks = self.file_handler.read_from_file(f'tasks_{self.username}.txt')
        tasks = [task for task in tasks if task.split(',')[0] != task_description]
        with open(f'tasks_{self.username}.txt', 'w') as file:
            for task in tasks:
                file.write(task + '\n')
        return True

    def get_tasks(self) -> list:
        return self.file_handler.read_from_file(f'tasks_{self.username}.txt')