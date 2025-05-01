import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Day Planner")
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()
        self.create_widgets()
        self.update_task_display()

    def create_widgets(self):
        # Input field for task name
        self.task_name_var = tk.StringVar()
        tk.Label(self.root, text="Task Name:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.task_name_var).grid(row=0, column=1)

        # Dropdown for priority
        self.priority_var = tk.StringVar(value="Normal")
        tk.Label(self.root, text="Priority:").grid(row=1, column=0)
        tk.OptionMenu(self.root, self.priority_var, "High", "Normal", "Low").grid(row=1, column=1)

        # Dropdown for category
        self.category_var = tk.StringVar(value="Work")
        tk.Label(self.root, text="Category:").grid(row=2, column=0)
        tk.OptionMenu(self.root, self.category_var, "Work", "Personal", "Custom").grid(row=2, column=1)

        # Input fields for start and end times
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        tk.Label(self.root, text="Start Time:").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.start_time_var).grid(row=3, column=1)
        tk.Label(self.root, text="End Time:").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.end_time_var).grid(row=4, column=1)

        # Buttons for adding, editing, and deleting tasks
        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=5, column=0)
        tk.Button(self.root, text="Edit Task", command=self.edit_task).grid(row=5, column=1)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=5, column=2)

        # Area to display tasks
        self.task_display = tk.Text(self.root, height=10, width=50)
        self.task_display.grid(row=6, column=0, columnspan=3)

    def add_task(self):
        name = self.task_name_var.get()
        priority = self.priority_var.get()
        category = self.category_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        
        if not name or not start_time or not end_time:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        self.task_manager.add_task(name, priority, category, start_time, end_time)
        self.update_task_display()
        self.clear_entries()

    def edit_task(self):
        selected_index = self.task_display.index(tk.INSERT).split('.')[0]  # Get the line number of the selected task
        index = int(selected_index) - 1  # Convert to zero-based index
        if 0 <= index < len(self.task_manager.tasks):
            task = self.task_manager.tasks[index]
            self.task_name_var.set(task.name)
            self.priority_var.set(task.priority)
            self.category_var.set(task.category)
            self.start_time_var.set(task.start_time)
            self.end_time_var.set(task.end_time)
            self.task_manager.edit_task(index, self.task_name_var.get(), self.priority_var.get(), self.category_var.get(), self.start_time_var.get(), self.end_time_var.get())
            self.update_task_display()

    def delete_task(self):
        selected_index = self.task_display.index(tk.INSERT).split('.')[0]  # Get the line number of the selected task
        index = int(selected_index) - 1  # Convert to zero-based index
        if 0 <= index < len(self.task_manager.tasks):
            self.task_manager.delete_task(index)
            self.update_task_display()

    def update_task_display(self):
        self.task_display.delete(1.0, tk.END)
        for index, task in enumerate(self.task_manager.tasks):
            self.task_display.insert(tk.END, f"{index + 1}: {task.name} | {task.priority} | {task.category} | {task.start_time} - {task.end_time}\n")

    def clear_entries(self):
        self.task_name_var.set("")
        self.start_time_var.set("")
        self.end_time_var.set("")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()