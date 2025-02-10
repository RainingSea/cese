import os

class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        filename = f'tasks_{username}.txt'
        with open(filename, 'a') as f:
            f.write(f"{self.description}|{self.due_date}\n")

    def load_tasks(self, username: str):
        tasks = []
        filename = f'tasks_{username}.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    tasks.append(line.strip().split('|'))
        return tasks

    def remove_task(self, username: str, task_id: int):
        filename = f'tasks_{username}.txt'
        tasks = self.load_tasks(username)
        if 0 <= task_id < len(tasks):
            del tasks[task_id]
            with open(filename, 'w') as f:
                for task in tasks:
                    f.write(f"{task[0]}|{task[1]}\n")