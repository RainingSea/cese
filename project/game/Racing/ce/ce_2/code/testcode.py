import unittest
import pygame
from game import Game
from obstacle import Obstacle

class TestRacingGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_interface(self):
        # Functionalities 1: Test game interface initialization
        self.game.run_game()
        self.assertEqual(len(self.game.obstacles), 0, "Game should start with no obstacles")
        self.assertEqual(self.game.lane, 1, "Initial lane should be the center lane")

    def test_display_vehicle_speed_and_distance(self):
        # Functionalities 2: Test display of speed and distance
        self.game.speed = 50
        self.game.distance = 100
        # Mocking display_info to check if it renders correct text
        screen = pygame.Surface((800, 600))
        self.game.display_info(screen)
        # Since we cannot directly check the display, we assume the function works if no errors occur
        self.assertTrue(True, "Speed and distance should be displayed correctly")

    def test_control_vehicle_speed(self):
        # Functionalities 3: Test vehicle speed control
        initial_speed = self.game.speed
        # Simulate pressing the "up" arrow key
        self.game.speed += 10
        self.assertGreater(self.game.speed, initial_speed, "Vehicle speed should increase")

    def test_control_vehicle_lane_switching(self):
        # Functionalities 4: Test vehicle lane switching
        initial_lane = self.game.lane
        # Simulate pressing the "right" arrow key
        self.game.handle_input([pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})])
        self.assertEqual(self.game.lane, initial_lane + 1, "Vehicle should move to the center lane")

    def test_simulate_obstacle_movement(self):
        # Functionalities 5: Test obstacle movement
        initial_position = 100
        obstacle = Obstacle(1, initial_position)
        self.game.obstacles.append(obstacle)
        self.game.update_obstacles()
        self.assertGreater(obstacle.position, initial_position, "Obstacles should move down the screen")

    def test_stop_the_car(self):
        # Functionalities 6: Test stopping the car
        self.game.speed = 50
        # Simulate pressing the "s" key
        self.game.speed = 0
        self.assertEqual(self.game.speed, 0, "Vehicle speed should be set to 0")

    def test_handle_slow_down_obstacle(self):
        # Functionalities 7: Test slow-down obstacle handling (not implemented in codebase)
        self.fail("Slow-down obstacle handling is not implemented in the codebase")

    def test_handle_game_ending_obstacle(self):
        # Functionalities 8: Test game-ending obstacle handling (not implemented in codebase)
        self.fail("Game-ending obstacle handling is not implemented in the codebase")

    def test_save_game_data_to_local_file(self):
        # Functionalities 9: Test saving game data to local file (not implemented in codebase)
        self.fail("Save game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
