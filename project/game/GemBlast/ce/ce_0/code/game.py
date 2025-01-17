import random

class Gem:
    def __init__(self, color):
        self.color = color


class Grid:
    def __init__(self, size):
        self.gems = []
        self.initialize_grid(size)

    def initialize_grid(self, size):
        self.gems = [[Gem(random.choice(['red', 'green', 'blue', 'yellow', 'purple'])) for _ in range(size)] for _ in range(size)]

    def swap(self, pos1, pos2):
        self.gems[pos1[0]][pos1[1]], self.gems[pos2[0]][pos2[1]] = self.gems[pos2[0]][pos2[1]], self.gems[pos1[0]][pos1[1]]

    def fall_gems(self):
        for col in range(len(self.gems[0])):
            empty_slots = 0
            for row in range(len(self.gems) - 1, -1, -1):
                if self.gems[row][col] is None:
                    empty_slots += 1
                elif empty_slots > 0:
                    self.gems[row + empty_slots][col] = self.gems[row][col]
                    self.gems[row][col] = None

    def get_gem(self, pos):
        return self.gems[pos[0]][pos[1]]


class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points):
        self.points += points

    def get_score(self):
        return self.points


class Timer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.time_remaining = time_limit

    def start_timer(self):
        self.time_remaining = self.time_limit

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self):
        return self.time_remaining <= 0


class Level:
    def __init__(self):
        self.current_level = 1
        self.grid_size = 8  # Default grid size

    def next_level(self):
        self.current_level += 1
        self.grid_size += 1  # Increase grid size for next level

    def reset_level(self):
        self.current_level = 1
        self.grid_size = 8  # Reset to default grid size


class Game:
    def __init__(self):
        self.grid = Grid(8)
        self.score = Score()
        self.timer = Timer(60)  # 60 seconds timer
        self.level = Level()

    def start_game(self):
        self.grid.initialize_grid(self.level.grid_size)
        self.score = Score()
        self.timer.start_timer()

    def swap_gems(self, pos1, pos2):
        self.grid.swap(pos1, pos2)
        matches = self.check_matches()
        if matches:
            self.clear_matches(matches)
            return True
        return False

    def check_matches(self):
        matches = []
        # Check for horizontal and vertical matches
        for row in range(len(self.grid.gems)):
            for col in range(len(self.grid.gems[row])):
                if col <= len(self.grid.gems[row]) - 3:  # Horizontal check
                    if (self.grid.gems[row][col].color == self.grid.gems[row][col + 1].color == self.grid.gems[row][col + 2].color):
                        matches.append((row, col))
                        matches.append((row, col + 1))
                        matches.append((row, col + 2))
                if row <= len(self.grid.gems) - 3:  # Vertical check
                    if (self.grid.gems[row][col].color == self.grid.gems[row + 1][col].color == self.grid.gems[row + 2][col].color):
                        matches.append((row, col))
                        matches.append((row + 1, col))
                        matches.append((row + 2, col))
        return list(set(matches))  # Remove duplicates

    def clear_matches(self, matches):
        for pos in matches:
            self.grid.gems[pos[0]][pos[1]] = None
        self.grid.fall_gems()
        self.update_score(len(matches))

    def update_score(self, points):
        self.score.add_points(points)

    def reset_game(self):
        self.level.reset_level()
        self.start_game()