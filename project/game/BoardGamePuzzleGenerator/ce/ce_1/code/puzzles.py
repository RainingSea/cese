import random
import time

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        return int(time.time() - self.start_time)

class Score:
    def calculate_score(self, time, accuracy):
        base_score = 1000
        time_penalty = time * 10
        return max(base_score - time_penalty, 0) if accuracy else 0

    def save_score(self, player_name, score):
        with open("scores.txt", "a") as file:
            file.write(f"{player_name}|{score}\n")

class PuzzleGenerator:
    def generate_puzzle(self, category):
        puzzles = {
            "logic": ["Logic Puzzle 1", "Logic Puzzle 2", "Logic Puzzle 3"],
            "pattern": ["Pattern Puzzle 1", "Pattern Puzzle 2"],
            "spatial": ["Spatial Puzzle 1", "Spatial Puzzle 2"]
        }
        return random.choice(puzzles.get(category, []))

class Game:
    def __init__(self):
        self.puzzle_generator = PuzzleGenerator()
        self.timer = Timer()
        self.score = Score()

    def start_game(self, category):
        puzzle = self.puzzle_generator.generate_puzzle(category)
        print(f"Puzzle: {puzzle}")
        self.timer.start()
        # Simulate player input and solution checking
        player_solution = input("Enter your solution: ")
        self.submit_solution(player_solution)

    def submit_solution(self, solution):
        # Here we would check the solution; for now, we assume it's correct
        accuracy = True  # Simulating that the solution is correct
        elapsed_time = self.timer.stop()
        score = self.score.calculate_score(elapsed_time, accuracy)
        player_name = "Player"  # Simulating player name
        self.score.save_score(player_name, score)
        print(f"Your score: {score}")