import tkinter as tk
from tkinter import messagebox
from plyer import notification
import time

class TimerApp:
    def __init__(self):
        self.duration = 0
        self.remaining_time = 0
        self.is_running = False
        self.load_settings()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("QuickTimer")

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.label = tk.Label(self.root, text="Time Remaining: 0")
        self.label.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def start_timer(self):
        try:
            self.duration = int(self.entry.get())
            self.remaining_time = self.duration
            self.is_running = True
            self.update_timer()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")

    def update_timer(self):
        if self.is_running and self.remaining_time > 0:
            self.label.config(text=f"Time Remaining: {self.remaining_time}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.notify_user()
            self.is_running = False

    def notify_user(self):
        notification.notify(
            title="Timer Finished",
            message="Your timer has ended!",
            app_name="QuickTimer"
        )

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as file:
                for line in file:
                    key, value = line.strip().split('=')
                    if key == 'last_duration':
                        self.duration = int(value)
        except FileNotFoundError:
            pass

    def save_settings(self):
        with open('settings.txt', 'w') as file:
            file.write(f'last_duration={self.duration}\n')

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

class Notification:
    def show_notification(self, message: str):
        notification.notify(
            title="Notification",
            message=message,
            app_name="QuickTimer"
        )