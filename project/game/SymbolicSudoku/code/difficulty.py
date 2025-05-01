class Difficulty:
    def __init__(self):
        self.level = "easy"

    def set_level(self, level: str):
        self.level = level

    def get_level(self) -> str:
        return self.level

    def get_puzzles(self, difficulty: str) -> list:
        return self.load_puzzles(difficulty)

    def load_puzzles(self, difficulty: str) -> list:
        puzzles = []
        with open('puzzles.txt', 'r') as file:
            for line in file:
                if line.startswith(difficulty):
                    _, *puzzle_lines = line.strip().split('|')
                    for puzzle in puzzle_lines:
                        puzzles.append([int(num) if num != '0' else 0 for num in puzzle.split(',')])
        return puzzles