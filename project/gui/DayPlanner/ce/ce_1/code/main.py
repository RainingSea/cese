import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Day Planner")
        self.create_ui()

    def create_ui(self):
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        self.task_description_entry = tk.Entry(self.root, width=50)
        self.task_description_entry.pack()

        self.priority_entry = tk.Entry(self.root, width=5)
        self.priority_entry.pack(side=tk.LEFT)

        self.category_entry = tk.Entry(self.root, width=20)
        self.category_entry.pack(side=tk.LEFT)

        self.time_slot_entry = tk.Entry(self.root, width=10)
        self.time_slot_entry.pack(side=tk.LEFT)

        add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_task_button.pack()

        self.load_tasks()

    def load_tasks(self):
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task.task_description} | {task.priority} | {task.category} | {task.time_slot}")

    def add_task(self):
        task_description = self.task_description_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        time_slot = self.time_slot_entry.get()

        if task_description and priority.isdigit() and category and time_slot:
            self.task_manager.add_task(task_description, int(priority), category, time_slot)
            self.task_listbox.insert(tk.END, f"{task_description} | {priority} | {category} | {time_slot}")
            self.clear_entries()
        else:
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")

    def clear_entries(self):
        self.task_description_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.time_slot_entry.delete(0, tk.END)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()