class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description},{self.due_date}\n")

    def remove(self, username: str):
        tasks = self.load_tasks(username)
        tasks = [task for task in tasks if task.description != self.description]
        with open(f'tasks_{username}.txt', 'w') as f:
            for task in tasks:
                f.write(f"{task.description},{task.due_date}\n")

class TaskManager:
    def add_task(self, username: str, description: str, due_date: str):
        task = Task(description, due_date)
        task.save(username)

    def remove_task(self, username: str, description: str):
        task = Task(description, "")
        task.remove(username)

    def load_tasks(self, username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    description, due_date = line.strip().split(',')
                    tasks.append(Task(description, due_date))
        except FileNotFoundError:
            pass
        return tasks