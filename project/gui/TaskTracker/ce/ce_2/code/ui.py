import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager
from tasks import Task

class UI:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.create_main_window()

    def create_main_window(self) -> None:
        self.root.title("Task Manager")
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.update_task_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        self.update_task_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Search", command=self.search_tasks)
        self.search_button.pack()

        self.display_tasks(self.task_manager.tasks)
        self.root.mainloop()

    def display_tasks(self, tasks: list[Task]) -> None:
        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task.title} - {task.status}")

    def get_task_input(self) -> Task:
        title = "Sample Title"  # Replace with actual input retrieval logic
        description = "Sample Description"
        due_date = "2023-12-31"
        priority = "High"
        return Task(title, description, due_date, priority)

    def add_task(self) -> None:
        task = self.get_task_input()
        self.task_manager.add_task(task)
        self.display_tasks(self.task_manager.tasks)

    def update_task(self) -> None:
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.get_task_input()  # Replace with actual input retrieval logic
            self.task_manager.update_task(task)
            self.display_tasks(self.task_manager.tasks)
        else:
            messagebox.showwarning("Update Task", "Please select a task to update.")

    def search_tasks(self) -> None:
        query = self.search_entry.get()
        results = self.task_manager.search_tasks(query)
        self.display_tasks(results)