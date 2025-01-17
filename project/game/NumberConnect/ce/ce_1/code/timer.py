import pygame

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int) -> None:
        """Starts the timer with a given duration in seconds."""
        self.time_remaining = duration

    def update_timer(self) -> None:
        """Updates the timer, reducing the time remaining by the elapsed time."""
        if self.time_remaining > 0:
            self.time_remaining -= 1 / 60  # Assuming 60 FPS

    def is_time_up(self) -> bool:
        """Checks if the time is up."""
        return self.time_remaining <= 0