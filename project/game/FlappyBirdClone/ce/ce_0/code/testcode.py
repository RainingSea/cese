import unittest
import pygame
import random
from game import Game

class TestFlappyBirdClone(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_bird_control(self):
        # Functionalities 1: Bird Control
        initial_position = self.game.bird.position[1]
        self.game.bird.flap()  # Simulate bird flap
        self.game.bird.update()  # Update bird position
        self.assertLess(self.game.bird.position[1], initial_position, "Bird should move upward after flap")

    def test_pipe_navigation(self):
        # Functionalities 2: Pipe Navigation
        gap_position = random.randint(100, 300)
        self.game.pipes.append(Pipe(gap_position))  # Add a pipe
        initial_bird_position = self.game.bird.position[1]
        self.game.bird.position[1] = gap_position + 75  # Position bird to pass through the gap
        self.game.check_collision()  # Check for collision
        self.assertTrue(self.game.running, "Bird should pass through the gap without colliding")

    def test_pipe_movement(self):
        # Functionalities 3: Pipe Movement
        self.game.pipes.append(Pipe(random.randint(100, 300)))  # Add a pipe
        initial_pipe_position = self.game.pipes[0].position[0]
        self.game.update()  # Update game state
        self.assertLess(self.game.pipes[0].position[0], initial_pipe_position, "Pipe should move left")

    def test_scoring_system(self):
        # Functionalities 4: Scoring System
        self.game.pipes.append(Pipe(random.randint(100, 300)))  # Add a pipe
        self.game.bird.position[1] = self.game.pipes[0].gap_position + 75  # Position bird to pass through
        self.game.update()  # Update game state
        self.assertEqual(self.game.score.current_score, 1, "Score should increase by one point after passing a pipe")

    def test_game_over_conditions(self):
        # Functionalities 5: Game Over Conditions
        self.game.bird.position[1] = 600  # Simulate bird falling to the ground
        self.game.check_collision()  # Check for collision
        self.assertFalse(self.game.running, "Game should end when the bird hits the ground")

        self.game.restart()  # Restart the game
        self.game.bird.position[1] = self.game.pipes[0].gap_position + 75  # Position bird to collide with pipe
        self.game.check_collision()  # Check for collision
        self.assertFalse(self.game.running, "Game should end when the bird collides with a pipe")

    def test_restart_game(self):
        # Functionalities 6: Restart Game
        self.game.bird.position[1] = 600  # Simulate bird falling to the ground
        self.game.check_collision()  # Check for collision
        self.assertFalse(self.game.running, "Game should end when the bird hits the ground")
        self.game.restart()  # Restart the game
        self.assertTrue(self.game.running, "Game should restart and be running")

    def test_high_score_storage(self):
        # Functionalities 7: High Score Storage
        self.game.score.current_score = 5
        self.game.score.save_high_score()  # Save high score
        self.game.restart()  # Restart the game
        self.assertEqual(self.game.score.high_score, 5, "High score should be saved and remain after restart")

        self.game.score.current_score = 3
        self.game.score.save_high_score()  # Attempt to save lower score
        self.assertEqual(self.game.score.high_score, 5, "High score should not change when a lower score is saved")

if __name__ == '__main__':
    unittest.main()
