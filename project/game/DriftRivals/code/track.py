import pygame

class Track:
    def __init__(self):
        self.layout = []

    def load(self, track_name: str) -> None:
        try:
            with open('tracks.txt', 'r') as file:
                for line in file:
                    name, layout = line.strip().split('|')
                    if name == track_name:
                        self.layout = layout.split('|')  # Assuming layout is defined with '|'
        except FileNotFoundError:
            print("Track file not found.")

    def render(self, screen) -> None:
        for segment in self.layout:
            x, y = map(int, segment.split('|'))
            pygame.draw.rect(screen, (0, 255, 0), (x, y, 100, 10))