import pygame
from mario import Mario
from block import Block
from mushroom import Mushroom
from enemy import Enemy
from score import Score

class Game:
    def __init__(self):
        self.mario = Mario((50, 400))
        self.block = Block((50, 350))
        self.mushroom = Mushroom((50, 320))
        self.enemy = Enemy((200, 400))
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))

    def run(self) -> None:
        running = True
        while running:
            self.handle_input()
            self.update()
            self.draw()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.mario.move_left()
                if event.key == pygame.K_RIGHT:
                    self.mario.move_right()
                if event.key == pygame.K_UP:
                    self.mario.jump()

    def update(self) -> None:
        self.enemy.move()
        if self.enemy.check_collision(self.mario):
            self.mario.touch_enemy()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))  # Clear screen
        # Draw Mario, Block, Enemy, etc. (not implemented)
        pygame.display.flip()

    def save_score(self) -> None:
        self.score.save_to_file()