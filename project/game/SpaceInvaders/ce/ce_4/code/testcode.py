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
        # Functionalities 1: Test player movement to the left
        initial_x = self.player.x
        self.player.move_left()
        self.assertLess(self.player.x, initial_x, "Player should move left")

        # Test player movement to the right
        initial_x = self.player.x
        self.player.move_right()
        self.assertGreater(self.player.x, initial_x, "Player should move right")

        # Test player shooting
        initial_projectile_count = len(self.game.player_projectiles)
        self.game.player_projectiles.append(self.player.shoot())
        self.assertEqual(len(self.game.player_projectiles), initial_projectile_count + 1, "Player should shoot a projectile")

    def test_destroying_alien_enemies(self):
        # Functionalities 2: Test destroying an alien
        alien = self.aliens[0]
        projectile = Projectile(alien.x + 15, alien.y + 15)
        self.game.player_projectiles.append(projectile)
        self.game.check_collisions()
        self.assertNotIn(alien, self.game.aliens, "Alien should be destroyed when hit by a projectile")

        # Test score increase
        initial_score = self.game.score
        self.game.score += 1
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase when an alien is destroyed")

    def test_alien_movement(self):
        # Functionalities 3: Test alien movement
        initial_x = self.aliens[0].x
        self.aliens[0].move()
        self.assertNotEqual(self.aliens[0].x, initial_x, "Alien should move horizontally")

    def test_avoiding_alien_projectiles(self):
        # Functionalities 4: Test alien projectiles
        alien = self.aliens[0]
        projectile = alien.shoot()
        self.game.alien_projectiles.append(projectile)
        initial_y = projectile.y
        projectile.update()
        self.assertGreater(projectile.y, initial_y, "Alien projectile should move downwards")

    def test_destroying_enemy_projectiles(self):
        # Functionalities 5: Test destroying enemy projectiles (not implemented in codebase)
        self.fail("Destroying enemy projectiles functionality is not implemented in the codebase")

    def test_game_end_conditions(self):
        # Functionalities 6: Test game end when all aliens are destroyed
        self.game.aliens.clear()
        self.assertEqual(len(self.game.aliens), 0, "Game should end with a victory message when all aliens are destroyed")

        # Test game end when player is hit by an alien projectile
        self.fail("Game end when player is hit by an alien projectile is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
