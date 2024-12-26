import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.dictionary = Dictionary()
        self.dictionary.load_words('dictionary.txt')
        self.scores = ScoreManager()

    def run(self):
        # Placeholder for game loop implementation
        pass

    def update_score(self, word: str):
        if self.dictionary.is_valid(word):
            points = self.calculate_points(word)
            self.score.add_points(points)

    def calculate_points(self, word: str) -> int:
        base_points = len(word)  # Base points based on word length
        bonus_points = self.calculate_bonus(word)  # Calculate bonus points for complexity
        return base_points + bonus_points

    def calculate_bonus(self, word: str) -> int:
        # Example of bonus calculation: 5 points for complex words (e.g., longer than 5 letters)
        if len(word) > 5:
            return 5
        return 0

class Grid:
    def __init__(self):
        self.letters = self.generate_grid()
        self.selected_letters = []

    def generate_grid(self):
        # Generate a 4x4 grid of random letters
        return [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(4)] for _ in range(4)]

    def display(self):
        # Display the grid in a user-friendly format
        for row in self.letters:
            print(" ".join(row))

    def connect_letters(self, start: tuple, end: tuple) -> str:
        # Logic to connect letters based on start and end coordinates
        start_x, start_y = start
        end_x, end_y = end
        if self.is_valid_connection(start, end):
            word = self.extract_word(start, end)
            self.selected_letters.append(word)
            return word
        return ""

    def is_valid_connection(self, start: tuple, end: tuple) -> bool:
        # Check if the connection between start and end is valid
        start_x, start_y = start
        end_x, end_y = end
        return (abs(start_x - end_x) <= 1 and abs(start_y - end_y) <= 1)

    def extract_word(self, start: tuple, end: tuple) -> str:
        # Extract the word formed by the connected letters
        word = ""
        start_x, start_y = start
        end_x, end_y = end
        # Assuming a simple straight line connection for now
        if start_x == end_x:  # Same row
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                word += self.letters[start_x][y]
        elif start_y == end_y:  # Same column
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                word += self.letters[x][start_y]
        return word

class Score:
    def __init__(self):
        self.total_score = 0

    def add_points(self, points: int):
        self.total_score += points

    def get_score(self) -> int:
        return self.total_score

class Dictionary:
    def __init__(self):
        self.valid_words = set()

    def load_words(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                self.valid_words.add(line.strip())

    def is_valid(self, word: str) -> bool:
        return word in self.valid_words

class ScoreManager:
    def __init__(self):
        self.scores = {}

    def load_scores(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                player, score = line.strip().split('|')
                self.scores[player] = int(score)

    def save_scores(self, file_path: str):
        with open(file_path, 'w') as file:
            for player, score in self.scores.items():
                file.write(f"{player}|{score}\n")

    def update_score(self, player: str, score: int):
        if player in self.scores:
            self.scores[player] += score
        else:
            self.scores[player] = score