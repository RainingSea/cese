import tkinter as tk
from tkinter import messagebox
import time
import threading

class Timer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration
        self.timer_thread = None
        self.is_paused = False

    def start(self):
        if self.timer_thread is None:
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()

    def run(self):
        while self.remaining_time > 0 and not self.is_paused:
            time.sleep(1)
            self.remaining_time -= 1

    def pause(self):
        self.is_paused = True

    def reset(self):
        self.remaining_time = self.duration
        self.is_paused = False
        if self.timer_thread is not None:
            self.timer_thread.join()
            self.timer_thread = None

class Notification:
    @staticmethod
    def send_notification(message: str):
        messagebox.showinfo("Notification", message)

class FocusTimeApp:
    def __init__(self):
        self.work_duration = 25  # Default work duration in minutes
        self.break_duration = 5   # Default break duration in minutes
        self.timer_running = False
        self.timer = None
        self.load_settings()
        
        self.root = tk.Tk()
        self.root.title("FocusTime Application")
        
        self.timer_label = tk.Label(self.root, text="00:00", font=("Helvetica", 48))
        self.timer_label.pack()

        self.work_entry = tk.Entry(self.root)
        self.work_entry.insert(0, str(self.work_duration))
        self.work_entry.pack()

        self.break_entry = tk.Entry(self.root)
        self.break_entry.insert(0, str(self.break_duration))
        self.break_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.work_duration = int(self.work_entry.get()) * 60
            self.timer = Timer(self.work_duration)
            self.timer.start()
            self.update_timer()

    def update_timer(self):
        if self.timer and self.timer.remaining_time > 0:
            minutes, seconds = divmod(self.timer.remaining_time, 60)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)
        elif self.timer and self.timer.remaining_time == 0:
            Notification.send_notification("Time's up! Take a break.")
            self.timer.reset()
            self.timer_running = False

    def pause_timer(self):
        if self.timer_running:
            self.timer.pause()
            self.timer_running = False

    def reset_timer(self):
        if self.timer:
            self.timer.reset()
            self.timer_running = False
            self.timer_label.config(text="00:00")

    def load_settings(self):
        try:
            with open("settings.txt", "r") as file:
                settings = file.read().strip().split('|')
                if len(settings) == 2:
                    self.work_duration = int(settings[0])
                    self.break_duration = int(settings[1])
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        with open("settings.txt", "w") as file:
            file.write(f"{self.work_duration}|{self.break_duration}")

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    FocusTimeApp()