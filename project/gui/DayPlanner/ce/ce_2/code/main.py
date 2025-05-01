import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        self.task_description = tk.Entry(self.master, width=50)
        self.task_description.pack(pady=10)

        self.priority_label = tk.Label(self.master, text="Priority (1-5):")
        self.priority_label.pack()
        self.priority_var = tk.IntVar()
        self.priority_dropdown = tk.OptionMenu(self.master, self.priority_var, *range(1, 6))
        self.priority_dropdown.pack()

        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.pack()
        self.category_var = tk.StringVar()
        self.category_dropdown = tk.OptionMenu(self.master, self.category_var, "Work", "Personal", "Study")
        self.category_dropdown.pack()

        self.time_slot_label = tk.Label(self.master, text="Time Slot:")
        self.time_slot_label.pack()
        self.time_slot_entry = tk.Entry(self.master, width=20)
        self.time_slot_entry.pack(pady=10)

        self.add_task_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        self.task_list_label = tk.Label(self.master, text="Today's Tasks:")
        self.task_list_label.pack()

        self.task_listbox = tk.Listbox(self.master, width=80)
        self.task_listbox.pack(pady=10)

        self.update_task_list()

    def add_task(self):
        description = self.task_description.get()
        priority = self.priority_var.get()
        category = self.category_var.get()
        time_slot = self.time_slot_entry.get()

        if description and priority and category and time_slot:
            self.task_manager.add_task(description, priority, category, time_slot)
            self.update_task_list()
            self.task_description.delete(0, tk.END)
            self.time_slot_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task.description} | Priority: {task.priority} | Category: {task.category} | Time Slot: {task.time_slot}")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()