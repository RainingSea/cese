import pygame
import random
import time

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()
        self.score = Score()
        self.levels = self.load_levels()

    def run(self):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Maze Runner")
        clock = pygame.time.Clock()
        self.timer.start()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move("left")
            if keys[pygame.K_RIGHT]:
                self.player.move("right")
            if keys[pygame.K_UP]:
                self.player.move("up")
            if keys[pygame.K_DOWN]:
                self.player.move("down")

            self.maze.draw(screen)
            self.player.collect_star()
            self.score.update_score(self.player.stars_collected, self.timer.get_elapsed_time(), self.player.moves)
            pygame.display.flip()
            clock.tick(60)

    def load_levels(self):
        with open('levels.txt', 'r') as f:
            levels = [line.strip() for line in f.readlines()]
        return levels

    def track_progress(self):
        with open('progress.txt', 'a') as f:
            f.write(f"Level completed: {self.player.level}\n")

class Maze:
    def __init__(self):
        self.layout = []

    def generate_maze(self, level: int):
        # Simple maze generation logic for demo purposes
        self.layout = [[random.randint(0, 1) for _ in range(20)] for _ in range(20)]

    def draw(self, screen):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                color = (255, 255, 255) if cell == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * 30, y * 30, 30, 30))

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.moves = 0
        self.stars_collected = 0
        self.level = 1

    def move(self, direction: str):
        if direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        elif direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1
        self.moves += 1

    def collect_star(self):
        # Logic to collect stars (not implemented for demo)
        pass

class Timer:
    def __init__(self):
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time

class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, stars_collected: int, time: float, moves: int) -> None:
        self.points += stars_collected * 10 - moves - int(time)