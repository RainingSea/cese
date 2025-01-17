import tkinter as tk
import os
import time

class CountdownTimer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration

    def start_countdown(self) -> None:
        while self.remaining_time > 0:
            time.sleep(1)
            self.remaining_time -= 1

    def reset_timer(self, new_duration: int) -> None:
        self.duration = new_duration
        self.remaining_time = new_duration

    def load_settings(self) -> list:
        if os.path.exists('countdown_settings.txt'):
            with open('countdown_settings.txt', 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        return []

    def save_settings(self, duration: int) -> None:
        with open('countdown_settings.txt', 'a') as file:
            file.write(f"{duration}\n")

class UI:
    def __init__(self):
        self.timer = CountdownTimer(0)
        self.window = tk.Tk()
        self.window.title("Countdown Timer")
        self.create_main_window()

    def create_main_window(self) -> None:
        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.start_button = tk.Button(self.window, text="Start", command=self.start_button_clicked)
        self.start_button.pack()

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_button_clicked)
        self.reset_button.pack()

        self.label = tk.Label(self.window, text="Remaining Time: 0")
        self.label.pack()

        self.window.mainloop()

    def start_button_clicked(self) -> None:
        duration = int(self.entry.get())
        self.timer.reset_timer(duration)
        self.timer.save_settings(duration)
        self.update_display(duration)
        self.timer.start_countdown()
        self.update_display(self.timer.remaining_time)

    def reset_button_clicked(self) -> None:
        new_duration = int(self.entry.get())
        self.timer.reset_timer(new_duration)
        self.update_display(new_duration)

    def update_display(self, remaining_time: int) -> None:
        self.label.config(text=f"Remaining Time: {remaining_time}")

if __name__ == "__main__":
    UI()