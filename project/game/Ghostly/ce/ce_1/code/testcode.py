import unittest
import pygame
from game import Game, PlayerGhost, Pellet, Wall, Monster

class TestGhostlyGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player_ghost = self.game.player_ghost
        self.pellets = self.game.pellets
        self.walls = self.game.walls
        self.monster = self.game.monster

    def test_control_ghost_movement(self):
        # Functionalities 1: Control the Ghost Movement
        initial_position = self.player_ghost.position.copy()
        self.player_ghost.move("UP")
        self.assertEqual(self.player_ghost.position, [initial_position[0], initial_position[1] - 1], "Ghost should move up")

    def test_collision_with_walls(self):
        # Functionalities 2: Collision with Walls
        initial_position = self.player_ghost.position.copy()
        self.player_ghost.position = [3, 3]  # Position the ghost at a wall
        self.player_ghost.move("LEFT")  # Attempt to move left into the wall
        self.assertEqual(self.player_ghost.position, initial_position, "Ghost should not pass through the wall")

    def test_eating_pellets(self):
        # Functionalities 3: Eating Pellets
        initial_pellet_count = len(self.pellets)
        self.player_ghost.position = self.pellets[0].position  # Move to the first pellet
        self.player_ghost.eat_pellet()  # Simulate eating the pellet
        self.assertEqual(len(self.pellets), initial_pellet_count - 1, "Pellet should be eaten and removed from the game")

    def test_eating_superpellets(self):
        # Functionalities 4: Eating Superpellets
        self.player_ghost.position = [1, 1]  # Assume a superpellet is at this position
        self.player_ghost.eat_superpellet()  # Simulate eating a superpellet
        self.assertTrue(self.player_ghost.has_superpellet, "Ghost should gain superpellet ability")

    def test_ghost_collision_with_superpellet_powerup(self):
        # Functionalities 5: Ghost Collision with Superpellet Power-up
        self.player_ghost.has_superpellet = True  # Activate superpellet
        other_ghost = PlayerGhost()  # Create another ghost
        other_ghost.position = self.player_ghost.position  # Position it at the player's ghost
        # Simulate collision
        self.assertNotEqual(other_ghost.position, self.player_ghost.position, "Other ghost should be eaten and disappear")

    def test_invalid_move_collision(self):
        # Functionalities 6: Invalid Move Collision
        other_ghost = PlayerGhost()  # Create another ghost
        other_ghost.position = self.player_ghost.position  # Position it at the player's ghost
        initial_position = self.player_ghost.position.copy()
        self.player_ghost.move("LEFT")  # Attempt to move into another ghost
        self.assertEqual(self.player_ghost.position, initial_position, "Ghost should not move into another ghost without power-up")

    def test_activation_of_monster(self):
        # Functionalities 7: Activation of the Monster
        for _ in range(50):  # Simulate 50 game ticks
            self.game.ticks += 1
        self.assertEqual(self.game.monster.position, [1, 1], "Monster should be activated and appear at position [1,1]")

    def test_monster_collision_with_player_ghost(self):
        # Functionalities 8: Monster Collision with Player’s Ghost
        self.player_ghost.position = [1, 1]  # Position the ghost where the monster will be
        self.game.monster.position = self.player_ghost.position  # Position monster at the ghost
        # Simulate collision
        self.assertFalse(self.game.running, "Game should end when monster collides with player's ghost")

    def test_end_game_conditions(self):
        # Functionalities 9: End of Game Conditions
        other_ghost = PlayerGhost()  # Create another ghost
        other_ghost.position = self.player_ghost.position  # Position it at the player's ghost
        self.player_ghost.has_superpellet = False  # Ensure superpellet is not active
        # Simulate collision
        self.assertFalse(self.game.running, "Game should end when player's ghost collides with another ghost without superpellet")

if __name__ == '__main__':
    unittest.main()
