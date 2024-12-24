import pygame

class Timer:
    def __init__(self):
        self.time_left = 0
        self.is_paused = False

    def start_timer(self, duration: int):
        self.time_left = duration
        self.is_paused = False

    def pause_timer(self):
        self.is_paused = True

    def resume_timer(self):
        self.is_paused = False

    def check_time(self) -> bool:
        return self.time_left > 0 and not self.is_paused

    def update_timer(self):
        if not self.is_paused and self.time_left > 0:
            self.time_left -= 1  # Decrease time left by 1 second

    def alert_time(self) -> bool:
        return self.time_left <= 10  # Alert if time left is 10 seconds or less

    def display_timer(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time Left: {self.time_left}", True, (0, 0, 0))
        screen.blit(timer_text, (650, 10))  # Display timer at the top right corner