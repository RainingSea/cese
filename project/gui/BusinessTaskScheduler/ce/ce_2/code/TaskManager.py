import os

class Task:
    def __init__(self, title: str, description: str, priority: int, assigned_member: str, deadline: str, status: str):
        self.title = title
        self.description = description
        self.priority = priority
        self.assigned_member = assigned_member
        self.deadline = deadline
        self.status = status

    def to_string(self) -> str:
        return f"{self.title}|{self.description}|{self.priority}|{self.assigned_member}|{self.deadline}|{self.status}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description, priority, assigned_member, deadline, status = line.strip().split('|')
                    task = Task(title, description, int(priority), assigned_member, deadline, status)
                    self.tasks.append(task)

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(task.to_string() + '\n')

    def create_task(self, title: str, description: str, priority: int, assigned_member: str, deadline: str) -> None:
        new_task = Task(title, description, priority, assigned_member, deadline, 'Pending')
        self.tasks.append(new_task)
        self.save_tasks()

    def update_task_status(self, title: str, status: str) -> None:
        for task in self.tasks:
            if task.title == title:
                task.status = status
                self.save_tasks()
                break

    def get_tasks(self) -> list[Task]:
        return self.tasks