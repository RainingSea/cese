import unittest
from game import Game
from grid import Grid
from timer import Timer
from score import Score
import os

class TestNumberConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.timer = self.game.timer
        self.score = self.game.score

    def test_connect_numbers_in_sequence(self):
        # Functionality 1: Connect Numbers in Sequence
        self.game.start_game(level=1)
        # Simulate clicking tiles in sequence from 1 to 9
        for number in range(1, 10):
            found = False
            for y, row in enumerate(self.grid.tiles):
                for x, value in enumerate(row):
                    if value == number:
                        self.game.click_tile(x, y)
                        found = True
                        break
                if found:
                    break
        self.assertTrue(self.game.check_path(), "The path should be valid for a correct sequence")

        self.game.start_game(level=2)
        # Simulate clicking a non-adjacent tile
        self.game.click_tile(0, 0)  # Assume this is number 1
        self.game.click_tile(2, 2)  # Assume this is number 2 but non-adjacent
        self.assertFalse(self.game.check_path(), "The path should be invalid for non-adjacent tiles")

    def test_movement_restrictions(self):
        # Functionality 2: Movement Restrictions
        self.game.start_game(level=3)
        # Simulate valid adjacent moves
        self.game.click_tile(0, 0)  # Assume this is number 1
        self.game.click_tile(0, 1)  # Assume this is number 2
        self.assertTrue(self.game.check_path(), "The path should be valid for adjacent tiles")

        # Simulate invalid non-adjacent move
        self.game.click_tile(2, 2)  # Assume this is number 3 but non-adjacent
        self.assertFalse(self.game.check_path(), "The path should be invalid for non-adjacent tiles")

        self.game.start_game(level=2)
        # Simulate revisiting a tile
        self.game.click_tile(0, 0)  # Assume this is number 1
        self.game.click_tile(0, 1)  # Assume this is number 2
        self.game.click_tile(0, 2)  # Assume this is number 3
        self.game.click_tile(0, 1)  # Revisit number 2
        self.assertFalse(self.game.check_path(), "The path should be invalid for revisiting tiles")

    def test_continuous_path_requirement(self):
        # Functionality 3: Continuous Path Requirement
        self.game.start_game(level=1)
        # Simulate skipping a number
        self.game.click_tile(0, 0)  # Assume this is number 1
        self.game.click_tile(0, 1)  # Assume this is number 2
        self.game.click_tile(1, 1)  # Assume this is number 4, skipping 3
        self.assertFalse(self.game.check_path(), "The path should be invalid for skipping numbers")

        self.game.start_game(level=2)
        # Simulate skipping a number
        self.game.click_tile(0, 0)  # Assume this is number 1
        self.game.click_tile(0, 1)  # Assume this is number 2
        self.game.click_tile(0, 2)  # Assume this is number 3
        self.game.click_tile(1, 2)  # Assume this is number 5, skipping 4
        self.assertFalse(self.game.check_path(), "The path should be invalid for skipping numbers")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 4: Multiple Levels with Increasing Difficulty
        self.game.start_game(level=1)
        self.assertEqual(len(self.grid.tiles), 3, "Level 1 should initialize a 3x3 grid")

        self.game.start_game(level=2)
        self.assertEqual(len(self.grid.tiles), 4, "Level 2 should initialize a 4x4 grid")

    def test_timer_challenge(self):
        # Functionality 5: Timer Challenge
        self.game.start_game(level=1)
        initial_time = self.timer.time_remaining
        self.timer.update_timer()
        self.assertLess(self.timer.time_remaining, initial_time, "Timer should decrease over time")

        # Simulate time running out
        self.timer.time_remaining = 0
        self.assertTrue(self.timer.is_time_up(), "Timer should indicate time is up when time_remaining is 0")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        self.game.save_game_state()
        self.assertTrue(os.path.exists('game_data.txt'), "Game state should be saved to a file")

        # Modify score and time, then load game state
        self.score.current_score = 100
        self.timer.time_remaining = 30
        self.game.load_game_state()
        self.assertEqual(self.score.current_score, 0, "Score should be loaded from the file")
        self.assertEqual(self.timer.time_remaining, 60.0, "Time should be loaded from the file")

if __name__ == '__main__':
    unittest.main()
