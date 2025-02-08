import unittest
import pygame
from game import Game, Snake, Food

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.snake = self.game.snake
        self.food = self.game.food

    def test_control_snake_with_arrow_keys(self):
        # Functionality 1: Control the Snake with Arrow Keys
        initial_head_position = self.snake.body[0]

        # Simulate pressing the Up arrow key
        self.snake.direction = 'UP'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_head_position[0], initial_head_position[1] - 10), "Snake should move upward")

        # Simulate pressing the Down arrow key
        self.snake.direction = 'DOWN'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_head_position[0], initial_head_position[1]), "Snake should move downward")

        # Simulate pressing the Left arrow key
        self.snake.direction = 'LEFT'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_head_position[0] - 10, initial_head_position[1]), "Snake should move left")

        # Simulate pressing the Right arrow key
        self.snake.direction = 'RIGHT'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_head_position[0], initial_head_position[1]), "Snake should move right")

    def test_eating_food(self):
        # Functionality 2: Eating Food
        self.snake.body[0] = self.food.position  # Simulate collision with food
        self.assertTrue(self.game.check_collision(), "Snake should collide with food")

        initial_score = self.game.score
        self.game.update_score()
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase by 1 after eating food")

    def test_avoiding_collisions(self):
        # Functionality 3: Avoiding Collisions
        # Simulate collision with wall
        self.snake.body[0] = (600, 400)  # Position outside the screen
        self.assertTrue(self.snake.check_self_collision(), "Game should end when snake collides with wall")

        # Simulate self-collision
        self.snake.body = [(100, 100), (90, 100), (100, 100)]  # Head collides with body
        self.assertTrue(self.snake.check_self_collision(), "Game should end when snake collides with itself")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        self.game.score = 0
        for _ in range(5):
            self.game.update_score()
        self.assertEqual(self.game.score, 5, "Score should be 5 after eating 5 pieces of food")

        for _ in range(5):
            self.game.update_score()
        self.assertEqual(self.game.score, 10, "Score should be 10 after eating 10 pieces of food")

    def test_increasing_difficulty(self):
        # Functionality 5: Increasing Difficulty
        # Not implemented in codebase, so we will fail this test
        self.fail("Increasing difficulty functionality is not implemented in the codebase")

    def test_pause_and_resume_game(self):
        # Functionality 6: Pause and Resume Game
        self.game.pause()
        self.assertTrue(self.game.is_paused, "Game should be paused")

        self.game.resume()
        self.assertFalse(self.game.is_paused, "Game should resume")

    def test_game_over_and_final_score_display(self):
        # Functionality 7: Game Over and Final Score Display
        # Not implemented in codebase, so we will fail this test
        self.fail("Game over and final score display functionality is not implemented in the codebase")

    def test_data_storage(self):
        # Functionality 8: Data Storage
        # Not implemented in codebase, so we will fail this test
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
