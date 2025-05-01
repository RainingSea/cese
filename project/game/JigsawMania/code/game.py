import pygame
import random
import time
import json

class Game:
    def __init__(self):
        self.current_puzzle = None
        self.timer = Timer()
        self.user_progress = UserProgress()
        self.load_user_progress()

    def start_game(self, image: str, difficulty: str):
        self.load_puzzle(image, difficulty)
        self.timer.start()

    def load_puzzle(self, image: str, difficulty: str):
        self.current_puzzle = Puzzle(image, difficulty)
        self.current_puzzle.shuffle()

    def restart_game(self):
        if self.current_puzzle is not None:
            self.current_puzzle.shuffle()
            self.timer.start()
        else:
            raise ValueError("No puzzle loaded. Please start a new game first.")

    def save_progress(self):
        self.user_progress.save_progress(self.current_puzzle.image, self.timer.get_elapsed_time())

    def load_user_progress(self):
        self.user_progress.load_progress()

    def create_custom_puzzle(self, image: str, layout: list):
        self.current_puzzle = Puzzle(image, layout)
        self.current_puzzle.shuffle()

    def provide_hint(self):
        if self.current_puzzle is not None:
            return self.current_puzzle.provide_hint()
        return "No puzzle loaded."

    def choose_difficulty_level(self, difficulty: str):
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty level. Choose from 'easy', 'medium', or 'hard'.")
        self.start_game(self.current_puzzle.image, difficulty)

class Puzzle:
    def __init__(self, image: str, difficulty: str):
        self.image = image
        self.difficulty = difficulty
        self.pieces = self.create_pieces(difficulty)

    def create_pieces(self, difficulty: str):
        if difficulty == "easy":
            return [Piece(self.image, (x, y)) for x in range(3) for y in range(3)]  # 3x3 puzzle
        elif difficulty == "medium":
            return [Piece(self.image, (x, y)) for x in range(4) for y in range(4)]  # 4x4 puzzle
        elif difficulty == "hard":
            return [Piece(self.image, (x, y)) for x in range(5) for y in range(5)]  # 5x5 puzzle
        return []

    def shuffle(self):
        random.shuffle(self.pieces)

    def rotate_piece(self, piece):
        piece.rotate()

    def provide_hint(self):
        # Provide a hint based on the current state of the puzzle
        return "Hint: Try moving the piece at position (0, 0) to the right."

class Piece:
    def __init__(self, image: str, position):
        self.image = image
        self.position = position
        self.rotation = 0  # Initialize rotation state

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360  # Rotate piece by 90 degrees

    def is_correct_position(self):
        # Logic to check if the piece is in the correct position
        return True

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            self.elapsed_time = time.time() - self.start_time

    def get_elapsed_time(self):
        if self.start_time is None:
            return '00:00'
        elapsed = time.time() - self.start_time
        return str(int(elapsed))

    def check_accuracy(self, expected_time: int):
        # Check if the elapsed time is accurate within a tolerance
        actual_time = self.get_elapsed_time()
        return abs(int(actual_time) - expected_time) < 1  # 1 second tolerance

class UserProgress:
    def __init__(self):
        self.user_id = None
        self.progress_data = {}

    def save_progress(self, image: str, time_taken: str):
        with open('progress.txt', 'w') as f:
            f.write(f"{self.user_id}|{{\"puzzle_image\": \"{image}\", \"time_taken\": \"{time_taken}\"}}")

    def load_progress(self):
        try:
            with open('progress.txt', 'r') as f:
                data = f.read().strip().split('|')
                self.user_id = data[0]
                self.progress_data = json.loads(data[1])
        except FileNotFoundError:
            self.user_id = "guest"
            self.progress_data = {}
            print("No progress file found. Starting fresh.")
        except json.JSONDecodeError:
            self.progress_data = {}
            print("Progress file is corrupted. Starting fresh.")