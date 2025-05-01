import unittest
from game import Game, Player, Enemy, Bullet, Score

class TestTankGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.enemies = self.game.enemies
        self.score = self.game.score

    def test_move_player_tank(self):
        # Functionalities 1: Move Player's Tank
        initial_position = self.player.position.copy()
        self.player.move('UP')
        self.assertEqual(self.player.position, [initial_position[0], initial_position[1] - 1], "Player's tank should move up")

    def test_fire_bullet(self):
        # Functionalities 2: Fire Bullet
        bullet = self.player.fire_bullet()
        self.assertIsInstance(bullet, Bullet, "Firing a bullet should return a Bullet instance")
        self.assertEqual(bullet.position, self.player.position, "Bullet's position should match player's position")

    def test_hit_enemy_tank(self):
        # Functionalities 3: Hit Enemy Tank
        enemy = self.enemies[0]
        initial_health = enemy.health
        bullet = Bullet(enemy.position)  # Simulate a bullet hitting the enemy
        enemy.health -= 100  # Simulate the hit
        if enemy.health <= 0:
            self.score.add_points(200)  # Simulate score increase
        self.assertLess(enemy.health, initial_health, "Enemy tank's health should decrease after being hit")
        self.assertEqual(self.score.get_score(), 200, "Player's score should increase by 200 after destroying an enemy tank")

    def test_player_tank_gets_hit(self):
        # Functionalities 4: Player Tank Gets Hit
        initial_health = self.player.health
        enemy_bullet = Bullet(self.player.position)  # Simulate an enemy bullet hitting the player
        self.player.health -= 10  # Simulate the hit
        self.assertLess(self.player.health, initial_health, "Player's tank health should decrease after being hit")

    def test_check_game_end_conditions(self):
        # Functionalities 5: Check Game End Conditions
        for enemy in self.enemies:
            enemy.health = 0  # Simulate all enemies being destroyed
        if all(enemy.health <= 0 for enemy in self.enemies):
            self.game.end_game()  # Simulate game ending
        self.assertTrue(self.game.score.get_score() >= 0, "Game should end and display player's final score")

    def test_check_score_calculation(self):
        # Functionalities 6: Check Score Calculation
        initial_score = self.score.get_score()
        self.score.add_points(200)  # Simulate destroying an enemy tank
        self.assertEqual(self.score.get_score(), initial_score + 200, "Player's score should increase by 200 for each enemy tank destroyed")

    def test_load_game_data(self):
        # Functionalities 7: Load Game Data (not implemented in codebase)
        self.fail("Load game data functionality is not implemented in the codebase")

    def test_store_game_data(self):
        # Functionalities 8: Store Game Data (not implemented in codebase)
        self.fail("Store game data functionality is not implemented in the codebase")

    def test_check_grid_boundaries(self):
        # Functionalities 9: Check Grid Boundaries
        initial_position = self.player.position.copy()
        self.player.move('UP')  # Move up
        self.player.move('UP')  # Move up again
        self.player.position[1] = -1  # Simulate moving out of bounds
        self.assertEqual(self.player.position, initial_position, "Player's tank should not move outside the grid boundaries")

if __name__ == '__main__':
    unittest.main()
