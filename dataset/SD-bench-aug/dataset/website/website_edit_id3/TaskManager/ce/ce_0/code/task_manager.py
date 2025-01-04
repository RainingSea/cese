from task import Task

class TaskManager:
    def __init__(self):
        pass

    def add_task(self, username: str, description: str, due_date: str) -> None:
        task = Task(description, due_date)
        task.save(username)

    def remove_task(self, username: str, task_description: str) -> None:
        task = Task(task_description, "")
        task.remove(username)

    def load_tasks(self, username: str) -> list:
        tasks = []
        filename = f'tasks_{username}.txt'
        try:
            with open(filename, 'r') as f:
                for line in f:
                    tasks.append(line.strip().split('|')[0])  # Only return descriptions
        except FileNotFoundError:
            pass  # File doesn't exist yet
        return tasks