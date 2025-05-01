import unittest
import pygame
import os
from main import Game

class TestBallGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_ball = self.game.player_ball
        self.enemy_balls = self.game.enemy_balls

    def test_player_ball_movement(self):
        # Functionalities 1: Simulate pressing the up arrow key to move the player's ball.
        initial_position = self.player_ball.position
        self.player_ball.move('UP')
        self.assertEqual(self.player_ball.position, (initial_position[0], initial_position[1] - 5), "Player's ball should move upward by 5 units.")

    def test_enemy_ball_collision(self):
        # Functionalities 2: Position the player's ball to collide with a smaller enemy ball.
        enemy_ball = self.enemy_balls[0]
        enemy_ball.position = (self.player_ball.position[0], self.player_ball.position[1])  # Position enemy ball for collision
        initial_size = self.player_ball.size
        initial_enemy_count = len(self.enemy_balls)

        self.game.check_collisions()

        self.assertGreater(self.player_ball.size, initial_size, "Player's ball should grow in size after collision.")
        self.assertEqual(len(self.enemy_balls), initial_enemy_count, "Enemy ball should be removed from the game.")

    def test_initialize_game_entities(self):
        # Functionalities 4: Trigger the game initialization function to set up the player's ball and enemy balls.
        self.assertEqual(self.player_ball.size, 30, "Player's ball should be initialized with size 30.")
        self.assertEqual(len(self.enemy_balls), 5, "There should be 5 enemy balls initialized.")

    def test_enemy_ball_spawning(self):
        # Functionalities 5: Call the function responsible for spawning enemy balls on the map.
        initial_enemy_count = len(self.enemy_balls)
        self.game.enemy_balls.append(EnemyBall())  # Simulate spawning a new enemy ball
        self.assertEqual(len(self.enemy_balls), initial_enemy_count + 1, "A new enemy ball should be spawned.")

    def test_save_game_state(self):
        # Functionalities 6: Save the game state to a local text file after an action is performed.
        game_state_path = 'game_data.txt'
        self.game.score = 10  # Set a score for testing
        with open(game_state_path, 'w') as f:
            f.write(f'score|{self.game.score}\ngame_state|running\n')

        # Verify if the file is created and contains the correct data
        self.assertTrue(os.path.exists(game_state_path), "Game state file should be created.")
        with open(game_state_path, 'r') as f:
            data = f.read()
            self.assertIn('score|10', data, "Game state file should contain the correct score.")
            self.assertIn('game_state|running', data, "Game state file should indicate that the game is running.")

        # Clean up
        os.remove(game_state_path)

if __name__ == '__main__':
    unittest.main()
