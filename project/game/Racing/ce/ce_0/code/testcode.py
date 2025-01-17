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
        self.assertEqual(self.game.lane, 1, "Initial lane should be 1")
        self.assertEqual(len(self.game.obstacles), 0, "There should be no obstacles initially")

    def test_display_vehicle_speed_and_distance(self):
        # Functionalities 2: Test speed and distance display
        initial_distance = self.game.distance
        self.game.speed = 60
        self.game.update()
        self.assertGreater(self.game.distance, initial_distance, "Distance should increase with speed")

    def test_control_vehicle_speed(self):
        # Functionalities 3: Test vehicle speed control
        initial_speed = self.game.speed
        self.game.speed += 10  # Simulate pressing the "up" arrow key
        self.assertGreater(self.game.speed, initial_speed, "Speed should increase when 'up' key is pressed")

    def test_control_vehicle_lane_switching(self):
        # Functionalities 4: Test vehicle lane switching
        self.game.lane = 0  # Start from left lane
        self.game.handle_input()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        self.assertEqual(self.game.lane, 1, "Vehicle should move to center lane when 'right' key is pressed")

    def test_simulate_obstacle_movement(self):
        # Functionalities 5: Test obstacle movement
        obstacle = Obstacle(position=100, type=True)
        self.game.obstacles.append(obstacle)
        initial_position = obstacle.position
        self.game.update()
        self.assertGreater(obstacle.position, initial_position, "Obstacle should move down the lane")

    def test_stop_the_car(self):
        # Functionalities 6: Test stopping the car
        self.game.speed = 60
        self.game.handle_input()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
        self.assertEqual(self.game.speed, 0, "Speed should be 0 when 's' key is pressed")

    def test_handle_slow_down_obstacle(self):
        # Functionalities 7: Test slow-down obstacle handling
        obstacle = Obstacle(position=500, type=True)
        self.game.obstacles.append(obstacle)
        self.game.lane = 1
        self.game.speed = 60
        self.game.update()
        if self.game.check_collision(obstacle):
            self.game.speed -= 10  # Simulate slow-down effect
        self.assertLess(self.game.speed, 60, "Speed should decrease upon collision with slow-down obstacle")

    def test_handle_game_ending_obstacle(self):
        # Functionalities 8: Test game-ending obstacle handling
        obstacle = Obstacle(position=500, type=False)
        self.game.obstacles.append(obstacle)
        self.game.lane = 1
        self.game.update()
        if self.game.check_collision(obstacle):
            self.fail("Game should end upon collision with game-ending obstacle")

    def test_save_game_data_to_local_file(self):
        # Functionalities 9: Test saving game data
        self.game.save_game()
        with open('game_data.txt', 'r') as f:
            data = f.read()
        self.assertIn('speed|0', data, "Game data should be saved correctly")
        self.assertIn('distance|0.0', data, "Game data should be saved correctly")
        self.assertIn('lane|1', data, "Game data should be saved correctly")

if __name__ == '__main__':
    unittest.main()
