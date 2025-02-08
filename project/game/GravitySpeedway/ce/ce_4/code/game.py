import pygame
from player import Player
from vehicle import Vehicle
from obstacle import Obstacle
from data_storage import DataStorage

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.vehicles = DataStorage().load_vehicles()
        self.obstacles = self.create_obstacles()
        self.running = True

    def create_obstacles(self):
        return [Obstacle((200, 300), (50, 50)), Obstacle((400, 200), (50, 50))]

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                self.player.move(pygame.key.name(event.key))

    def update(self):
        self.player.update_physics()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        pygame.display.flip()