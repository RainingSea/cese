import time

class Timer:
    def __init__(self):
        self.time_left = 0
        self.running = False

    def start_timer(self, duration: int) -> None:
        self.time_left = duration
        self.running = True
        while self.running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1

    def get_time(self) -> int:
        return self.time_left

    def stop_timer(self) -> None:
        self.running = False