import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager, Task

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("DayPlanner")
        self.task_manager = TaskManager()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Input field for task title
        self.task_title = tk.Entry(self.root, width=50)
        self.task_title.pack(pady=10)

        # Dropdown for priority
        self.priority_var = tk.StringVar(self.root)
        self.priority_var.set("Select Priority")
        self.priority_menu = tk.OptionMenu(self.root, self.priority_var, *self.load_priorities())
        self.priority_menu.pack(pady=10)

        # Dropdown for category
        self.category_var = tk.StringVar(self.root)
        self.category_var.set("Select Category")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.load_categories())
        self.category_menu.pack(pady=10)

        # Input field for time slot
        self.time_slot = tk.Entry(self.root, width=50)
        self.time_slot.pack(pady=10)

        # Add task button
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Task list display
        self.task_list = tk.Listbox(self.root, width=75)
        self.task_list.pack(pady=10)

    def load_data(self):
        self.task_manager.load_tasks()

    def load_priorities(self):
        with open('priorities.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def load_categories(self):
        with open('categories.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def add_task(self):
        title = self.task_title.get()
        priority = self.priority_var.get()
        category = self.category_var.get()
        time_slot = self.time_slot.get()

        if title and priority != "Select Priority" and category != "Select Category" and time_slot:
            task = Task(title, priority, category, time_slot)
            self.task_manager.add_task(task)
            self.update_task_list()
            self.clear_inputs()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.task_manager.get_tasks():
            self.task_list.insert(tk.END, f"{task.title} | {task.priority} | {task.category} | {task.time_slot}")

    def clear_inputs(self):
        self.task_title.delete(0, tk.END)
        self.priority_var.set("Select Priority")
        self.category_var.set("Select Category")
        self.time_slot.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()