import random
import pygame

class Maze:
    def __init__(self):
        self.walls = []
        self.treasure_location = (0, 0)

    def generate_maze(self):
        # Simple maze generation logic
        self.walls = [(x, y) for x in range(20) for y in range(15) if random.choice([True, False])]
        self.treasure_location = (random.randint(0, 19), random.randint(0, 14))

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (255, 0, 0), (wall[0] * 40, wall[1] * 40, 40, 40))
        pygame.draw.rect(screen, (255, 255, 0), (self.treasure_location[0] * 40, self.treasure_location[1] * 40, 40, 40))