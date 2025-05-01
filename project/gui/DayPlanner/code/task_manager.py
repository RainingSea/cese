import os

class Task:
    def __init__(self, name: str, priority: str, category: str, start_time: str, end_time: str):
        self.name = name
        self.priority = priority
        self.category = category
        self.start_time = start_time
        self.end_time = end_time

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, name: str, priority: str, category: str, start_time: str, end_time: str):
        new_task = Task(name, priority, category, start_time, end_time)
        self.tasks.append(new_task)
        self.save_tasks()

    def edit_task(self, index: int, name: str, priority: str, category: str, start_time: str, end_time: str):
        if 0 <= index < len(self.tasks):
            self.tasks[index] = Task(name, priority, category, start_time, end_time)
            self.save_tasks()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def load_tasks(self):
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                self.tasks.clear()  # Clear existing tasks to avoid duplicates
                for line in file:
                    name, priority, category, start_time, end_time = line.strip().split('|')
                    self.tasks.append(Task(name, priority, category, start_time, end_time))

    def save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.name}|{task.priority}|{task.category}|{task.start_time}|{task.end_time}\n")