import tkinter as tk
import time
import threading

class Timer:
    def __init__(self, duration: int):
        self.duration = duration
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self.run_timer).start()

    def run_timer(self):
        time.sleep(self.duration)
        if self.is_running:
            self.notify()

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False

    def notify(self):
        print("Time's up!")

class FocusTimeApp:
    def __init__(self):
        self.work_duration = 25 * 60  # Default work duration in seconds
        self.break_duration = 5 * 60   # Default break duration in seconds
        self.timer = None
        self.load_settings()

        self.window = tk.Tk()
        self.window.title("FocusTime")

        self.work_label = tk.Label(self.window, text="Work Duration (minutes):")
        self.work_label.pack()
        self.work_entry = tk.Entry(self.window)
        self.work_entry.pack()
        self.work_entry.insert(0, str(self.work_duration // 60))

        self.break_label = tk.Label(self.window, text="Break Duration (minutes):")
        self.break_label.pack()
        self.break_entry = tk.Entry(self.window)
        self.break_entry.pack()
        self.break_entry.insert(0, str(self.break_duration // 60))

        self.start_button = tk.Button(self.window, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = tk.Button(self.window, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

        self.window.mainloop()

    def start_timer(self):
        work_minutes = int(self.work_entry.get())
        self.work_duration = work_minutes * 60
        self.timer = Timer(self.work_duration)
        self.timer.start()

    def pause_timer(self):
        if self.timer:
            self.timer.pause()

    def reset_timer(self):
        if self.timer:
            self.timer.reset()

    def load_settings(self):
        try:
            with open("settings.txt", "r") as file:
                settings = file.readlines()
                if settings:
                    self.work_duration = int(settings[0].strip()) * 60
                    self.break_duration = int(settings[1].strip()) * 60
        except FileNotFoundError:
            pass

    def save_settings(self):
        with open("settings.txt", "w") as file:
            file.write(f"{self.work_duration // 60}\n")
            file.write(f"{self.break_duration // 60}\n")

if __name__ == "__main__":
    app = FocusTimeApp()