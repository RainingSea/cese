import pygame
from tracks import Track
from car import Car
from score import Score

class Game:
    def __init__(self):
        self.tracks = []
        self.car = Car("Default Model")
        self.score = Score()
        self.load_tracks()

    def load_tracks(self):
        with open("tracks.txt", "r") as file:
            for line in file:
                track = Track()
                track.load_track(line.strip())
                self.tracks.append(track)

    def start_game(self):
        # Initialize game loop here
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Game controls and logic would go here

    def pause_game(self):
        # Logic for pausing the game
        pass

    def update_score(self, drift_precision: float, speed: float, style: float):
        self.score.calculate_score(drift_precision, speed, style)