import tkinter as tk
from tkinter import messagebox
import threading
import time

class CountdownTimer:
    def __init__(self, countdown_time: int):
        self.countdown_time = countdown_time
        self.remaining_time = countdown_time
        self.running = False

    def start_timer(self):
        self.running = True
        while self.remaining_time > 0 and self.running:
            time.sleep(1)
            self.remaining_time -= 1

    def update_timer(self):
        return self.remaining_time

    def reset_timer(self):
        self.remaining_time = self.countdown_time
        self.running = False

    def save_setting(self):
        with open('countdown_settings.txt', 'a') as file:
            file.write(f'countdown_time={self.countdown_time}\n')

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Countdown Timer")
        self.timer = None
        self.create_widgets()

    def create_widgets(self):
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_countdown)
        self.reset_button.pack(pady=5)

        self.label = tk.Label(self.root, text="Remaining Time: ")
        self.label.pack(pady=10)

    def start_countdown(self):
        try:
            countdown_time = int(self.entry.get())
            self.timer = CountdownTimer(countdown_time)
            self.timer.save_setting()
            threading.Thread(target=self.run_timer).start()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")

    def run_timer(self):
        self.timer.start_timer()
        while self.timer.remaining_time > 0:
            time.sleep(1)
            self.update_display()

    def reset_countdown(self):
        if self.timer:
            self.timer.reset_timer()
            self.entry.delete(0, tk.END)
            self.label.config(text="Remaining Time: ")

    def update_display(self):
        self.label.config(text=f"Remaining Time: {self.timer.update_timer()} seconds")

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()