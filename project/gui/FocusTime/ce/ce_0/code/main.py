import tkinter as tk
from tkinter import messagebox
from timer import Timer

class FocusTimeApp:
    def __init__(self):
        self.work_duration = 25 * 60  # default 25 minutes
        self.break_duration = 5 * 60   # default 5 minutes
        self.timer = None
        self.load_settings()

        self.root = tk.Tk()
        self.root.title("FocusTime")

        self.work_label = tk.Label(self.root, text="Work Duration (minutes):")
        self.work_label.pack()
        self.work_entry = tk.Entry(self.root)
        self.work_entry.pack()

        self.break_label = tk.Label(self.root, text="Break Duration (minutes):")
        self.break_label.pack()
        self.break_entry = tk.Entry(self.root)
        self.break_entry.pack()

        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.remaining_time_label = tk.Label(self.root, text="")
        self.remaining_time_label.pack()

        self.root.mainloop()

    def start_timer(self):
        work_duration = int(self.work_entry.get()) * 60
        break_duration = int(self.break_entry.get()) * 60
        self.timer = Timer(work_duration)
        self.timer.start()
        self.remaining_time_label.config(text=f"Working for {work_duration // 60} minutes.")

    def load_settings(self):
        try:
            with open("settings.txt", "r") as file:
                settings = file.readlines()
                for line in settings:
                    key, value = line.strip().split('|')
                    if key == 'work_duration':
                        self.work_duration = int(value) * 60
                    elif key == 'break_duration':
                        self.break_duration = int(value) * 60
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        with open("settings.txt", "w") as file:
            file.write(f"work_duration|{self.work_duration // 60}\n")
            file.write(f"break_duration|{self.break_duration // 60}\n")