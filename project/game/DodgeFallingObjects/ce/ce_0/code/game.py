import pygame
from player import Player
from block import Block
import random

class Game:
    def __init__(self):
        self.player = Player(375)
        self.blocks = []
        self.score = 0
        self.is_running = True
        self.clock = pygame.time.Clock()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dodge the Falling Blocks")
        
        while self.is_running:
            self.update()
            self.display_score(screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('left')
        if keys[pygame.K_RIGHT]:
            self.player.move('right')

        if random.randint(1, 20) == 1:
            new_block = Block(random.randint(0, 750), random.randint(1, 5))
            self.blocks.append(new_block)

        for block in self.blocks:
            block.fall()
            if block.y_position > 600:
                self.blocks.remove(block)
                self.score += 1

        self.check_collisions()

    def check_collisions(self) -> bool:
        for block in self.blocks:
            if (self.player.x_position < block.x_position + 50 and
                self.player.x_position + self.player.width > block.x_position and
                550 < block.y_position + 50):
                self.game_over()

    def display_score(self, screen):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def game_over(self):
        self.is_running = False
        with open('scores.txt', 'a') as score_file:
            score_file.write(f'score: {self.score}\n')