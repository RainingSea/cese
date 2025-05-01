import pygame
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.score_manager = ScoreManager()
        self.level = 1
        self.difficulty = "medium"
        self.grid_size = 4  # Default grid size

    def start_game(self):
        self.load_config()
        self.grid.initialize_grid(self.grid_size)
        self.timer.start_timer(60)  # 60 seconds timer
        self.score_manager.load_scores()
        self.main_loop()

    def load_config(self):
        with open('config.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                if key == "grid_size":
                    self.grid_size = int(value)
                elif key == "difficulty":
                    self.difficulty = value
        self.set_level(self.level)

    def set_level(self, level):
        if level in [1, 2]:
            self.grid_size = level + 2  # Set grid size based on level
        self.grid.initialize_grid(self.grid_size)

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.handle_move("up")
                    elif event.key == pygame.K_DOWN:
                        self.handle_move("down")
                    elif event.key == pygame.K_LEFT:
                        self.handle_move("left")
                    elif event.key == pygame.K_RIGHT:
                        self.handle_move("right")

            self.update_score()
            self.grid.render()
            self.timer.update_time()
            pygame.display.flip()

            if self.timer.get_remaining_time() <= 0:
                running = False  # End game when time runs out

    def handle_move(self, direction):
        if self.check_move(direction):
            self.update_grid(direction)

    def check_move(self, direction):
        current_position = self.grid.get_empty_tile_position()
        if direction == "up":
            return current_position[0] > 0
        elif direction == "down":
            return current_position[0] < self.grid_size - 1
        elif direction == "left":
            return current_position[1] > 0
        elif direction == "right":
            return current_position[1] < self.grid_size - 1
        return False

    def update_grid(self, direction):
        current_position = self.grid.get_empty_tile_position()
        if direction == "up":
            self.grid.swap_tiles(current_position, (current_position[0] - 1, current_position[1]))
        elif direction == "down":
            self.grid.swap_tiles(current_position, (current_position[0] + 1, current_position[1]))
        elif direction == "left":
            self.grid.swap_tiles(current_position, (current_position[0], current_position[1] - 1))
        elif direction == "right":
            self.grid.swap_tiles(current_position, (current_position[0], current_position[1] + 1))

    def update_score(self):
        # Update the player's score based on the current game progress
        pass  # Placeholder for actual score update logic

class Grid:
    def __init__(self):
        self.tiles = []
        self.size = 0

    def initialize_grid(self, size):
        self.size = size
        self.tiles = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]
        self.tiles[size - 1][size - 1] = 0  # Set the last tile as empty

    def render(self):
        screen = pygame.display.set_mode((400, 400))  # Example screen size
        screen.fill((255, 255, 255))  # Fill background with white
        tile_size = 100  # Example tile size
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                pygame.draw.rect(screen, (0, 0, 0), (j * tile_size, i * tile_size, tile_size, tile_size), 1)
                font = pygame.font.Font(None, 36)
                text = font.render(str(tile), True, (0, 0, 0))
                screen.blit(text, (j * tile_size + 35, i * tile_size + 35))

    def get_empty_tile_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j] == 0:
                    return (i, j)

    def swap_tiles(self, pos1, pos2):
        self.tiles[pos1[0]][pos1[1]], self.tiles[pos2[0]][pos2[1]] = self.tiles[pos2[0]][pos2[1]], self.tiles[pos1[0]][pos1[1]]

class Timer:
    def __init__(self):
        self.start_time = 0
        self.duration = 0

    def start_timer(self, duration):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def get_remaining_time(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds
        remaining_time = self.duration - elapsed_time
        return max(remaining_time, 0)

    def update_time(self):
        # This function can be used to update any time-related UI elements if needed
        pass

class ScoreManager:
    def __init__(self):
        self.scores = {}

    def load_scores(self):
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    player_name, score, level, last_played, best_score = line.strip().split(':')
                    self.scores[player_name] = {
                        'score': int(score),
                        'level': int(level),
                        'last_played': last_played,
                        'best_score': int(best_score)
                    }
        except FileNotFoundError:
            print("Scores file not found. Starting with empty scores.")

    def save_score(self, player_name, score):
        self.scores[player_name] = score
        with open('scores.txt', 'a') as file:
            file.write(f"{player_name}:{score}:1:2023-10-01:0\n")  # Example data format