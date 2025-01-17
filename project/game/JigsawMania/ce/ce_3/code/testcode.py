import unittest
import pygame
import os
import json
from main import Game
from puzzle import Puzzle, Piece

class TestJigsawMania(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()
        self.puzzle = self.game.puzzle

    def test_select_puzzle_image(self):
        # Functionalities 1: Select Puzzle Image
        try:
            self.puzzle.create_puzzle('path/to/puzzle/image.png', 'easy')
            self.assertIsNotNone(self.puzzle.image, "Puzzle image should be loaded successfully")
        except pygame.error:
            self.fail("Failed to load the puzzle image")

    def test_choose_difficulty_level(self):
        # Functionalities 2: Choose Difficulty Level
        self.puzzle.create_puzzle('path/to/puzzle/image.png', 'easy')
        self.assertEqual(len(self.puzzle.pieces), 4, "Easy difficulty should create 4 pieces")

        self.puzzle.create_puzzle('path/to/puzzle/image.png', 'hard')
        self.assertEqual(len(self.puzzle.pieces), 9, "Hard difficulty should create 9 pieces")

    def test_start_timer(self):
        # Functionalities 3: Start Timer
        self.game.start_game('path/to/puzzle/image.png', 'easy')
        self.assertGreater(self.game.timer.get_elapsed_time(), 0, "Timer should start and update in real time")

    def test_save_progress(self):
        # Functionalities 4: Save Progress
        self.game.start_game('path/to/puzzle/image.png', 'easy')
        self.game.save_progress()
        self.assertTrue(os.path.exists('progress.txt'), "Progress should be saved in a local text file")

    def test_rotate_puzzle_piece(self):
        # Functionalities 5: Rotate Puzzle Piece
        self.puzzle.create_puzzle('path/to/puzzle/image.png', 'easy')
        initial_image = self.puzzle.pieces[0].image.copy()
        self.puzzle.rotate_piece(0)
        rotated_image = self.puzzle.pieces[0].image
        self.assertNotEqual(initial_image, rotated_image, "Puzzle piece should rotate by 90 degrees")

    def test_restart_puzzle(self):
        # Functionalities 6: Restart Puzzle
        self.game.start_game('path/to/puzzle/image.png', 'easy')
        self.game.restart_puzzle()
        self.assertEqual(len(self.puzzle.pieces), 0, "Puzzle should reset to its original state")

    def test_use_hint_feature(self):
        # Functionalities 7: Use Hint Feature (not implemented in codebase)
        self.fail("Hint feature is not implemented in the codebase")

    def test_create_custom_puzzle(self):
        # Functionalities 8: Create Custom Puzzle (not implemented in codebase)
        self.fail("Create custom puzzle functionality is not implemented in the codebase")

    def test_check_timer_accuracy(self):
        # Functionalities 9: Check Timer Accuracy
        self.game.start_game('path/to/puzzle/image.png', 'easy')
        pygame.time.delay(1000)  # Simulate 1 second delay
        elapsed_time = self.game.timer.get_elapsed_time()
        self.assertAlmostEqual(elapsed_time, 1, delta=0.1, "Timer should accurately track time")

if __name__ == '__main__':
    unittest.main()
