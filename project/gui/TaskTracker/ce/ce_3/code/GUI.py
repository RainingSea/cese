import tkinter as tk
from tkinter import messagebox, simpledialog
from TaskManager import TaskManager
from Task import Task

class GUI:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.window = tk.Tk()
        self.window.title("Task Manager")
        self.task_listbox = tk.Listbox(self.window, width=50)
        self.task_listbox.pack()

        self.add_button = tk.Button(self.window, text="Add Task", command=self.create_task)
        self.add_button.pack()

        self.update_button = tk.Button(self.window, text="Update Task", command=self.update_task)
        self.update_button.pack()

        self.delete_button = tk.Button(self.window, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.search_button = tk.Button(self.window, text="Search Task", command=self.search_task)
        self.search_button.pack()

        self.display_tasks()

    def create_task(self) -> None:
        title = simpledialog.askstring("Input", "Enter task title:")
        description = simpledialog.askstring("Input", "Enter task description:")
        due_date = simpledialog.askstring("Input", "Enter due date (YYYY-MM-DD):")
        priority = simpledialog.askstring("Input", "Enter task priority:")
        status = "Incomplete"
        if title and description and due_date and priority:
            task = Task(title, description, due_date, priority, status)
            self.task_manager.add_task(task)
            self.display_tasks()
        else:
            messagebox.showwarning("Warning", "All fields must be filled.")

    def update_task(self) -> None:
        try:
            selected_index = self.task_listbox.curselection()[0]
            title = simpledialog.askstring("Input", "Enter new task title:")
            description = simpledialog.askstring("Input", "Enter new task description:")
            due_date = simpledialog.askstring("Input", "Enter new due date (YYYY-MM-DD):")
            priority = simpledialog.askstring("Input", "Enter new task priority:")
            status = "Incomplete"
            if title and description and due_date and priority:
                task = Task(title, description, due_date, priority, status)
                self.task_manager.update_task(selected_index, task)
                self.display_tasks()
            else:
                messagebox.showwarning("Warning", "All fields must be filled.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to update.")

    def delete_task(self) -> None:
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_manager.delete_task(selected_index)
            self.display_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def search_task(self) -> None:
        keyword = simpledialog.askstring("Input", "Enter search keyword:")
        if keyword:
            results = self.task_manager.search_tasks(keyword)
            self.task_listbox.delete(0, tk.END)
            for task in results:
                self.task_listbox.insert(tk.END, task.to_string())
        else:
            messagebox.showwarning("Warning", "Search keyword cannot be empty.")

    def display_tasks(self) -> None:
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.get_tasks():
            self.task_listbox.insert(tk.END, task.to_string())

    def run(self) -> None:
        self.window.mainloop()