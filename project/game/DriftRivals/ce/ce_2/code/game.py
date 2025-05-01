import pygame
from player import Player
from track import Track
from score import Score

class Game:
    def __init__(self):
        self.player = Player("Player1")
        self.tracks = [Track(1, "Easy"), Track(2, "Medium"), Track(3, "Hard")]
        self.score = Score()

    def start_game(self):
        # Initialize game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Handle other events like key presses for drifting

            # Update game state and render graphics here

        self.score.save_score(self.player.name, self.player.score)
    
    def update_score(self):
        # Update the player's score based on drift performance
        points = 100  # Example points for drifting
        self.player.update_score(points)