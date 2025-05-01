import unittest
import pygame
from game import Game, Mario, Mushroom, Enemy

class TestMarioGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.mario = self.game.mario
        self.mushrooms = self.game.mushrooms
        self.enemies = self.game.enemies
        self.blocks = self.game.blocks

    def test_move_mario(self):
        # Functionalities 1: Move Mario
        initial_x = self.mario.x
        self.mario.move_right()  # Simulate pressing the right arrow key
        self.assertGreater(self.mario.x, initial_x, "Mario should move right")

    def test_jump_mario(self):
        # Functionalities 2: Jump with Mario
        initial_y = self.mario.y
        self.mario.jump()  # Simulate pressing the jump key
        self.assertLess(self.mario.y, initial_y, "Mario should jump up")
        # Simulate falling back down
        self.mario.y += 10  # Simplified fall back
        self.assertGreaterEqual(self.mario.y, initial_y, "Mario should fall back down")

    def test_interact_with_block(self):
        # Functionalities 3: Interact with a Block
        self.mario.x = self.blocks[0].x  # Position Mario below the block
        self.mario.hit_block()  # Simulate hitting the block
        mushroom = self.blocks[0].release_mushroom()
        self.mushrooms.append(mushroom)
        self.assertEqual(len(self.mushrooms), 1, "A mushroom should appear above the block")

    def test_collect_mushroom(self):
        # Functionalities 4: Collect a Mushroom
        mushroom = Mushroom(100, 250)
        self.mushrooms.append(mushroom)
        self.mario.x = mushroom.x  # Position Mario to touch the mushroom
        self.mario.touch_mushroom()  # Simulate collecting the mushroom
        self.assertEqual(len(self.mushrooms), 0, "The mushroom should disappear after being collected")
        self.assertEqual(self.mario.score, 10, "Mario's score should increase by 10")

    def test_encounter_enemy(self):
        # Functionalities 5: Encounter an Enemy
        self.mario.x = self.enemies[0].x  # Position Mario to touch the enemy
        self.mario.touch_enemy()  # Simulate touching the enemy
        self.assertEqual(self.mario.score, -5, "Mario's score should decrease by 5")

    def test_follow_mushroom_behavior(self):
        # Functionalities 8: Follow Mushroom Behavior
        mushroom = Mushroom(100, 100)
        self.mushrooms.append(mushroom)
        initial_y = mushroom.y
        mushroom.fall()  # Simulate mushroom falling
        self.assertGreater(mushroom.y, initial_y, "Mushroom should fall down")

    def test_enemy_movement_behavior(self):
        # Functionalities 9: Enemy Movement Behavior
        initial_x = self.enemies[0].x
        self.enemies[0].move_randomly()  # Simulate enemy movement
        self.assertNotEqual(self.enemies[0].x, initial_x, "Enemy should move left or right randomly")

    def test_save_game_data(self):
        # Functionalities 10: Save Game Data (not implemented in codebase)
        self.fail("Save game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
