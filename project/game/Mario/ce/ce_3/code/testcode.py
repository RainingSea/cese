import unittest
import pygame
from game import Game
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy

class TestMarioGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.mario = self.game.mario
        self.mushrooms = self.game.mushrooms
        self.enemies = self.game.enemies

    def test_move_mario(self):
        # Functionalities 1: Move Mario
        initial_x = self.mario.x
        self.mario.move('right')
        self.assertGreater(self.mario.x, initial_x, "Mario should move right")

    def test_jump_with_mario(self):
        # Functionalities 2: Jump with Mario
        initial_y = self.mario.y
        self.mario.jump()
        self.assertNotEqual(self.mario.velocity, 0, "Mario should have a velocity for jumping")

    def test_interact_with_block(self):
        # Functionalities 3: Interact with a Block (not implemented in codebase)
        self.fail("Interact with a Block functionality is not implemented in the codebase")

    def test_collect_mushroom(self):
        # Functionalities 4: Collect a Mushroom
        mushroom = self.mushrooms[0]
        self.mario.x, self.mario.y = mushroom.x, mushroom.y
        self.game.update_game_logic()
        self.assertNotIn(mushroom, self.game.mushrooms, "Mushroom should disappear after collection")
        self.assertEqual(self.game.score, 10, "Score should increase by 10 after collecting a mushroom")

    def test_encounter_enemy(self):
        # Functionalities 5: Encounter an Enemy (not fully implemented in codebase)
        self.fail("Encounter an Enemy functionality is not fully implemented in the codebase")

    def test_reach_flagpole(self):
        # Functionalities 6: Reach the Flagpole (not implemented in codebase)
        self.fail("Reach the Flagpole functionality is not implemented in the codebase")

    def test_score_increases_over_time(self):
        # Functionalities 7: Score Increases Over Time (not implemented in codebase)
        self.fail("Score Increases Over Time functionality is not implemented in the codebase")

    def test_follow_mushroom_behavior(self):
        # Functionalities 8: Follow Mushroom Behavior
        mushroom = self.mushrooms[0]
        initial_y = mushroom.y
        mushroom.fall()
        self.assertGreater(mushroom.y, initial_y, "Mushroom should fall downwards")

    def test_enemy_movement_behavior(self):
        # Functionalities 9: Enemy Movement Behavior (not fully implemented in codebase)
        self.fail("Enemy Movement Behavior functionality is not fully implemented in the codebase")

    def test_save_game_data(self):
        # Functionalities 10: Save Game Data
        self.game.save_data()
        with open('game_data.txt', 'r') as file:
            saved_score = int(file.readline().strip())
        self.assertEqual(saved_score, self.game.score, "Game data should be saved correctly")

if __name__ == '__main__':
    unittest.main()
