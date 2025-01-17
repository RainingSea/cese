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
        self.mario.move_right()
        self.assertEqual(self.mario.x, initial_x + 5, "Mario should move right by 5 units")

    def test_jump_with_mario(self):
        # Functionalities 2: Jump with Mario
        initial_y = self.mario.y
        self.mario.jump()
        self.assertEqual(self.mario.y, initial_y - 10, "Mario should jump up by 10 units")

    def test_interact_with_block(self):
        # Functionalities 3: Interact with a Block
        # Not implemented in codebase
        self.fail("Interact with a Block functionality is not implemented in the codebase")

    def test_collect_mushroom(self):
        # Functionalities 4: Collect a Mushroom
        initial_score = self.mario.score
        self.mario.touch_mushroom()
        self.assertEqual(self.mario.score, initial_score + 50, "Mario should gain 50 points for touching a mushroom")

    def test_encounter_enemy(self):
        # Functionalities 5: Encounter an Enemy
        initial_score = self.mario.score
        self.mario.touch_enemy()
        self.assertEqual(self.mario.score, initial_score - 20, "Mario should lose 20 points for touching an enemy")

    def test_reach_flagpole(self):
        # Functionalities 6: Reach the Flagpole
        # Not implemented in codebase
        self.fail("Reach the Flagpole functionality is not implemented in the codebase")

    def test_score_increases_over_time(self):
        # Functionalities 7: Score Increases Over Time
        # Not implemented in codebase
        self.fail("Score Increases Over Time functionality is not implemented in the codebase")

    def test_follow_mushroom_behavior(self):
        # Functionalities 8: Follow Mushroom Behavior
        initial_y = self.mushroom.y
        self.mushroom.fall()
        self.assertEqual(self.mushroom.y, initial_y + 5, "Mushroom should fall down by 5 units")

    def test_enemy_movement_behavior(self):
        # Functionalities 9: Enemy Movement Behavior
        initial_x = self.enemy.x
        self.enemy.move()
        self.assertEqual(self.enemy.x, initial_x + 2, "Enemy should move right by 2 units")

    def test_save_game_data(self):
        # Functionalities 10: Save Game Data
        self.game.save_data()
        with open('game_data.txt', 'r') as f:
            data = f.read().strip()
        self.assertEqual(data, f'score|{self.mario.score}', "Game data should be saved correctly in the text file")

if __name__ == '__main__':
    unittest.main()
