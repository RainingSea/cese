class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str) -> None:
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description}|{self.due_date}\n")

    @staticmethod
    def load_tasks(username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    description, due_date = line.strip().split('|')
                    tasks.append({'description': description, 'due_date': due_date})
        except FileNotFoundError:
            pass
        return tasks

    @staticmethod
    def remove_task(username: str, task_description: str) -> None:
        tasks = Task.load_tasks(username)
        tasks = [task for task in tasks if task['description'] != task_description]
        with open(f'tasks_{username}.txt', 'w') as f:
            for task in tasks:
                f.write(f"{task['description']}|{task['due_date']}\n")