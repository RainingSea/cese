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
                duration = int(file.read().strip())
                return duration
        except (FileNotFoundError, ValueError):
            return 0

    def save_last_duration(self, duration: int) -> None:
        with open('last_duration.txt', 'w') as file:
            file.write(str(duration))

    def update_display(self) -> None:
        print(f"Time remaining: {self.remaining_time} seconds")

class App:
    def __init__(self):
        self.timer = CountdownTimer(self.timer.load_last_duration())
        self.window = tk.Tk()
        self.window.title("Countdown Timer")
        
        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.start_button = tk.Button(self.window, text="Start", command=self.start_button_clicked)
        self.start_button.pack()

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_button_clicked)
        self.reset_button.pack()

        self.label = tk.Label(self.window, text="Time remaining: ")
        self.label.pack()

    def run(self) -> None:
        self.window.mainloop()

    def start_button_clicked(self) -> None:
        duration = int(self.entry.get())
        self.timer.duration = duration
        self.timer.save_last_duration(duration)
        self.timer.start_timer()

    def reset_button_clicked(self) -> None:
        self.timer.reset_timer()

if __name__ == "__main__":
    app = App()
    app.run()