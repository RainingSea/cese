import pygame
import random

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.paths = []
        self.treasure_location = None
        self.generate_maze()

    def generate_maze(self):
        # Simple maze generation logic (random for demo purposes)
        for x in range(self.width):
            for y in range(self.height):
                if random.choice([True, False]):
                    self.walls.append((x, y))
                else:
                    self.paths.append((x, y))
        self.treasure_location = random.choice(self.paths)

    def draw_maze(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), (wall[0]*20, wall[1]*20, 20, 20))
        for path in self.paths:
            pygame.draw.rect(screen, (255, 255, 255), (path[0]*20, path[1]*20, 20, 20))
        if self.treasure_location:
            pygame.draw.rect(screen, (255, 0, 0), (self.treasure_location[0]*20, self.treasure_location[1]*20, 20, 20))

class Player:
    def __init__(self, start_position):
        self.position = start_position

    def move(self, direction):
        if direction == 'UP':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'DOWN':
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == 'LEFT':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'RIGHT':
            self.position = (self.position[0] + 1, self.position[1])

    def check_treasure(self, treasure_location):
        return self.position == treasure_location

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def get_time(self):
        self.elapsed_time = pygame.time.get_ticks() - self.start_time
        return self.elapsed_time / 1000.0  # return in seconds

    def reset(self):
        self.start()

class Score:
    def __init__(self):
        self.current_score = 0
        self.best_time = float('inf')

    def increase_score(self):
        self.current_score += 1

    def save_best_time(self, time):
        if time < self.best_time:
            self.best_time = time
            with open('best_time.txt', 'w') as f:
                f.write(str(self.best_time))

class Game:
    def __init__(self):
        self.maze = Maze(10, 10)
        self.player = Player((0, 0))
        self.timer = Timer()
        self.score = Score()

    def start_game(self):
        self.timer.start()

    def update(self):
        # Game update logic goes here
        pass

    def render(self, screen):
        self.maze.draw_maze(screen)
        # Draw player and other UI elements here

    def restart_game(self):
        self.maze = Maze(10, 10)
        self.player = Player((0, 0))
        self.timer.reset()
        self.score.current_score = 0