import time
import threading
from tkinter import messagebox

class Timer:
    def __init__(self, duration: int):
        self.duration = duration

    def start(self):
        threading.Thread(target=self._run_timer).start()

    def _run_timer(self):
        time.sleep(self.duration)
        self.notify()

    def notify(self):
        messagebox.showinfo("FocusTime", "Time's up! Take a break or continue working.")