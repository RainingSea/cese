import tkinter as tk
from tkinter import messagebox, simpledialog
from task_manager import TaskManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Office Task Tracker")
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()
        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.master, width=50, height=15)
        self.task_listbox.pack()

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.edit_button = tk.Button(self.master, text="Edit Task", command=self.edit_task)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.refresh_task_list()

    def add_task(self):
        title = simpledialog.askstring("Input", "Enter task title:")
        description = simpledialog.askstring("Input", "Enter task description:")
        deadline = simpledialog.askstring("Input", "Enter task deadline:")
        priority = simpledialog.askstring("Input", "Enter task priority:")
        status = simpledialog.askstring("Input", "Enter task status:")
        category = simpledialog.askstring("Input", "Enter task category:")
        
        if title and description and deadline and priority and status and category:
            self.task_manager.add_task(title, description, deadline, priority, status, category)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled out.")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = selected_task_index[0]
            title = simpledialog.askstring("Input", "Enter new task title:", initialvalue=self.task_manager.tasks[task_id]['title'])
            description = simpledialog.askstring("Input", "Enter new task description:", initialvalue=self.task_manager.tasks[task_id]['description'])
            deadline = simpledialog.askstring("Input", "Enter new task deadline:", initialvalue=self.task_manager.tasks[task_id]['deadline'])
            priority = simpledialog.askstring("Input", "Enter new task priority:", initialvalue=self.task_manager.tasks[task_id]['priority'])
            status = simpledialog.askstring("Input", "Enter new task status:", initialvalue=self.task_manager.tasks[task_id]['status'])
            category = simpledialog.askstring("Input", "Enter new task category:", initialvalue=self.task_manager.tasks[task_id]['category'])

            if title and description and deadline and priority and status and category:
                self.task_manager.edit_task(task_id, title, description, deadline, priority, status, category)
                self.refresh_task_list()
            else:
                messagebox.showwarning("Input Error", "All fields must be filled out.")
        else:
            messagebox.showwarning("Selection Error", "No task selected.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = selected_task_index[0]
            self.task_manager.delete_task(task_id)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Selection Error", "No task selected.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task['title']} - {task['status']}")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()