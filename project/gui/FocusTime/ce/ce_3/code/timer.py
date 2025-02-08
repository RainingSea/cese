import time
import threading

class Timer:
    def __init__(self, duration: int):
        self.duration = duration
        self.thread = None
        self.is_running = False

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._run_timer)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()

    def _run_timer(self):
        for remaining in range(self.duration, 0, -1):
            if not self.is_running:
                break
            time.sleep(1)
        if self.is_running:
            self.is_running = False
            print("Timer completed!")