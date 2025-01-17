import pygame
from mario import Mario
from block import Block
from mushroom import Mushroom
from enemy import Enemy

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.mario = Mario(100, 500)
        self.block = Block(400, 500)
        self.mushroom = Mushroom(450, 450)
        self.enemies = [Enemy(600, 500)]
        self.score = 0
        self.load_score()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.update()
            self.check_collisions()
            self.draw()
            self.clock.tick(60)

    def update(self):
        self.mario.move_left()  # Placeholder for actual input handling
        self.mario.move_right()  # Placeholder for actual input handling
        self.mushroom.fall()

    def check_collisions(self):
        if self.mushroom.check_touch(self.mario):
            self.mario.touch_mushroom()
            self.update_score(100)

        for enemy in self.enemies:
            if enemy.check_touch(self.mario):
                self.mario.touch_enemy()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.mario.draw(self.screen)
        self.block.draw(self.screen)
        self.mushroom.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.flip()

    def update_score(self, points):
        self.score += points
        self.save_score()

    def load_score(self):
        try:
            with open('score.txt', 'r') as file:
                self.score = int(file.read().strip())
        except FileNotFoundError:
            self.score = 0

    def save_score(self):
        with open('score.txt', 'w') as file:
            file.write(str(self.score))