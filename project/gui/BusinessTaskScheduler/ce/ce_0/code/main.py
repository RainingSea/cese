import tkinter as tk
from tkinter import messagebox
from TaskManager import TaskManager
from UserManager import UserManager
from Notification import Notification

class BusinessTaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Task Scheduler")
        
        self.task_manager = TaskManager()
        self.user_manager = UserManager()
        self.notification = Notification()
        
        self.task_manager.load_tasks('tasks.txt')
        self.user_manager.load_users('users.txt')

        self.create_ui()

    def create_ui(self):
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        task_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tasks", menu=task_menu)
        task_menu.add_command(label="Create Task", command=self.create_task)
        task_menu.add_command(label="View Tasks", command=self.view_tasks)

        self.root.mainloop()

    def create_task(self):
        # Create a new window for task creation
        task_window = tk.Toplevel(self.root)
        task_window.title("Create Task")

        tk.Label(task_window, text="Title").grid(row=0, column=0)
        tk.Label(task_window, text="Description").grid(row=1, column=0)
        tk.Label(task_window, text="Priority (1-5)").grid(row=2, column=0)
        tk.Label(task_window, text="Assignee").grid(row=3, column=0)
        tk.Label(task_window, text="Deadline (YYYY-MM-DD)").grid(row=4, column=0)

        title_entry = tk.Entry(task_window)
        description_entry = tk.Entry(task_window)
        priority_entry = tk.Entry(task_window)
        assignee_entry = tk.Entry(task_window)
        deadline_entry = tk.Entry(task_window)

        title_entry.grid(row=0, column=1)
        description_entry.grid(row=1, column=1)
        priority_entry.grid(row=2, column=1)
        assignee_entry.grid(row=3, column=1)
        deadline_entry.grid(row=4, column=1)

        tk.Button(task_window, text="Submit", command=lambda: self.submit_task(
            title_entry.get(), description_entry.get(), priority_entry.get(), 
            assignee_entry.get(), deadline_entry.get(), task_window)).grid(row=5, columnspan=2)

    def submit_task(self, title, description, priority, assignee, deadline, window):
        try:
            priority = int(priority)
            self.task_manager.create_task(title, description, priority, assignee, deadline)
            self.notification.send_notification(f"Task '{title}' created successfully.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Priority must be an integer.")

    def view_tasks(self):
        tasks = self.task_manager.get_all_tasks()
        tasks_window = tk.Toplevel(self.root)
        tasks_window.title("View Tasks")
        
        for index, task in enumerate(tasks):
            tk.Label(tasks_window, text=f"{index + 1}. {task['title']} - {task['status']}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessTaskSchedulerApp(root)