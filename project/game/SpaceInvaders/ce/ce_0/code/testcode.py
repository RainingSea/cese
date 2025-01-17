import unittest
import pygame
from game import Game
from spaceship import Spaceship
from alien import Alien
from projectile import Projectile

class TestSpaceInvadersGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.spaceship = self.game.spaceship
        self.aliens = self.game.aliens
        self.projectiles = self.game.projectiles

    def test_player_controls_spaceship(self):
        # Functionality 1: Test spaceship movement to the left
        initial_position = self.spaceship.position
        self.spaceship.move('left')
        self.assertLess(self.spaceship.position[0], initial_position[0], "Spaceship should move left")

        # Test spaceship movement to the right
        initial_position = self.spaceship.position
        self.spaceship.move('right')
        self.assertGreater(self.spaceship.position[0], initial_position[0], "Spaceship should move right")

        # Test shooting a projectile
        initial_projectile_count = len(self.projectiles)
        self.projectiles.append(self.spaceship.shoot())
        self.assertEqual(len(self.projectiles), initial_projectile_count + 1, "Spaceship should shoot a projectile")

    def test_destroying_alien_enemies(self):
        # Functionality 2: Test destroying an alien
        alien = self.aliens[0]
        projectile = Projectile((alien.position[0], alien.position[1] - 5), 'down')
        self.projectiles.append(projectile)
        self.game.update()
        self.assertNotIn(alien, self.aliens, "Alien should be destroyed when hit by a projectile")

        # Test score increase
        initial_score = self.game.score
        self.game.update()
        self.assertGreater(self.game.score, initial_score, "Score should increase when an alien is destroyed")

    def test_alien_movement(self):
        # Functionality 3: Test alien movement
        initial_positions = [alien.position for alien in self.aliens]
        for alien in self.aliens:
            alien.move()
        new_positions = [alien.position for alien in self.aliens]
        self.assertNotEqual(initial_positions, new_positions, "Aliens should move")

    def test_avoiding_alien_projectiles(self):
        # Functionality 4: Test alien projectiles
        alien = self.aliens[0]
        projectile = alien.shoot()
        self.assertEqual(projectile.direction, 'down', "Alien projectiles should move downwards")

    def test_destroying_enemy_projectiles(self):
        # Functionality 5: Test destroying enemy projectiles (not implemented in codebase)
        self.fail("Destroying enemy projectiles functionality is not implemented in the codebase")

    def test_game_end_conditions(self):
        # Functionality 6: Test game end conditions
        # Simulate all aliens being destroyed
        self.game.aliens.clear()
        self.assertEqual(len(self.game.aliens), 0, "All aliens should be destroyed")
        # Simulate game over condition
        self.fail("Game end conditions functionality is not fully implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
