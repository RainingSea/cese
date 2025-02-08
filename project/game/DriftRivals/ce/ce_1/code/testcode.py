import unittest
import pygame
from game import Game, Car, Track, Score

class TestDriftRivalsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.car = self.game.car
        self.score = self.game.score

    def test_player_controls_drift_car(self):
        # Functionality 1: Test car acceleration
        initial_speed = self.car.speed
        self.car.speed = 5.0  # Simulate pressing the up arrow key
        self.car.move('up')
        self.assertGreater(self.car.position_y, 0, "Car should move forward")

        # Test car turning left
        initial_x = self.car.position_x
        self.car.move('left')
        self.assertLess(self.car.position_x, initial_x, "Car should turn left")

        # Test car braking
        self.car.speed = 0.0  # Simulate pressing the down arrow key
        self.car.move('down')
        self.assertEqual(self.car.speed, 0.0, "Car should stop")

        # Test car turning right
        initial_x = self.car.position_x
        self.car.move('right')
        self.assertGreater(self.car.position_x, initial_x, "Car should turn right")

    def test_variety_of_tracks(self):
        # Functionality 2: Test track loading
        self.game.load_tracks()
        self.assertGreater(len(self.game.tracks), 0, "Tracks should be loaded")

        # Test navigating through the track
        for track in self.game.tracks:
            self.assertIsInstance(track, Track, "Track should be an instance of Track class")

    def test_drift_challenges_and_scoring_system(self):
        # Functionality 3: Test score calculation
        drift_precision = self.car.drift()
        speed = 10.0
        style = 1.0
        calculated_score = self.score.calculate_score(drift_precision, speed, style)
        self.assertEqual(calculated_score, drift_precision * speed * style, "Score should be calculated correctly")

    def test_data_storage(self):
        # Functionality 4: Test score saving
        self.score.score_value = 100.0
        self.score.save_to_file()
        with open('scores.txt', 'r') as f:
            scores = f.readlines()
            self.assertIn("100.0\n", scores, "Score should be saved to file")

        # Test score retrieval
        with open('scores.txt', 'r') as f:
            scores = f.readlines()
            self.assertIn("100.0\n", scores, "Saved score should be retrievable from file")

if __name__ == '__main__':
    unittest.main()
