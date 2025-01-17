import tkinter as tk
from tkinter import messagebox
from TaskManager import TaskManager
from Notification import Notification
from CalendarIntegration import CalendarIntegration

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.task_manager = TaskManager()
        self.notification = Notification()
        self.calendar_integration = CalendarIntegration()
        
        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack(pady=10)

        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "Task Title")

        self.description_entry = tk.Entry(self.root, width=50)
        self.description_entry.pack(pady=5)
        self.description_entry.insert(0, "Task Description")

        self.priority_entry = tk.Entry(self.root, width=50)
        self.priority_entry.pack(pady=5)
        self.priority_entry.insert(0, "Priority (1-5)")

        self.assigned_member_entry = tk.Entry(self.root, width=50)
        self.assigned_member_entry.pack(pady=5)
        self.assigned_member_entry.insert(0, "Assigned Member")

        self.deadline_entry = tk.Entry(self.root, width=50)
        self.deadline_entry.pack(pady=5)
        self.deadline_entry.insert(0, "Deadline (YYYY-MM-DD)")

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        self.update_status_button = tk.Button(self.root, text="Update Status", command=self.update_status)
        self.update_status_button.pack(pady=10)

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.get_tasks():
            self.task_listbox.insert(tk.END, task.to_string())

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        priority = int(self.priority_entry.get())
        assigned_member = self.assigned_member_entry.get()
        deadline = self.deadline_entry.get()
        self.task_manager.create_task(title, description, priority, assigned_member, deadline)
        self.load_tasks()

    def update_status(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            title = selected_task.split('|')[0]
            self.task_manager.update_task_status(title, 'Completed')
            self.load_tasks()
            messagebox.showinfo("Info", f"Task '{title}' status updated to Completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()