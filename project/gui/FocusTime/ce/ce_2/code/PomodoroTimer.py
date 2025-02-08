import time
import threading
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, work_duration: int, break_duration: int):
        self.work_duration = work_duration * 60  # convert to seconds
        self.break_duration = break_duration * 60  # convert to seconds
        self.remaining_time = 0
        self.timer_thread = None
        self.is_running = False

    def start_timer(self, is_break: bool):
        self.remaining_time = self.break_duration if is_break else self.work_duration
        self.is_running = True
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()

    def run_timer(self):
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.notify_user()

    def notify_user(self):
        messagebox.showinfo("Pomodoro Timer", "Time's up! Take a break!" if self.remaining_time == 0 else "Break time is over! Back to work!")
        self.is_running = False

    def update_timer(self):
        return self.remaining_time