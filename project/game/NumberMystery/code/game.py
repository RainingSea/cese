import pygame
import os

class Player:
    def __init__(self, name: str):
        self.name = name
        self.current_level = 0

    def submit_answer(self, answer: str, puzzle) -> bool:
        return puzzle.is_correct(answer)

    def request_hint(self, puzzle) -> str:
        return puzzle.get_hint()

    def load_progress(self) -> None:
        if os.path.exists('user_progress.txt'):
            with open('user_progress.txt', 'r') as file:
                for line in file:
                    name, level = line.strip().split('|')
                    if name == self.name:
                        self.current_level = int(level)

class Puzzle:
    def __init__(self, question: str, solution: str, hints: list):
        self.question = question
        self.solution = solution
        self.hints = hints

    def is_correct(self, answer: str) -> bool:
        return self.solution.lower() == answer.lower()

    def get_hint(self) -> str:
        if self.hints:
            return self.hints.pop(0)
        return "No more hints available."

class Game:
    def __init__(self):
        self.player = None
        self.puzzles = []
        self.current_level = 0
        self.load_progress()
        self.load_puzzles()

    def start_game(self):
        print("Game started!")
        while self.current_level < len(self.puzzles):
            current_puzzle = self.puzzles[self.current_level]
            print(current_puzzle.question)
            answer = input("Your answer: ")
            if self.handle_invalid_input(answer, current_puzzle):
                print("Correct!")
                self.current_level += 1
                self.save_progress()
            else:
                print("Incorrect! Here's a hint: ", self.player.request_hint(current_puzzle))
        print("Congratulations! You've completed all puzzles.")

    def load_puzzles(self) -> None:
        if os.path.exists('puzzles.txt'):
            with open('puzzles.txt', 'r') as file:
                for line in file:
                    question, answer = line.strip().split('|')
                    hint = self.get_hint_for_question(question)
                    self.puzzles.append(Puzzle(question, answer, [hint]))

    def get_hint_for_question(self, question: str) -> str:
        if os.path.exists('hints.txt'):
            with open('hints.txt', 'r') as file:
                for line in file:
                    q, hint = line.strip().split('|')
                    if q == question:
                        return hint
        return "No hint available."

    def save_progress(self) -> None:
        if self.player:
            with open('user_progress.txt', 'w') as file:
                file.write(f"{self.player.name}|{self.current_level}\n")

    def load_progress(self) -> None:
        if os.path.exists('user_progress.txt'):
            with open('user_progress.txt', 'r') as file:
                for line in file:
                    name, level = line.strip().split('|')
                    self.player = Player(name)
                    self.player.current_level = int(level)

    def handle_invalid_input(self, answer: str, current_puzzle: Puzzle) -> bool:
        return current_puzzle.is_correct(answer)

    def reset_game(self) -> None:
        self.current_level = 0
        if self.player:
            self.player.current_level = 0
        print("Game has been reset.")

    def feedback_on_progress(self) -> str:
        return f"Player {self.player.name} is currently at level {self.player.current_level}."

    def tracking_level_completion(self) -> None:
        self.load_puzzles()
        if self.player:
            self.player.current_level += 1  # Move to the next level
            assert self.player.current_level == 1