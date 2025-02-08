import json

class Game:
    def __init__(self):
        self.puzzles = {}
        self.hints = {}
        self.progress = {}

    def load_data(self):
        self.load_puzzles()
        self.load_hints()
        self.load_progress()

    def load_puzzles(self):
        with open('puzzles.json', 'r') as file:
            self.puzzles = json.load(file)

    def load_hints(self):
        with open('hints.txt', 'r') as file:
            self.hints = {line.split('|')[0]: line.split('|')[1] for line in file.read().strip().splitlines()}

    def load_progress(self):
        with open('progress.txt', 'r') as file:
            self.progress = {line.split('|')[0]: line.split('|')[1] for line in file.read().strip().splitlines()}

    def display_puzzle(self):
        # Logic to display the current puzzle
        pass

    def check_solution(self, user_input: str) -> bool:
        # Logic to check if the user's input matches the solution
        pass

    def provide_hint(self) -> str:
        # Logic to provide a hint
        pass

    def save_progress(self) -> None:
        with open('progress.txt', 'w') as file:
            for key, value in self.progress.items():
                file.write(f"{key}|{value}\n")