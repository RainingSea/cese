import pygame
import json
import random

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points: int) -> None:
        self.points += points

    def get_score(self) -> int:
        return self.points

class Timer:
    def __init__(self, time_limit: int):
        self.time_limit = time_limit
        self.time_remaining = time_limit

    def start_timer(self) -> None:
        self.time_remaining = self.time_limit

    def update_timer(self) -> None:
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self) -> bool:
        return self.time_remaining <= 0

class Level:
    def __init__(self, level_data: dict):
        self.current_level = level_data['level']
        self.grid_size = level_data['grid_size']
        self.color_count = level_data['color_count']

    def increase_level(self, level_data: dict) -> None:
        self.current_level += 1
        self.grid_size = level_data['grid_size']
        self.color_count = level_data['color_count']

    def get_level(self) -> int:
        return self.current_level

class Grid:
    def __init__(self):
        self.gems = []

    def create_grid(self, size: int, color_count: int) -> None:
        colors = ['R', 'G', 'B', 'Y', 'P'][:color_count]
        self.gems = [[random.choice(colors) for _ in range(size)] for _ in range(size)]

    def swap(self, pos1: tuple, pos2: tuple) -> None:
        self.gems[pos1[0]][pos1[1]], self.gems[pos2[0]][pos2[1]] = self.gems[pos2[0]][pos2[1]], self.gems[pos1[0]][pos1[1]]

    def clear_matches(self) -> list:
        matches = []
        # Check for horizontal matches
        for row in range(len(self.gems)):
            for i in range(len(self.gems[row]) - 2):
                if self.gems[row][i] == self.gems[row][i + 1] == self.gems[row][i + 2] != ' ':
                    matches.append((row, i))
                    self.gems[row][i] = self.gems[row][i + 1] = self.gems[row][i + 2] = ' '

        # Check for vertical matches
        for col in range(len(self.gems[0])):
            for i in range(len(self.gems) - 2):
                if self.gems[i][col] == self.gems[i + 1][col] == self.gems[i + 2][col] != ' ':
                    matches.append((i, col))
                    self.gems[i][col] = self.gems[i + 1][col] = self.gems[i + 2][col] = ' '

        return matches

    def fall_gems(self) -> None:
        for col in range(len(self.gems[0])):
            empty_slots = 0
            for row in range(len(self.gems) - 1, -1, -1):
                if self.gems[row][col] == ' ':
                    empty_slots += 1
                elif empty_slots > 0:
                    self.gems[row + empty_slots][col] = self.gems[row][col]
                    self.gems[row][col] = ' '

    def get_gem_at(self, pos: tuple) -> str:
        return self.gems[pos[0]][pos[1]]

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer(60)  # 60 seconds timer
        self.level = Level(self.load_level_data(1))  # Load initial level data
        self.grid.create_grid(self.level.grid_size, self.level.color_count)

    def load_level_data(self, level: int) -> dict:
        with open('levels.txt', 'r') as f:
            levels = json.load(f)
            return levels[str(level)]

    def start_game(self) -> None:
        self.timer.start_timer()
        while not self.timer.is_time_up():
            self.timer.update_timer()
            matches = self.check_matches()
            if matches:
                self.update_score(len(matches) * 10)  # Example scoring
                self.grid.fall_gems()
            if self.check_level_up():
                self.level.increase_level(self.load_level_data(self.level.current_level + 1))
                self.grid.create_grid(self.level.grid_size, self.level.color_count)

        self.handle_game_over()

    def handle_game_over(self) -> None:
        print("Game Over! Your score:", self.score.get_score())
        self.save_game_state('game_states.txt')

    def check_level_up(self) -> bool:
        return self.score.get_score() >= self.level.current_level * 100  # Example condition for leveling up

    def reset_game(self) -> None:
        self.score = Score()
        self.level = Level(self.load_level_data(1))  # Reset to level 1
        self.grid.create_grid(self.level.grid_size, self.level.color_count)
        self.timer.start_timer()

    def swap_gems(self, pos1: tuple, pos2: tuple) -> bool:
        if self.is_valid_swap(pos1, pos2):
            self.grid.swap(pos1, pos2)
            return True
        return False

    def is_valid_swap(self, pos1: tuple, pos2: tuple) -> bool:
        # Check if the positions are adjacent
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) == 1 and y1 == y2) or (abs(y1 - y2) == 1 and x1 == x2)

    def check_matches(self) -> list:
        return self.grid.clear_matches()

    def update_score(self, points: int) -> None:
        self.score.add_points(points)

    def load_game_state(self, file: str) -> None:
        with open(file, 'r') as f:
            state = json.load(f)
            self.score.points = state['score']
            self.level.current_level = state['level']
            self.grid.gems = state['gems']
            self.timer.time_remaining = state['time_remaining']

    def save_game_state(self, file: str) -> None:
        state = {
            'score': self.score.get_score(),
            'level': self.level.get_level(),
            'gems': self.grid.gems,
            'time_remaining': self.timer.time_remaining
        }
        with open(file, 'w') as f:
            json.dump(state, f)