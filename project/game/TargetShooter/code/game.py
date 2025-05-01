import pygame
import random
from pygame.locals import *
from leaderboard import Leaderboard
from target_manager import TargetManager
from score_manager import ScoreManager
from timer import Timer
from shooter import Shooter

class Game:
    def __init__(self):
        self.shooter = Shooter()
        self.target_manager = TargetManager()
        self.score_manager = ScoreManager()
        self.leaderboard = Leaderboard()
        self.timer = Timer()
        self.difficulty = self.load_difficulty()
        self.set_difficulty_parameters()
        self.time_limit = 60  # seconds
        self.timer.start_timer(self.time_limit)  # Start the timer

    def load_difficulty(self) -> str:
        try:
            with open('settings.txt', 'r') as f:
                for line in f:
                    if line.startswith('difficulty'):
                        return line.split('|')[1].strip()
        except FileNotFoundError:
            return 'medium'  # Default difficulty

    def set_difficulty_parameters(self) -> None:
        if self.difficulty == 'easy':
            self.target_manager.set_target_speed(2)
        elif self.difficulty == 'hard':
            self.target_manager.set_target_speed(5)
        else:  # medium
            self.target_manager.set_target_speed(3)

    def start_game(self) -> None:
        while True:
            self.update()
            self.render()
            if self.check_game_over():
                self.handle_game_over()
                break

    def restart_game(self) -> None:
        pygame.quit()  # Quit the current Pygame instance
        pygame.init()  # Reinitialize Pygame
        pygame.font.init()  # Ensure font is initialized
        self.__init__()  # Reset the game state

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                self.shooter.aim(pygame.mouse.get_pos())  # Aim at mouse position
                self.shooter.shoot()

        self.target_manager.move_targets()
        self.timer.update_timer()  # Update the timer

    def render(self) -> None:
        # Placeholder for rendering logic
        pass

    def check_game_over(self) -> bool:
        return self.timer.time_remaining <= 0

    def handle_game_over(self) -> None:
        player_name = input("Enter your name: ")
        self.score_manager.save_score(player_name, self.shooter.score)
        self.leaderboard.update_leaderboard(player_name, self.shooter.score)