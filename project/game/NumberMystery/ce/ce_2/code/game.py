import pygame

class Game:
    def __init__(self):
        self.puzzles = []
        self.current_level = 0
        self.player_progress = ""
        self.load_puzzles()

    def load_puzzles(self) -> None:
        with open('puzzles.txt', 'r') as file:
            self.puzzles = [line.strip() for line in file.readlines()]

    def show_puzzle(self) -> str:
        if self.current_level < len(self.puzzles):
            return self.puzzles[self.current_level]
        return "No more puzzles!"

    def check_answer(self, answer: str) -> bool:
        correct_answer = self.puzzles[self.current_level].split('|')[1]
        return answer == correct_answer

    def provide_hint(self) -> str:
        hint = self.puzzles[self.current_level].split('|')[2]
        return hint

    def next_level(self) -> None:
        self.current_level += 1
        if self.current_level < len(self.puzzles):
            self.player_progress = f"Progress: Level {self.current_level + 1}"
        else:
            self.player_progress = "You've completed all levels!"