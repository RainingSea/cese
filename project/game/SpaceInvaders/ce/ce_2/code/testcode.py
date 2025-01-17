import unittest
import pygame
from game import Game, Spaceship, Alien, Projectile

class TestSpaceInvadersGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.spaceship = self.game.spaceship
        self.aliens = self.game.aliens
        self.projectiles = self.game.projectiles

    def test_player_controls_spaceship(self):
        # Functionalities 1: Test spaceship movement to the left
        initial_position = self.spaceship.position
        self.spaceship.move_left()
        self.assertLess(self.spaceship.position[0], initial_position[0], "Spaceship should move left")

        # Test spaceship movement to the right
        self.spaceship.move_right()
        self.assertGreater(self.spaceship.position[0], initial_position[0], "Spaceship should move right")

        # Test shooting a projectile
        initial_projectile_count = len(self.projectiles)
        projectile = self.spaceship.shoot()
        self.projectiles.append(projectile)
        self.assertEqual(len(self.projectiles), initial_projectile_count + 1, "A projectile should be fired")

    def test_destroying_alien_enemies(self):
        # Functionalities 2: Test destroying an alien
        alien = self.aliens[0]
        projectile = Projectile((alien.position[0], alien.position[1] + 5))
        self.projectiles.append(projectile)
        self.game.check_collisions()
        self.assertNotIn(alien, self.aliens, "Alien should be destroyed when hit by a projectile")
        self.assertEqual(self.game.score, 10, "Score should increase by 10 when an alien is destroyed")

    def test_alien_movement(self):
        # Functionalities 3: Test alien movement
        initial_positions = [alien.position for alien in self.aliens]
        for alien in self.aliens:
            alien.move()
        for i, alien in enumerate(self.aliens):
            self.assertGreater(alien.position[1], initial_positions[i][1], "Aliens should move downwards")

    def test_avoiding_alien_projectiles(self):
        # Functionalities 4: Not implemented in codebase
        self.fail("Avoiding alien projectiles functionality is not implemented in the codebase")

    def test_destroying_enemy_projectiles(self):
        # Functionalities 5: Not implemented in codebase
        self.fail("Destroying enemy projectiles functionality is not implemented in the codebase")

    def test_game_end_conditions(self):
        # Functionalities 6: Test game end when all aliens are destroyed
        self.game.aliens.clear()
        self.assertTrue(self.game.game_over, "Game should end with a victory message when all aliens are destroyed")

        # Test game end when spaceship is hit by an alien projectile
        # Not implemented in codebase
        self.fail("Game end when spaceship is hit by an alien projectile is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
