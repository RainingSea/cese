import unittest
import pygame
from game import Game, Board, Player, ScoreManager

class TestSokobanGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.board = self.game.board
        self.player = self.game.player
        self.score_manager = self.game.score_manager

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        self.assertIsInstance(self.board, Board, "Game board should be initialized as an instance of Board")
        self.assertGreater(len(self.board.grid), 0, "Game board grid should be initialized with rows")

    def test_load_level_from_file(self):
        # Functionalities 2: Load a Level from a Text File
        self.board.load_from_file('game_state.txt')
        self.assertGreater(len(self.board.grid), 0, "Level should be loaded with a non-empty grid")
        self.assertEqual(self.board.grid[1][1], 1, "Objects should be loaded correctly on the game board")

    def test_move_player_using_arrow_keys(self):
        # Functionalities 3: Move the Player Using Arrow Keys
        initial_position = self.player.get_position()
        self.player.move('right')
        new_position = self.player.get_position()
        self.assertEqual(new_position, (initial_position[0] + 1, initial_position[1]), "Player should move one grid square to the right")

    def test_push_box(self):
        # Functionalities 4: Push a Box (Not implemented in codebase)
        self.fail("Push a box functionality is not implemented in the codebase")

    def test_check_win_condition(self):
        # Functionalities 5: Check Win Condition (Not implemented in codebase)
        self.fail("Check win condition functionality is not implemented in the codebase")

    def test_save_game_progress(self):
        # Functionalities 6: Save Game Progress
        self.game.save_game_state()
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
        self.assertGreater(len(lines), 0, "Game state should be saved to a file")

    def test_load_saved_game(self):
        # Functionalities 7: Load Saved Game
        self.game.load_game_state()
        self.assertGreater(len(self.board.grid), 0, "Saved game state should be loaded with a non-empty grid")

    def test_reset_game_level(self):
        # Functionalities 8: Reset the Game Level (Not implemented in codebase)
        self.fail("Reset game level functionality is not implemented in the codebase")

    def test_exit_game(self):
        # Functionalities 9: Exit the Game
        pygame.quit()
        self.assertFalse(pygame.get_init(), "Game should close successfully")

if __name__ == '__main__':
    unittest.main()
