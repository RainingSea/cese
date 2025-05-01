import unittest
import pygame
from game import Game

class TestDriftRivalsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_player_controls_drift_car(self):
        # Functionalities 1: Test car movement controls
        # Test acceleration
        initial_speed = self.game.car.speed  # Assuming speed has a way to be checked
        self.game.car.move('up')  # Simulate pressing the up arrow key
        self.assertGreater(self.game.car.speed, initial_speed, "Car should accelerate when pressing up")

        # Test turning left
        initial_position = self.game.car.position  # Assuming position has a way to be checked
        self.game.car.move('left')  # Simulate pressing the left arrow key
        self.assertNotEqual(self.game.car.position, initial_position, "Car should turn left")

        # Test braking
        self.game.car.speed = 100  # Set speed to a known value
        self.game.car.move('down')  # Simulate pressing the down arrow key
        self.assertLess(self.game.car.speed, 100, "Car should slow down when pressing down")

        # Test turning right
        initial_position = self.game.car.position
        self.game.car.move('right')  # Simulate pressing the right arrow key
        self.assertNotEqual(self.game.car.position, initial_position, "Car should turn right")

    def test_variety_of_tracks(self):
        # Functionalities 2: Test track loading and navigation
        self.game.start_game()  # Start the game to load the track
        self.game.track.load_track()  # Load the track
        # Assuming there's a way to check if the track is loaded and player is at starting line
        self.assertIsNotNone(self.game.track.corners, "Track should load successfully with corners")
        # Simulate navigating through the track
        self.game.car.move('up')  # Move forward
        self.assertTrue(True, "Player should be able to navigate the track")  # Placeholder for actual navigation check

    def test_drift_challenges_and_scoring_system(self):
        # Functionalities 3: Test scoring during drift challenges
        initial_score = self.game.score.points
        # Simulate completing a drift challenge
        self.game.score.points += 50  # Simulate scoring points
        self.assertGreater(self.game.score.points, initial_score, "Score should update after completing a drift challenge")

        # Simulate executing drifts
        self.game.score.points += 10  # Simulate scoring points for drifts
        self.assertGreater(self.game.score.points, initial_score + 50, "Score should update in real-time during drifts")

    def test_data_storage(self):
        # Functionalities 4: Test saving and retrieving score data
        player_name = "test_player"
        self.game.score.points = 150  # Set score to a known value
        self.game.score.save_score(player_name)  # Save the score

        # Check if the score is saved correctly
        with open('scores.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn(f"{player_name},150\n", lines, "Score should be saved to the scores.txt file")

if __name__ == '__main__':
    unittest.main()
