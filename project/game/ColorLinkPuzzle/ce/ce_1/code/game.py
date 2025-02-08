import pygame
import random

class Grid:
    def __init__(self):
        self.blocks = []
        self.initialize_grid()

    def initialize_grid(self):
        self.blocks = [[random.choice(['red', 'green', 'blue', 'yellow']) for _ in range(8)] for _ in range(8)]

    def draw_grid(self, screen):
        block_size = 50
        for x in range(len(self.blocks)):
            for y in range(len(self.blocks[x])):
                color = self.blocks[x][y]
                pygame.draw.rect(screen, color, (y * block_size, x * block_size, block_size, block_size))

    def check_connection(self, start, end):
        # Simplified connection check for demo purposes
        return self.blocks[start[0]][start[1]] == self.blocks[end[0]][end[1]]

    def clear_connected_blocks(self, start):
        color = self.blocks[start[0]][start[1]]
        connected = [(start[0], start[1])]
        self._find_connected_blocks(start[0], start[1], color, connected)
        for block in connected:
            self.blocks[block[0]][block[1]] = None
        return connected

    def _find_connected_blocks(self, x, y, color, connected):
        if x < 0 or x >= len(self.blocks) or y < 0 or y >= len(self.blocks[0]):
            return
        if (x, y) in connected or self.blocks[x][y] != color:
            return
        connected.append((x, y))
        self._find_connected_blocks(x + 1, y, color, connected)
        self._find_connected_blocks(x - 1, y, color, connected)
        self._find_connected_blocks(x, y + 1, color, connected)
        self._find_connected_blocks(x, y - 1, color, connected)

class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points):
        self.current_score += points

    def get_score(self):
        return self.current_score

class Level:
    def __init__(self):
        self.difficulty = 1

    def increase_level(self):
        self.difficulty += 1

    def get_difficulty(self):
        return self.difficulty

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.level = Level()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Color Link Puzzle")

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.grid.draw_grid(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[1] // 50
            y = pos[0] // 50
            # Logic to handle block selection and connection can be added here

    def clear_blocks(self, blocks):
        for block in blocks:
            self.grid.blocks[block[0]][block[1]] = None