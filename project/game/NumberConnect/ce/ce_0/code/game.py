import pygame
import time

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int):
        self.time_remaining = duration

    def update_time(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self) -> bool:
        return self.time_remaining <= 0

class Grid:
    def __init__(self):
        self.tiles = []
        self.size = 0

    def initialize_grid(self, size: int):
        self.size = size
        self.tiles = [[i + j * size for i in range(size)] for j in range(size)]

    def draw_grid(self, screen):
        tile_size = 50
        for row in range(self.size):
            for col in range(self.size):
                number = self.tiles[row][col]
                pygame.draw.rect(screen, (255, 255, 255), (col * tile_size, row * tile_size, tile_size, tile_size))
                font = pygame.font.Font(None, 36)
                text = font.render(str(number), True, (0, 0, 0))
                screen.blit(text, (col * tile_size + tile_size // 4, row * tile_size + tile_size // 4))

    def is_valid_move(self, current_pos: tuple, next_pos: tuple) -> bool:
        current_row, current_col = current_pos
        next_row, next_col = next_pos
        return (0 <= next_row < self.size and 
                0 <= next_col < self.size and 
                (abs(current_row - next_row) + abs(current_col - next_col) == 1))

class ScoreManager:
    def __init__(self):
        self.scores = {}

    def load_scores(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    player, score = line.strip().split('|')
                    self.scores[player] = int(score)
        except FileNotFoundError:
            print("Score file not found, starting with empty scores.")

    def save_score(self, player: str, score: int):
        self.scores[player] = score
        with open('scores.txt', 'w') as file:
            for player, score in self.scores.items():
                file.write(f"{player}|{score}\n")

    def get_high_scores(self) -> list:
        return sorted(self.scores.items(), key=lambda item: item[1], reverse=True)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.score_manager = ScoreManager()

    def start_game(self, level: int):
        self.grid.initialize_grid(level)
        self.timer.start_timer(60)  # 60 seconds for the game
        self.score_manager.load_scores('scores.txt')

    def check_move(self, current_pos: tuple, next_pos: tuple) -> bool:
        return self.grid.is_valid_move(current_pos, next_pos)

    def update_timer(self):
        self.timer.update_time()

    def end_game(self):
        # Logic to end the game and save score
        pass