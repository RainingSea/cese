import tkinter as tk
import time
import threading

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self._running = False

    def start(self):
        self._running = True
        threading.Thread(target=self._run_timer).start()

    def stop(self):
        self._running = False

    def _run_timer(self):
        time.sleep(self.duration)
        if self._running:
            self.notify()

    def notify(self):
        print("Time's up!")

class FocusTimeApp:
    def __init__(self):
        self.work_duration = 25 * 60  # Default work duration in seconds
        self.break_duration = 5 * 60   # Default break duration in seconds
        self.timer = None
        self.root = tk.Tk()
        self.root.title("FocusTime")

        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        self.work_label = tk.Label(self.root, text="Work Duration (minutes):")
        self.work_label.pack()

        self.work_entry = tk.Entry(self.root)
        self.work_entry.pack()

        self.break_label = tk.Label(self.root, text="Break Duration (minutes):")
        self.break_label.pack()

        self.break_entry = tk.Entry(self.root)
        self.break_entry.pack()

        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Timer", command=self.stop_timer)
        self.stop_button.pack()

        self.status_label = tk.Label(self.root, text="Timer Status: Not Started")
        self.status_label.pack()

    def start_timer(self):
        work_duration = int(self.work_entry.get()) * 60
        break_duration = int(self.break_entry.get()) * 60
        self.timer = Timer(work_duration)
        self.timer.start()
        self.status_label.config(text="Timer Status: Working")
        self.save_settings()

    def stop_timer(self):
        if self.timer:
            self.timer.stop()
        self.status_label.config(text="Timer Status: Stopped")

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as f:
                settings = f.read().strip().split('|')
                self.work_duration = int(settings[0]) * 60
                self.break_duration = int(settings[1]) * 60
                self.work_entry.insert(0, str(self.work_duration // 60))
                self.break_entry.insert(0, str(self.break_duration // 60))
        except FileNotFoundError:
            pass

    def save_settings(self):
        with open('settings.txt', 'w') as f:
            f.write(f"{self.work_duration // 60}|{self.break_duration // 60}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FocusTimeApp()
    app.run()