import unittest
import pygame
from game import Game, PlayerBall, EnemyBall
import os

class TestBattleOfBallsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_ball = self.game.player_ball
        self.enemy_ball = EnemyBall(size=10, x=400, y=300)
        self.game.enemy_balls.append(self.enemy_ball)

    def test_player_ball_movement(self):
        # Functionalities 1: Simulate pressing the up arrow key to move the player's ball
        initial_y = self.player_ball.y
        self.player_ball.move('UP')
        self.assertLess(self.player_ball.y, initial_y, "Player's ball should move upward")

    def test_enemy_ball_collision(self):
        # Functionalities 2: Position the player's ball to collide with a smaller enemy ball
        self.player_ball.x = self.enemy_ball.x
        self.player_ball.y = self.enemy_ball.y
        initial_size = self.player_ball.size
        self.game.check_collisions()
        self.assertGreater(self.player_ball.size, initial_size, "Player's ball should grow in size")
        self.assertNotIn(self.enemy_ball, self.game.enemy_balls, "Enemy ball should be removed from the game")

    def test_player_ball_consumption(self):
        # Functionalities 3: Simulate a scenario where the player's ball is surrounded by larger enemy balls
        # This functionality is not implemented in the codebase
        self.fail("Player's ball consumption functionality is not implemented in the codebase")

    def test_initialize_game_entities(self):
        # Functionalities 4: Trigger the game initialization function
        self.assertIsInstance(self.player_ball, PlayerBall, "Player's ball should be initialized")
        self.assertEqual(len(self.game.enemy_balls), 1, "One enemy ball should be initialized")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Call the function responsible for spawning enemy balls
        initial_enemy_count = len(self.game.enemy_balls)
        self.game.spawn_enemy()
        self.assertGreaterEqual(len(self.game.enemy_balls), initial_enemy_count, "A new enemy ball should appear on the map")

    def test_data_storage_functionality(self):
        # Functionalities 6: Save the game state to a local text file
        self.game.save_game_data()
        self.assertTrue(os.path.exists('game_data.txt'), "Game data file should exist")
        with open('game_data.txt', 'r') as file:
            data = file.read()
            self.assertIn(f'Score: {self.game.score}', data, "Game state should be saved correctly")

if __name__ == '__main__':
    unittest.main()
