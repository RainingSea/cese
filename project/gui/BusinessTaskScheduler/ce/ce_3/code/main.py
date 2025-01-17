import tkinter as tk
from tkinter import messagebox
from task_manager import Task, TaskManager
from team_manager import User, TeamManager
from notification_manager import Notification, NotificationManager

class BusinessTaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Task Scheduler")

        self.task_manager = TaskManager()
        self.team_manager = TeamManager()
        self.notification_manager = NotificationManager()

        self.task_manager.load_tasks()
        self.team_manager.load_team_members()
        self.notification_manager.load_notifications()

        self.create_widgets()

    def create_widgets(self):
        # Create input fields for task details
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack()
        self.deadline_entry = tk.Entry(self.root)
        self.deadline_entry.pack()

        # Create buttons for actions
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        priority = int(self.priority_entry.get())
        deadline = self.deadline_entry.get()

        if title and description and priority and deadline:
            task = Task(title, description, priority, deadline)
            self.task_manager.add_task(task)
            self.status_bar.config(text=f"Task '{title}' added successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Input Error", "Please fill all fields.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessTaskSchedulerApp(root)
    root.mainloop()