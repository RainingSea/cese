import unittest
import pygame
from game import Game, Piece

class TestJigsawMania(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()

    def test_select_puzzle_image(self):
        # Functionalities 1: Select Puzzle Image
        self.game.start_game("images/puzzle1.jpg", "medium")
        self.assertEqual(self.game.current_image, "images/puzzle1.jpg", "The selected image should be loaded successfully.")

    def test_choose_difficulty_level(self):
        # Functionalities 2: Choose Difficulty Level
        self.game.start_game("images/puzzle1.jpg", "medium")
        self.assertEqual(self.game.difficulty, "medium", "The difficulty level should be set correctly.")

    def test_start_timer(self):
        # Functionalities 3: Start Timer
        self.game.timer.start()
        self.assertGreaterEqual(self.game.timer.get_time(), 0, "Timer should start counting from zero.")

    def test_save_progress(self):
        # Functionalities 4: Save Progress
        self.game.start_game("images/puzzle1.jpg", "medium")
        self.game.save_progress()
        with open('progress.txt', 'r') as f:
            progress_data = json.load(f)
        self.assertEqual(progress_data['current_image'], "images/puzzle1.jpg", "Progress should be saved with the correct image.")
        self.assertEqual(progress_data['difficulty'], "medium", "Progress should be saved with the correct difficulty level.")

    def test_rotate_puzzle_piece(self):
        # Functionalities 5: Rotate Puzzle Piece
        piece = Piece(1, pygame.Surface((100, 100)))
        self.game.rotate_piece(piece)
        self.fail("Rotate puzzle piece functionality is not implemented in the codebase.")

    def test_restart_puzzle(self):
        # Functionalities 6: Restart Puzzle
        self.game.start_game("images/puzzle1.jpg", "medium")
        self.game.restart_game()
        self.assertEqual(len(self.game.pieces), 0, "The puzzle should reset to its original state.")

    def test_use_hint_feature(self):
        # Functionalities 7: Use Hint Feature
        self.fail("Hint feature is not implemented in the codebase.")

    def test_create_custom_puzzle(self):
        # Functionalities 8: Create Custom Puzzle
        self.fail("Create custom puzzle functionality is not implemented in the codebase.")

    def test_check_timer_accuracy(self):
        # Functionalities 9: Check Timer Accuracy
        self.game.timer.start()
        pygame.time.delay(1000)  # Simulate 1 second delay
        self.game.timer.stop()
        self.assertAlmostEqual(self.game.timer.get_time(), 1000, delta=100, "The timer should accurately track the elapsed time.")

if __name__ == '__main__':
    unittest.main()
