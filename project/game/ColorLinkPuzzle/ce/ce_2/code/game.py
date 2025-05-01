import pygame
import random

class Block:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def is_connected(self, other):
        return abs(self.position[0] - other.position[0]) + abs(self.position[1] - other.position[1]) == 1

class Grid:
    def __init__(self, width, height):
        self.blocks = [[Block(self.random_color(), (x, y)) for y in range(height)] for x in range(width)]

    def random_color(self):
        return random.choice(['red', 'green', 'blue', 'yellow', 'purple'])

    def draw(self, screen):
        for row in self.blocks:
            for block in row:
                pygame.draw.rect(screen, block.color, (block.position[0] * 30, block.position[1] * 30, 30, 30))

    def check_connection(self, start, end):
        return start.is_connected(end)

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points):
        self.points += points

    def get_score(self):
        return self.points

class Game:
    def __init__(self):
        self.grid = Grid(10, 10)
        self.score = Score()
        self.screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption("Block Clearing Game")

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))
            self.grid.draw(self.screen)
            pygame.display.flip()

    def clear_blocks(self):
        # Logic to clear blocks would go here
        pass

    def update_score(self, points):
        self.score.add_points(points)