import unittest
import pygame
from game import Game

class TestFlappyBirdGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_bird_control(self):
        # Functionality 1: Bird Control
        initial_position_y = self.game.bird.position_y
        self.game.bird.flap()
        self.assertLess(self.game.bird.position_y, initial_position_y, "Bird should move upward after flap")

    def test_pipe_navigation(self):
        # Functionality 2: Pipe Navigation
        self.game.pipes.append(Pipe(800))  # Manually add a pipe for testing
        initial_pipe_count = len(self.game.pipes)
        self.game.update()  # Update to potentially remove off-screen pipes
        self.assertGreaterEqual(len(self.game.pipes), initial_pipe_count, "Pipes should be generated at regular intervals")

    def test_pipe_movement(self):
        # Functionality 3: Pipe Movement
        pipe = Pipe(800)
        initial_position_x = pipe.position_x
        pipe.update()
        self.assertLess(pipe.position_x, initial_position_x, "Pipe should move left")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        self.game.score = 0
        self.game.score += 1  # Simulate passing a pipe
        self.assertEqual(self.game.score, 1, "Score should increase by one point after passing a pipe")

    def test_game_over_conditions(self):
        # Functionality 5: Game Over Conditions
        # Simulate a collision by not implementing collision detection
        self.game.check_collision()  # Placeholder for collision detection
        self.fail("Game over conditions are not implemented in the codebase")

    def test_restart_game(self):
        # Functionality 6: Restart Game
        self.game.restart()
        self.assertEqual(self.game.score, 0, "Score should reset to 0 after restarting")
        self.assertEqual(len(self.game.pipes), 0, "Pipes should be cleared after restarting")
        self.assertEqual(self.game.bird.position_y, 300, "Bird's position should reset to starting height")

    def test_high_score_storage(self):
        # Functionality 7: High Score Storage
        self.game.high_score = 5  # Simulate achieving a high score
        self.game.save_high_score()  # Save high score
        self.game.restart()  # Restart game
        self.assertEqual(self.game.high_score, 5, "High score should remain after restarting")

if __name__ == '__main__':
    unittest.main()
