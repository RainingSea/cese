import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self) -> None:
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Time Tracker")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.pack()

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.show_report)
        self.report_button.pack()

        self.update_task_listbox()

    def add_task(self) -> None:
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            self.task_manager.add_task(title, description)
            self.update_task_listbox()
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")

    def update_task_listbox(self) -> None:
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, f"{task.title} - {task.description}")

    def show_report(self) -> None:
        report = self.task_manager.generate_report()
        messagebox.showinfo("Report", report)

    def main(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()