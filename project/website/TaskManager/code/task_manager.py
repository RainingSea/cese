class TaskManager:
    def __init__(self, tasks_file: str):
        self.tasks_file = tasks_file
        self.load_tasks()

    def load_tasks(self):
        self.tasks = {}
        try:
            with open(self.tasks_file, 'r') as file:
                for line in file:
                    username, task_id, description, due_date = line.strip().split('|')
                    if username not in self.tasks:
                        self.tasks[username] = []
                    self.tasks[username].append((int(task_id), description, due_date))
        except FileNotFoundError:
            pass

    def add_task(self, username: str, description: str, due_date: str) -> bool:
        task_id = len(self.tasks.get(username, [])) + 1
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append((task_id, description, due_date))
        with open(self.tasks_file, 'a') as file:
            file.write(f"{username}|{task_id}|{description}|{due_date}\n")
        return True

    def remove_task(self, username: str, task_id: int) -> bool:
        if username in self.tasks:
            self.tasks[username] = [task for task in self.tasks[username] if task[0] != task_id]
            self.save_tasks()
            return True
        return False

    def save_tasks(self):
        with open(self.tasks_file, 'w') as file:
            for username, tasks in self.tasks.items():
                for task in tasks:
                    file.write(f"{username}|{task[0]}|{task[1]}|{task[2]}\n")

    def get_tasks(self, username: str) -> list:
        return self.tasks.get(username, [])