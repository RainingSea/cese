import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management Application")
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()
        self.create_widgets()

    def create_widgets(self):
        # Task Creation Form
        tk.Label(self.root, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Description").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Assigned To").grid(row=2, column=0)
        self.assigned_to_entry = tk.Entry(self.root)
        self.assigned_to_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Deadline").grid(row=3, column=0)
        self.deadline_entry = tk.Entry(self.root)
        self.deadline_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Priority").grid(row=4, column=0)
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Create Task", command=self.create_task).grid(row=5, column=0, columnspan=2)

        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.grid(row=6, column=0, columnspan=2)

    def create_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        assigned_to = self.assigned_to_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        
        if title and description and assigned_to and deadline and priority:
            self.task_manager.create_task(title, description, assigned_to, deadline, priority)
            self.update_task_list()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.title} - {task.progress}")

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()