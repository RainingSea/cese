import pygame

class Game:
    def __init__(self):
        self.puzzles = []
        self.current_level = 0
        self.load_puzzles()

    def load_puzzles(self) -> None:
        with open('puzzles.txt', 'r') as file:
            self.puzzles = [line.strip() for line in file.readlines()]

    def display_puzzle(self) -> str:
        return self.puzzles[self.current_level]

    def check_answer(self, player_answer: str) -> bool:
        return player_answer == self.puzzles[self.current_level]

    def provide_hint(self) -> str:
        with open('hints.txt', 'r') as file:
            hints = [line.strip() for line in file.readlines()]
        return hints[self.current_level]

    def track_progress(self) -> None:
        with open('progress.txt', 'a') as file:
            file.write(f"Level {self.current_level} completed\n")