import os

class Task:
    def __init__(self, description: str = "", due_date: str = ""):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        filename = f'tasks_{username}.txt'
        with open(filename, 'a') as file:
            file.write(f"{self.description}|{self.due_date}\n")

    def load_tasks(self, username: str):
        filename = f'tasks_{username}.txt'
        tasks = []
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    task_data = line.strip().split('|')
                    tasks.append({'description': task_data[0], 'due_date': task_data[1]})
        return tasks

    def remove_task(self, username: str, task_index: int):
        filename = f'tasks_{username}.txt'
        tasks = self.load_tasks(username)
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            with open(filename, 'w') as file:
                for task in tasks:
                    file.write(f"{task['description']}|{task['due_date']}\n")