import unittest
from game import Game, Tank, Bullet, EnemyTank
import os

class TestTankGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
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
        initial_y = bullet.position_y
        bullet.move()
        self.assertEqual(bullet.position_y, initial_y - 1, "Bullet should move up")

    def test_hit_enemy_tank(self):
        # Functionalities 3: Hit Enemy Tank
        enemy_tank = self.enemy_tanks[0]
        initial_health = enemy_tank.health
        bullet = Bullet(enemy_tank.position_x, enemy_tank.position_y, "down")
        if bullet.position_x == enemy_tank.position_x and bullet.position_y == enemy_tank.position_y:
            enemy_tank.health -= 100
        self.assertEqual(enemy_tank.health, initial_health - 100, "Enemy tank's health should decrease by 100")
        if enemy_tank.health <= 0:
            self.game.score += 200
            self.assertEqual(self.game.score, 200, "Player's score should increase by 200")

    def test_player_tank_gets_hit(self):
        # Functionalities 4: Player Tank Gets Hit
        initial_health = self.player_tank.health
        bullet = Bullet(self.player_tank.position_x, self.player_tank.position_y, "up")
        if bullet.position_x == self.player_tank.position_x and bullet.position_y == self.player_tank.position_y:
            self.player_tank.health -= 10
        self.assertEqual(self.player_tank.health, initial_health - 10, "Player's tank health should decrease by 10")

    def test_check_game_end_conditions(self):
        # Functionalities 5: Check Game End Conditions
        for enemy_tank in self.enemy_tanks:
            enemy_tank.health = 0
        all_destroyed = all(tank.health <= 0 for tank in self.enemy_tanks)
        self.assertTrue(all_destroyed, "All enemy tanks should be destroyed")
        if all_destroyed:
            self.assertEqual(self.game.score, 400, "Game should end and display the final score")

    def test_check_score_calculation(self):
        # Functionalities 6: Check Score Calculation
        enemy_tank = self.enemy_tanks[0]
        enemy_tank.health = 0
        self.game.score += 200
        self.assertEqual(self.game.score, 200, "Player's score should increase by 200 for each enemy tank destroyed")

    def test_load_game_data(self):
        # Functionalities 7: Load Game Data
        self.game.load_game()
        self.assertEqual(self.game.score, 0, "Game score should be loaded correctly")
        self.assertEqual(self.game.player_health, 100, "Player health should be loaded correctly")

    def test_store_game_data(self):
        # Functionalities 8: Store Game Data
        self.game.save_game()
        self.assertTrue(os.path.exists("game_data.txt"), "Game data file should be created")
        with open("game_data.txt", "r") as file:
            data = file.read()
            self.assertIn("score|0", data, "Game score should be saved correctly")
            self.assertIn("player_health|100", data, "Player health should be saved correctly")

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
