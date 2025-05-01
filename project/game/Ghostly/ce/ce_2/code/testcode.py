import unittest
from game import Game, Ghost, Monster

class TestGhostlyGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.ghost = self.game.ghost
        self.monster = self.game.monster

    def test_control_ghost_movement(self):
        # Functionalities 1: Control the Ghost Movement
        initial_position = (self.ghost.x, self.ghost.y)
        self.ghost.move("UP")
        self.assertEqual((self.ghost.x, self.ghost.y), (initial_position[0], initial_position[1] - 1), "Ghost should move up")

    def test_collision_with_walls(self):
        # Functionalities 2: Collision with Walls
        initial_position = (self.ghost.x, self.ghost.y)
        self.ghost.move("LEFT")  # Assuming the wall is at (50, 50)
        self.assertEqual((self.ghost.x, self.ghost.y), initial_position, "Ghost should not pass through the wall")

    def test_eating_pellets(self):
        # Functionalities 3: Eating Pellets
        initial_pellet_count = len(self.game.pellets)
        self.ghost.x, self.ghost.y = self.game.pellets[0].x, self.game.pellets[0].y  # Move ghost to pellet position
        self.ghost.eatPellet()  # Assuming this method would remove the pellet
        self.assertEqual(len(self.game.pellets), initial_pellet_count - 1, "Pellet should be eaten and removed from the game")

    def test_eating_superpellets(self):
        # Functionalities 4: Eating Superpellets
        initial_superpower_state = self.ghost.hasSuperpower
        self.ghost.x, self.ghost.y = self.game.superpellets[0].x, self.game.superpellets[0].y  # Move ghost to superpellet position
        self.ghost.eatSuperPellet()  # Eat the superpellet
        self.assertTrue(self.ghost.hasSuperpower, "Ghost should gain superpower after eating superpellet")

    def test_ghost_collision_with_superpellet_powerup(self):
        # Functionalities 5: Ghost Collision with Superpellet Power-up
        self.ghost.hasSuperpower = True  # Activate superpower
        other_ghost = Ghost(1, 1)  # Create another ghost
        initial_position = (other_ghost.x, other_ghost.y)
        self.ghost.x, self.ghost.y = initial_position  # Move ghost to collide with another ghost
        # Assuming there's a method to eat another ghost
        self.ghost.eatGhost(other_ghost)  # This method would need to be implemented
        self.assertNotEqual((other_ghost.x, other_ghost.y), initial_position, "Other ghost should be eaten and disappear")

    def test_invalid_move_collision(self):
        # Functionalities 6: Invalid Move Collision
        other_ghost = Ghost(1, 1)  # Create another ghost
        initial_position = (self.ghost.x, self.ghost.y)
        self.ghost.x, self.ghost.y = initial_position  # Move ghost to collide with another ghost
        self.ghost.move("UP")  # Attempt to move into another ghost without superpower
        self.assertEqual((self.ghost.x, self.ghost.y), initial_position, "Ghost should not move into another ghost without superpower")

    def test_activation_of_monster(self):
        # Functionalities 7: Activation of the Monster
        for _ in range(50):
            self.game.update()  # Simulate game ticks
        self.assertEqual((self.monster.x, self.monster.y), (1, 1), "Monster should be activated and appear at position [1,1]")

    def test_monster_collision_with_player_ghost(self):
        # Functionalities 8: Monster Collision with Player’s Ghost
        self.ghost.x, self.ghost.y = self.monster.x, self.monster.y  # Move ghost to monster position
        # Assuming there's a method to handle collision with monster
        self.game.checkCollisions()  # This method would need to handle game over
        self.assertFalse(self.game.running, "Game should end when monster collides with ghost")

    def test_end_game_conditions(self):
        # Functionalities 9: End of Game Conditions
        other_ghost = Ghost(1, 1)  # Create another ghost
        self.ghost.x, self.ghost.y = other_ghost.x, other_ghost.y  # Move ghost to collide with another ghost
        self.ghost.hasSuperpower = False  # Ensure superpower is not active
        self.game.checkCollisions()  # Check for collisions
        self.assertFalse(self.game.running, "Game should end when ghost collides with another ghost without superpower")

if __name__ == '__main__':
    unittest.main()
