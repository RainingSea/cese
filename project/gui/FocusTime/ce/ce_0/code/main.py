import tkinter as tk
from tkinter import messagebox
import threading
import time

class Timer:
    def __init__(self):
        self.work_duration = 0
        self.break_duration = 0
        self.timer_thread = None
        self.running = False

    def start(self, duration):
        self.running = True
        self.timer_thread = threading.Thread(target=self._countdown, args=(duration,))
        self.timer_thread.start()

    def stop(self):
        self.running = False

    def _countdown(self, duration):
        while duration > 0 and self.running:
            time.sleep(1)
            duration -= 1
        self.running = False

class Settings:
    def __init__(self):
        self.work_duration = 25  # default work duration in minutes
        self.break_duration = 5   # default break duration in minutes
        self.load_settings()

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as file:
                settings = file.readlines()
                for setting in settings:
                    key, value = setting.strip().split('|')
                    if key == 'work_duration':
                        self.work_duration = int(value)
                    elif key == 'break_duration':
                        self.break_duration = int(value)
        except FileNotFoundError:
            self.save_settings(self.work_duration, self.break_duration)

    def save_settings(self, work_duration, break_duration):
        with open('settings.txt', 'w') as file:
            file.write(f'work_duration|{work_duration}\n')
            file.write(f'break_duration|{break_duration}\n')

class FocusTimeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FocusTime")
        self.settings = Settings()
        self.timer = Timer()

        self.work_duration_var = tk.IntVar(value=self.settings.work_duration)
        self.break_duration_var = tk.IntVar(value=self.settings.break_duration)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        tk.Label(self.root, text="Work Duration (minutes):").pack()
        tk.Entry(self.root, textvariable=self.work_duration_var).pack()

        tk.Label(self.root, text="Break Duration (minutes):").pack()
        tk.Entry(self.root, textvariable=self.break_duration_var).pack()

        tk.Button(self.root, text="Start", command=self.start_timer).pack()
        self.time_label = tk.Label(self.root, text="")
        self.time_label.pack()

    def start_timer(self):
        work_duration = self.work_duration_var.get() * 60
        break_duration = self.break_duration_var.get() * 60
        self.timer.start(work_duration)
        self.update_display()

    def update_display(self):
        if self.timer.running:
            time_left = self.timer.work_duration if self.timer.running else 0
            self.time_label.config(text=f"Time left: {time_left} seconds")
            self.root.after(1000, self.update_display)
        else:
            self.show_notification("Time's up!")
            self.save_settings()

    def show_notification(self, message):
        messagebox.showinfo("Notification", message)

    def save_settings(self):
        self.settings.save_settings(self.work_duration_var.get(), self.break_duration_var.get())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FocusTimeApp()
    app.run()