import pygame
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy

class Game:
    def __init__(self):
        self.mario = Mario(100, 300)
        self.mushrooms = [Mushroom(150, 0)]
        self.enemies = [Enemy(300, 300)]
        self.score = 0
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mario Game")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.update()
            self.render()
            clock.tick(60)

    def update(self):
        self.mario.update()
        for mushroom in self.mushrooms:
            mushroom.fall()
        for enemy in self.enemies:
            enemy.move()
        self.handle_collisions()

    def render(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white background
        self.mario.draw(self.screen)
        for mushroom in self.mushrooms:
            mushroom.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.flip()

    def handle_collisions(self):
        # Collision detection logic goes here
        pass