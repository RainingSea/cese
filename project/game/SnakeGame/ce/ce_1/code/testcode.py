import unittest
import pygame
import os
from main import Game, Snake, Food

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.snake = self.game.snake
        self.food = self.game.food

    def test_control_snake_movement(self):
        # Functionalities 1 Test snake movement with arrow keys
        initial_position = self.snake.get_head_position()
        
        # Simulate Up arrow key
        self.snake.direction = (0, -10)
        self.snake.move()
        self.assertEqual(self.snake.get_head_position(), (initial_position[0], initial_position[1] - 10), "Snake should move up")

        # Simulate Down arrow key
        self.snake.direction = (0, 10)
        self.snake.move()
        self.assertEqual(self.snake.get_head_position(), (initial_position[0], initial_position[1]), "Snake should move down")

        # Simulate Left arrow key
        self.snake.direction = (-10, 0)
        self.snake.move()
        self.assertEqual(self.snake.get_head_position(), (initial_position[0] - 10, initial_position[1]), "Snake should move left")

        # Simulate Right arrow key
        self.snake.direction = (10, 0)
        self.snake.move()
        self.assertEqual(self.snake.get_head_position(), (initial_position[0], initial_position[1]), "Snake should move right")

    def test_eating_food(self):
        # Functionalities 2 Test snake eating food
        initial_length = len(self.snake.body)
        self.snake.body[0] = self.food.position  # Move snake head to food position
        self.snake.grow()
        self.food.spawn()  # Food should respawn
        self.assertGreater(len(self.snake.body), initial_length, "Snake should grow after eating food")
        self.assertEqual(self.game.score, 1, "Score should increase by 1 after eating food")

    def test_avoiding_collisions(self):
        # Functionalities 3 Test collision with wall
        self.snake.body[0] = (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)  # Move snake head out of bounds
        self.assertTrue(self.game.check_collision(), "Game should detect collision with wall")

        # Test collision with itself
        self.snake.body = [(100, 100), (90, 100), (80, 100)]  # Set snake body
        self.snake.body[0] = (90, 100)  # Move head to collide with body
        self.assertTrue(self.game.check_collision(), "Game should detect collision with itself")

    def test_scoring_system(self):
        # Functionalities 4 Test score after eating food
        for _ in range(5):
            self.snake.body[0] = self.food.position  # Move snake head to food position
            self.snake.grow()
            self.food.spawn()
        self.assertEqual(self.game.score, 5, "Score should be 5 after eating 5 pieces of food")

        for _ in range(5):
            self.snake.body[0] = self.food.position  # Move snake head to food position
            self.snake.grow()
            self.food.spawn()
        self.assertEqual(self.game.score, 10, "Score should be 10 after eating 10 pieces of food")

    def test_game_over_display(self):
        # Functionalities 7 Test game over display
        self.snake.body[0] = (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)  # Move snake head out of bounds
        self.game.check_collision()
        self.assertTrue(self.game.score > 0, "Final score should be greater than 0 after game over")

    def test_data_storage(self):
        # Functionalities 8 Test score saving
        self.game.score = 15
        self.game.game_over()  # This should save the score
        with open('highscore.txt', 'r') as file:
            saved_score = int(file.read())
        self.assertEqual(saved_score, 15, "Score should be saved in highscore.txt")

        # Test loading score
        self.game = Game()  # Restart game to load score
        self.assertEqual(self.game.high_score, 15, "High score should be loaded from highscore.txt")

if __name__ == '__main__':
    unittest.main()
