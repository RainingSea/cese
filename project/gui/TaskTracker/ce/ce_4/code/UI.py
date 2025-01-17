import tkinter as tk
from tkinter import messagebox
from TaskManager import TaskManager
from Task import Task

class UI:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.window = tk.Tk()
        self.window.title("Office Task Tracker")
        self.create_main_window()

    def create_main_window(self) -> None:
        self.task_listbox = tk.Listbox(self.window, width=50)
        self.task_listbox.pack(pady=10)

        self.search_entry = tk.Entry(self.window)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.window, text="Search", command=self.search_ui)
        self.search_button.pack(pady=5)

        self.add_button = tk.Button(self.window, text="Add Task", command=self.add_task_ui)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(self.window, text="Update Task", command=lambda: self.update_task_ui(self.task_listbox.curselection()[0]))
        self.update_button.pack(pady=5)

        self.complete_button = tk.Button(self.window, text="Mark Complete", command=lambda: self.mark_complete_ui(self.task_listbox.curselection()[0]))
        self.complete_button.pack(pady=5)

        self.load_tasks()

    def load_tasks(self) -> None:
        self.task_manager.load_tasks('tasks.txt')
        self.refresh_task_list()

    def refresh_task_list(self) -> None:
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, task.to_string())

    def add_task_ui(self) -> None:
        title = "New Task"
        description = "Task Description"
        due_date = "2023-12-31"
        priority = "Medium"
        task = Task(title, description, due_date, priority)
        self.task_manager.add_task(task)
        self.refresh_task_list()

    def update_task_ui(self, index: int) -> None:
        title = "Updated Task"
        description = "Updated Description"
        due_date = "2023-12-31"
        priority = "High"
        task = Task(title, description, due_date, priority)
        self.task_manager.update_task(index, task)
        self.refresh_task_list()

    def mark_complete_ui(self, index: int) -> None:
        self.task_manager.mark_task_complete(index)
        self.refresh_task_list()

    def search_ui(self) -> None:
        keyword = self.search_entry.get()
        results = self.task_manager.search_tasks(keyword)
        self.task_listbox.delete(0, tk.END)
        for task in results:
            self.task_listbox.insert(tk.END, task.to_string())