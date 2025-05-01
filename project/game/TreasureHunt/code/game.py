import pygame
import random

class Game:
    def __init__(self):
        self.player = Player()
        self.maze = Maze()
        self.timer = Timer()
        self.score = Score()

    def start_game(self):
        self.maze.generate_maze()
        self.timer.start()
        self.score.load_best_time()
        self.main_loop()

    def main_loop(self):
        running = True
        while running:
            self.update()
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move("right")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move("up")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move("down")
        
        self.timer.elapsed_time += pygame.time.Clock().tick(60) / 1000  # Update elapsed time
        if self.timer.is_time_up():
            self.restart()

        if self.player.find_treasure(self.maze):
            self.score.update_score()
            self.score.update_best_time(self.timer.elapsed_time)
            self.next_level()

    def render(self):
        self.maze.draw_maze()
        # Additional rendering logic can be added here

    def restart(self):
        self.maze = Maze()  # Regenerate maze
        self.player = Player()  # Reset player position
        self.timer.start()  # Restart timer
        self.score.load_best_time()  # Reload best time

    def next_level(self):
        self.maze = Maze()  # Generate a new maze for the next level
        self.player = Player()  # Reset player position
        self.timer.start()  # Restart timer
        self.score.load_best_time()  # Reload best time

class Player:
    def __init__(self):
        self.position = (1, 1)

    def move(self, direction: str):
        if direction == "left":
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == "up":
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == "down":
            self.position = (self.position[0], self.position[1] + 1)

    def find_treasure(self, maze):
        return self.position == maze.treasure_location

class Maze:
    def __init__(self):
        self.layout = []
        self.treasure_location = (random.randint(0, 9), random.randint(0, 9))

    def generate_maze(self):
        self.layout = [[random.choice([' ', '#']) for _ in range(10)] for _ in range(10)]
        # Ensure the treasure is placed in a valid location
        self.layout[self.treasure_location[1]][self.treasure_location[0]] = 'T'

    def draw_maze(self):
        for row in self.layout:
            print(''.join(row))  # For demonstration purposes

class Timer:
    def __init__(self):
        self.time_limit = 60
        self.elapsed_time = 0

    def start(self):
        self.elapsed_time = 0

    def is_time_up(self):
        return self.elapsed_time >= self.time_limit

class Score:
    def __init__(self):
        self.current_score = 0
        self.best_time = float('inf')

    def update_score(self):
        self.current_score += 1

    def load_best_time(self):
        try:
            with open('best_time.txt', 'r') as file:
                self.best_time = float(file.readline().strip())
        except FileNotFoundError:
            self.best_time = float('inf')

    def save_best_time(self):
        with open('best_time.txt', 'w') as file:
            file.write(str(self.best_time))

    def save_score(self, player_name):
        with open('scores.txt', 'a') as file:
            file.write(f'{player_name}|{self.current_score}\n')

    def update_best_time(self, new_time):
        if new_time < self.best_time:
            self.best_time = new_time
            self.save_best_time()