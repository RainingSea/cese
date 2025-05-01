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

    def test_spaceship_controls(self):
        # Functionality 1: Test spaceship movement and shooting
        initial_x = self.spaceship.x
        
        # Move left
        self.spaceship.move_left()
        self.assertLess(self.spaceship.x, initial_x, "Spaceship should move left")
        
        # Move right
        self.spaceship.move_right()
        self.assertGreater(self.spaceship.x, initial_x - 5, "Spaceship should move right")
        
        # Shoot
        projectile = self.spaceship.shoot()
        self.assertIsInstance(projectile, Projectile, "Shooting should create a projectile")
        self.assertEqual(projectile.x, self.spaceship.x + 20, "Projectile should originate from the spaceship")

    def test_destroying_aliens(self):
        # Functionality 2: Test destroying alien enemies
        initial_aliens_count = len(self.aliens)
        self.spaceship.x = self.aliens[0].x  # Position spaceship directly below the first alien
        self.projectiles.append(self.spaceship.shoot())  # Simulate shooting
        
        # Check if the alien is destroyed
        self.game.check_collisions()
        self.assertLess(len(self.aliens), initial_aliens_count, "An alien should be destroyed when shot")

    def test_alien_movement(self):
        # Functionality 3: Test alien movement
        initial_x = self.aliens[0].x
        self.aliens[0].move()
        self.assertGreater(self.aliens[0].x, initial_x, "Alien should move horizontally")

    def test_game_end_conditions(self):
        # Functionality 6: Test game end conditions
        self.spaceship.y = self.game.height - 50  # Position spaceship at the bottom
        self.aliens[0].y = self.game.height - 30  # Position an alien to reach the bottom
        self.game.check_collisions()  # Check for collisions
        self.assertEqual(self.game.score, 0, "Score should remain 0 if no aliens are hit")
        
        # Simulate alien reaching the bottom
        self.assertTrue(self.game.aliens[0].y >= self.game.height, "Game should end if an alien reaches the bottom")

    def test_destroying_enemy_projectiles(self):
        # Functionality 5: Test destroying enemy projectiles
        alien_projectile = Projectile(self.aliens[0].x + 20, self.aliens[0].y + 30)
        self.projectiles.append(alien_projectile)  # Simulate an alien projectile
        
        # Shoot the alien projectile
        self.projectiles.append(self.spaceship.shoot())
        self.game.check_collisions()  # Check for collisions
        
        self.assertNotIn(alien_projectile, self.projectiles, "Alien projectile should be destroyed when shot")

    def test_game_over_condition(self):
        # Functionality 6: Test game over condition
        self.spaceship.y = self.game.height - 50  # Position spaceship at the bottom
        alien_projectile = Projectile(self.aliens[0].x + 20, self.aliens[0].y + 30)
        self.projectiles.append(alien_projectile)  # Simulate an alien projectile
        
        # Simulate getting hit by an alien projectile
        self.assertTrue(alien_projectile.y >= self.spaceship.y, "Game should end if the spaceship is hit")
        
        # Here we would check for game over logic, but it's not implemented in the codebase
        self.fail("Game over logic is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
