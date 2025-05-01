from task import Task
from data_storage import read_tasks, write_tasks
from plyer import notification

class TaskManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, title: str, description: str, assigned_to: str, deadline: str, priority: str) -> None:
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, assigned_to, deadline, "Not Started", priority)
        self.tasks.append(new_task)
        self.save_tasks()
        self.send_notification(assigned_to, f"New task assigned: {title}")

    def assign_task(self, task_id: int, user: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.assigned_to = user
                self.save_tasks()
                self.send_notification(user, f"Task assigned: {task.title}")

    def set_deadline(self, task_id: int, deadline: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.deadline = deadline
                self.save_tasks()

    def track_progress(self, task_id: int, status: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.progress = status
                self.save_tasks()

    def prioritize_task(self, task_id: int, priority: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.priority = priority
                self.save_tasks()

    def send_notification(self, user: str, message: str) -> None:
        notification.notify(title="Task Notification", message=message, timeout=10)

    def load_tasks(self) -> None:
        self.tasks = read_tasks()

    def save_tasks(self) -> None:
        write_tasks(self.tasks)