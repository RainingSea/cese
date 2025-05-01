import pygame
from player import Player
from block import Block
from score import Score
import random

class Game:
    def __init__(self):
        self.player = Player()
        self.blocks = []
        self.score = 0
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Falling Blocks Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def start(self):
        while self.running:
            self.update()
            self.check_collision()
            self.draw()
            self.clock.tick(60)

    def update(self):
        self.player.move()
        if random.randint(1, 20) == 1:  # Randomly generate blocks
            self.blocks.append(Block(random.randint(0, 750), 0))
        for block in self.blocks:
            block.fall()
            if block.position_y > 600:
                self.blocks.remove(block)

    def check_collision(self):
        for block in self.blocks:
            if (self.player.position_x < block.position_x + block.width and
                self.player.position_x + self.player.width > block.position_x and
                block.position_y + block.height > 550):  # Assuming player is at y=550
                self.running = False
                self.save_score()

    def save_score(self):
        score_handler = Score()
        score_handler.write_score(self.score)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)
        for block in self.blocks:
            block.draw(self.screen)
        pygame.display.flip()