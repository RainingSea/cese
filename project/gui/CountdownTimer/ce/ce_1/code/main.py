import tkinter as tk
import time

class CountdownTimer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration
        self.is_running = False

    def start_timer(self) -> None:
        self.is_running = True
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_display()

    def reset_timer(self) -> None:
        self.is_running = False
        self.remaining_time = self.duration
        self.update_display()

    def load_last_duration(self) -> int:
        try:
            with open('last_duration.txt', 'r') as file:
                return int(file.readline().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_last_duration(self, duration: int) -> None:
        with open('last_duration.txt', 'w') as file:
            file.write(str(duration))

    def update_display(self) -> None:
        pass  # This will be handled by the GUI class

class GUI:
    def __init__(self):
        self.timer = CountdownTimer(self.timer.load_last_duration())
        self.root = tk.Tk()
        self.root.title("Countdown Timer")
        
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_countdown)
        self.reset_button.pack()

        self.countdown_label = tk.Label(self.root, text="00:00")
        self.countdown_label.pack()

        self.root.mainloop()

    def start_countdown(self) -> None:
        try:
            duration = int(self.time_entry.get())
            self.timer.duration = duration
            self.timer.remaining_time = duration
            self.timer.save_last_duration(duration)
            self.timer.start_timer()
        except ValueError:
            self.countdown_label.config(text="Invalid input")

    def reset_countdown(self) -> None:
        self.timer.reset_timer()
        self.update_label()

    def update_label(self) -> None:
        minutes, seconds = divmod(self.timer.remaining_time, 60)
        self.countdown_label.config(text=f"{minutes:02}:{seconds:02}")