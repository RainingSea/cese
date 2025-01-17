import tkinter as tk
from tkinter import messagebox
import threading
import time

class QuickTimer:
    def __init__(self):
        self.duration = 0
        self.timer = None
        self.root = tk.Tk()
        self.root.title("QuickTimer")
        
        self.time_input = tk.Entry(self.root, width=10)
        self.time_input.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.timer_display = tk.Label(self.root, text="Timer: 0", font=("Helvetica", 16))
        self.timer_display.pack(pady=10)

        self.root.mainloop()

    def start_timer(self):
        try:
            self.duration = int(self.time_input.get())
            self.save_timer(self.duration)
            self.update_timer_display()
            self.timer = threading.Timer(self.duration, self.notify_user)
            self.timer.start()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def update_timer_display(self):
        if self.duration > 0:
            self.timer_display.config(text=f"Timer: {self.duration}")
            self.duration -= 1
            self.root.after(1000, self.update_timer_display)

    def notify_user(self):
        messagebox.showinfo("Time's up!", "The timer has reached zero.")

    def save_timer(self, duration: int):
        with open("timers.txt", "a") as file:
            file.write(f"duration: {duration}\n")