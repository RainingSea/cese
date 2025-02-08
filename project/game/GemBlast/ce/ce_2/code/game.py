import random

class Gem:
    def __init__(self, color: str) -> None:
        self.color = color

class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.gems = [[self.random_gem() for _ in range(cols)] for _ in range(rows)]

    def random_gem(self) -> Gem:
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        return Gem(random.choice(colors))

    def initialize_grid(self) -> None:
        for row in range(len(self.gems)):
            for col in range(len(self.gems[row])):
                self.gems[row][col] = self.random_gem()

    def swap(self, pos1: tuple, pos2: tuple) -> None:
        self.gems[pos1[0]][pos1[1]], self.gems[pos2[0]][pos2[1]] = self.gems[pos2[0]][pos2[1]], self.gems[pos1[0]][pos1[1]]

    def clear_matches(self, matches: list) -> None:
        for (row, col) in matches:
            self.gems[row][col] = self.random_gem()

    def fall_down(self) -> None:
        for col in range(len(self.gems[0])):
            empty_slots = 0
            for row in range(len(self.gems) - 1, -1, -1):
                if self.gems[row][col] is None:
                    empty_slots += 1
                elif empty_slots > 0:
                    self.gems[row + empty_slots][col] = self.gems[row][col]
                    self.gems[row][col] = None

class Score:
    def __init__(self) -> None:
        self.points = 0

    def add_points(self, points: int) -> None:
        self.points += points

    def get_score(self) -> int:
        return self.points

class Timer:
    def __init__(self, time_limit: int) -> None:
        self.time_limit = time_limit

    def start_timer(self) -> None:
        pass  # Timer logic not implemented

    def check_time(self) -> bool:
        return True  # Placeholder for time checking logic

class Game:
    def __init__(self) -> None:
        self.grid = Grid(8, 8)  # Example grid size
        self.score = Score()
        self.timer = Timer(60)  # 60 seconds time limit

    def start_game(self) -> None:
        self.grid.initialize_grid()

    def swap_gems(self, pos1: tuple, pos2: tuple) -> bool:
        self.grid.swap(pos1, pos2)
        return True  # Placeholder for swap success logic

    def check_matches(self) -> list:
        return []  # Placeholder for match checking logic

    def update_score(self, points: int) -> None:
        self.score.add_points(points)

    def reset_game(self) -> None:
        self.grid.initialize_grid()
        self.score = Score()
        self.timer = Timer(60)