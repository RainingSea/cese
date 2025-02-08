import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager
from timer_manager import TimerManager
from report_generator import ReportGenerator

class Main:
    def __init__(self) -> None:
        self.task_manager = TaskManager()
        self.timer_manager = TimerManager()
        self.report_generator = ReportGenerator()
        self.task_manager.load_tasks()
        self.timer_manager.load_timers()

        self.root = tk.Tk()
        self.root.title("Task Timer Application")

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.create_task_button = tk.Button(self.root, text="Create Task", command=self.create_task)
        self.create_task_button.pack()

        self.start_timer_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_timer_button.pack()

        self.stop_timer_button = tk.Button(self.root, text="Stop Timer", command=self.stop_timer)
        self.stop_timer_button.pack()

        self.generate_report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack()

        self.root.mainloop()

    def create_task(self) -> None:
        title = self.title_entry.get()
        description = self.description_entry.get()
        self.task_manager.create_task(title, description)
        messagebox.showinfo("Task Created", f"Task '{title}' created.")

    def start_timer(self) -> None:
        title = self.title_entry.get()
        self.timer_manager.start_timer(title)
        messagebox.showinfo("Timer Started", f"Timer started for task '{title}'.")

    def stop_timer(self) -> None:
        title = self.title_entry.get()
        self.timer_manager.stop_timer(title)
        messagebox.showinfo("Timer Stopped", f"Timer stopped for task '{title}'.")

    def generate_report(self) -> None:
        report = self.report_generator.generate_report()
        messagebox.showinfo("Generated Report", report)

if __name__ == "__main__":
    Main()