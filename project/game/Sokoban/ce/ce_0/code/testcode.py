import unittest
import pygame
from game import Game

class TestSokobanGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        self.game.load_level('level.txt')
        self.assertTrue(self.game.board, "The game board should be initialized with a grid layout.")

    def test_load_level_from_text_file(self):
        # Functionalities 2: Load a Level from a Text File
        self.game.load_level('level.txt')
        expected_player_position = (1, 1)
        expected_goals = [(3, 2)]
        self.assertEqual(self.game.player_position, expected_player_position, "Player position should be loaded correctly.")
        self.assertEqual(self.game.goals, expected_goals, "Goals should be loaded correctly.")

    def test_move_player_using_arrow_keys(self):
        # Functionalities 3: Move the Player Using Arrow Keys
        self.game.load_level('level.txt')
        initial_position = self.game.player_position
        self.game.move_player('RIGHT')
        new_position = self.game.player_position
        self.assertNotEqual(initial_position, new_position, "Player should move one grid square to the right.")

    def test_push_box(self):
        # Functionalities 4: Push a Box (not implemented in codebase)
        self.fail("Push a box functionality is not implemented in the codebase")

    def test_check_win_condition(self):
        # Functionalities 5: Check Win Condition (not implemented in codebase)
        self.fail("Check win condition functionality is not implemented in the codebase")

    def test_save_game_progress(self):
        # Functionalities 6: Save Game Progress
        self.game.load_level('level.txt')
        self.game.save_game_state()
        with open('game_state.txt', 'r') as file:
            data = file.read()
        self.assertIn('player_position|1|1', data, "Game state should be saved with the correct player position.")

    def test_load_saved_game(self):
        # Functionalities 7: Load Saved Game
        self.game.load_game_state()
        expected_player_position = (1, 1)
        self.assertEqual(self.game.player_position, expected_player_position, "Player position should be loaded correctly from saved game.")

    def test_reset_game_level(self):
        # Functionalities 8: Reset the Game Level (not implemented in codebase)
        self.fail("Reset game level functionality is not implemented in the codebase")

    def test_exit_game(self):
        # Functionalities 9: Exit the Game (not implemented in codebase)
        self.fail("Exit game functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
