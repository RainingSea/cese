import random

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
        self.puzzles = []
        self.current_level = 0
        self.hints_used = 0

    def load_puzzles(self) -> None:
        with open('puzzles.txt', 'r') as file:
            for line in file:
                question, solution = line.strip().split('|')
                hints = self.load_hints(question)
                self.puzzles.append(Puzzle(question, solution, hints))

    def load_hints(self, question: str) -> list:
        hints = []
        with open('hints.txt', 'r') as file:
            for line in file:
                if line.startswith(question):
                    hints = line.strip().split('|')[1:]  # Skip the question part
                    break
        return hints

    def check_answer(self, answer: str) -> bool:
        if self.current_level < len(self.puzzles):
            return self.puzzles[self.current_level].is_correct(answer)
        return False

    def get_hint(self) -> str:
        if self.current_level < len(self.puzzles):
            self.hints_used += 1
            return self.puzzles[self.current_level].get_hint()
        return "No hints available."

    def track_progress(self) -> None:
        with open('progress.txt', 'w') as file:
            file.write(f"{self.current_level}|{self.hints_used}\n")