import pygame

class Puzzle:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

class Game:
    def __init__(self):
        self.current_level = 0
        self.puzzles = []
        self.hints = []
        self.load_data()

    def load_data(self):
        with open('puzzles.txt', 'r') as puzzle_file:
            for line in puzzle_file:
                question, answer = line.strip().split('|')
                self.puzzles.append(Puzzle(question, answer))

        with open('hints.txt', 'r') as hint_file:
            self.hints = [line.strip() for line in hint_file]

    def start(self):
        pygame.init()
        self.display_puzzle()
        # Main game loop can be implemented here

    def display_puzzle(self):
        if self.current_level < len(self.puzzles):
            print(self.puzzles[self.current_level].question)

    def check_answer(self, user_input: str) -> bool:
        return user_input.lower() == self.puzzles[self.current_level].answer.lower()

    def give_hint(self) -> str:
        if self.current_level < len(self.hints):
            return self.hints[self.current_level]
        return "No hints available."