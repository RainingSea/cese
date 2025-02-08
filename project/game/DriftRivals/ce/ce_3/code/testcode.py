import unittest
from car import Car
from game import Game
from score import Score
from tracks import Track
import os

class TestDriftRivalsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.car = self.game.car
        self.score = self.game.score

    def test_player_controls_drift_car(self):
        # Functionalities 1: Test car movement controls
        initial_x = self.car.position_x
        initial_y = self.car.position_y

        # Test moving up
        self.car.move('up')
        self.assertLess(self.car.position_y, initial_y, "Car should move up")

        # Test moving left
        self.car.move('left')
        self.assertLess(self.car.position_x, initial_x, "Car should move left")

        # Test moving down
        self.car.move('down')
        self.assertGreater(self.car.position_y, initial_y, "Car should move down")

        # Test moving right
        self.car.move('right')
        self.assertGreater(self.car.position_x, initial_x, "Car should move right")

    def test_variety_of_tracks(self):
        # Functionalities 2: Test track loading
        self.assertGreater(len(self.game.tracks), 0, "Tracks should be loaded")

        # Test navigating through the track
        track = self.game.tracks[0]
        self.assertIsInstance(track, Track, "Track should be an instance of Track class")

    def test_drift_challenges_and_scoring_system(self):
        # Functionalities 3: Test scoring system
        initial_score = self.score.current_score
        self.game.update_score(1.0, 2.0, 3.0)
        self.assertGreater(self.score.current_score, initial_score, "Score should increase based on performance")

    def test_data_storage(self):
        # Functionalities 4: Test score saving
        filename = "test_scores.txt"
        self.score.save_score(filename)
        self.assertTrue(os.path.exists(filename), "Score file should be created")

        # Check if score is saved correctly
        with open(filename, "r") as file:
            lines = file.readlines()
            self.assertIn("Player|", lines[-1], "Score should be saved in the file")

        # Clean up
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
