import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Input form
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "Task Title")

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack(pady=5)
        self.category_entry.insert(0, "Category")

        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack(pady=5)
        self.priority_entry.insert(0, "Priority (1-5)")

        self.time_slot_entry = tk.Entry(self.root)
        self.time_slot_entry.pack(pady=5)
        self.time_slot_entry.insert(0, "Time Slot")

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_list = tk.Listbox(self.root)
        self.task_list.pack(pady=5)

        self.load_tasks()

    def add_task(self):
        title = self.title_entry.get()
        category = self.category_entry.get()
        priority = int(self.priority_entry.get())
        time_slot = self.time_slot_entry.get()
        self.task_manager.add_task(title, category, priority, time_slot)
        self.task_manager.save_tasks()
        self.load_tasks()

    def load_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_list.insert(tk.END, f"{task.title} - {task.category} - {task.priority} - {task.time_slot}")

if __name__ == "__main__":
    Main()