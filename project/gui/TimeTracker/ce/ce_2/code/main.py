import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Task Manager")
        self.task_manager = TaskManager()
        self.create_widgets()

    def create_widgets(self) -> None:
        self.title_label = tk.Label(self.root, text="Task Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        self.description_label = tk.Label(self.root, text="Task Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.create_button = tk.Button(self.root, text="Create Task", command=self.create_task)
        self.create_button.pack()

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.show_report)
        self.report_button.pack()

    def create_task(self) -> None:
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            self.task_manager.create_task(title, description)
            messagebox.showinfo("Success", "Task created successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")

    def show_report(self) -> None:
        report = self.task_manager.generate_report()
        messagebox.showinfo("Task Report", report)

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()