import pygame
from player import Player
from block import Block
import random

class Game:
    def __init__(self):
        self.player = Player(300)
        self.blocks = []
        self.score = 0
        self.is_running = True
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Dodge the Falling Blocks")

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.is_running:
            self.update()
            self.draw()
            clock.tick(60)

    def update(self) -> None:
        self.handle_input()
        self.spawn_blocks()
        for block in self.blocks:
            block.fall()
        self.check_collision()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))  # Clear screen with white
        player_pos = self.player.get_position()
        pygame.draw.rect(self.screen, (0, 0, 255), (player_pos[0], player_pos[1], self.player.width, self.player.height))
        for block in self.blocks:
            block_pos = block.get_position()
            pygame.draw.rect(self.screen, (255, 0, 0), (block_pos[0], block_pos[1], 50, 50))
        pygame.display.flip()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move('left')
                if event.key == pygame.K_RIGHT:
                    self.player.move('right')

    def spawn_blocks(self) -> None:
        if random.randint(1, 20) == 1:  # Spawn a block randomly
            new_block = Block(random.randint(0, 550), random.randint(1, 5))
            self.blocks.append(new_block)

    def check_collision(self) -> None:
        player_rect = pygame.Rect(self.player.get_position()[0], self.player.get_position()[1], self.player.width, self.player.height)
        for block in self.blocks:
            block_rect = pygame.Rect(block.get_position()[0], block.get_position()[1], 50, 50)
            if player_rect.colliderect(block_rect):
                self.is_running = False
                self.save_score()

    def save_score(self) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')