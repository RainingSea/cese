import pygame
import json
from puzzle import Puzzle
from timer import Timer

class Game:
    def __init__(self):
        self.current_puzzle = None
        self.timer = Timer()
        self.load_progress()
        self.puzzles = self.load_puzzles()

    def load_puzzles(self):
        try:
            with open('puzzles.json', 'r') as f:
                data = json.load(f)
                return [Puzzle(puzzle['image_path'], puzzle['difficulty']) for puzzle in data['puzzles']]
        except FileNotFoundError:
            print("Puzzles file not found. Please ensure 'puzzles.json' exists.")
            return []
        except json.JSONDecodeError:
            print("Puzzles file is corrupted. Please check the file format.")
            return []

    def start_game(self, puzzle: Puzzle) -> None:
        self.current_puzzle = puzzle
        self.current_puzzle.shuffle_pieces()
        self.timer.start()

    def save_progress(self) -> None:
        if self.current_puzzle is None:
            print("No puzzle is currently active. Cannot save progress.")
            return
        
        progress_data = {
            'pieces': [(piece.get_position(), piece.image_path) for piece in self.current_puzzle.pieces],
            'elapsed_time': self.timer.get_elapsed_time(),
            'current_image': self.current_puzzle.image_path,
            'difficulty': self.current_puzzle.difficulty
        }
        with open('progress.json', 'w') as f:
            json.dump(progress_data, f)

    def load_progress(self) -> None:
        try:
            with open('progress.json', 'r') as f:
                progress_data = json.load(f)
                self.current_puzzle = Puzzle(progress_data['current_image'], progress_data['difficulty'])
                for index, (position, image_path) in enumerate(progress_data['pieces']):
                    self.current_puzzle.pieces[index].set_position(position)
                self.timer.elapsed_time = progress_data['elapsed_time']
        except FileNotFoundError:
            print("No progress file found. Starting a new game.")
        except json.JSONDecodeError:
            print("Progress file is corrupted. Starting a new game.")

    def restart_puzzle(self) -> None:
        if self.puzzles:
            self.current_puzzle = None
            self.start_game(self.puzzles[0])  # Restart with the first puzzle for simplicity
        else:
            print("No puzzles available to restart.")

    def use_hint(self) -> None:
        if self.current_puzzle:
            print(f"Hint: The correct position for one of the pieces is {self.current_puzzle.pieces[0].get_position()}.")
        else:
            print("No puzzle is currently active. Cannot provide a hint.")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Update game state and render here
            pygame.display.flip()
        self.save_progress()