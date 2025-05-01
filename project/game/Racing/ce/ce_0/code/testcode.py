import unittest
import pygame
from game import Game, Vehicle, Obstacle

class TestRacingGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.vehicle = self.game.vehicle

    def test_initialize_game_interface(self):
        # Functionalities 1: Check if the game initializes correctly
        self.assertEqual(len(self.game.obstacles), 0, "Game should start with no obstacles")

    def test_display_vehicle_speed_and_distance(self):
        # Functionalities 2: Check if speed and distance are displayed correctly
        self.game.speed = 10
        self.game.distance = 50
        self.assertEqual(self.game.speed, 10, "Speed should be 10")
        self.assertEqual(self.game.distance, 50, "Distance should be 50")

    def test_control_vehicle_speed(self):
        # Functionalities 3: Test speed control with the up arrow key
        initial_speed = self.game.speed
        self.game.handle_input([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
        self.assertGreater(self.game.speed, initial_speed, "Speed should increase when up arrow is pressed")

    def test_control_vehicle_lane_switching(self):
        # Functionalities 4: Test lane switching with the right arrow key
        initial_lane = self.vehicle.lane
        self.game.handle_input([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)])
        self.assertEqual(self.vehicle.lane, initial_lane + 1, "Vehicle should move to the right lane")

    def test_simulate_obstacle_movement(self):
        # Functionalities 5: Test obstacle movement
        obstacle = Obstacle()
        self.game.obstacles.append(obstacle)
        initial_position = obstacle.position
        obstacle.move()
        self.assertGreater(obstacle.position, initial_position, "Obstacle should move down the screen")

    def test_stop_the_car(self):
        # Functionalities 6: Test stopping the car with 's' key
        self.game.speed = 20
        self.game.handle_input([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)])
        self.assertEqual(self.game.speed, 0, "Vehicle speed should be set to 0 when 's' is pressed")

    def test_handle_slow_down_obstacle(self):
        # Functionalities 7: Test collision with a slow-down obstacle
        obstacle = Obstacle()
        obstacle.type = True  # Slow down obstacle
        self.game.obstacles.append(obstacle)
        self.vehicle.position = obstacle.position  # Simulate collision
        initial_speed = self.game.speed
        self.game.update()
        self.assertLess(self.game.speed, initial_speed, "Vehicle speed should decrease when colliding with a slow-down obstacle")

    def test_handle_game_ending_obstacle(self):
        # Functionalities 8: Test collision with a game-ending obstacle
        obstacle = Obstacle()
        obstacle.type = False  # Game-ending obstacle
        self.game.obstacles.append(obstacle)
        self.vehicle.position = obstacle.position  # Simulate collision
        self.game.update()
        self.assertFalse(self.game.running, "Game should end when colliding with a game-ending obstacle")

    def test_save_game_data(self):
        # Functionalities 9: Test saving game data (not implemented in codebase)
        self.fail("Save game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
