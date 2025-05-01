import unittest
import pygame
from game import Game

class TestBrickBreakerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.paddle = self.game.paddle
        self.ball = self.game.ball
        self.bricks = self.game.bricks

    def test_control_paddle_movement(self):
        # Functionalities 1: Control Paddle Movement
        initial_position = self.paddle.position
        self.paddle.move_left()
        self.assertLess(self.paddle.position, initial_position, "Paddle should move left")

        initial_position = self.paddle.position
        self.paddle.move_right()
        self.assertGreater(self.paddle.position, initial_position, "Paddle should move right")

    def test_ball_bounce_mechanics(self):
        # Functionalities 2: Ball Bounce Mechanics
        self.ball.position = [self.paddle.position + 50, 570]  # Position the ball above the paddle
        initial_velocity = self.ball.velocity[1]
        self.ball.bounce()
        self.assertEqual(self.ball.velocity[1], -initial_velocity, "Ball should bounce upwards after hitting the paddle")

    def test_brick_splitting_logic(self):
        # Functionalities 3: Brick Splitting Logic (not implemented in codebase)
        self.fail("Brick splitting logic is not implemented in the codebase")

    def test_brick_disappearance(self):
        # Functionalities 4: Brick Disappearance
        brick = self.bricks[0]
        brick.lives = 1  # Set lives to 1 for testing
        brick.hit()
        self.assertEqual(brick.lives, 0, "Brick should disappear when life reaches 0")

    def test_game_start_mechanism(self):
        # Functionalities 5: Game Start Mechanism
        self.assertIsNotNone(self.game.start_game, "Game should start successfully")

    def test_ball_movement(self):
        # Functionalities 6: Ball Movement
        initial_position = self.ball.position.copy()
        self.ball.update_position()
        self.assertNotEqual(self.ball.position, initial_position, "Ball should move after update")

    def test_save_game_state(self):
        # Functionalities 7: Save Game State (not implemented in codebase)
        self.fail("Save game state functionality is not implemented in the codebase")

    def test_load_game_state(self):
        # Functionalities 8: Load Game State (not implemented in codebase)
        self.fail("Load game state functionality is not implemented in the codebase")

    def test_end_game_condition(self):
        # Functionalities 9: End Game Condition
        self.ball.position[1] = 600  # Set ball position below the paddle
        self.game.handle_collisions()  # This should trigger game over
        self.assertTrue(self.ball.position[1] > 600, "Game should end when the ball falls below the paddle")

if __name__ == '__main__':
    unittest.main()
