import unittest
import pygame
from game import Game
from player_ball import PlayerBall
from enemy_ball import EnemyBall
import os

class TestBallGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        pygame.init()
        self.game = Game()
        self.player_ball = self.game.player_ball
        self.enemy_balls = self.game.enemy_balls

    def test_player_ball_movement(self):
        # Functionalities 1: Test player's ball movement upwards
        initial_position = self.player_ball.position
        self.player_ball.move('UP')
        self.assertEqual(self.player_ball.position, (initial_position[0], initial_position[1] - 5), "Player's ball should move up")

    def test_enemy_ball_collision(self):
        # Functionalities 2: Test collision with enemy ball
        self.player_ball.position = (100, 100)
        enemy_ball = EnemyBall(size=10, position=(105, 105))
        self.enemy_balls.append(enemy_ball)
        self.game.check_collisions()
        self.assertEqual(self.player_ball.size, 25, "Player's ball should grow in size after collision")
        self.assertNotIn(enemy_ball, self.enemy_balls, "Enemy ball should be removed after collision")

    def test_player_ball_consumption(self):
        # Functionalities 3: Test player's ball consumption by larger enemy balls
        self.player_ball.size = 10
        self.enemy_balls = [EnemyBall(size=30, position=(400, 300))]
        self.game.check_collisions()
        # Assuming game ends when player is consumed, which is not implemented
        self.fail("Game end on player consumption is not implemented in the codebase")

    def test_initialize_game_entities(self):
        # Functionalities 4: Test game initialization
        self.assertEqual(len(self.enemy_balls), 5, "There should be 5 enemy balls initialized")
        self.assertGreater(self.player_ball.size, max(enemy.size for enemy in self.enemy_balls), "Player's ball should be larger than enemy balls")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Test enemy ball spawning
        initial_count = len(self.enemy_balls)
        self.game.initialize_balls()
        self.assertEqual(len(self.enemy_balls), initial_count + 5, "Five new enemy balls should be spawned")

    def test_data_storage_functionality(self):
        # Functionalities 6: Test saving and loading game state
        self.player_ball.size = 30
        self.game.save_game_data()
        self.player_ball.size = 20
        self.game.load_game_data()
        self.assertEqual(self.player_ball.size, 30, "Game state should be loaded correctly from file")
        os.remove('game_data.txt')  # Clean up after test

if __name__ == '__main__':
    unittest.main()
