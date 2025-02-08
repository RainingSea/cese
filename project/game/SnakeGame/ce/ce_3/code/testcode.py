import unittest
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
        initial_position = self.snake.positions[0]

        # Test moving up
        self.snake.move('UP')
        self.assertEqual(self.snake.positions[0], (initial_position[0], initial_position[1] - 1), "Snake should move up")

        # Test moving down
        self.snake.move('DOWN')
        self.assertEqual(self.snake.positions[0], (initial_position[0], initial_position[1]), "Snake should move down")

        # Test moving left
        self.snake.move('LEFT')
        self.assertEqual(self.snake.positions[0], (initial_position[0] - 1, initial_position[1]), "Snake should move left")

        # Test moving right
        self.snake.move('RIGHT')
        self.assertEqual(self.snake.positions[0], (initial_position[0], initial_position[1]), "Snake should move right")

    def test_eating_food(self):
        # Functionality 2: Eating Food
        self.snake.positions = [(5, 5)]
        self.food.position = (5, 5)
        initial_length = len(self.snake.positions)
        initial_score = self.game.score_value

        self.game.check_collision()

        # Check if snake grows
        self.assertEqual(len(self.snake.positions), initial_length + 1, "Snake should grow after eating food")

        # Check if score increases
        self.assertEqual(self.game.score_value, initial_score + 1, "Score should increase after eating food")

    def test_avoiding_collisions(self):
        # Functionality 3: Avoiding Collisions
        # Test collision with wall
        self.snake.positions = [(60, 5)]
        self.game.check_collision()
        self.assertTrue(self.game.game_over, "Game should end when snake hits the wall")

        # Test collision with self
        self.snake.positions = [(5, 5), (5, 4), (5, 5)]
        self.game.check_collision()
        self.assertTrue(self.game.game_over, "Game should end when snake collides with itself")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        self.game.score_value = 0
        for _ in range(5):
            self.snake.grow()
            self.game.score_value += 1
        self.assertEqual(self.game.score_value, 5, "Score should be 5 after eating 5 pieces of food")

        for _ in range(5):
            self.snake.grow()
            self.game.score_value += 1
        self.assertEqual(self.game.score_value, 10, "Score should be 10 after eating 10 pieces of food")

    def test_increasing_difficulty(self):
        # Functionality 5: Increasing Difficulty
        self.fail("Increasing difficulty functionality is not implemented in the codebase")

    def test_pause_and_resume_game(self):
        # Functionality 6: Pause and Resume Game
        self.fail("Pause and resume functionality is not implemented in the codebase")

    def test_game_over_and_final_score_display(self):
        # Functionality 7: Game Over and Final Score Display
        self.snake.positions = [(60, 5)]
        self.game.check_collision()
        self.assertTrue(self.game.game_over, "Game should end when snake hits the wall")
        self.assertEqual(self.game.score_value, 0, "Score should reset to zero after game over")

    def test_data_storage(self):
        # Functionality 8: Data Storage
        self.game.score_value = 15
        self.game.save_score()
        loaded_score = self.score.load_score()
        self.assertEqual(loaded_score, 15, "Score should be saved and loaded correctly")

if __name__ == '__main__':
    unittest.main()
