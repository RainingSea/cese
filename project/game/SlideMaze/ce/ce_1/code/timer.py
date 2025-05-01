import time

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self) -> None:
        self.start_time = time.time()

    def elapsed_time(self) -> float:
        return time.time() - self.start_time