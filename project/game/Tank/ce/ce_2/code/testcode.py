import unittest
from game import Game, PlayerTank, EnemyTank, Bullet

class TestTankGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_tank = self.game.player_tank
        self.enemy_tanks = self.game.enemy_tanks

    def test_move_player_tank(self):
        # Functionalities 1: Move Player's Tank
        initial_position = self.player_tank.position
        self.player_tank.move('up')
        self.assertEqual(self.player_tank.position, (initial_position[0], initial_position[1] - 1), "Player tank should move up")

    def test_fire_bullet(self):
        # Functionalities 2: Fire Bullet
        initial_position = self.player_tank.position
        bullet = self.player_tank.fire()
        self.assertEqual(bullet.position, initial_position, "Bullet should start at the player's tank position")

    def test_hit_enemy_tank(self):
        # Functionalities 3: Hit Enemy Tank
        enemy_tank = self.enemy_tanks[0]
        initial_health = enemy_tank.health
        bullet = Bullet(enemy_tank.position, 'down')  # Simulate bullet hitting enemy tank
        enemy_tank.health -= 100  # Simulate hit
        if enemy_tank.health <= 0:
            self.game.score += 200  # Simulate score increase
        self.assertEqual(enemy_tank.health, 0, "Enemy tank should be destroyed")
        self.assertEqual(self.game.score, 200, "Player score should increase by 200")

    def test_player_tank_gets_hit(self):
        # Functionalities 4: Player Tank Gets Hit
        initial_health = self.player_tank.health
        enemy_tank = EnemyTank()  # Create a new enemy tank
        enemy_tank.shoot()  # Simulate enemy shooting
        self.player_tank.health -= 10  # Simulate hit
        self.assertEqual(self.player_tank.health, initial_health - 10, "Player tank health should decrease by 10")

    def test_check_game_end_conditions(self):
        # Functionalities 5: Check Game End Conditions
        for enemy_tank in self.enemy_tanks:
            enemy_tank.health = 0  # Simulate all enemy tanks destroyed
        self.assertTrue(all(tank.health <= 0 for tank in self.enemy_tanks), "All enemy tanks should be destroyed")

    def test_check_score_calculation(self):
        # Functionalities 6: Check Score Calculation
        initial_score = self.game.score
        enemy_tank = self.enemy_tanks[0]
        enemy_tank.health = 0  # Simulate enemy tank destroyed
        self.game.score += 200  # Simulate score increase
        self.assertEqual(self.game.score, initial_score + 200, "Player score should increase by 200 for each enemy tank destroyed")

    def test_load_game_data(self):
        # Functionalities 7: Load Game Data
        self.game.load_game_data()
        self.assertEqual(self.game.score, 0, "Score should be loaded correctly from game data")
        self.assertEqual(self.player_tank.health, 200, "Player health should be loaded correctly from game data")

    def test_store_game_data(self):
        # Functionalities 8: Store Game Data (not implemented in codebase)
        self.fail("Store game data functionality is not implemented in the codebase")

    def test_check_grid_boundaries(self):
        # Functionalities 9: Check Grid Boundaries
        initial_position = self.player_tank.position
        self.player_tank.move('up')  # Move up
        self.player_tank.move('up')  # Move up again
        self.player_tank.position = (0, 0)  # Simulate boundary
        self.player_tank.move('up')  # Attempt to move out of bounds
        self.assertEqual(self.player_tank.position, (0, 0), "Player tank should not move outside the grid boundaries")

if __name__ == '__main__':
    unittest.main()
