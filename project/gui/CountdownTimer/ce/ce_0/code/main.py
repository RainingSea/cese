import tkinter as tk
import os

class CountdownTimer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration

    def start_timer(self) -> None:
        if self.remaining_time > 0:
            self.remaining_time -= 1
            return self.remaining_time
        return 0

    def reset_timer(self) -> None:
        self.remaining_time = self.duration

    def load_duration(self) -> None:
        if os.path.exists('countdown_duration.txt'):
            with open('countdown_duration.txt', 'r') as file:
                self.duration = int(file.read().strip())
                self.remaining_time = self.duration

    def save_duration(self) -> None:
        with open('countdown_duration.txt', 'w') as file:
            file.write(str(self.duration))


class GUI:
    def __init__(self):
        self.timer = CountdownTimer(0)
        self.timer.load_duration()
        self.root = tk.Tk()
        self.root.title("Countdown Timer")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_button_clicked)
        self.start_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_button_clicked)
        self.reset_button.pack()

        self.timer_label = tk.Label(self.root, text="")
        self.timer_label.pack()

        self.update_timer_display()

    def start_button_clicked(self) -> None:
        try:
            duration = int(self.entry.get())
            self.timer = CountdownTimer(duration)
            self.timer.save_duration()
            self.update_timer()
        except ValueError:
            self.timer_label.config(text="Please enter a valid number.")

    def reset_button_clicked(self) -> None:
        self.timer.reset_timer()
        self.update_timer_display()

    def update_timer(self) -> None:
        remaining = self.timer.start_timer()
        if remaining > 0:
            self.timer_label.config(text=f"Time remaining: {remaining} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")

    def update_timer_display(self) -> None:
        self.timer_label.config(text=f"Last duration: {self.timer.duration} seconds")


if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()