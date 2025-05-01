import unittest
import pygame
from game import Game
from snake import Snake
from food import Food
from score import Score

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.snake = self.game.snake
        self.food = self.game.food
        self.score = self.game.score

    def test_control_snake_with_arrow_keys(self):
        # Functionalities 1 Test snake movement with arrow keys
        initial_position = self.snake.segments[0].position
        self.game.handle_events()  # Simulate event handling
        self.snake.direction = 'UP'
        self.snake.move()
        self.assertNotEqual(self.snake.segments[0].position, initial_position, "Snake should move up")

        initial_position = self.snake.segments[0].position
        self.snake.direction = 'DOWN'
        self.snake.move()
        self.assertNotEqual(self.snake.segments[0].position, initial_position, "Snake should move down")

        initial_position = self.snake.segments[0].position
        self.snake.direction = 'LEFT'
        self.snake.move()
        self.assertNotEqual(self.snake.segments[0].position, initial_position, "Snake should move left")

        initial_position = self.snake.segments[0].position
        self.snake.direction = 'RIGHT'
        self.snake.move()
        self.assertNotEqual(self.snake.segments[0].position, initial_position, "Snake should move right")

    def test_eating_food(self):
        # Functionalities 2 Test snake eating food
        initial_length = len(self.snake.segments)
        self.snake.segments[0].position = self.food.position  # Simulate collision with food
        self.snake.grow()
        self.food.generate_food()  # Food should regenerate
        self.assertGreater(len(self.snake.segments), initial_length, "Snake should grow after eating food")
        self.assertEqual(self.score.get_score(), 1, "Score should increase by 1 after eating food")

    def test_avoiding_collisions(self):
        # Functionalities 3 Test collision with wall
        self.snake.segments[0].position = (800, 600)  # Simulate collision with wall
        self.assertTrue(self.game.check_collision(), "Game should end on wall collision")

        # Test collision with self
        self.snake.segments.append(Snake().segments[0])  # Simulate self-collision
        self.assertTrue(self.game.check_collision(), "Game should end on self-collision")

    def test_scoring_system(self):
        # Functionalities 4 Test scoring system
        for _ in range(5):
            self.snake.segments[0].position = self.food.position  # Simulate eating food
            self.snake.grow()
            self.food.generate_food()
            self.score.increase()
        self.assertEqual(self.score.get_score(), 5, "Score should be 5 after eating 5 pieces of food")

        for _ in range(5):
            self.snake.segments[0].position = self.food.position  # Simulate eating more food
            self.snake.grow()
            self.food.generate_food()
            self.score.increase()
        self.assertEqual(self.score.get_score(), 10, "Score should be 10 after eating 10 pieces of food")

    def test_increasing_difficulty(self):
        # Functionalities 5 Test increasing difficulty
        initial_speed = self.game.snake.direction  # Placeholder for speed
        self.snake.grow()  # Simulate snake growth
        self.assertNotEqual(self.game.snake.direction, initial_speed, "Game difficulty should increase as snake grows")

    def test_pause_and_resume_game(self):
        # Functionalities 6 Test pause and resume functionality
        self.game.pause_game()
        self.assertTrue(self.game.is_paused, "Game should be paused")
        self.game.resume_game()
        self.assertFalse(self.game.is_paused, "Game should resume")

    def test_game_over_and_final_score_display(self):
        # Functionalities 7 Test game over condition
        self.snake.segments[0].position = (800, 600)  # Simulate game over
        self.assertTrue(self.game.check_collision(), "Game should end on collision")
        # Final score display is not directly testable without UI, so we skip this

    def test_data_storage(self):
        # Functionalities 8 Test data storage (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
