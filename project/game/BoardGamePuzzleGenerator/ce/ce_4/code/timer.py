import time

class Timer:
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> float:
        self.end_time = time.time()
        return self.end_time - self.start_time