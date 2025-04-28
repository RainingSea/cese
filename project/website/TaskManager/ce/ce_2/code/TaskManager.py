class TaskManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        self.tasks = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    description, due_date = line.strip().split('|')
                    self.tasks.append({'description': description, 'due_date': due_date})

    def add_task(self, description: str, due_date: str) -> bool:
        self.tasks.append({'description': description, 'due_date': due_date})
        with open(self.filename, 'a') as file:
            file.write(f"{description}|{due_date}\n")
        return True

    def remove_task(self, task_id: int) -> bool:
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task['description']}|{task['due_date']}\n")

    def get_tasks(self) -> list:
        return self.tasks