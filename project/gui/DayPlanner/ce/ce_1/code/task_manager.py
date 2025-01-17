from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task_description: str, priority: int, category: str, time_slot: str) -> None:
        task = Task(task_description, priority, category, time_slot)
        self.tasks.append(task)
        self.save_tasks()

    def load_tasks(self) -> None:
        try:
            with open('tasks.txt', 'r') as file:
                for line in file:
                    task_description, priority, category, time_slot = line.strip().split('|')
                    self.tasks.append(Task(task_description, int(priority), category, time_slot))
        except FileNotFoundError:
            pass

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.task_description}|{task.priority}|{task.category}|{task.time_slot}\n")

    def get_tasks(self) -> list:
        return self.tasks