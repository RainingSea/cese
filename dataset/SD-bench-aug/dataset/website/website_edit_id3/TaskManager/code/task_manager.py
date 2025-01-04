class TaskManager:
    def __init__(self):
        pass

    def add_task(self, username: str, description: str, due_date: str) -> None:
        with open(f'tasks_{username}.txt', 'a') as file:
            file.write(f"{description}|{due_date}\n")

    def remove_task(self, username: str, task_description: str) -> None:
        tasks = self.load_tasks(username)
        tasks = [task for task in tasks if task[0] != task_description]
        self.save_tasks(username, tasks)

    def load_tasks(self, username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as file:
                for line in file:
                    description, due_date = line.strip().split('|')
                    tasks.append((description, due_date))
        except FileNotFoundError:
            pass
        return tasks

    def save_tasks(self, username: str, tasks: list) -> None:
        with open(f'tasks_{username}.txt', 'w') as file:
            for description, due_date in tasks:
                file.write(f"{description}|{due_date}\n")