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
        self.mushroom = self.game.mushrooms[0]
        self.enemy = self.game.enemies[0]

    def test_move_mario(self):
        # Functionalities 1: Move Mario
        initial_x = self.mario.x
        self.mario.move_right()  # Simulate pressing the right arrow key
        self.assertGreater(self.mario.x, initial_x, "Mario should move right")

    def test_jump_mario(self):
        # Functionalities 2: Jump with Mario
        initial_y = self.mario.y
        self.mario.jump()  # Simulate pressing the up arrow key
        self.mario.update()  # Update to simulate the jump
        self.assertLess(self.mario.y, initial_y, "Mario should move upward when jumping")

    def test_interact_with_block(self):
        # Functionalities 3: Interact with a Block
        initial_score = self.mario.score
        self.mario.hit_block()  # Simulate hitting a block
        self.assertEqual(self.mario.score, initial_score + 100, "Score should increase by 100 when hitting a block")

    def test_collect_mushroom(self):
        # Functionalities 4: Collect a Mushroom
        initial_score = self.mario.score
        self.mario.collect_mushroom()  # Simulate collecting a mushroom
        self.assertEqual(self.mario.score, initial_score + 1000, "Score should increase by 1000 when collecting a mushroom")

    def test_encounter_enemy(self):
        # Functionalities 5: Encounter an Enemy
        initial_lives = 3  # Assume Mario starts with 3 lives
        self.mario.lives = initial_lives
        self.mario.x = self.enemy.x  # Position Mario to collide with the enemy
        self.mario.update()  # Update to simulate the collision
        self.assertEqual(self.mario.lives, initial_lives - 1, "Mario should lose a life when encountering an enemy")

    def test_reach_flagpole(self):
        # Functionalities 6: Reach the Flagpole
        initial_score = self.mario.score
        self.mario.touch_flagpole()  # Simulate touching the flagpole
        self.assertEqual(self.mario.score, initial_score + 10000, "Score should increase by 10000 when reaching the flagpole")

    def test_score_increases_over_time(self):
        # Functionalities 7: Score Increases Over Time
        initial_score = self.mario.score
        pygame.time.delay(1000)  # Wait for one second
        self.game.update()  # Update the game to reflect score increase
        self.assertEqual(self.mario.score, initial_score + 1, "Score should increase by 1 after one second")

    def test_follow_mushroom_behavior(self):
        # Functionalities 8: Follow Mushroom Behavior
        initial_y = self.mushroom.y
        self.mushroom.fall()  # Simulate mushroom falling
        self.assertGreater(self.mushroom.y, initial_y, "Mushroom should fall downwards")

    def test_enemy_movement_behavior(self):
        # Functionalities 9: Enemy Movement Behavior
        initial_x = self.enemy.x
        self.enemy.move()  # Simulate enemy movement
        self.assertNotEqual(self.enemy.x, initial_x, "Enemy should move left or right")

    def test_save_game_data(self):
        # Functionalities 10: Save Game Data
        self.fail("Save game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
