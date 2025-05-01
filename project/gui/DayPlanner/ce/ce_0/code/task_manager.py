import os

class Task:
    def __init__(self, title: str, priority: str, category: str, time_slot: str):
        self.title = title
        self.priority = priority
        self.category = category
        self.time_slot = time_slot

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_id: int):
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def load_tasks(self):
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, priority, category, time_slot = line.strip().split('|')
                    task = Task(title, priority, category, time_slot)
                    self.tasks.append(task)

    def save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.priority}|{task.category}|{task.time_slot}\n")