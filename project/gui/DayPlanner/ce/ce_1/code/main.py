import tkinter as tk
from tkinter import messagebox
from TaskManager import TaskManager

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Day Planner")
        self.create_widgets()

    def create_widgets(self):
        self.task_name_entry = tk.Entry(self.root, width=50)
        self.task_name_entry.pack(pady=10)

        self.priority_var = tk.StringVar(value="Medium")
        tk.OptionMenu(self.root, self.priority_var, "High", "Medium", "Low").pack(pady=10)

        self.category_var = tk.StringVar(value="Work")
        tk.OptionMenu(self.root, self.category_var, "Work", "Personal", "Custom").pack(pady=10)

        self.start_time_entry = tk.Entry(self.root, width=20)
        self.start_time_entry.pack(pady=10)
        self.start_time_entry.insert(0, "Start Time (HH:MM)")

        self.end_time_entry = tk.Entry(self.root, width=20)
        self.end_time_entry.pack(pady=10)
        self.end_time_entry.insert(0, "End Time (HH:MM)")

        self.save_button = tk.Button(self.root, text="Save Task", command=self.save_task)
        self.save_button.pack(pady=10)

        self.display_area = tk.Text(self.root, width=60, height=15)
        self.display_area.pack(pady=10)
        self.display_tasks()

    def save_task(self):
        name = self.task_name_entry.get()
        priority = self.priority_var.get()
        category = self.category_var.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        if not name or not start_time or not end_time:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        self.task_manager.add_task(name, priority, category, start_time, end_time)
        self.display_tasks()
        self.clear_entries()

    def display_tasks(self):
        self.display_area.delete(1.0, tk.END)
        for task in self.task_manager.tasks:
            self.display_area.insert(tk.END, f"{task.name} | {task.priority} | {task.category} | {task.start_time} - {task.end_time}\n")

    def clear_entries(self):
        self.task_name_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.start_time_entry.insert(0, "Start Time (HH:MM)")
        self.end_time_entry.delete(0, tk.END)
        self.end_time_entry.insert(0, "End Time (HH:MM)")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()