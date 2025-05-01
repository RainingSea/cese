import os

class Task:
    def __init__(self, description: str, priority: int, category: str, time_slot: str):
        self.description = description
        self.priority = priority
        self.category = category
        self.time_slot = time_slot

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description: str, priority: int, category: str, time_slot: str):
        new_task = Task(description, priority, category, time_slot)
        self.tasks.append(new_task)
        self.save_tasks()

    def load_tasks(self):
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    description, priority, category, time_slot = line.strip().split('|')
                    self.tasks.append(Task(description, int(priority), category, time_slot))

    def save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.description}|{task.priority}|{task.category}|{task.time_slot}\n")

    def get_tasks(self):
        return self.tasks