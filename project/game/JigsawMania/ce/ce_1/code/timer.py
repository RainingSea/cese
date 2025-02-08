import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.elapsed_time = int(time.time() - self.start_time)

    def get_elapsed_time(self):
        return self.elapsed_time