import unittest
from game import Game
from puzzles import Puzzle
from timer import Timer
from user_progress import UserProgress

class TestJigsawManiaGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.puzzle = Puzzle()
        self.timer = Timer()
        self.user_progress = UserProgress()

    def test_select_puzzle_image(self):
        # Functionalities 1: Select Puzzle Image
        self.puzzle.create_puzzle('image1.png', 'easy')
        self.assertIsNotNone(self.puzzle.pieces, "Puzzle pieces should be loaded")

    def test_choose_difficulty_level(self):
        # Functionalities 2: Choose Difficulty Level
        self.puzzle.create_puzzle('image1.png', 'easy')
        easy_pieces = len(self.puzzle.pieces)
        self.puzzle.create_puzzle('image1.png', 'hard')
        hard_pieces = len(self.puzzle.pieces)
        self.assertGreater(hard_pieces, easy_pieces, "Hard difficulty should have more pieces than easy")

    def test_start_timer(self):
        # Functionalities 3: Start Timer
        self.timer.start()
        self.assertGreater(self.timer.start_time, 0, "Timer should start counting from a time greater than zero")

    def test_save_progress(self):
        # Functionalities 4: Save Progress
        self.game.start_game('image1.png', 'easy')
        self.game.save_progress()
        with open('progress.txt', 'r') as f:
            data = f.read()
        self.assertIn('puzzle_state', data, "Progress should be saved in the file")

    def test_rotate_puzzle_piece(self):
        # Functionalities 5: Rotate Puzzle Piece
        self.puzzle.create_puzzle('image1.png', 'easy')
        if self.puzzle.pieces:
            initial_state = self.puzzle.pieces[0].get_state()
            self.puzzle.rotate_piece(0)
            rotated_state = self.puzzle.pieces[0].get_state()
            self.assertNotEqual(initial_state, rotated_state, "Puzzle piece should rotate")

    def test_restart_puzzle(self):
        # Functionalities 6: Restart Puzzle
        self.game.start_game('image1.png', 'easy')
        self.game.restart_game()
        self.assertIsNone(self.game.puzzle, "Puzzle should be reset to None after restart")

    def test_use_hint_feature(self):
        # Functionalities 7: Use Hint Feature (not implemented in codebase)
        self.fail("Hint feature is not implemented in the codebase")

    def test_create_custom_puzzle(self):
        # Functionalities 8: Create Custom Puzzle (not implemented in codebase)
        self.fail("Create custom puzzle functionality is not implemented in the codebase")

    def test_check_timer_accuracy(self):
        # Functionalities 9: Check Timer Accuracy
        self.timer.start()
        time.sleep(1)  # Simulate 1 second passing
        elapsed_time = self.timer.stop()
        self.assertAlmostEqual(elapsed_time, 1, delta=0.1, "Timer should accurately track time")

if __name__ == '__main__':
    unittest.main()
