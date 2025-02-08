import unittest
import os
import json
import pygame
from game import Game
from puzzle import Puzzle
from piece import Piece
from timer import Timer

class TestJigsawManiaGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.puzzle = self.game.puzzle
        self.timer = self.game.timer

    def test_select_puzzle_image(self):
        # Functionalities 1: Select Puzzle Image
        try:
            self.puzzle.load_image('path/to/image.png')
            image_loaded = True
        except Exception:
            image_loaded = False
        self.assertTrue(image_loaded, "The selected image should be loaded successfully")

    def test_choose_difficulty_level(self):
        # Functionalities 2: Choose Difficulty Level
        self.game.start_game('path/to/image.png', 'easy')
        self.assertEqual(len(self.puzzle.pieces), 4, "Easy difficulty should create 4 pieces")

        self.game.start_game('path/to/image.png', 'medium')
        self.assertEqual(len(self.puzzle.pieces), 9, "Medium difficulty should create 9 pieces")

        self.game.start_game('path/to/image.png', 'hard')
        self.assertEqual(len(self.puzzle.pieces), 16, "Hard difficulty should create 16 pieces")

    def test_start_timer(self):
        # Functionalities 3: Start Timer
        self.timer.start()
        self.assertGreater(self.timer.start_time, 0, "Timer should start counting from zero")

    def test_save_progress(self):
        # Functionalities 4: Save Progress
        self.game.start_game('path/to/image.png', 'easy')
        self.game.save_progress()
        self.assertTrue(os.path.exists('progress.txt'), "Progress should be saved in a local text file")

    def test_rotate_puzzle_piece(self):
        # Functionalities 5: Rotate Puzzle Piece
        self.game.start_game('path/to/image.png', 'easy')
        initial_image = self.puzzle.pieces[0].image
        self.puzzle.rotate_piece(0)
        self.assertNotEqual(self.puzzle.pieces[0].image, initial_image, "The piece should rotate by 90 degrees")

    def test_restart_puzzle(self):
        # Functionalities 6: Restart Puzzle
        self.game.start_game('path/to/image.png', 'easy')
        self.game.restart_game()
        self.assertEqual(len(self.puzzle.pieces), 0, "The puzzle should reset to its original state")

    def test_use_hint_feature(self):
        # Functionalities 7: Use Hint Feature (not implemented in codebase)
        self.fail("Hint feature is not implemented in the codebase")

    def test_create_custom_puzzle(self):
        # Functionalities 8: Create Custom Puzzle (not implemented in codebase)
        self.fail("Create custom puzzle functionality is not implemented in the codebase")

    def test_check_timer_accuracy(self):
        # Functionalities 9: Check Timer Accuracy
        self.timer.start()
        self.timer.stop()
        recorded_time = self.timer.get_time()
        self.assertEqual(recorded_time, self.timer.elapsed_time, "The recorded time should match the timer displayed")

if __name__ == '__main__':
    unittest.main()
