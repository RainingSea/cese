import time

class CountdownTimer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration

    def start_timer(self) -> None:
        while self.remaining_time > 0:
            time.sleep(1)
            self.remaining_time -= 1

    def reset_timer(self) -> None:
        self.remaining_time = self.duration

    def load_settings(self) -> list:
        try:
            with open('countdowns.txt', 'r') as file:
                settings = [int(line.strip()) for line in file.readlines()]
            return settings
        except FileNotFoundError:
            return []

    def save_setting(self, duration: int) -> None:
        with open('countdowns.txt', 'a') as file:
            file.write(f"{duration}\n")