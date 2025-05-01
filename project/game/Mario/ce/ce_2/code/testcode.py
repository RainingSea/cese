import unittest
import pygame
from game import Game
from mario import Mario
from mushroom import Mushroom
from block import Block
from enemy import Enemy

class TestMarioGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.mario = self.game.mario
        self.block = self.game.block
        self.mushroom = Mushroom(self.block.position.x, self.block.position.y - 50)
        self.enemy = Enemy()

    def test_move_mario(self):
        # Functionalities 1: Move Mario right
        initial_x = self.mario.position.x
        self.mario.move_right()
        self.assertGreater(self.mario.position.x, initial_x, "Mario should move right")

    def test_jump_mario(self):
        # Functionalities 2: Jump with Mario
        initial_y = self.mario.position.y
        self.mario.jump()
        self.assertLess(self.mario.position.y, initial_y, "Mario should jump up")
        # Simulate falling back down
        self.mario.position.y += 10  # Simulate gravity
        self.assertGreater(self.mario.position.y, initial_y, "Mario should fall back down")

    def test_interact_with_block(self):
        # Functionalities 3: Interact with a Block
        initial_score = self.mario.score
        self.mario.rect.topleft = (self.block.position.x, self.block.position.y + 50)  # Position Mario below the block
        self.mario.hit_block()
        mushroom = self.block.release_mushroom()
        self.assertEqual(mushroom.position.y, self.block.position.y - 50, "Mushroom should appear above the block")
        self.assertEqual(self.mario.score, initial_score + 10, "Score should increase by 10 when hitting a block")

    def test_collect_mushroom(self):
        # Functionalities 4: Collect a Mushroom
        self.mario.rect.topleft = (self.mushroom.position.x, self.mushroom.position.y)  # Position Mario to touch the mushroom
        initial_score = self.mario.score
        self.mario.touch_mushroom()
        self.assertEqual(self.mario.score, initial_score + 20, "Score should increase by 20 when collecting a mushroom")

    def test_encounter_enemy(self):
        # Functionalities 5: Encounter an Enemy
        self.mario.rect.topleft = (self.enemy.position.x, self.enemy.position.y)  # Position Mario to touch the enemy
        initial_score = self.mario.score
        self.mario.touch_enemy()
        self.assertEqual(self.mario.score, initial_score - 5, "Score should decrease by 5 when touching an enemy")

    def test_reach_flagpole(self):
        # Functionalities 6: Reach the Flagpole (not implemented in codebase)
        self.fail("Reach flagpole functionality is not implemented in the codebase")

    def test_score_increases_over_time(self):
        # Functionalities 7: Score Increases Over Time (not implemented in codebase)
        self.fail("Score increase over time functionality is not implemented in the codebase")

    def test_follow_mushroom_behavior(self):
        # Functionalities 8: Follow Mushroom Behavior (not implemented in codebase)
        self.fail("Mushroom behavior functionality is not implemented in the codebase")

    def test_enemy_movement_behavior(self):
        # Functionalities 9: Enemy Movement Behavior (not implemented in codebase)
        self.fail("Enemy movement behavior functionality is not implemented in the codebase")

    def test_save_game_data(self):
        # Functionalities 10: Save Game Data (not implemented in codebase)
        self.fail("Save game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
