class TaskManager:
    def __init__(self):
        pass

    def get_tasks_file(self, username: str) -> str:
        return f"{username}_tasks.txt"

    def add_task(self, username: str, task_description: str, due_date: str) -> None:
        tasks_file = self.get_tasks_file(username)
        with open(tasks_file, 'a') as file:
            file.write(f"{task_description}|{due_date}\n")

    def remove_task(self, username: str, task_description: str) -> None:
        tasks_file = self.get_tasks_file(username)
        tasks = self.list_tasks(username)
        with open(tasks_file, 'w') as file:
            for task in tasks:
                if not task.startswith(task_description):
                    file.write(task + '\n')

    def list_tasks(self, username: str) -> list:
        tasks_file = self.get_tasks_file(username)
        if not os.path.exists(tasks_file):
            return []
        with open(tasks_file, 'r') as file:
            return [line.strip() for line in file]