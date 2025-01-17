import tkinter as tk
from TimeTracker import TimeTracker

class TimeTrackerApp:
    def __init__(self, root):
        self.tracker = TimeTracker()
        self.root = root
        self.root.title("Time Tracker")

        self.create_widgets()

    def create_widgets(self):
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.start_timer_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_timer_button.pack()

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.pack()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        self.tracker.add_task(title, description)

    def start_timer(self):
        task_id = len(self.tracker.tasks)  # Start timer for the last task
        self.tracker.start_timer(task_id)

    def generate_report(self):
        report = self.tracker.generate_report()
        print(report)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()