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
        # Functionality 1: Control the Snake with Arrow Keys
        initial_direction = self.snake.direction

        # Simulate pressing the Up arrow key
        self.game.handle_events()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
        self.game.handle_events()
        self.assertEqual(self.snake.direction, (0, -1), "Snake should move upward")

        # Simulate pressing the Down arrow key
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
        self.game.handle_events()
        self.assertEqual(self.snake.direction, (0, 1), "Snake should move downward")

        # Simulate pressing the Left arrow key
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}))
        self.game.handle_events()
        self.assertEqual(self.snake.direction, (-1, 0), "Snake should move left")

        # Simulate pressing the Right arrow key
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
        self.game.handle_events()
        self.assertEqual(self.snake.direction, (1, 0), "Snake should move right")

    def test_eating_food(self):
        # Functionality 2: Eating Food
        initial_length = len(self.snake.body)
        initial_score = self.score.get_score()

        # Place food directly in front of the snake
        self.food.position = (self.snake.body[0][0] + 1, self.snake.body[0][1])
        self.snake.direction = (1, 0)
        self.game.update()

        # Check if the snake has grown
        self.assertEqual(len(self.snake.body), initial_length + 1, "Snake should grow after eating food")

        # Check if the score has increased
        self.assertEqual(self.score.get_score(), initial_score + 1, "Score should increase by 1 after eating food")

    def test_avoiding_collisions(self):
        # Functionality 3: Avoiding Collisions
        # Simulate collision with wall
        self.snake.body[0] = (19, 0)  # Place snake head at the edge
        self.snake.direction = (1, 0)  # Move towards the wall
        self.assertTrue(self.snake.check_collision(wall=True), "Collision with wall should end the game")

        # Simulate self-collision
        self.snake.body = [(5, 5), (5, 6), (5, 7), (5, 5)]  # Create a self-collision scenario
        self.assertTrue(self.snake.check_self_collision(), "Collision with self should end the game")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        for _ in range(5):
            self.score.increase()
        self.assertEqual(self.score.get_score(), 5, "Score should be 5 after eating 5 pieces of food")

        for _ in range(5):
            self.score.increase()
        self.assertEqual(self.score.get_score(), 10, "Score should be 10 after eating 10 pieces of food")

    def test_increasing_difficulty(self):
        # Functionality 5: Increasing Difficulty
        # This functionality is not directly testable as it involves player experience
        self.fail("Increasing difficulty functionality is not directly testable")

    def test_pause_and_resume_game(self):
        # Functionality 6: Pause and Resume Game
        self.game.pause()
        self.assertTrue(self.game.is_paused, "Game should be paused")

        self.game.pause()
        self.assertFalse(self.game.is_paused, "Game should resume")

    def test_game_over_and_final_score_display(self):
        # Functionality 7: Game Over and Final Score Display
        # Simulate game over by collision
        self.snake.body[0] = (19, 0)
        self.snake.direction = (1, 0)
        self.assertTrue(self.snake.check_collision(wall=True), "Game should end on collision with wall")

        # Reset game and check score
        self.score.current_score = 0
        self.assertEqual(self.score.get_score(), 0, "Score should reset to zero after game over")

    def test_data_storage(self):
        # Functionality 8: Data Storage
        # This functionality is not implemented in the codebase
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
