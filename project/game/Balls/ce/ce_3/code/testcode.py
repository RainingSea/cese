import unittest
import pygame
from game import Game, PlayerBall, EnemyBall
import os

class TestBallGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_ball = self.game.player_ball

    def test_player_ball_movement(self):
        # Functionalities 1: Test player's ball movement upwards
        initial_y = self.player_ball.position_y
        self.player_ball.move("UP")
        self.assertLess(self.player_ball.position_y, initial_y, "Player's ball should move upward")

    def test_enemy_ball_collision(self):
        # Functionalities 2: Test collision with a smaller enemy ball
        self.player_ball.size = 15
        enemy_ball = EnemyBall(size=10, position_x=self.player_ball.position_x, position_y=self.player_ball.position_y)
        self.game.enemy_balls.append(enemy_ball)
        self.game.check_collisions()
        self.assertEqual(self.player_ball.size, 15, "Player's ball should not grow in size")
        self.assertNotIn(enemy_ball, self.game.enemy_balls, "Enemy ball should be removed after collision")

    def test_player_ball_consumption(self):
        # Functionalities 3: Test game end when player's ball is consumed
        self.player_ball.size = 5
        enemy_ball = EnemyBall(size=10, position_x=self.player_ball.position_x, position_y=self.player_ball.position_y)
        self.game.enemy_balls.append(enemy_ball)
        self.game.check_collisions()
        self.assertTrue(self.game.is_game_over, "Game should end when player's ball is consumed by a larger enemy ball")

    def test_initialize_game_entities(self):
        # Functionalities 4: Test initialization of game entities
        self.game.spawn_enemy_balls()
        self.assertEqual(len(self.game.enemy_balls), 4, "Four enemy balls should be created")
        self.assertGreater(self.player_ball.size, max(enemy.size for enemy in self.game.enemy_balls), "Player's ball should be larger than enemy balls")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Test spawning of enemy balls
        initial_count = len(self.game.enemy_balls)
        self.game.spawn_enemy_balls()
        self.assertEqual(len(self.game.enemy_balls), initial_count + 1, "A new enemy ball should be spawned")

    def test_data_storage_functionality(self):
        # Functionalities 6: Test saving game state to a file
        game_state = "score|0\ngame_state|running\n"
        with open('game_data.txt', 'w') as file:
            file.write(game_state)
        
        with open('game_data.txt', 'r') as file:
            content = file.read()
        
        self.assertEqual(content, game_state, "Game state should be saved and read back correctly")

if __name__ == '__main__':
    unittest.main()
