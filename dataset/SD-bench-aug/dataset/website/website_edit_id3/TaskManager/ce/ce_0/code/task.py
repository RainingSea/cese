class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str) -> None:
        filename = f'tasks_{username}.txt'
        with open(filename, 'a') as f:
            f.write(f"{self.description}|{self.due_date}\n")

    def remove(self, username: str) -> None:
        filename = f'tasks_{username}.txt'
        tasks = []
        with open(filename, 'r') as f:
            tasks = f.readlines()
        with open(filename, 'w') as f:
            for task in tasks:
                if task.strip().split('|')[0] != self.description:
                    f.write(task)