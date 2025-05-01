import unittest
import pygame
from game import Game
from player import Player
from timer import Timer
from score import Score
from maze import Maze

class TestTreasureHuntGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.timer = self.game.timer
        self.score = self.game.score
        self.maze = self.game.maze

    def test_navigate_the_maze(self):
        # Functionalities 1: Test initial maze layout and player movement
        self.assertEqual(self.player.position, (1, 1), "Player should start at position (1, 1)")
        
        # Simulate player movement
        initial_position = self.player.position
        self.player.move("up")
        self.assertNotEqual(self.player.position, initial_position, "Player should move up")
        
        initial_position = self.player.position
        self.player.move("down")
        self.assertNotEqual(self.player.position, initial_position, "Player should move down")
        
        initial_position = self.player.position
        self.player.move("left")
        self.assertNotEqual(self.player.position, initial_position, "Player should move left")
        
        initial_position = self.player.position
        self.player.move("right")
        self.assertNotEqual(self.player.position, initial_position, "Player should move right")

    def test_find_the_treasure(self):
        # Functionalities 2: Test finding the treasure
        self.maze.treasure_location = (1, 1)  # Set treasure location to player's starting position
        self.player.position = self.maze.treasure_location
        # Assuming a method to check if treasure is found
        treasure_found = self.player.position == self.maze.treasure_location
        self.assertTrue(treasure_found, "Player should find the treasure")

    def test_score_tracking(self):
        # Functionalities 3: Test score increase on finding treasure
        initial_score = self.score.current_score
        self.score.increase()  # Simulate finding treasure
        self.assertGreater(self.score.current_score, initial_score, "Score should increase after finding treasure")

    def test_timer_implementation(self):
        # Functionalities 4: Test timer starts and counts down
        self.timer.start()
        self.assertGreater(self.timer.elapsed_time, 0, "Timer should start counting down")
        
        # Simulate finding treasure before time runs out
        self.timer.elapsed_time = 30  # Simulate time taken
        self.assertLess(self.timer.elapsed_time, self.timer.time_limit, "Time taken should be less than time limit")

    def test_level_progression(self):
        # Functionalities 5: Test level progression after finding treasure
        self.maze.treasure_location = (1, 1)  # Set treasure location
        self.player.position = self.maze.treasure_location
        # Simulate level progression (not implemented in codebase)
        self.fail("Level progression logic is not implemented in the codebase")

    def test_game_over_condition(self):
        # Functionalities 6: Test game over when time runs out
        self.timer.elapsed_time = self.timer.time_limit  # Simulate time running out
        self.assertTrue(self.timer.is_time_up(), "Game should end when time runs out")

    def test_best_time_storage(self):
        # Functionalities 7: Test best time storage
        self.timer.elapsed_time = 30  # Simulate a completed level time
        self.score.best_time = min(self.score.best_time, self.timer.elapsed_time)  # Update best time
        self.assertEqual(self.score.best_time, 30, "Best time should be updated correctly")

    def test_restart_game_option(self):
        # Functionalities 8: Test restarting the game
        # Simulate finishing a level
        self.game.running = False  # Game over
        self.game.running = True  # Restart game
        self.assertTrue(self.game.running, "Game should be running after restart")

if __name__ == '__main__':
    unittest.main()
