import pygame
from player import Player
from monster import Monster
from wall import Wall
from pellet import Pellet

class Game:
    def __init__(self):
        self.player = Player(100, 100)
        self.monster = Monster(200, 200)
        self.walls = [Wall(50, 50), Wall(150, 150)]
        self.pellets = [Pellet(300, 300, False), Pellet(400, 400, True)]
        self.score = 0
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ghostly Game")
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

    def update(self):
        self.monster.chase(self.player)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.monster.draw(self.screen)
        for wall in self.walls:
            wall.draw(self.screen)
        for pellet in self.pellets:
            pellet.draw(self.screen)
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move("up")
                elif event.key == pygame.K_DOWN:
                    self.player.move("down")
                elif event.key == pygame.K_LEFT:
                    self.player.move("left")
                elif event.key == pygame.K_RIGHT:
                    self.player.move("right")