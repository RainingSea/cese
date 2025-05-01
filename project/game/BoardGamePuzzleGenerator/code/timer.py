import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def start(self) -> None:
        self.start_time = time.time()  # Start timer

    def stop(self) -> None:
        self.end_time = time.time()

    def get_elapsed_time(self) -> float:
        return self.end_time - self.start_time  # Calculate elapsed time