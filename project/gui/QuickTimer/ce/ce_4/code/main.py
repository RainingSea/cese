import tkinter as tk
from tkinter import messagebox
import threading
import time

class Timer:
    def __init__(self, duration: int):
        self.duration = duration

    def start(self):
        self.countdown()

    def countdown(self):
        while self.duration:
            time.sleep(1)
            self.duration -= 1

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QuickTimer")

        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.countdown_label = tk.Label(self.root, text="Time left: 0")
        self.countdown_label.pack(pady=10)

        self.countdown_time = 0

        self.root.mainloop()

    def start_timer(self):
        try:
            self.countdown_time = int(self.duration_entry.get())
            self.countdown_label.config(text=f"Time left: {self.countdown_time}")
            timer = Timer(self.countdown_time)
            threading.Thread(target=self.run_timer, args=(timer,)).start()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def run_timer(self, timer):
        timer.start()
        self.update_timer()

    def update_timer(self):
        while self.countdown_time:
            time.sleep(1)
            self.countdown_time -= 1
            self.countdown_label.config(text=f"Time left: {self.countdown_time}")
        self.notify_user()

    def notify_user(self):
        messagebox.showinfo("Timer Complete", "The timer has finished!")