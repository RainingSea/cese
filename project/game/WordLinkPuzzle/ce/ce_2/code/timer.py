import time

class Timer:
    def __init__(self):
        self.duration = 60  # Default duration in seconds
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def get_time(self) -> int:
        if self.start_time is None:
            return self.duration
        elapsed_time = time.time() - self.start_time
        remaining_time = self.duration - int(elapsed_time)
        return max(0, remaining_time)