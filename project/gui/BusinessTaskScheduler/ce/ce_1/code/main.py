import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager
from notification_manager import NotificationManager

class App:
    def __init__(self):
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager()
        self.root = tk.Tk()
        self.root.title("Business Task Scheduler")
        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.pack(fill=tk.BOTH, expand=True)

        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.load_tasks()

        self.create_task_button = tk.Button(self.root, text="Create Task", command=self.create_task)
        self.create_task_button.pack(side=tk.LEFT)

        self.update_status_button = tk.Button(self.root, text="Update Status", command=self.update_status)
        self.update_status_button.pack(side=tk.LEFT)

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.get_tasks():
            self.task_listbox.insert(tk.END, f"{task.title} - {task.status}")

    def create_task(self):
        title = "Sample Task"
        description = "This is a sample task description."
        priority = "High"
        assignee = "User1"
        deadline = "2023-12-31"
        self.task_manager.create_task(title, description, priority, assignee, deadline)
        self.load_tasks()
        self.notification_manager.add_notification(f"Task '{title}' created.")
        self.status_bar.config(text=f"Task '{title}' created.")

    def update_status(self):
        selected_task = self.task_listbox.curselection()
        if selected_task:
            title = self.task_listbox.get(selected_task).split(" - ")[0]
            self.task_manager.update_task_status(title, "Completed")
            self.load_tasks()
            self.notification_manager.add_notification(f"Task '{title}' status updated to Completed.")
            self.status_bar.config(text=f"Task '{title}' status updated to Completed.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()