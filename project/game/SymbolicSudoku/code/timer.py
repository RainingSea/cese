import pygame

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def get_time(self) -> str:
        seconds = self.elapsed_time / 1000
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"