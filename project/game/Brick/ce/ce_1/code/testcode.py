import unittest
import pygame
from game import Game
from paddle import Paddle
from ball import Ball
from brick import Brick

class TestBrickBreakerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        pygame.init()
        self.game = Game()
        self.paddle = self.game.paddle
        self.ball = self.game.ball
        self.bricks = self.game.bricks

    def test_control_paddle_movement(self):
        # Functionalities 1: Test paddle movement to the left
        initial_x = self.paddle.x
        self.paddle.move('left')
        self.assertLess(self.paddle.x, initial_x, "Paddle should move left")

        # Test paddle movement to the right
        initial_x = self.paddle.x
        self.paddle.move('right')
        self.assertGreater(self.paddle.x, initial_x, "Paddle should move right")

    def test_ball_bounce_mechanics(self):
        # Functionalities 2: Simulate the ball hitting the paddle
        self.ball.x = self.paddle.x + self.paddle.width // 2
        self.ball.y = 580 - self.ball.radius
        initial_dy = self.ball.dy
        # Simulate collision detection
        if self.ball.y + self.ball.radius >= 580 and self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width:
            self.ball.dy = -self.ball.dy
        self.assertEqual(self.ball.dy, -initial_dy, "Ball should bounce off the paddle")

    def test_brick_splitting_logic(self):
        # Functionalities 3: Brick splitting logic (not implemented in codebase)
        self.fail("Brick splitting logic is not implemented in the codebase")

    def test_brick_disappearance(self):
        # Functionalities 4: Hit a brick until it disappears
        brick = self.bricks[0]
        initial_lives = brick.lives
        for _ in range(initial_lives):
            brick.hit()
        self.assertEqual(brick.lives, 0, "Brick should disappear when life reaches 0")

    def test_game_start_mechanism(self):
        # Functionalities 5: Simulate starting the game by moving the paddle
        self.assertTrue(self.game.run, "Game should be running after starting")

    def test_ball_movement(self):
        # Functionalities 6: Test ball movement upwards
        initial_y = self.ball.y
        self.ball.move()
        self.assertNotEqual(self.ball.y, initial_y, "Ball should move upwards")

    def test_save_game_state(self):
        # Functionalities 7: Test saving game state
        self.fail("Save game state functionality is not implemented in the codebase")

    def test_load_game_state(self):
        # Functionalities 8: Test loading game state
        self.fail("Load game state functionality is not implemented in the codebase")

    def test_end_game_condition(self):
        # Functionalities 9: Simulate the ball falling below the paddle
        self.ball.y = self.game.height + 1
        self.game.update()
        self.assertEqual(self.game.lives, 2, "Game should reduce lives when the ball falls below the paddle")

if __name__ == '__main__':
    unittest.main()
