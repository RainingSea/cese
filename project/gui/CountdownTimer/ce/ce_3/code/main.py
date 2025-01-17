import tkinter as tk
import time

class CountdownTimer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration

    def start_timer(self):
        while self.remaining_time > 0:
            time.sleep(1)
            self.update_remaining_time()

    def reset_timer(self):
        self.remaining_time = self.duration

    def update_remaining_time(self):
        self.remaining_time -= 1

    def save_settings(self):
        with open('countdown_settings.txt', 'a') as file:
            file.write(f"{self.duration}\n")

    def load_settings(self):
        try:
            with open('countdown_settings.txt', 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []

class TimerUI:
    def __init__(self):
        self.countdown_timer = None
        self.root = tk.Tk()
        self.root.title("Countdown Timer")
        self.create_widgets()

    def create_widgets(self):
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_countdown)
        self.reset_button.pack()

        self.display_label = tk.Label(self.root, text="")
        self.display_label.pack()

    def start_countdown(self):
        duration = int(self.time_entry.get())
        self.countdown_timer = CountdownTimer(duration)
        self.countdown_timer.save_settings()
        self.update_display()
        self.countdown_timer.start_timer()

    def reset_countdown(self):
        if self.countdown_timer:
            self.countdown_timer.reset_timer()
            self.update_display()

    def update_display(self):
        if self.countdown_timer:
            self.display_label.config(text=f"Time Remaining: {self.countdown_timer.remaining_time} seconds")
            self.root.after(1000, self.update_display)

if __name__ == "__main__":
    app = TimerUI()
    app.root.mainloop()