import time

class Timer:
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0

    def start(self):
        self.start_time = time.time()  # Record start time

    def stop(self) -> float:
        self.end_time = time.time()  # Record end time
        return self.get_time()

    def get_time(self) -> float:
        return self.end_time - self.start_time  # Return tracked time