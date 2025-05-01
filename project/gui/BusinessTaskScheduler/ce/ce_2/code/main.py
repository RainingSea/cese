import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import os

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Task Management System")
        self.create_main_window()
        self.load_data()
        self.root.mainloop()

    def create_main_window(self):
        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.pack(fill=tk.BOTH, expand=True)

        self.create_task_button = tk.Button(self.root, text="Create Task", command=self.create_task)
        self.create_task_button.pack(side=tk.LEFT)

        self.assign_task_button = tk.Button(self.root, text="Assign Task", command=self.assign_task)
        self.assign_task_button.pack(side=tk.LEFT)

        self.prioritize_task_button = tk.Button(self.root, text="Prioritize Task", command=self.prioritize_task)
        self.prioritize_task_button.pack(side=tk.LEFT)

        self.progress_button = tk.Button(self.root, text="Track Progress", command=self.track_progress)
        self.progress_button.pack(side=tk.LEFT)

    def create_task(self):
        title = simpledialog.askstring("Input", "Enter task title:")
        description = simpledialog.askstring("Input", "Enter task description:")
        assignee = simpledialog.askstring("Input", "Enter assignee:")
        deadline = simpledialog.askstring("Input", "Enter deadline:")
        priority = simpledialog.askstring("Input", "Enter priority:")
        self.task_manager.create_task(title, description, assignee, deadline, priority)
        self.update_task_list()

    def assign_task(self):
        task_id = simpledialog.askinteger("Input", "Enter task ID to assign:")
        user_id = simpledialog.askinteger("Input", "Enter user ID to assign to:")
        self.task_manager.assign_task(task_id, user_id)
        self.update_task_list()

    def prioritize_task(self):
        task_id = simpledialog.askinteger("Input", "Enter task ID to prioritize:")
        priority = simpledialog.askstring("Input", "Enter new priority:")
        self.task_manager.prioritize_task(task_id, priority)
        self.update_task_list()

    def track_progress(self):
        task_id = simpledialog.askinteger("Input", "Enter task ID to track progress:")
        status = self.task_manager.track_progress(task_id)
        messagebox.showinfo("Task Status", status)

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.title} - {task.status}")

    def load_data(self):
        self.task_manager.load_tasks()
        self.task_manager.load_users()
        self.update_task_list()

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.users = []

    def create_task(self, title: str, description: str, assignee: str, deadline: str, priority: str) -> None:
        task = Task(title, description, assignee, deadline, priority, "Pending")
        self.tasks.append(task)
        self.save_tasks()

    def assign_task(self, task_id: int, user_id: int) -> None:
        if 0 <= task_id < len(self.tasks) and 0 <= user_id < len(self.users):
            self.tasks[task_id].assignee = self.users[user_id].name
            self.save_tasks()

    def set_deadline(self, task_id: int, deadline: str) -> None:
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].deadline = deadline
            self.save_tasks()

    def track_progress(self, task_id: int) -> str:
        if 0 <= task_id < len(self.tasks):
            return f"Task: {self.tasks[task_id].title}, Status: {self.tasks[task_id].status}"
        return "Task not found."

    def prioritize_task(self, task_id: int, priority: str) -> None:
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].priority = priority
            self.save_tasks()

    def send_notification(self, task_id: int) -> None:
        # Placeholder for notification logic
        pass

    def integrate_calendar(self) -> None:
        # Placeholder for calendar integration logic
        pass

    def load_tasks(self) -> None:
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    title, description, assignee, deadline, priority, status = line.strip().split("|")
                    task = Task(title, description, assignee, deadline, priority, status)
                    self.tasks.append(task)

    def load_users(self) -> None:
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as file:
                for line in file:
                    name, email = line.strip().split("|")
                    user = User(name, email)
                    self.users.append(user)

    def save_tasks(self) -> None:
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.title}|{task.description}|{task.assignee}|{task.deadline}|{task.priority}|{task.status}\n")

class Task:
    def __init__(self, title: str, description: str, assignee: str, deadline: str, priority: str, status: str):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.deadline = deadline
        self.priority = priority
        self.status = status

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

if __name__ == "__main__":
    Main()