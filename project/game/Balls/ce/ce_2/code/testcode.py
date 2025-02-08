import unittest
import pygame
from game import Game, PlayerBall, EnemyBall

class TestBattleOfBallsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.initialize_game()

    def test_player_ball_movement(self):
        # Functionalities 1: Test player's ball movement upwards
        initial_position = self.game.player_ball.position
        self.game.player_ball.move('up')
        expected_position = (initial_position[0], initial_position[1] - self.game.player_ball.size)
        self.assertEqual(self.game.player_ball.position, expected_position, "Player's ball should move upwards")

    def test_enemy_ball_collision(self):
        # Functionalities 2: Test collision with smaller enemy ball
        enemy_ball = EnemyBall(size=10, position=self.game.player_ball.position)
        self.game.enemy_balls.append(enemy_ball)
        self.game.update()
        self.assertNotIn(enemy_ball, self.game.enemy_balls, "Enemy ball should be removed after collision")
        self.assertGreater(self.game.player_ball.size, 20, "Player's ball should grow after consuming enemy ball")

    def test_player_ball_consumption(self):
        # Functionalities 3: Test game end when surrounded by larger enemy balls
        self.game.player_ball.size = 10
        self.game.enemy_balls = [EnemyBall(size=30, position=self.game.player_ball.position)]
        self.game.check_collisions()
        self.assertEqual(self.game.score, 0, "Game should end with score 0 when player's ball is consumed")

    def test_initialize_game_entities(self):
        # Functionalities 4: Test game initialization
        self.assertEqual(len(self.game.enemy_balls), 5, "There should be 5 enemy balls initialized")
        self.assertGreater(self.game.player_ball.size, max(enemy.size for enemy in self.game.enemy_balls), "Player's ball should be larger than any enemy ball")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Test enemy ball spawning
        initial_count = len(self.game.enemy_balls)
        self.game.enemy_balls.append(EnemyBall(size=10, position=(100, 100)))
        self.assertEqual(len(self.game.enemy_balls), initial_count + 1, "A new enemy ball should appear on the map")

    def test_data_storage_functionality(self):
        # Functionalities 6: Test saving and loading game state
        self.game.score = 10
        self.game.save_game_data()
        self.game.score = 0
        self.game.load_game_data()
        self.assertEqual(self.game.score, 10, "Game state should be saved and loaded correctly")

if __name__ == '__main__':
    unittest.main()
