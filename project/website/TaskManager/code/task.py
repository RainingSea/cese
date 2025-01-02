from datetime import datetime

class Task:
    def __init__(self, description: str = '', due_date: str = ''):
        self.description = description
        self.due_date = due_date

    def save(self, username: str) -> None:
        # Ensure the due date is in the correct format
        formatted_due_date = datetime.strptime(self.due_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description}|{formatted_due_date}\n")

    def load_tasks(self, username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    tasks.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return tasks

    def remove_task(self, username: str, task_description: str) -> None:
        tasks = self.load_tasks(username)
        tasks = [task for task in tasks if task[0] != task_description]
        with open(f'tasks_{username}.txt', 'w') as f:
            for task in tasks:
                f.write(f"{task[0]}|{task[1]}\n")