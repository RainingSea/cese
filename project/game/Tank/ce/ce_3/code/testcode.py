import unittest
from game import Game, PlayerTank, EnemyTank, Bullet

class TestTankGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_tank = self.game.player_tank
        self.enemy_tank = self.game.enemy_tanks[0]

    def test_move_player_tank(self):
        # Functionalities 1: Move Player's Tank
        initial_y = self.player_tank.position_y
        self.player_tank.move('up')
        self.assertEqual(self.player_tank.position_y, initial_y - 1, "Player's tank should move one cell up")

    def test_fire_bullet(self):
        # Functionalities 2: Fire Bullet
        initial_bullet_count = len(self.game.bullets)
        bullet = self.player_tank.fire()
        self.game.bullets.append(bullet)
        self.assertEqual(len(self.game.bullets), initial_bullet_count + 1, "A bullet should be fired and added to the bullets list")

    def test_hit_enemy_tank(self):
        # Functionalities 3: Hit Enemy Tank
        bullet = Bullet(self.enemy_tank.position_x, self.enemy_tank.position_y, 'up')
        self.game.bullets.append(bullet)
        initial_health = self.enemy_tank.health
        self.game.check_collisions()
        self.assertLess(self.enemy_tank.health, initial_health, "Enemy tank's health should decrease when hit by a bullet")

    def test_player_tank_gets_hit(self):
        # Functionalities 4: Player Tank Gets Hit
        initial_health = self.player_tank.health
        self.player_tank.take_damage(10)
        self.assertEqual(self.player_tank.health, initial_health - 10, "Player's tank health should decrease by 10 points when hit")

    def test_check_game_end_conditions(self):
        # Functionalities 5: Check Game End Conditions
        self.game.enemy_tanks = []  # Simulate all enemy tanks destroyed
        self.game.end_game()
        with open('score.txt', 'r') as f:
            score = int(f.read())
        self.assertEqual(score, self.game.player_score, "Game should end and display the player's final score")

    def test_check_score_calculation(self):
        # Functionalities 6: Check Score Calculation
        initial_score = self.game.player_score
        self.enemy_tank.take_damage(100)  # Simulate destroying an enemy tank
        self.game.player_score += 200
        self.assertEqual(self.game.player_score, initial_score + 200, "Player's score should increase by 200 points for each enemy tank destroyed")

    def test_load_game_data(self):
        # Functionalities 7: Load Game Data (not implemented in codebase)
        self.fail("Load game data functionality is not implemented in the codebase")

    def test_store_game_data(self):
        # Functionalities 8: Store Game Data (not implemented in codebase)
        self.fail("Store game data functionality is not implemented in the codebase")

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
