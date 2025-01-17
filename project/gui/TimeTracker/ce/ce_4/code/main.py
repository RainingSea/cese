import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager

class Main:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Time Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.pack()

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        create_task_button = tk.Button(self.root, text="Create Task", command=self.create_task)
        create_task_button.pack()

        start_timer_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        start_timer_button.pack()

        report_button = tk.Button(self.root, text="Generate Report", command=self.show_report)
        report_button.pack()

        self.update_task_list()

    def create_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            self.task_manager.create_task(title, description)
            self.update_task_list()
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")

    def start_timer(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.task_manager.start_timer(selected_task_index[0])

    def show_report(self):
        report = self.task_manager.generate_report()
        messagebox.showinfo("Task Report", report)

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_listbox.insert(tk.END, task.title)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()