import tkinter as tk
from task_manager import TaskManager
from reminder import Reminder

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.reminder = Reminder()
        self.reminder.load_reminders()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Task Manager")

        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.pack()

        self.task_name_entry = tk.Entry(self.root)
        self.task_name_entry.pack()

        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.time_slot_entry = tk.Entry(self.root)
        self.time_slot_entry.pack()

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.load_tasks()

        self.root.mainloop()

    def add_task(self):
        name = self.task_name_entry.get()
        priority = int(self.priority_entry.get())
        category = self.category_entry.get()
        time_slot = self.time_slot_entry.get()
        task = Task(name, priority, category, time_slot)
        self.task_manager.add_task(task)
        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.name} | Priority: {task.priority} | Category: {task.category} | Time Slot: {task.time_slot}")