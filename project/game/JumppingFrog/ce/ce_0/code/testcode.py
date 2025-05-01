import unittest
import pygame
from game import Game

class TestJumpingFrogGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_frog_movement_control(self):
        # Functionalities 1: Frog Movement Control
        initial_x = self.game.frog.x
        
        # Move left
        self.game.frog.move_left()
        self.assertLess(self.game.frog.x, initial_x, "Frog should move left")

        # Move right
        initial_x = self.game.frog.x
        self.game.frog.move_right()
        self.assertGreater(self.game.frog.x, initial_x, "Frog should move right")

        # Simulate 'A' key press for left movement
        self.game.frog.move_left()
        self.assertLess(self.game.frog.x, initial_x - 5, "Frog should move left with 'A' key")

        # Simulate 'D' key press for right movement
        initial_x = self.game.frog.x
        self.game.frog.move_right()
        self.assertGreater(self.game.frog.x, initial_x + 5, "Frog should move right with 'D' key")

    def test_jumping_mechanism(self):
        # Functionalities 2: Jumping Mechanism
        initial_y = self.game.frog.y
        
        # Jump
        self.game.frog.jump()
        self.assertLess(self.game.frog.y, initial_y, "Frog should jump up")

        # Simulate falling off a platform (not implemented, so we just check position)
        self.game.frog.y = 400  # Reset position
        self.game.frog.jump()
        self.assertLess(self.game.frog.y, 400, "Frog should jump off the platform")

    def test_platform_movement(self):
        # Functionalities 3: Platform Movement
        initial_x = self.game.platforms[0].x
        self.game.platforms[0].move()
        self.assertNotEqual(self.game.platforms[0].x, initial_x, "Platform should move")

    def test_game_over_condition(self):
        # Functionalities 4: Game Over Condition
        self.game.frog.y = 600  # Simulate falling into water
        self.game.update()
        self.assertEqual(self.game.score, 0, "Score should be reset after falling into water")

    def test_scoring_system(self):
        # Functionalities 5: Scoring System
        self.game.frog.y = self.game.platforms[0].y - 50  # Position frog above platform
        self.game.check_collision()
        self.assertEqual(self.game.score, 1, "Score should increase by 1 after landing on a platform")

        # Jump onto multiple platforms
        self.game.check_collision()  # Simulate landing again
        self.assertEqual(self.game.score, 2, "Score should reflect total landings")

    def test_timer_functionality(self):
        # Functionalities 6: Timer Functionality
        initial_timer = self.game.timer
        self.game.update()  # Update to decrease timer
        self.assertLess(self.game.timer, initial_timer, "Timer should decrease over time")

    def test_data_storage(self):
        # Functionalities 7: Data Storage (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
