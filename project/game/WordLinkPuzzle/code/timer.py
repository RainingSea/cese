import time

class Timer:
    def __init__(self):
        self.time_left = 0
        self.start_time = None

    def start_timer(self, duration: int):
        self.time_left = duration
        self.start_time = time.time()

    def update_timer(self):
        if self.time_left > 0:
            elapsed_time = int(time.time() - self.start_time)
            self.time_left = max(0, self.time_left - elapsed_time)
            self.start_time = time.time()  # Reset start time for next update

    def is_time_up(self) -> bool:
        return self.time_left <= 0