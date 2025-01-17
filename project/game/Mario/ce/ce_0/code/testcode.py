import unittest
import pygame
from game import Game
from mario import Mario
from block import Block
from mushroom import Mushroom
from enemy import Enemy

class TestMarioGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()
        self.mario = self.game.mario
        self.block = self.game.block
        self.mushroom = self.game.mushroom
        self.enemy = self.game.enemies[0]

    def test_move_mario(self):
        # Functionalities 1: Move Mario
        initial_x = self.mario.x
        self.mario.move_right()
        self.assertGreater(self.mario.x, initial_x, "Mario should move right")

    def test_jump_with_mario(self):
        # Functionalities 2: Jump with Mario
        self.fail("Jump functionality is not implemented in the codebase")

    def test_interact_with_block(self):
        # Functionalities 3: Interact with a Block
        self.fail("Block interaction functionality is not implemented in the codebase")

    def test_collect_mushroom(self):
        # Functionalities 4: Collect a Mushroom
        initial_score = self.mario.score
        self.mario.x, self.mario.y = self.mushroom.x, self.mushroom.y
        self.game.check_collisions()
        self.assertEqual(self.mario.score, initial_score + 100, "Score should increase by 100 when collecting a mushroom")

    def test_encounter_enemy(self):
        # Functionalities 5: Encounter an Enemy
        initial_score = self.mario.score
        self.mario.x, self.mario.y = self.enemy.x, self.enemy.y
        self.game.check_collisions()
        self.assertEqual(self.mario.score, initial_score - 50, "Score should decrease by 50 when encountering an enemy")

    def test_reach_flagpole(self):
        # Functionalities 6: Reach the Flagpole
        self.fail("Flagpole functionality is not implemented in the codebase")

    def test_score_increases_over_time(self):
        # Functionalities 7: Score Increases Over Time
        initial_score = self.game.score
        pygame.time.delay(1000)  # Wait for one second
        self.game.update_score(1)
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase by 1 over time")

    def test_follow_mushroom_behavior(self):
        # Functionalities 8: Follow Mushroom Behavior
        initial_y = self.mushroom.y
        self.mushroom.fall()
        self.assertGreater(self.mushroom.y, initial_y, "Mushroom should fall down")

    def test_enemy_movement_behavior(self):
        # Functionalities 9: Enemy Movement Behavior
        initial_x = self.enemy.x
        self.enemy.move_randomly()
        self.assertNotEqual(self.enemy.x, initial_x, "Enemy should move randomly")

    def test_save_game_data(self):
        # Functionalities 10: Save Game Data
        self.game.save_score()
        with open('score.txt', 'r') as file:
            saved_score = int(file.read().strip())
        self.assertEqual(saved_score, self.game.score, "Game data should be saved correctly")

if __name__ == '__main__':
    unittest.main()
