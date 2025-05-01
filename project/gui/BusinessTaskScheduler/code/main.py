import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from plyer import notification
from tkcalendar import Calendar

class Task:
    def __init__(self, task_id, title, description, assigned_to, deadline, status='Not Started', priority='low'):
        self.id = task_id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.deadline = deadline
        self.status = status
        self.priority = priority

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists('tasks.txt'):
            with open('tasks.txt', 'r') as file:
                for line in file:
                    task_data = line.strip().split('|')
                    if len(task_data) == 7:
                        task = Task(int(task_data[0]), task_data[1], task_data[2], task_data[3], task_data[4], task_data[5], task_data[6])
                        self.tasks.append(task)

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

    def edit_task(self, task_id: int, title: str, description: str, assigned_to: str, deadline: str, priority: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.title = title
                task.description = description
                task.assigned_to = assigned_to
                task.deadline = deadline
                task.priority = priority
                self.save_tasks()
                return

    def delete_task(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def track_progress(self, task_id: int) -> str:
        for task in self.tasks:
            if task.id == task_id:
                return task.status
        return "Task not found."

    def set_deadline(self, task_id: int, deadline: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.deadline = deadline
                self.save_tasks()
                return

    def prioritize_task(self, task_id: int, priority: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.priority = priority
                self.save_tasks()

    def save_tasks(self) -> None:
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.id}|{task.title}|{task.description}|{task.assigned_to}|{task.deadline}|{task.status}|{task.priority}\n")

    def send_notification(self, user: str, message: str) -> None:
        notification.notify(title="Task Notification", message=message, timeout=10)

class CalendarWidget:
    def __init__(self, master):
        self.calendar = Calendar(master)
        self.calendar.pack()

    def display_calendar(self):
        self.calendar.pack()

    def select_date(self) -> str:
        selected_date = self.calendar.get_date()
        return selected_date

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Task Management Application")
        self.calendar_widget = CalendarWidget(self.root)
        self.create_ui()

    def create_ui(self):
        self.calendar_widget.display_calendar()
        # Additional UI components can be created here

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()