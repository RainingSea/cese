import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os
import json
from typing import List
from datetime import datetime

class Task:
    def __init__(self, title: str, description: str, deadline: str, priority: str, category: str, status: str = "Not Started"):
        self.title = title
        self.description = description
        self.deadline = self.validate_deadline(deadline)
        self.priority = priority
        self.category = category
        self.status = status

    def validate_deadline(self, deadline: str) -> str:
        """Validate that the deadline is not in the past."""
        if datetime.strptime(deadline, "%Y-%m-%d") < datetime.now():
            raise ValueError("Deadline cannot be in the past.")
        return deadline

    def edit_task(self, title: str = None, description: str = None, deadline: str = None, priority: str = None, status: str = None, category: str = None) -> None:
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if deadline is not None:
            self.deadline = self.validate_deadline(deadline)
        if priority is not None:
            self.priority = priority
        if status is not None:
            self.status = status
        if category is not None:
            self.category = category

    def to_string(self) -> str:
        return f"{self.title}|{self.description}|{self.deadline}|{self.priority}|{self.category}|{self.status}"

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, title: str, description: str, deadline: str, priority: str, category: str) -> None:
        new_task = Task(title, description, deadline, priority, category)
        self.tasks.append(new_task)
        self.save_tasks()

    def edit_task(self, task_id: int, title: str = None, description: str = None, deadline: str = None, priority: str = None, category: str = None, status: str = None) -> None:
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].edit_task(title, description, deadline, priority, status, category)
            self.save_tasks()
        else:
            messagebox.showerror("Error", "Task not found.")

    def delete_task(self, title: str) -> None:
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def search_tasks(self, query: str) -> List[Task]:
        return [task for task in self.tasks if query.lower() in task.title.lower()]

    def load_tasks(self) -> None:
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    self.tasks.append(Task(**task_data))

    def save_tasks(self) -> None:
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def display_progress(self) -> None:
        for task in self.tasks:
            print(f"{task.title}: {task.status}")

    def filter_tasks(self, category: str = None, priority: str = None) -> List[Task]:
        filtered_tasks = self.tasks
        if category:
            filtered_tasks = [task for task in filtered_tasks if task.category.lower() == category.lower()]
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority.lower() == priority.lower()]
        return filtered_tasks

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.create_ui()

    def create_ui(self):
        self.add_task_frame()
        self.display_tasks_frame()

    def add_task_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Description").grid(row=1, column=0)
        self.description_entry = tk.Entry(frame)
        self.description_entry.grid(row=1, column=1)

        tk.Label(frame, text="Deadline (YYYY-MM-DD)").grid(row=2, column=0)
        self.deadline_entry = tk.Entry(frame)
        self.deadline_entry.grid(row=2, column=1)

        tk.Label(frame, text="Priority").grid(row=3, column=0)
        self.priority_entry = tk.Entry(frame)
        self.priority_entry.grid(row=3, column=1)

        tk.Label(frame, text="Category").grid(row=4, column=0)
        self.category_entry = tk.Entry(frame)
        self.category_entry.grid(row=4, column=1)

        tk.Button(frame, text="Add Task", command=self.add_task).grid(row=5, columnspan=2)

    def display_tasks_frame(self):
        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.pack(pady=10)

        self.update_tasks_listbox()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()

        try:
            self.task_manager.add_task(title, description, deadline, priority, category)
            self.update_tasks_listbox()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.tasks_listbox.insert(tk.END, task.to_string())

    def main(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()