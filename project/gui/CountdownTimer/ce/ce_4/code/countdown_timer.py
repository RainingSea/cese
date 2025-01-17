import time
import os

class CountdownTimer:
    def __init__(self, duration: int):
        self.duration = duration
        self.remaining_time = duration
        self.is_running = False

    def start_timer(self):
        self.is_running = True
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            self.remaining_time -= 1

    def reset_timer(self):
        self.remaining_time = self.duration
        self.is_running = False

    def update_time(self):
        return self.remaining_time

    def save_settings(self):
        with open('countdown_settings.txt', 'a') as file:
            file.write(f"{self.duration}\n")

    def load_settings(self):
        if os.path.exists('countdown_settings.txt'):
            with open('countdown_settings.txt', 'r') as file:
                durations = file.readlines()
                return [int(duration.strip()) for duration in durations]
        return []