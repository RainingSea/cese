import time

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> float:
        return time.time() - self.start_time

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time