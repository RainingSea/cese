import unittest
import pygame
from game import Game
from obstacle import Obstacle

class TestRacingGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_interface(self):
        # Functionalities 1: Initialize the Game Interface
        self.assertEqual(len(self.game.obstacles), 0, "Game should start with no obstacles.")
        self.assertEqual(self.game.lane_position, 0, "Initial lane position should be 0.")
        self.assertTrue(self.game.running, "Game should be running after initialization.")

    def test_display_vehicle_speed_and_distance(self):
        # Functionalities 2: Display Vehicle's Speed and Distance Traveled
        self.game.speed = 10
        self.game.distance = 5
        self.assertEqual(self.game.speed, 10, "Speed should be displayed correctly.")
        self.assertEqual(self.game.distance, 5, "Distance should be displayed correctly.")

    def test_control_vehicle_speed(self):
        # Functionalities 3: Control Vehicle Speed
        initial_speed = self.game.speed
        self.game.handle_input()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
        self.game.handle_input()
        self.assertGreater(self.game.speed, initial_speed, "Speed should increase when 'up' arrow is pressed.")

    def test_control_vehicle_lane_switching(self):
        # Functionalities 4: Control Vehicle's Lane Switching
        initial_lane_position = self.game.lane_position
        self.game.handle_input()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        self.game.handle_input()
        self.assertNotEqual(self.game.lane_position, initial_lane_position, "Lane position should change when 'right' arrow is pressed.")

    def test_simulate_obstacle_movement(self):
        # Functionalities 5: Simulate Obstacle Movement
        obstacle = Obstacle(type=1, position=100)
        self.game.obstacles.append(obstacle)
        initial_position = obstacle.position
        self.game.update_obstacles()
        self.assertGreater(obstacle.position, initial_position, "Obstacles should move downwards.")

    def test_stop_the_car(self):
        # Functionalities 6: Stop the Car
        self.game.speed = 10
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
        self.game.handle_input()
        self.assertEqual(self.game.speed, 0, "Speed should be 0 when 's' key is pressed.")

    def test_handle_slow_down_obstacle(self):
        # Functionalities 7: Handle Slow-Down Obstacle (not implemented in codebase)
        self.fail("Handle slow-down obstacle functionality is not implemented in the codebase")

    def test_handle_game_ending_obstacle(self):
        # Functionalities 8: Handle Game-Ending Obstacle (not implemented in codebase)
        self.fail("Handle game-ending obstacle functionality is not implemented in the codebase")

    def test_save_game_data_to_local_file(self):
        # Functionalities 9: Save Game Data to Local File
        self.game.save_game_state()
        with open('game_data.txt', 'r') as f:
            data = f.read()
        self.assertIn(f"{self.game.speed}|{self.game.distance}|{len(self.game.obstacles)}", data, "Game data should be saved to local file.")

if __name__ == '__main__':
    unittest.main()
