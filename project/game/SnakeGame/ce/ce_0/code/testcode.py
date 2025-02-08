import unittest
import pygame
from game import Game, Snake, Food, Score

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.snake = self.game.snake
        self.food = self.game.food
        self.score = self.game.score

    def test_control_snake_with_arrow_keys(self):
        # Functionalities 1: Control the Snake with Arrow Keys
        initial_position = self.snake.body[0]

        # Simulate pressing the Up arrow key
        self.snake.direction = 'UP'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_position[0], initial_position[1] - 1), "Snake should move upward")

        # Simulate pressing the Down arrow key
        self.snake.direction = 'DOWN'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_position[0], initial_position[1]), "Snake should move downward")

        # Simulate pressing the Left arrow key
        self.snake.direction = 'LEFT'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_position[0] - 1, initial_position[1]), "Snake should move left")

        # Simulate pressing the Right arrow key
        self.snake.direction = 'RIGHT'
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_position[0], initial_position[1]), "Snake should move right")

    def test_eating_food(self):
        # Functionalities 2: Eating Food
        self.snake.body[0] = self.food.position  # Simulate snake head on food
        self.game.snake.grow()
        self.food.generate_new_position()
        self.game.update_score()
        self.assertEqual(len(self.snake.body), 2, "Snake should grow longer after eating food")
        self.assertEqual(self.score.get_score(), 1, "Score should increase by 1 after eating food")

    def test_avoiding_collisions(self):
        # Functionalities 3: Avoiding Collisions
        # Simulate collision with wall
        self.snake.body[0] = (-1, 0)  # Out of bounds
        self.assertTrue(self.game.check_collision(), "Game should end when snake hits the wall")

        # Simulate self-collision
        self.snake.body = [(10, 10), (10, 11), (10, 10)]  # Head collides with body
        self.assertTrue(self.snake.check_self_collision(), "Game should end when snake collides with itself")

    def test_scoring_system(self):
        # Functionalities 4: Scoring System
        for _ in range(5):
            self.score.increment()
        self.assertEqual(self.score.get_score(), 5, "Score should be 5 after eating 5 pieces of food")

        for _ in range(5):
            self.score.increment()
        self.assertEqual(self.score.get_score(), 10, "Score should be 10 after eating 10 pieces of food")

    def test_increasing_difficulty(self):
        # Functionalities 5: Increasing Difficulty
        # This functionality is not directly testable with the current codebase
        self.fail("Increasing difficulty based on snake length is not implemented in the codebase")

    def test_pause_and_resume_game(self):
        # Functionalities 6: Pause and Resume Game
        self.game.pause()
        self.assertTrue(self.game.is_paused, "Game should be paused")
        self.game.resume()
        self.assertFalse(self.game.is_paused, "Game should resume from pause")

    def test_game_over_and_final_score_display(self):
        # Functionalities 7: Game Over and Final Score Display
        self.snake.body[0] = (-1, 0)  # Simulate collision
        self.assertTrue(self.game.check_collision(), "Game should end when snake hits the wall")
        # Restart game logic is not implemented in the codebase
        self.fail("Restart game functionality is not implemented in the codebase")

    def test_data_storage(self):
        # Functionalities 8: Data Storage
        self.score.current_score = 15
        self.game.save_high_score()
        with open('highscores.txt', 'r') as f:
            scores = f.readlines()
        self.assertIn("15\n", scores, "Score of 15 should be saved in the local text file")

if __name__ == '__main__':
    unittest.main()
