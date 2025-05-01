import unittest
import pygame
from main import Game, Paddle, Ball, Brick

class TestBrickBreakerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.paddle = self.game.paddle
        self.ball = self.game.ball
        self.bricks = self.game.bricks

    def test_control_paddle_movement(self):
        # Functionalities 1: Control Paddle Movement
        initial_x = self.paddle.position[0]
        
        # Move paddle left
        self.paddle.move_left()
        self.assertLess(self.paddle.position[0], initial_x, "Paddle should move left")

        # Move paddle right
        initial_x = self.paddle.position[0]
        self.paddle.move_right()
        self.assertGreater(self.paddle.position[0], initial_x, "Paddle should move right")

    def test_ball_bounce_mechanics(self):
        # Functionalities 2: Ball Bounce Mechanics
        self.ball.launch()
        self.ball.position = [self.paddle.position[0] + PADDLE_WIDTH // 2, self.paddle.position[1] - BALL_RADIUS]
        initial_velocity_y = self.ball.velocity[1]
        
        # Simulate bounce
        self.ball.bounce(self.paddle, self.bricks)
        self.assertEqual(self.ball.velocity[1], -initial_velocity_y, "Ball should bounce off the paddle")

    def test_brick_splitting_logic(self):
        # Functionalities 3: Brick Splitting Logic (not implemented in codebase)
        self.fail("Brick splitting logic is not implemented in the codebase")

    def test_brick_disappearance(self):
        # Functionalities 4: Brick Disappearance
        brick = Brick(0, 0, 1)  # Create a brick with 1 life
        for _ in range(brick.lives):
            brick.hit()
        self.assertEqual(brick.lives, 0, "Brick should disappear when life reaches 0")

    def test_game_start_mechanism(self):
        # Functionalities 5: Game Start Mechanism
        self.game.start_game()
        self.assertTrue(self.game.running, "Game should be running after starting")

    def test_ball_movement(self):
        # Functionalities 6: Ball Movement
        self.ball.launch()
        initial_y = self.ball.position[1]
        self.ball.bounce(self.paddle, self.bricks)  # Simulate a bounce
        self.assertNotEqual(self.ball.position[1], initial_y, "Ball should move upwards after being launched")

    def test_save_game_state(self):
        # Functionalities 7: Save Game State (not implemented in codebase)
        self.fail("Save game state functionality is not implemented in the codebase")

    def test_load_game_state(self):
        # Functionalities 8: Load Game State (not implemented in codebase)
        self.fail("Load game state functionality is not implemented in the codebase")

    def test_end_game_condition(self):
        # Functionalities 9: End Game Condition
        self.ball.position[1] = self.paddle.position[1] + PADDLE_HEIGHT + 1  # Simulate ball falling below paddle
        self.game.update()  # Update game state
        self.assertFalse(self.game.running, "Game should end when the ball falls below the paddle")

if __name__ == '__main__':
    unittest.main()
