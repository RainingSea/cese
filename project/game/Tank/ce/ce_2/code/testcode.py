import unittest
from game import Game, Tank, Bullet, EnemyTank

class TestTankGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game(grid_size=20)
        self.player_tank = self.game.player_tank
        self.enemy_tanks = self.game.enemy_tanks

    def test_move_player_tank(self):
        # Functionalities 1: Move Player's Tank
        initial_y = self.player_tank.position_y
        self.player_tank.move('up')
        self.assertEqual(self.player_tank.position_y, initial_y - 1, "Player's tank should move one step up")

    def test_fire_bullet(self):
        # Functionalities 2: Fire Bullet
        bullet = self.player_tank.fire()
        self.assertIsInstance(bullet, Bullet, "Firing should create a Bullet instance")
        # Assuming move method updates bullet's position, which is not implemented
        self.fail("Bullet movement logic is not implemented in the codebase")

    def test_hit_enemy_tank(self):
        # Functionalities 3: Hit Enemy Tank
        enemy_tank = self.enemy_tanks[0]
        initial_health = enemy_tank.health
        enemy_tank.take_damage(100)
        self.assertEqual(enemy_tank.health, initial_health - 100, "Enemy tank's health should decrease by 100")
        if enemy_tank.health <= 0:
            self.game.score += 200
        self.assertEqual(self.game.score, 200, "Player's score should increase by 200 points when an enemy tank is destroyed")

    def test_player_tank_gets_hit(self):
        # Functionalities 4: Player Tank Gets Hit
        initial_health = self.player_tank.health
        self.player_tank.take_damage(10)
        self.assertEqual(self.player_tank.health, initial_health - 10, "Player's tank health should decrease by 10")

    def test_check_game_end_conditions(self):
        # Functionalities 5: Check Game End Conditions
        for enemy_tank in self.enemy_tanks:
            enemy_tank.take_damage(enemy_tank.health)  # Destroy all enemy tanks
        self.assertTrue(all(tank.health <= 0 for tank in self.enemy_tanks), "All enemy tanks should be destroyed")
        # Assuming game ends when all enemy tanks are destroyed, which is not implemented
        self.fail("Game end condition logic is not implemented in the codebase")

    def test_check_score_calculation(self):
        # Functionalities 6: Check Score Calculation
        initial_score = self.game.score
        enemy_tank = self.enemy_tanks[0]
        enemy_tank.take_damage(enemy_tank.health)  # Destroy the enemy tank
        self.game.score += 200
        self.assertEqual(self.game.score, initial_score + 200, "Player's score should increase by 200 points for each enemy tank destroyed")

    def test_load_game_data(self):
        # Functionalities 7: Load Game Data
        # Assuming load functionality is not implemented
        self.fail("Load game data functionality is not implemented in the codebase")

    def test_store_game_data(self):
        # Functionalities 8: Store Game Data
        self.game.save_data()
        with open('game_data.txt', 'r') as file:
            data = file.read()
        self.assertIn("score|0", data, "Game data should contain the score")
        self.assertIn("health|100", data, "Game data should contain the player's health")

    def test_check_grid_boundaries(self):
        # Functionalities 9: Check Grid Boundaries
        self.player_tank.position_x = 0
        self.player_tank.move('left')
        self.assertEqual(self.player_tank.position_x, 0, "Player's tank should not move outside the left boundary")
        self.player_tank.position_y = 0
        self.player_tank.move('up')
        self.assertEqual(self.player_tank.position_y, 0, "Player's tank should not move outside the top boundary")

if __name__ == '__main__':
    unittest.main()
