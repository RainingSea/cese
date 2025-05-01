import time

class Timer:
    def __init__(self):
        self.time_limit = 60  # 60 seconds
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def update(self):
        self.elapsed_time = int(time.time() - self.start_time)

    def is_time_up(self):
        return self.elapsed_time >= self.time_limit