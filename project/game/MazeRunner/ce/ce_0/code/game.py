import pygame
from player import Player
from maze import Maze
from star import Star

class Game:
    def __init__(self):
        self.player = Player()
        self.maze = Maze()
        self.stars = []
        self.score = 0
        self.timer = 0.0

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.update()
            self.render()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        if keys[pygame.K_RIGHT]:
            self.player.move("right")
        if keys[pygame.K_UP]:
            self.player.move("up")
        if keys[pygame.K_DOWN]:
            self.player.move("down")
        self.timer += 1 / 60  # Increment timer

    def render(self):
        # Rendering logic here
        pass