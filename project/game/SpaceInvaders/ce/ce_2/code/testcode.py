import unittest
import pygame
from game import Game, Player, Alien, Projectile

class TestSpaceInvadersGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.aliens = self.game.aliens

    def test_player_controls_spaceship(self):
        # Functionalities 1 Test moving left
        initial_x = self.player.rect.x
        self.player.move_left()
        self.assertLess(self.player.rect.x, initial_x, "Player should move left")

        # Test moving right
        initial_x = self.player.rect.x
        self.player.move_right()
        self.assertGreater(self.player.rect.x, initial_x, "Player should move right")

        # Test shooting
        initial_projectile_count = len(self.game.player_projectiles)
        self.player.shoot()
        self.assertEqual(len(self.game.player_projectiles), initial_projectile_count + 1, "Player should shoot a projectile")

    def test_destroying_alien_enemies(self):
        # Functionalities 2 Test destroying an alien
        self.player.rect.x = self.aliens[0].rect.x  # Position player directly below the first alien
        self.player.rect.y = self.aliens[0].rect.y + 30  # Position player above the alien
        self.player.shoot()
        self.game.check_collisions()
        self.assertEqual(len(self.game.aliens), 4, "One alien should be destroyed")

    def test_alien_movement(self):
        # Functionalities 3 Test alien movement
        initial_y_positions = [alien.rect.y for alien in self.aliens]
        self.game.update()
        for alien in self.aliens:
            self.assertGreater(alien.rect.y, initial_y_positions[0], "Aliens should move downwards")

    def test_avoiding_alien_projectiles(self):
        # Functionalities 4 Test alien shooting projectiles
        # This functionality is not implemented in the codebase
        self.fail("Alien projectiles functionality is not implemented in the codebase")

    def test_destroying_enemy_projectiles(self):
        # Functionalities 5 Test destroying an alien projectile
        # This functionality is not implemented in the codebase
        self.fail("Destroying enemy projectiles functionality is not implemented in the codebase")

    def test_game_end_conditions(self):
        # Functionalities 6 Test game end when all aliens are destroyed
        for _ in range(len(self.aliens)):
            self.player.rect.x = self.aliens[0].rect.x
            self.player.rect.y = self.aliens[0].rect.y + 30
            self.player.shoot()
            self.game.check_collisions()
        self.assertTrue(self.game.game_over, "Game should end when all aliens are destroyed")

        # Test game end when hit by alien projectile
        # This functionality is not implemented in the codebase
        self.fail("Game end condition when hit by alien projectile is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
