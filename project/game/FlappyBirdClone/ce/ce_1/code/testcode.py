import unittest
import pygame
from game import Game, Bird, Pipe

class TestFlappyBirdGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.bird = self.game.bird
        self.pipes = self.game.pipes

    def test_bird_control(self):
        # Functionality 1: Bird Control
        initial_y = self.bird.y
        self.bird.fall()
        self.assertGreater(self.bird.y, initial_y, "Bird should fall due to gravity")

        self.bird.flap()
        self.assertLess(self.bird.y, initial_y, "Bird should move upward when flapped")

    def test_pipe_navigation(self):
        # Functionality 2: Pipe Navigation
        self.assertGreater(len(self.pipes), 0, "Pipes should be generated at the start of the game")
        for pipe in self.pipes:
            self.assertTrue(pipe.x > 0, "Pipes should appear from the right side of the screen")

    def test_pipe_movement(self):
        # Functionality 3: Pipe Movement
        initial_x_positions = [pipe.x for pipe in self.pipes]
        self.game.update()
        for i, pipe in enumerate(self.pipes):
            self.assertLess(pipe.x, initial_x_positions[i], "Pipes should move from right to left")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.game.score
        self.game.update()
        if any(pipe.x + pipe.width < 0 for pipe in self.pipes):
            self.assertGreater(self.game.score, initial_score, "Score should increase when passing through pipes")

    def test_game_over_conditions(self):
        # Functionality 5: Game Over Conditions
        self.bird.y = 600  # Simulate bird falling to the ground
        self.assertTrue(self.game.check_collision(), "Game should end when the bird falls to the ground")

        self.bird.y = 250  # Reset bird position
        self.pipes[0].x = self.bird.x  # Simulate collision with pipe
        self.assertTrue(self.game.check_collision(), "Game should end when the bird collides with a pipe")

    def test_restart_game(self):
        # Functionality 6: Restart Game
        self.game.restart()
        self.assertEqual(self.game.score, 0, "Game should reset score to 0 on restart")
        self.assertEqual(len(self.game.pipes), 2, "Game should regenerate pipes on restart")

    def test_high_score_storage(self):
        # Functionality 7: High Score Storage
        self.game.score = 5
        self.game.save_high_score()
        self.assertEqual(self.game.high_score, 5, "High score should be saved when a new high score is achieved")

        self.game.score = 3
        self.game.save_high_score()
        self.assertEqual(self.game.high_score, 5, "High score should not be overwritten by a lower score")

if __name__ == '__main__':
    unittest.main()
