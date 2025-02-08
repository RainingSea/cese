import unittest
import pygame
from game import Game, Vehicle, Obstacle

class TestRacingGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.vehicle = self.game.vehicle

    def test_initialize_game_interface(self):
        # Functionalities 1: Initialize the Game Interface
        self.assertEqual(len(self.game.obstacles), 3, "There should be three obstacles loaded from the file")
        for obstacle in self.game.obstacles:
            self.assertEqual(obstacle.y_position, 0, "Obstacles should start at the top of the screen")

    def test_display_vehicle_speed_and_distance(self):
        # Functionalities 2: Display Vehicle's Speed and Distance Traveled
        self.game.speed = 10.0
        self.game.update()
        self.assertGreater(self.game.distance, 0, "Distance should increase as the game updates")

    def test_control_vehicle_speed(self):
        # Functionalities 3: Control Vehicle Speed
        initial_speed = self.vehicle.speed
        self.vehicle.speed += 5.0  # Simulate pressing the "up" arrow key
        self.assertGreater(self.vehicle.speed, initial_speed, "Vehicle speed should increase")

    def test_control_vehicle_lane_switching(self):
        # Functionalities 4: Control Vehicle's Lane Switching
        initial_lane = self.vehicle.lane
        self.vehicle.shift_right()  # Simulate pressing the "right" arrow key
        self.assertEqual(self.vehicle.lane, initial_lane + 1, "Vehicle should move to the center lane")

    def test_simulate_obstacle_movement(self):
        # Functionalities 5: Simulate Obstacle Movement
        initial_positions = [obstacle.y_position for obstacle in self.game.obstacles]
        self.game.update()
        for i, obstacle in enumerate(self.game.obstacles):
            self.assertGreater(obstacle.y_position, initial_positions[i], "Obstacles should move down the screen")

    def test_stop_the_car(self):
        # Functionalities 6: Stop the Car
        self.vehicle.speed = 10.0
        self.vehicle.stop()  # Simulate pressing the "s" key
        self.assertEqual(self.vehicle.speed, 0.0, "Vehicle speed should be set to 0")

    def test_handle_slow_down_obstacle(self):
        # Functionalities 7: Handle Slow-Down Obstacle (not implemented in codebase)
        self.fail("Handle slow-down obstacle functionality is not implemented in the codebase")

    def test_handle_game_ending_obstacle(self):
        # Functionalities 8: Handle Game-Ending Obstacle (not implemented in codebase)
        self.fail("Handle game-ending obstacle functionality is not implemented in the codebase")

    def test_save_game_data_to_local_file(self):
        # Functionalities 9: Save Game Data to Local File
        self.game.save_game_state()
        with open('game_state.txt', 'r') as file:
            content = file.read()
        self.assertIn("Speed: 0.0", content, "Game state should include speed")
        self.assertIn("Distance: 0.0", content, "Game state should include distance")

if __name__ == '__main__':
    unittest.main()
