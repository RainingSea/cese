import random

class Game:
    def __init__(self):
        self.puzzles = []
        self.hints = []
        self.current_level = 0

    def load_puzzles(self) -> None:
        with open('puzzles.txt', 'r') as file:
            self.puzzles = [line.strip() for line in file.readlines()]

    def load_hints(self) -> None:
        with open('hints.txt', 'r') as file:
            self.hints = [line.strip() for line in file.readlines()]

    def check_answer(self, input: str) -> bool:
        correct_answer = self.puzzles[self.current_level].split('|')[1]
        return input == correct_answer

    def provide_hint(self) -> str:
        return self.hints[self.current_level]

    def update_progress(self) -> None:
        with open('progress.txt', 'a') as file:
            file.write(f"Level {self.current_level} completed.\n")
            self.current_level += 1