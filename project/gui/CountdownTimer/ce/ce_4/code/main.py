import tkinter as tk
from tkinter import messagebox
from countdown_timer import CountdownTimer

class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Countdown Timer")
        self.create_widgets()
        self.timer = None

    def create_widgets(self):
        self.duration_entry = tk.Entry(self.window)
        self.duration_entry.pack(pady=10)

        self.start_button = tk.Button(self.window, text="Start", command=self.start_countdown)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_countdown)
        self.reset_button.pack(pady=5)

        self.time_label = tk.Label(self.window, text="Remaining Time: 0")
        self.time_label.pack(pady=10)

    def start_countdown(self):
        try:
            duration = int(self.duration_entry.get())
            self.timer = CountdownTimer(duration)
            self.timer.save_settings()
            self.update_time()
            self.timer.start_timer()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def reset_countdown(self):
        if self.timer:
            self.timer.reset_timer()
            self.time_label.config(text="Remaining Time: 0")
            self.duration_entry.delete(0, tk.END)

    def update_time(self):
        if self.timer and self.timer.is_running:
            remaining_time = self.timer.update_time()
            self.time_label.config(text=f"Remaining Time: {remaining_time}")
            self.window.after(1000, self.update_time)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = UI()
    app.run()