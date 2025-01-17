import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class Timer:
    def __init__(self, duration: int, timer_type: str):
        self.duration = duration
        self.timer_type = timer_type

    def countdown(self):
        while self.duration:
            mins, secs = divmod(self.duration, 60)
            timer_format = '{:02d}:{:02d}'.format(mins, secs)
            print(timer_format, end='\r')  # Display timer in console for debugging
            time.sleep(1)
            self.duration -= 1

class FocusTime:
    def __init__(self, work_duration: int, break_duration: int):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.is_running = False
        self.timer_thread = None

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self._run_timer)
            self.timer_thread.start()

    def stop_timer(self):
        self.is_running = False
        if self.timer_thread is not None:
            self.timer_thread.join()

    def reset_timer(self):
        self.stop_timer()
        self.load_settings()

    def load_settings(self) -> None:
        if os.path.exists('settings.txt'):
            with open('settings.txt', 'r') as file:
                settings = file.read().splitlines()
                self.work_duration = int(settings[0])
                self.break_duration = int(settings[1])

    def save_settings(self) -> None:
        with open('settings.txt', 'w') as file:
            file.write(f"{self.work_duration}\n")
            file.write(f"{self.break_duration}\n")

    def send_notification(self, message: str) -> None:
        messagebox.showinfo("Notification", message)

    def _run_timer(self):
        while self.is_running:
            self.send_notification("Work time!")
            timer = Timer(self.work_duration, "work")
            timer.countdown()
            if not self.is_running:
                break
            self.send_notification("Break time!")
            timer = Timer(self.break_duration, "break")
            timer.countdown()

class FocusTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusTime")
        self.focus_time = FocusTime(25 * 60, 5 * 60)  # Default to 25 min work, 5 min break
        self.focus_time.load_settings()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="FocusTime Timer")
        self.label.pack()

        self.work_duration_entry = tk.Entry(self.root)
        self.work_duration_entry.insert(0, str(self.focus_time.work_duration // 60))
        self.work_duration_entry.pack()

        self.break_duration_entry = tk.Entry(self.root)
        self.break_duration_entry.insert(0, str(self.focus_time.break_duration // 60))
        self.break_duration_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop)
        self.stop_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.pack()

    def start(self):
        self.focus_time.work_duration = int(self.work_duration_entry.get()) * 60
        self.focus_time.break_duration = int(self.break_duration_entry.get()) * 60
        self.focus_time.save_settings()
        self.focus_time.start_timer()

    def stop(self):
        self.focus_time.stop_timer()

    def reset(self):
        self.focus_time.reset_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = FocusTimeApp(root)
    root.mainloop()