import os

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title: str, description: str, deadline: str, priority: str, status: str, category: str) -> None:
        task = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'priority': priority,
            'status': status,
            'category': category
        }
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, task_id: int, title: str, description: str, deadline: str, priority: str, status: str, category: str) -> None:
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id] = {
                'title': title,
                'description': description,
                'deadline': deadline,
                'priority': priority,
                'status': status,
                'category': category
            }
            self.save_tasks()

    def delete_task(self, task_id: int) -> None:
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.save_tasks()

    def get_tasks(self) -> list:
        return self.tasks

    def search_tasks(self, query: str) -> list:
        return [task for task in self.tasks if query.lower() in task['title'].lower()]

    def load_tasks(self) -> None:
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    title, description, deadline, priority, status, category = line.strip().split('|')
                    self.tasks.append({
                        'title': title,
                        'description': description,
                        'deadline': deadline,
                        'priority': priority,
                        'status': status,
                        'category': category
                    })

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task['title']}|{task['description']}|{task['deadline']}|{task['priority']}|{task['status']}|{task['category']}\n")