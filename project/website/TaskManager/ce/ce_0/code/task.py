class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str) -> None:
        with open(f'tasks_{username}.txt', 'a') as file:
            file.write(f'{self.description},{self.due_date}\n')

    def remove(self, username: str) -> None:
        tasks = []
        with open(f'tasks_{username}.txt', 'r') as file:
            tasks = file.readlines()
        with open(f'tasks_{username}.txt', 'w') as file:
            for task in tasks:
                if task.strip() != f'{self.description},{self.due_date}':
                    file.write(task)