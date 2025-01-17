import pygame

class Track:
    def __init__(self):
        self.track_data = {}

    def load_track(self, track_id):
        # Placeholder for loading track data
        pass

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (100, 100, 600, 400))