import unittest
import os
from game import Game

class TestSokobanGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.initial_state = [
            ['#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', '#'],
            ['#', ' ', 'P', ' ', '#'],
            ['#', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#']
        ]
        self.game.board = [row[:] for row in self.initial_state]
        self.game.player_position = (2, 2)

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        self.assertEqual(self.game.board, self.initial_state, "Game board should initialize correctly")

    def test_load_level_from_file(self):
        # Functionalities 2: Load a Level from a Text File
        self.game.load_game_state('game_state.txt')
        expected_state = [
            ['#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', '#'],
            ['#', ' ', 'P', ' ', '#'],
            ['#', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#']
        ]
        self.assertEqual(self.game.board, expected_state, "Level should load correctly from file")

    def test_move_player_right(self):
        # Functionalities 3: Move the Player Using Arrow Keys
        self.game.move_player('right')
        expected_position = (3, 2)
        self.assertEqual(self.game.player_position, expected_position, "Player should move right")

    def test_push_box(self):
        # Functionalities 4: Push a Box (not implemented in codebase)
        self.fail("Push box functionality is not implemented in the codebase")

    def test_check_win_condition(self):
        # Functionalities 5: Check Win Condition (not implemented in codebase)
        self.fail("Win condition check is not implemented in the codebase")

    def test_save_game_progress(self):
        # Functionalities 6: Save Game Progress
        self.game.save_game_state('test_save.txt')
        self.assertTrue(os.path.exists('test_save.txt'), "Game state should be saved to a file")
        os.remove('test_save.txt')

    def test_load_saved_game(self):
        # Functionalities 7: Load Saved Game
        self.game.save_game_state('test_save.txt')
        self.game.load_game_state('test_save.txt')
        self.assertEqual(self.game.board, self.initial_state, "Saved game state should load correctly")
        os.remove('test_save.txt')

    def test_reset_game_level(self):
        # Functionalities 8: Reset the Game Level (not implemented in codebase)
        self.fail("Reset game level functionality is not implemented in the codebase")

    def test_exit_game(self):
        # Functionalities 9: Exit the Game (not implemented in codebase)
        self.fail("Exit game functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
