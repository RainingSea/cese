class Task:
    def __init__(self, description: str = None, due_date: str = None):
        self.description = description
        self.due_date = due_date

    def save(self, username: str) -> None:
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description}|{self.due_date}\n")

    def load_tasks(self, username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    description, due_date = line.strip().split('|')
                    tasks.append(Task(description, due_date))
        except FileNotFoundError:
            pass
        return tasks

    def remove_task(self, username: str, task_index: int) -> None:
        tasks = self.load_tasks(username)
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            with open(f'tasks_{username}.txt', 'w') as f:
                for task in tasks:
                    f.write(f"{task.description}|{task.due_date}\n")