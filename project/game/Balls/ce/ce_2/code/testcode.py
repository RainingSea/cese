import unittest
import pygame
from game import Game

class TestBallGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_ball = self.game.player_ball
        self.enemy_balls = self.game.enemy_balls

    def test_player_ball_movement(self):
        # Functionalities 1: Simulate pressing the up arrow key to move the player's ball.
        initial_y = self.player_ball.y_position
        self.player_ball.move('UP')
        self.assertEqual(self.player_ball.y_position, initial_y - 5, "Player's ball should move upward by 5 units")

    def test_enemy_ball_collision(self):
        # Functionalities 2: Position the player's ball to collide with a smaller enemy ball.
        enemy_ball = Ball(20, self.player_ball.x_position, self.player_ball.y_position)
        self.enemy_balls.append(enemy_ball)
        initial_size = self.player_ball.size
        self.game.check_collisions()
        self.assertGreater(self.player_ball.size, initial_size, "Player's ball should grow in size after consuming an enemy ball")
        self.assertNotIn(enemy_ball, self.enemy_balls, "Enemy ball should be removed after being consumed")

    def test_player_ball_consumption(self):
        # Functionalities 3: Simulate a scenario where the player's ball is surrounded by larger enemy balls.
        self.enemy_balls = [Ball(40, 100, 100), Ball(50, 200, 200), Ball(60, 300, 300), Ball(70, 400, 400)]
        self.game.check_collisions()
        # Since the player's ball is smaller than all enemy balls, it should trigger game over
        self.assertRaises(SystemExit, self.game.check_collisions)

    def test_initialize_game_entities(self):
        # Functionalities 4: Trigger the game initialization function.
        self.game.initialize()
        self.assertEqual(self.player_ball.size, 30, "Player's ball should be initialized with size 30")
        self.assertEqual(len(self.enemy_balls), 4, "There should be 4 enemy balls initialized")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Call the function responsible for spawning enemy balls.
        initial_enemy_count = len(self.enemy_balls)
        self.game.check_collisions()  # This will cause an enemy ball to spawn
        self.assertEqual(len(self.enemy_balls), initial_enemy_count + 1, "A new enemy ball should spawn after consuming one")

    def test_save_game_state(self):
        # Functionalities 6: Test saving game state (not implemented in codebase)
        self.fail("Save game state functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
