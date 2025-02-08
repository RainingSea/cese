import tkinter as tk
from TaskManager import TaskManager

class BusinessTaskScheduler:
    def __init__(self, master):
        self.master = master
        self.master.title("Business Task Scheduler")
        self.task_manager = TaskManager()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Task Title:")
        self.title_label.pack()

        self.title_entry = tk.Entry(self.master)
        self.title_entry.pack()

        self.description_label = tk.Label(self.master, text="Description:")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.master)
        self.description_entry.pack()

        self.priority_label = tk.Label(self.master, text="Priority (1-5):")
        self.priority_label.pack()

        self.priority_entry = tk.Entry(self.master)
        self.priority_entry.pack()

        self.deadline_label = tk.Label(self.master, text="Deadline:")
        self.deadline_label.pack()

        self.deadline_entry = tk.Entry(self.master)
        self.deadline_entry.pack()

        self.add_task_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.view_tasks_button = tk.Button(self.master, text="View Tasks", command=self.view_tasks)
        self.view_tasks_button.pack()

        self.notification_area = tk.Text(self.master, height=10, width=50)
        self.notification_area.pack()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        priority = int(self.priority_entry.get())
        deadline = self.deadline_entry.get()
        task = Task(title, description, priority, deadline)
        self.task_manager.add_task(task)
        self.notification_area.insert(tk.END, f"Task '{title}' added successfully!\n")

    def view_tasks(self):
        self.notification_area.delete(1.0, tk.END)
        for task in self.task_manager.tasks:
            self.notification_area.insert(tk.END, f"{task.title} | {task.description} | {task.priority} | {task.deadline} | {task.status}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessTaskScheduler(root)
    root.mainloop()