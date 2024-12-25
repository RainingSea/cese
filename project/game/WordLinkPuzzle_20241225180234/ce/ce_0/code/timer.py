import pygame

class Timer:
    def __init__(self):
        self.time_left = 0
        self.running = False
        self.start_ticks = 0  # To track the start time for countdown

    def start_timer(self, duration: int):
        """Starts the timer with the given duration in seconds."""
        self.time_left = duration
        self.running = True
        self.start_ticks = pygame.time.get_ticks()  # Record the start time

    def pause_timer(self):
        """Pauses the timer."""
        self.running = False

    def check_time(self) -> bool:
        """Checks if the time is up and updates the time left."""
        if self.running:
            elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000  # Convert milliseconds to seconds
            self.time_left = max(0, self.time_left - elapsed_time)  # Update time left
            self.start_ticks = pygame.time.get_ticks()  # Reset start time for the next check
            if self.time_left <= 0:
                self.running = False
                return True
        return False