import pygame
from player import Player
from wall import Wall
from pellet import Pellet
from super_pellet import SuperPellet
from ghost import Ghost
from monster import Monster

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.player = Player(100, 100)
        self.walls = [Wall(50, 50), Wall(200, 50)]
        self.pellets = [Pellet(150, 150)]
        self.superpellets = [SuperPellet(300, 300)]
        self.ghosts = [Ghost(400, 400)]
        self.monster = Monster(500, 500)
        self.game_ticks = 0

    def run(self):
        running = True
        while running:
            self.handle_input()
            self.update()
            self.draw()
            self.check_collisions()
            pygame.display.flip()
            self.game_ticks += 1

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move('left')
                elif event.key == pygame.K_RIGHT:
                    self.player.move('right')
                elif event.key == pygame.K_UP:
                    self.player.move('up')
                elif event.key == pygame.K_DOWN:
                    self.player.move('down')

    def update(self):
        self.monster.chase(self.player)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for wall in self.walls:
            wall.draw(self.screen)
        for pellet in self.pellets:
            pellet.draw(self.screen)
        for superpellet in self.superpellets:
            superpellet.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        self.player.draw(self.screen)
        self.monster.draw(self.screen)

    def check_collisions(self):
        # Collision detection logic here
        pass