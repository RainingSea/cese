class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save_task(self, username: str):
        with open(f'tasks_{username}.txt', 'a') as file:
            file.write(f"{self.description}|{self.due_date}\n")

    @staticmethod
    def load_tasks(username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as file:
                for line in file:
                    description, due_date = line.strip().split('|')
                    tasks.append(Task(description, due_date))
        except FileNotFoundError:
            pass  # If the file does not exist, return an empty list
        return tasks

    @staticmethod
    def remove_task(username: str, task_index: int):
        tasks = Task.load_tasks(username)
        if 0 <= task_index < len(tasks):
            tasks.pop(task_index)
            with open(f'tasks_{username}.txt', 'w') as file:
                for task in tasks:
                    file.write(f"{task.description}|{task.due_date}\n")