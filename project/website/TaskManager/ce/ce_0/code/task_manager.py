from task import Task

class TaskManager:
    def load_tasks(self, username: str) -> list:
        tasks = []
        try:
            with open(f'tasks_{username}.txt', 'r') as file:
                for line in file:
                    description, due_date = line.strip().split(',')
                    tasks.append(Task(description, due_date))
        except FileNotFoundError:
            pass
        return tasks

    def add_task(self, username: str, task: Task) -> None:
        task.save(username)

    def remove_task(self, username: str, task: Task) -> None:
        task.remove(username)