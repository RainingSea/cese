import pygame
from pygame.locals import *
from typing import List, Tuple
from tracks import Track
from player import Player
from score_manager import ScoreManager

class Game:
    def __init__(self):
        self.current_track = Track()
        self.player = Player()
        self.score_manager = ScoreManager()
        self.running = True
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Drift Rivals")

    def start(self) -> None:
        self.current_track.load_from_file("tracks.txt")
        while self.running:
            self.handle_input()
            self.update()
            self.render()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                else:
                    self.player.control(pygame.key.name(event.key))

    def update(self) -> None:
        self.player.calculate_score()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))  # Clear screen with white
        self.current_track.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()