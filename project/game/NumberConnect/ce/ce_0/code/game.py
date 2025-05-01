import pygame
import random

class Timer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.start_time = None

    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    def get_remaining_time(self):
        if self.start_time is None:
            return self.time_limit
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        return max(0, self.time_limit - elapsed_time)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def update_score(self, points):
        self.score += points

class Grid:
    def __init__(self):
        self.tiles = []

    def generate_grid(self, size):
        self.tiles = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]

    def draw_grid(self, screen):
        tile_size = 50
        for i, row in enumerate(self.tiles):
            for j, value in enumerate(row):
                pygame.draw.rect(screen, (255, 255, 255), (j * tile_size, i * tile_size, tile_size, tile_size))
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, (0, 0, 0))
                screen.blit(text, (j * tile_size + 15, i * tile_size + 10))

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer(60)  # 60 seconds
        self.player = Player("Player1")
        self.size = 4  # Default grid size

    def start_game(self):
        screen = pygame.display.set_mode((self.size * 50, self.size * 50 + 100))
        pygame.display.set_caption("Number Connect Game")
        self.grid.generate_grid(self.size)
        self.timer.start_timer()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            self.grid.draw_grid(screen)
            remaining_time = self.timer.get_remaining_time()
            font = pygame.font.Font(None, 36)
            timer_text = font.render(f'Time Left: {remaining_time}', True, (255, 255, 255))
            screen.blit(timer_text, (10, self.size * 50))
            pygame.display.flip()

            if remaining_time <= 0:
                running = False

        self.save_game_data()

    def save_game_data(self):
        with open('game_data.txt', 'a') as f:
            f.write(f'{self.player.name}:{self.player.score}:{self.size}\n')