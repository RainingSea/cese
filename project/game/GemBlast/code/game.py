import pygame
import random
import json

class Game:
    def __init__(self):
        self.board = None
        self.score = Score()
        self.timer = Timer()
        self.levels = []
        self.current_level = 0
        self.load_game_data()

    def start_game(self):
        self.load_levels()
        self.reset_game()
        self.timer.start_timer()
        self.game_loop()

    def reset_game(self):
        level_data = self.levels[self.current_level]
        self.board = Board(level_data['grid_size'])
        self.score = Score()
        self.timer.start_timer()

    def load_levels(self):
        with open('levels.txt', 'r') as file:
            levels = file.readlines()
            self.levels = [self.parse_level(line) for line in levels]

    def parse_level(self, line):
        level_data = line.strip().split('|')
        grid_size = int(level_data[2])
        return {
            'name': level_data[0],
            'difficulty': level_data[1],
            'time_limit': int(level_data[2]),
            'grid_size': grid_size
        }

    def game_loop(self):
        while not self.timer.check_time():
            matches = self.board.check_matches()
            if matches:
                self.board.clear_matches(matches)
                self.score.update_score(len(matches) * 10)
                self.check_for_chain_reactions()

    def check_for_chain_reactions(self):
        while True:
            matches = self.board.check_matches()
            if not matches:
                break
            self.board.clear_matches(matches)
            self.score.update_score(len(matches) * 10)

    def load_game_data(self):
        try:
            with open('game_data.json', 'r') as file:
                data = json.load(file)
                self.current_level = data.get('current_level', 0)
                self.score.current_score = data.get('current_score', 0)
        except FileNotFoundError:
            self.current_level = 0
            self.score.current_score = 0

    def save_game_data(self):
        data = {
            'current_level': self.current_level,
            'current_score': self.score.current_score
        }
        with open('game_data.json', 'w') as file:
            json.dump(data, file)

class Board:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.create_grid()

    def create_grid(self):
        return [[random.choice(['R', 'G', 'B', 'Y']) for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def swap_gems(self, pos1, pos2):
        if self.is_adjacent(pos1, pos2):
            self.grid[pos1[0]][pos1[1]], self.grid[pos2[0]][pos2[1]] = self.grid[pos2[0]][pos2[1]], self.grid[pos1[0]][pos1[1]]
            return True
        return False

    def is_adjacent(self, pos1, pos2):
        return (abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]) or (pos1[0] == pos2[0] and abs(pos1[1] - pos2[1]) == 1)

    def check_matches(self):
        matches = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] is not None:
                    match = self.find_match(row, col)
                    if match:
                        matches.append(match)
        return matches

    def find_match(self, row, col):
        gem_color = self.grid[row][col]
        match = [(row, col)]
        
        # Check horizontal
        for c in range(col + 1, len(self.grid[row])):
            if self.grid[row][c] == gem_color:
                match.append((row, c))
            else:
                break
        
        # Check vertical
        for r in range(row + 1, len(self.grid)):
            if self.grid[r][col] == gem_color:
                match.append((r, col))
            else:
                break
        
        return match if len(match) >= 3 else None

    def clear_matches(self, matches):
        for match in matches:
            for pos in match:
                self.grid[pos[0]][pos[1]] = None
        self.fall_gems()

    def fall_gems(self):
        for col in range(len(self.grid[0])):
            for row in range(self.grid_size - 1, -1, -1):
                if self.grid[row][col] is None:
                    for r in range(row - 1, -1, -1):
                        if self.grid[r][col] is not None:
                            self.grid[row][col] = self.grid[r][col]
                            self.grid[r][col] = None
                            break

class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points):
        self.current_score += points

    def save_score(self, player_name):
        with open('scores.txt', 'a') as file:
            file.write(f"{player_name}|{self.current_score}\n")

class Timer:
    def __init__(self):
        self.time_limit = 60
        self.start_time = None

    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    def check_time(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        return elapsed_time >= self.time_limit