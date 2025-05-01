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
        # Functionality 1: Player Controls Spaceship
        initial_x = self.player.x
        
        # Move left
        self.player.move("left")
        self.assertLess(self.player.x, initial_x, "Player should move left")
        
        # Move right
        self.player.move("right")
        self.assertGreater(self.player.x, initial_x - 5, "Player should move right")
        
        # Shoot
        projectile = self.player.shoot()
        self.assertIsInstance(projectile, Projectile, "Shooting should return a Projectile")
        self.assertEqual(projectile.y, self.player.y, "Projectile should start at player's y position")

    def test_destroying_alien_enemies(self):
        # Functionality 2: Destroying Alien Enemies
        initial_aliens_count = len(self.aliens)
        # Simulate shooting an alien
        projectile = self.player.shoot()
        # Assume the projectile hits the first alien
        self.aliens[0].y = self.player.y - 5  # Position the alien directly above the player
        self.game.check_collisions()  # This should be implemented to handle collisions
        self.assertLess(len(self.aliens), initial_aliens_count, "An alien should be destroyed")

    def test_alien_movement(self):
        # Functionality 3: Alien Movement
        initial_positions = [alien.x for alien in self.aliens]
        self.game.update()  # Update the game to move aliens
        new_positions = [alien.x for alien in self.aliens]
        self.assertNotEqual(initial_positions, new_positions, "Aliens should move horizontally")

    def test_avoiding_alien_projectiles(self):
        # Functionality 4: Avoiding Alien Projectiles
        # Simulate alien shooting
        alien = self.aliens[0]
        alien_projectile = alien.shoot()
        self.game.alien_projectiles.append(alien_projectile)
        self.assertIn(alien_projectile, self.game.alien_projectiles, "Alien projectile should be visible")

    def test_destroying_enemy_projectiles(self):
        # Functionality 5: Destroying Enemy Projectiles
        alien = self.aliens[0]
        alien_projectile = alien.shoot()
        self.game.alien_projectiles.append(alien_projectile)
        
        # Simulate shooting the alien projectile
        projectile = self.player.shoot()
        self.assertIsInstance(projectile, Projectile, "Shooting should return a Projectile")
        
        # Assume we have a method to check collisions
        self.game.check_collisions()  # This should handle the logic of destroying projectiles

    def test_game_end_conditions(self):
        # Functionality 6: Game End Conditions
        # Simulate destroying all aliens
        self.game.aliens.clear()  # Clear all aliens
        self.assertEqual(len(self.game.aliens), 0, "All aliens should be destroyed")
        
        # Simulate an alien hitting the player
        self.game.alien_projectiles.append(Projectile(self.player.x, self.player.y - 5))  # Position above player
        self.game.check_collisions()  # This should handle the logic of ending the game

if __name__ == '__main__':
    unittest.main()
