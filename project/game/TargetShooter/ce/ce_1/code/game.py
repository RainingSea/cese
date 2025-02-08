import pygame
from shooter import Shooter
from target import Target
from score import Score

class Game:
    def __init__(self):
        self.score = 0
        self.time_remaining = 60  # game duration in seconds
        self.targets = []
        self.shooter = Shooter(400, 300)  # Initial shooter position
        self.load_leaderboard()

    def start_game(self) -> None:
        # Initialize game state and start the game loop
        pass

    def update(self) -> None:
        for target in self.targets:
            target.move()
            # Check for collisions and update score
            pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((255, 255, 255))  # Clear screen with white background
        for target in self.targets:
            target.draw(screen)
        # Draw shooter and score
        pass

    def restart_game(self) -> None:
        self.score = 0
        self.targets.clear()
        self.start_game()

    def load_leaderboard(self) -> list:
        leaderboard = []
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split('|')
                    leaderboard.append(Score(name, int(score)))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return leaderboard

    def save_score(self, name: str, score: int) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f"{name}|{score}\n")