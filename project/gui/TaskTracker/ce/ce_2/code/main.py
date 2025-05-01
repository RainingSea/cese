import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class Task:
    def __init__(self, id: int, title: str, description: str, deadline: str, priority: str, category: str):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.category = category

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title: str, description: str, deadline: str, priority: str, category: str) -> None:
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, deadline, priority, category)
        self.tasks.append(new_task)
        self.save_tasks()

    def edit_task(self, task_id: int, title: str, description: str, deadline: str, priority: str, category: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.title = title
                task.description = description
                task.deadline = deadline
                task.priority = priority
                task.category = category
                self.save_tasks()
                return

    def delete_task(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def search_tasks(self, query: str):
        return [task for task in self.tasks if query.lower() in task.title.lower()]

    def load_tasks(self) -> None:
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**task) for task in tasks_data]

    def save_tasks(self) -> None:
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Office Task Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()
        self.deadline_entry = tk.Entry(self.root)
        self.deadline_entry.pack()
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack()
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_button.pack()

        edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        edit_button.pack()

        delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_button.pack()

        search_button = tk.Button(self.root, text="Search Tasks", command=self.search_tasks)
        search_button.pack()

        self.load_task_list()

    def load_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.id}: {task.title}")

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        self.task_manager.add_task(title, description, deadline, priority, category)
        self.load_task_list()

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = selected_task_index[0] + 1
            title = self.title_entry.get()
            description = self.description_entry.get()
            deadline = self.deadline_entry.get()
            priority = self.priority_entry.get()
            category = self.category_entry.get()
            self.task_manager.edit_task(task_id, title, description, deadline, priority, category)
            self.load_task_list()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = selected_task_index[0] + 1
            self.task_manager.delete_task(task_id)
            self.load_task_list()

    def search_tasks(self):
        query = simpledialog.askstring("Search", "Enter task title to search:")
        if query:
            results = self.task_manager.search_tasks(query)
            self.task_listbox.delete(0, tk.END)
            for task in results:
                self.task_listbox.insert(tk.END, f"{task.id}: {task.title}")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()