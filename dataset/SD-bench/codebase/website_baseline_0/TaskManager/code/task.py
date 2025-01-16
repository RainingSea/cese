import os

class Task:
    def __init__(self, description: str = '', due_date: str = ''):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        with open(f'tasks_{username}.txt', 'a') as file:
            file.write(f"{self.description}|{self.due_date}\n")

    def load_tasks(self, username: str) -> list:
        tasks = []
        if os.path.exists(f'tasks_{username}.txt'):
            with open(f'tasks_{username}.txt', 'r') as file:
                for line in file:
                    tasks.append(line.strip().split('|'))
        return tasks

    def remove_task(self, username: str, task_index: int):
        tasks = self.load_tasks(username)
        if 0 <= task_index < len(tasks):
            tasks.pop(task_index)
            with open(f'tasks_{username}.txt', 'w') as file:
                for task in tasks:
                    file.write(f"{task[0]}|{task[1]}\n")