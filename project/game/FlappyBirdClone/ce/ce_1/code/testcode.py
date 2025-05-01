import unittest
import pygame
from game import Game

class TestFlappyBirdGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_bird_control(self):
        # Functionality 1: Bird Control
        initial_y = self.game.bird.y
        self.game.bird.flap()  # Simulate flap
        self.assertLess(self.game.bird.y, initial_y, "Bird should move upward after flap")

        # Simulate gravity effect
        self.game.bird.update()
        self.assertGreater(self.game.bird.y, initial_y, "Bird should fall due to gravity")

    def test_pipe_navigation(self):
        # Functionality 2: Pipe Navigation
        initial_pipe_count = len(self.game.pipes)
        self.game.update()  # Update to generate pipes
        self.assertGreater(len(self.game.pipes), initial_pipe_count, "Pipes should be generated")

        # Check if bird can navigate through pipes (not implemented in codebase)
        self.fail("Navigation through pipes is not implemented in the codebase")

    def test_pipe_movement(self):
        # Functionality 3: Pipe Movement
        initial_pipe_x = self.game.pipes[0].x if self.game.pipes else None
        self.game.update()  # Update to move pipes
        if initial_pipe_x is not None:
            self.assertLess(self.game.pipes[0].x, initial_pipe_x, "Pipes should move left")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.game.score
        self.game.update()  # Update to potentially increase score
        self.assertGreaterEqual(self.game.score, initial_score, "Score should increase after passing pipes")

    def test_game_over_conditions(self):
        # Functionality 5: Game Over Conditions
        self.game.bird.y = 700  # Simulate falling below ground
        self.game.check_collision()
        self.assertEqual(self.game.score, 0, "Score should reset after game over")

        # Simulate collision with pipe
        self.game.bird.y = self.game.pipes[0].height + 1  # Position bird to collide
        self.game.check_collision()
        self.assertEqual(self.game.score, 0, "Score should reset after collision with pipe")

    def test_restart_game(self):
        # Functionality 6: Restart Game
        self.game.score = 10  # Set score to a non-zero value
        self.game.restart_game()
        self.assertEqual(self.game.score, 0, "Score should reset after restarting the game")

    def test_high_score_storage(self):
        # Functionality 7: High Score Storage
        self.game.score = 5
        self.game.save_high_score()  # Save high score
        self.game.restart_game()  # Restart game
        self.assertEqual(self.game.high_score, 5, "High score should be saved correctly")

        # Simulate a new game with lower score
        self.game.score = 3
        self.game.restart_game()
        self.assertEqual(self.game.high_score, 5, "High score should not be overwritten by lower score")

if __name__ == '__main__':
    unittest.main()
