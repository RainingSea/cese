import tkinter as tk
from tkinter import messagebox
from task import Task
from task_manager import TaskManager

class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.task_manager = TaskManager()
        self.task_manager.load_tasks('tasks.txt')

        self.create_main_window()

    def create_main_window(self) -> None:
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.task_listbox = tk.Listbox(self.frame, width=50)
        self.task_listbox.pack()

        self.title_entry = tk.Entry(self.frame, width=50)
        self.title_entry.pack()
        self.description_entry = tk.Entry(self.frame, width=50)
        self.description_entry.pack()
        self.due_date_entry = tk.Entry(self.frame, width=50)
        self.due_date_entry.pack()
        self.priority_entry = tk.Entry(self.frame, width=50)
        self.priority_entry.pack()

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.pack()
        self.update_button = tk.Button(self.frame, text="Update Task", command=self.update_task)
        self.update_button.pack()
        self.complete_button = tk.Button(self.frame, text="Complete Task", command=self.complete_task)
        self.complete_button.pack()

        self.display_tasks(self.task_manager.tasks)

    def display_tasks(self, tasks: list[Task]) -> None:
        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            self.task_listbox.insert(tk.END, task.to_string())

    def get_task_details(self) -> Task:
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()
        return Task(title, description, due_date, priority)

    def add_task(self) -> None:
        task = self.get_task_details()
        self.task_manager.add_task(task)
        self.task_manager.save_tasks('tasks.txt')
        self.display_tasks(self.task_manager.tasks)

    def update_task(self) -> None:
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.get_task_details()
            self.task_manager.update_task(selected_index[0], task)
            self.task_manager.save_tasks('tasks.txt')
            self.display_tasks(self.task_manager.tasks)

    def complete_task(self) -> None:
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.task_manager.mark_task_complete(selected_index[0])
            self.task_manager.save_tasks('tasks.txt')
            self.display_tasks(self.task_manager.tasks)

    def show_message(self, message: str) -> None:
        messagebox.showinfo("Information", message)