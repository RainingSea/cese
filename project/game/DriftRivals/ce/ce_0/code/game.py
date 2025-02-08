import pygame
from track import Track
from scoreboard import Scoreboard

class Game:
    def __init__(self):
        self.pygame_instance = pygame
        self.tracks = []
        self.scoreboard = Scoreboard()
        self.load_tracks()

    def load_tracks(self):
        with open('tracks.txt', 'r') as file:
            for line in file:
                name, path = line.strip().split('|')
                path_points = [tuple(map(int, point.split(','))) for point in path.split(';')]
                self.tracks.append(Track(name, path_points))

    def run(self):
        running = True
        while running:
            self.update()
            self.render()
            for event in self.pygame_instance.event.get():
                if event.type == self.pygame_instance.QUIT:
                    running = False

    def update(self):
        # Update game state logic here
        pass

    def render(self):
        # Render game graphics here
        pass