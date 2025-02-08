class Task:
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description


class TaskManager:
    def __init__(self) -> None:
        self.tasks = []

    def create_task(self, title: str, description: str) -> None:
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def load_tasks(self) -> None:
        try:
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description = line.strip().split('|')
                    self.tasks.append(Task(title, description))
        except FileNotFoundError:
            pass

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.description}\n")