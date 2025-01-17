import tkinter as tk
from tkinter import messagebox
from CountdownTimer import CountdownTimer

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Countdown Timer")
        self.timer = None
        self.create_widgets()

    def create_widgets(self) -> None:
        self.label = tk.Label(self.root, text="Enter countdown time in seconds:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_countdown)
        self.reset_button.pack()

        self.time_display = tk.Label(self.root, text="")
        self.time_display.pack()

    def start_countdown(self) -> None:
        try:
            duration = int(self.entry.get())
            self.timer = CountdownTimer(duration)
            self.timer.save_setting(duration)
            self.update_display()
            self.timer.start_timer()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer.")

    def reset_countdown(self) -> None:
        if self.timer:
            self.timer.reset_timer()
        self.entry.delete(0, tk.END)
        self.time_display.config(text="")

    def update_display(self) -> None:
        if self.timer:
            remaining = self.timer.remaining_time
            self.time_display.config(text=f"Time remaining: {remaining} seconds")
            if remaining > 0:
                self.root.after(1000, self.update_display)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.run()