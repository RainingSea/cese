import os

class Task:
    def __init__(self, title: str, priority: int, category: str, time_slot: str):
        self.title = title
        self.priority = priority
        self.category = category
        self.time_slot = time_slot

    def save(self):
        with open('tasks.txt', 'a') as file:
            file.write(f"{self.title}|{self.priority}|{self.category}|{self.time_slot}\n")

    @staticmethod
    def load() -> list:
        if not os.path.exists('tasks.txt'):
            return []
        with open('tasks.txt', 'r') as file:
            tasks = [line.strip().split('|') for line in file.readlines()]
        return tasks

    @staticmethod
    def delete(task_id: int):
        tasks = Task.load()
        if 0 <= task_id < len(tasks):
            del tasks[task_id]
            with open('tasks.txt', 'w') as file:
                for task in tasks:
                    file.write('|'.join(task) + '\n')