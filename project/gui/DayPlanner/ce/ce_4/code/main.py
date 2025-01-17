import tkinter as tk
from tkinter import messagebox
import json
import os

class Task:
    def __init__(self, id: int, name: str, priority: int, category: str, time_slot: str):
        self.id = id
        self.name = name
        self.priority = priority
        self.category = category
        self.time_slot = time_slot

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                task_data = json.load(file)
                self.tasks = [Task(**task) for task in task_data]

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, indent=4)

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.window = tk.Tk()
        self.create_ui()

    def create_ui(self):
        self.window.title("Day Planner")
        self.task_listbox = tk.Listbox(self.window)
        self.task_listbox.pack()

        tk.Label(self.window, text="Task Name:").pack()
        self.task_name_entry = tk.Entry(self.window)
        self.task_name_entry.pack()

        tk.Label(self.window, text="Priority:").pack()
        self.task_priority_entry = tk.Entry(self.window)
        self.task_priority_entry.pack()

        tk.Label(self.window, text="Category:").pack()
        self.task_category_entry = tk.Entry(self.window)
        self.task_category_entry.pack()

        tk.Label(self.window, text="Time Slot:").pack()
        self.task_time_slot_entry = tk.Entry(self.window)
        self.task_time_slot_entry.pack()

        tk.Button(self.window, text="Add Task", command=self.add_task).pack()
        tk.Button(self.window, text="Delete Task", command=self.delete_task).pack()

        self.update_task_listbox()
        self.window.mainloop()

    def add_task(self):
        name = self.task_name_entry.get()
        priority = int(self.task_priority_entry.get())
        category = self.task_category_entry.get()
        time_slot = self.task_time_slot_entry.get()
        task_id = len(self.task_manager.tasks) + 1
        
        new_task = Task(task_id, name, priority, category, time_slot)
        self.task_manager.add_task(new_task)
        self.update_task_listbox()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = self.task_manager.tasks[selected_task_index[0]].id
            self.task_manager.remove_task(task_id)
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.name} - {task.priority} - {task.category} - {task.time_slot}")

if __name__ == "__main__":
    main = Main()