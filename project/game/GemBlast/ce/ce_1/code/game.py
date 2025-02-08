import random

class Grid:
    def __init__(self, grid_size=(8, 8), gem_types=5):
        self.gems = []
        self.grid_size = grid_size
        self.gem_types = gem_types
        self.initialize_grid()

    def initialize_grid(self) -> None:
        self.gems = [[random.randint(0, self.gem_types - 1) for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

    def swap(self, pos1: tuple, pos2: tuple) -> None:
        self.gems[pos1[0]][pos1[1]], self.gems[pos2[0]][pos2[1]] = self.gems[pos2[0]][pos2[1]], self.gems[pos1[0]][pos1[1]]

    def clear_matches(self, matches: list) -> None:
        for match in matches:
            for pos in match:
                self.gems[pos[0]][pos[1]] = -1  # Mark for clearing

    def fall_gems(self) -> None:
        for col in range(self.grid_size[1]):
            empty_space = 0
            for row in range(self.grid_size[0] - 1, -1, -1):
                if self.gems[row][col] == -1:
                    empty_space += 1
                elif empty_space > 0:
                    self.gems[row + empty_space][col] = self.gems[row][col]
                    self.gems[row][col] = -1

class Scoreboard:
    def __init__(self):
        self.score = 0

    def add_points(self, points: int) -> None:
        self.score += points

    def get_score(self) -> int:
        return self.score

class Timer:
    def __init__(self, time_limit: int):
        self.time_limit = time_limit
        self.time_remaining = time_limit

    def start_timer(self) -> None:
        self.time_remaining = self.time_limit

    def update_time(self) -> None:
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def is_time_up(self) -> bool:
        return self.time_remaining <= 0

class Level:
    def __init__(self):
        self.difficulty = 1
        self.grid = None

    def load_level(self, difficulty: int) -> None:
        self.difficulty = difficulty
        self.grid = Grid(grid_size=(8, 8), gem_types=difficulty + 2)

class Game:
    def __init__(self):
        self.grid = Grid()
        self.scoreboard = Scoreboard()
        self.timer = Timer(time_limit=60)  # 60 seconds timer
        self.level = Level()

    def start_game(self) -> None:
        self.level.load_level(difficulty=1)
        self.timer.start_timer()

    def swap_gems(self, pos1: tuple, pos2: tuple) -> bool:
        self.grid.swap(pos1, pos2)
        matches = self.check_matches()
        if matches:
            self.grid.clear_matches(matches)
            self.grid.fall_gems()
            self.update_score(points=len(matches) * 10)  # Example scoring
            return True
        return False

    def check_matches(self) -> list:
        # This is a placeholder for match detection logic.
        return []

    def update_score(self, points: int) -> None:
        self.scoreboard.add_points(points)

    def reset_game(self) -> None:
        self.grid.initialize_grid()
        self.scoreboard = Scoreboard()
        self.timer.start_timer()
        self.level.load_level(difficulty=1)