class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        with open(f'tasks_{username}.txt', 'a') as file:
            file.write(f"{self.description}|{self.due_date}\n")

    def remove(self, username: str):
        tasks = []
        with open(f'tasks_{username}.txt', 'r') as file:
            tasks = file.readlines()
        with open(f'tasks_{username}.txt', 'w') as file:
            for task in tasks:
                if task.split('|')[0] != self.description:
                    file.write(task)

class TaskManager:
    def __init__(self, tasks_file: str):
        self.tasks_file = tasks_file

    def add_task(self, task_description: str, due_date: str, username: str):
        task = Task(task_description, due_date)
        task.save(username)

    def remove_task(self, task_description: str, username: str):
        task = Task(task_description, '')
        task.remove(username)

    def get_tasks(self, username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as file:
                tasks = file.readlines()
        except FileNotFoundError:
            return []
        return [task.strip().split('|') for task in tasks]