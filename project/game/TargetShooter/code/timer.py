import pygame

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int) -> None:
        self.time_remaining = duration

    def update_timer(self) -> None:
        if self.time_remaining > 0:
            self.time_remaining -= 1  # Decrement timer by 1 second (simulated)