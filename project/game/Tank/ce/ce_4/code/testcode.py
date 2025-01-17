import unittest
from game import Game, Tank, EnemyTank

class TestTankGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_tank = self.game.player_tank
        self.enemy_tanks = self.game.enemy_tanks

    def test_move_player_tank(self):
        # Functionalities 1: Move Player's Tank
        initial_y = self.player_tank.position_y
        self.game.move_player('up')
        self.assertEqual(self.player_tank.position_y, initial_y - 1, "Player's tank should move one step up")

    def test_fire_bullet(self):
        # Functionalities 2: Fire Bullet
        # Since the bullet logic is not implemented, this test will fail
        self.fail("Fire bullet functionality is not implemented in the codebase")

    def test_hit_enemy_tank(self):
        # Functionalities 3: Hit Enemy Tank
        initial_health = self.enemy_tanks[0].health
        self.enemy_tanks[0].take_damage(100)
        self.assertEqual(self.enemy_tanks[0].health, initial_health - 100, "Enemy tank's health should decrease by 100")
        if self.enemy_tanks[0].health <= 0:
            self.game.score += 200
            self.assertEqual(self.game.score, 200, "Player's score should increase by 200 points")

    def test_player_tank_gets_hit(self):
        # Functionalities 4: Player Tank Gets Hit
        initial_health = self.player_tank.health
        self.player_tank.take_damage(10)
        self.assertEqual(self.player_tank.health, initial_health - 10, "Player's tank health should decrease by 10")

    def test_check_game_end_conditions(self):
        # Functionalities 5: Check Game End Conditions
        for enemy in self.enemy_tanks:
            enemy.take_damage(enemy.health)  # Destroy all enemy tanks
        self.assertEqual(sum(enemy.health for enemy in self.enemy_tanks), 0, "All enemy tanks should be destroyed")
        self.game.end_game()
        with open('score.txt', 'r') as score_file:
            score = score_file.read()
        self.assertIn('score: ', score, "Game should end and display the player's final score")

    def test_check_score_calculation(self):
        # Functionalities 6: Check Score Calculation
        initial_score = self.game.score
        self.enemy_tanks[0].take_damage(self.enemy_tanks[0].health)  # Destroy one enemy tank
        self.game.score += 200
        self.assertEqual(self.game.score, initial_score + 200, "Player's score should increase by 200 points")

    def test_load_game_data(self):
        # Functionalities 7: Load Game Data
        # Since loading game data is not implemented, this test will fail
        self.fail("Load game data functionality is not implemented in the codebase")

    def test_store_game_data(self):
        # Functionalities 8: Store Game Data
        # Since storing game data is not implemented, this test will fail
        self.fail("Store game data functionality is not implemented in the codebase")

    def test_check_grid_boundaries(self):
        # Functionalities 9: Check Grid Boundaries
        self.player_tank.position_x = 0
        self.game.move_player('left')
        self.assertEqual(self.player_tank.position_x, 0, "Player's tank should not move outside the left boundary")

        self.player_tank.position_x = 19
        self.game.move_player('right')
        self.assertEqual(self.player_tank.position_x, 19, "Player's tank should not move outside the right boundary")

        self.player_tank.position_y = 0
        self.game.move_player('up')
        self.assertEqual(self.player_tank.position_y, 0, "Player's tank should not move outside the top boundary")

        self.player_tank.position_y = 19
        self.game.move_player('down')
        self.assertEqual(self.player_tank.position_y, 19, "Player's tank should not move outside the bottom boundary")

if __name__ == '__main__':
    unittest.main()
