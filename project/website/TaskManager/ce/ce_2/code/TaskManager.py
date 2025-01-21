from FileHandler import FileHandler

class TaskManager:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""

    def register(self, username: str, password: str, email: str) -> bool:
        users = FileHandler.read_from_file('users.txt')
        for user in users:
            if user.split('|')[0] == username:
                return False  # User already exists
        FileHandler.write_to_file('users.txt', f"{username}|{password}|{email}")
        return True

    def login(self, username: str, password: str) -> bool:
        users = FileHandler.read_from_file('users.txt')
        for user in users:
            if user.split('|')[0] == username and user.split('|')[1] == password:
                self.username = username
                return True
        return False

    def add_task(self, task_description: str, due_date: str) -> bool:
        task_id = len(FileHandler.read_from_file(f'tasks_{self.username}.txt')) + 1
        FileHandler.write_to_file(f'tasks_{self.username}.txt', f"{task_id}|{task_description}|{due_date}")
        return True

    def remove_task(self, task_id: int) -> bool:
        tasks = FileHandler.read_from_file(f'tasks_{self.username}.txt')
        updated_tasks = [task for task in tasks if int(task.split('|')[0]) != task_id]
        with open(f'tasks_{self.username}.txt', 'w') as file:
            for task in updated_tasks:
                file.write(task + '\n')
        return len(tasks) != len(updated_tasks)

    def get_tasks(self) -> list:
        return FileHandler.read_from_file(f'tasks_{self.username}.txt')