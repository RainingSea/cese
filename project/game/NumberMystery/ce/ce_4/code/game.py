import json

class Puzzle:
    def __init__(self, rule: str, message: str, hint: str):
        self.rule = rule
        self.message = message
        self.hint = hint

    def is_solved(self, answer: str) -> bool:
        # Simple evaluation based on expected answers
        if self.rule == "Find the number that is the sum of 2 and 3":
            return answer == "5"
        elif self.rule == "What is 10 divided by 2?":
            return answer == "5"
        elif self.rule == "What is the square of 5?":
            return answer == "25"
        return False

class Game:
    def __init__(self):
        self.puzzles = []
        self.current_level = 0

    def load_puzzles(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            for line in file:
                rule, message, hint = line.strip().split('|')
                self.puzzles.append(Puzzle(rule, message, hint))

    def start_game(self) -> None:
        print("Welcome to the Number Mystery Game!")
        self.current_level = 0
        self.display_current_puzzle()

    def submit_answer(self, answer: str) -> bool:
        if self.current_level < len(self.puzzles):
            solved = self.puzzles[self.current_level].is_solved(answer)
            if solved:
                print("Correct! Moving to the next puzzle.")
                self.current_level += 1
                self.display_current_puzzle()
            else:
                print("Incorrect answer. Try again!")
            return solved
        return False

    def get_hint(self) -> str:
        if self.current_level < len(self.puzzles):
            return self.puzzles[self.current_level].hint
        return "No more hints available."

    def get_progress(self) -> str:
        return f"Current Level: {self.current_level + 1}/{len(self.puzzles)}"

    def display_current_puzzle(self) -> None:
        if self.current_level < len(self.puzzles):
            print(self.puzzles[self.current_level].message)
        else:
            print("Congratulations! You've completed all puzzles.")