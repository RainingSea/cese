import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Task:
    def __init__(self, title, description, deadline, priority, status="Not Started", category="General"):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.category = category

    def create_task(self):
        return {
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority,
            "status": self.status,
            "category": self.category
        }

    def edit_task(self, title=None, description=None, deadline=None, priority=None, status=None, category=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if deadline:
            self.deadline = deadline
        if priority:
            self.priority = priority
        if status:
            self.status = status
        if category:
            self.category = category

    def delete_task(self):
        return None

    def update_status(self, status):
        self.status = status


class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.create_task() for task in self.tasks], file)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()

    def search_tasks(self, query):
        return [task for task in self.tasks if query.lower() in task.title.lower()]


class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Office Task Tracker")
        self.task_manager = TaskManager()

        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.grid(row=0, column=0, columnspan=4)

        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=1, column=0)

        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1)

        self.deadline_entry = tk.Entry(self.root)
        self.deadline_entry.grid(row=1, column=2)

        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.grid(row=1, column=3)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0)

        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=2, column=1)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=2)

        self.show_tasks()

    def show_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, task.title)

    def get_task_input(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        return Task(title, description, deadline, priority)

    def add_task(self):
        task = self.get_task_input()
        self.task_manager.add_task(task)
        self.show_tasks()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.task_manager.tasks[selected_index[0]]
            task.edit_task(
                title=self.title_entry.get(),
                description=self.description_entry.get(),
                deadline=self.deadline_entry.get(),
                priority=self.priority_entry.get()
            )
            self.task_manager.save_tasks()
            self.show_tasks()
        else:
            messagebox.showwarning("Edit Task", "Please select a task to edit.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.task_manager.tasks[selected_index[0]]
            self.task_manager.remove_task(task)
            self.show_tasks()
        else:
            messagebox.showwarning("Delete Task", "Please select a task to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()