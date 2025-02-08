import tkinter as tk
from tkinter import messagebox
from countdown_timer import CountdownTimer

class GUI:
    def __init__(self):
        self.timer = None
        self.root = tk.Tk()
        self.root.title("Countdown Timer")

        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack(pady=5)

        self.countdown_label = tk.Label(self.root, text="")
        self.countdown_label.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_countdown)
        self.reset_button.pack(pady=5)

        self.load_last_duration()

    def start_countdown(self) -> None:
        try:
            duration = int(self.duration_entry.get())
            self.timer = CountdownTimer(duration)
            self.timer.start_timer()
            self.update_display()
            self.timer.save_duration()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer.")

    def reset_countdown(self) -> None:
        if self.timer:
            self.timer.reset_timer()
            self.countdown_label.config(text="")
            self.duration_entry.delete(0, tk.END)

    def update_display(self) -> None:
        if self.timer and self.timer.remaining_time >= 0:
            self.countdown_label.config(text=str(self.timer.remaining_time))
            self.root.after(1000, self.update_display)

    def load_last_duration(self) -> None:
        last_duration = CountdownTimer(0).load_duration()
        if last_duration > 0:
            self.duration_entry.insert(0, str(last_duration))

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()