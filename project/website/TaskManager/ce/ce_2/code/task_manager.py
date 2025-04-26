class TaskManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        self.tasks = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    task_description, due_date = line.strip().split('|')
                    self.tasks.append((task_description, due_date))
        except FileNotFoundError:
            pass

    def add_task(self, task_description: str, due_date: str) -> None:
        self.tasks.append((task_description, due_date))
        with open(self.filename, 'a') as file:
            file.write(f"{task_description}|{due_date}\n")

    def remove_task(self, task_index: int) -> None:
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()

    def save_tasks(self) -> None:
        with open(self.filename, 'w') as file:
            for task_description, due_date in self.tasks:
                file.write(f"{task_description}|{due_date}\n")

    def get_tasks(self) -> list:
        return self.tasks