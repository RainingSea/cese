import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.setup_ui()

    def setup_ui(self):
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack()
        self.description_entry = tk.Entry(self.root, width=50)
        self.description_entry.pack()
        self.due_date_entry = tk.Entry(self.root, width=50)
        self.due_date_entry.pack()
        self.priority_entry = tk.Entry(self.root, width=50)
        self.priority_entry.pack()

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_button.pack()

        update_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        update_button.pack()

        complete_button = tk.Button(self.root, text="Complete Task", command=self.complete_task)
        complete_button.pack()

        search_entry = tk.Entry(self.root, width=50)
        search_entry.pack()
        search_button = tk.Button(self.root, text="Search Task", command=lambda: self.search_tasks(search_entry.get()))
        search_button.pack()

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.id}: {task.title} - {task.due_date}")

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()
        self.task_manager.add_task(title, description, due_date, priority)
        self.load_tasks()

    def update_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_manager.tasks[selected_task[0]].id
            title = self.title_entry.get()
            description = self.description_entry.get()
            due_date = self.due_date_entry.get()
            priority = self.priority_entry.get()
            self.task_manager.update_task(task_id, title, description, due_date, priority)
            self.load_tasks()
        else:
            messagebox.showwarning("Update Task", "Please select a task to update.")

    def complete_task(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            task_id = self.task_manager.tasks[selected_task[0]].id
            self.task_manager.complete_task(task_id)
            self.load_tasks()
        else:
            messagebox.showwarning("Complete Task", "Please select a task to complete.")

    def search_tasks(self, keyword: str):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.search_tasks(keyword):
            self.task_listbox.insert(tk.END, f"{task.id}: {task.title} - {task.due_date}")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()