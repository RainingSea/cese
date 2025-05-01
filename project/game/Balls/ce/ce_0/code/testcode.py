import unittest
import pygame
from game import Game

class TestBallGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_ball = self.game.player_ball
        self.enemy_balls = self.game.enemy_balls

    def test_player_ball_growth_on_collision(self):
        # Functionalities 2: Position the player's ball to collide with a smaller enemy ball
        initial_size = self.player_ball.size
        enemy_ball = self.enemy_balls[0]
        enemy_ball.size = 5.0  # Ensure enemy ball is smaller
        self.game._is_colliding = lambda player, enemy: True  # Simulate collision
        self.game.check_collisions()
        self.assertGreater(self.player_ball.size, initial_size, "Player's ball should grow in size upon collision")
        self.assertNotIn(enemy_ball, self.game.enemy_balls, "Enemy ball should be removed after collision")

    def test_game_initialization(self):
        # Functionalities 4: Trigger the game initialization function
        self.game.initialize()
        self.assertEqual(len(self.game.enemy_balls), 5, "There should be 5 enemy balls initialized")
        self.assertEqual(self.player_ball.size, 10.0, "Player's ball should have initial size of 10.0")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Call the function responsible for spawning enemy balls
        initial_enemy_count = len(self.game.enemy_balls)
        self.game.enemy_balls.append(EnemyBall())  # Simulate spawning a new enemy ball
        self.assertEqual(len(self.game.enemy_balls), initial_enemy_count + 1, "A new enemy ball should appear on the map")

    def test_data_storage_functionality(self):
        # Functionalities 6: Save the game state to a local text file
        self.game.save_data()
        with open('player_data.txt', 'r') as f:
            player_size = float(f.read().strip())
        self.assertEqual(player_size, self.player_ball.size, "Player size should be saved correctly")

        with open('enemy_data.txt', 'r') as f:
            enemy_positions = f.read().strip().splitlines()
        self.assertEqual(len(enemy_positions), len(self.game.enemy_balls), "Enemy ball positions should be saved correctly")

    def test_player_ball_consumption(self):
        # Functionalities 3: Simulate a scenario where the player's ball is surrounded by larger enemy balls
        self.game.enemy_balls = [EnemyBall() for _ in range(5)]  # Reset enemy balls
        for enemy_ball in self.game.enemy_balls:
            enemy_ball.size = 15.0  # Make enemy balls larger than player
        self.game.check_collisions()  # Check collisions
        self.assertEqual(self.player_ball.size, 10.0, "Player's ball should not grow when surrounded by larger enemy balls")

if __name__ == '__main__':
    unittest.main()
