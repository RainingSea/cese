import unittest
from game import Game
from car import Car
from obstacle import Obstacle

class TestRacingGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.car = self.game.car

    def test_initialize_game_interface(self):
        # Functionalities 1: Initialize the Game Interface
        self.assertEqual(self.car.lane, 1, "Car should start in the center lane")
        self.assertEqual(len(self.game.obstacles), 0, "There should be no obstacles at the start")

    def test_display_vehicle_speed_and_distance(self):
        # Functionalities 2: Display Vehicle's Speed and Distance Traveled
        self.game.speed = 5
        self.game.update()
        self.assertEqual(self.game.distance, 5, "Distance should be updated based on speed")

    def test_control_vehicle_speed(self):
        # Functionalities 3: Control Vehicle Speed
        initial_speed = self.car.speed
        self.car.shift_right()  # Simulate pressing the "up" arrow key
        self.assertGreater(self.car.speed, initial_speed, "Car speed should increase")

    def test_control_vehicle_lane_switching(self):
        # Functionalities 4: Control Vehicle's Lane Switching
        initial_lane = self.car.lane
        self.car.move_down()  # Simulate pressing the "right" arrow key
        self.assertEqual(self.car.lane, initial_lane + 1, "Car should move to the right lane")

    def test_simulate_obstacle_movement(self):
        # Functionalities 5: Simulate Obstacle Movement
        obstacle = Obstacle(lane=1, is_hazard=False)
        self.game.obstacles.append(obstacle)
        initial_lane = obstacle.lane
        obstacle.move()
        self.assertEqual(obstacle.lane, initial_lane, "Obstacle should move down the lane")

    def test_stop_the_car(self):
        # Functionalities 6: Stop the Car
        self.car.shift_right()  # Increase speed
        self.car.stop()  # Simulate pressing the "s" key
        self.assertEqual(self.car.speed, 0, "Car speed should be 0 after stopping")

    def test_handle_slow_down_obstacle(self):
        # Functionalities 7: Handle Slow-Down Obstacle
        self.fail("Slow-down obstacle handling is not implemented in the codebase")

    def test_handle_game_ending_obstacle(self):
        # Functionalities 8: Handle Game-Ending Obstacle
        self.fail("Game-ending obstacle handling is not implemented in the codebase")

    def test_save_game_data_to_local_file(self):
        # Functionalities 9: Save Game Data to Local File
        self.fail("Save game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
