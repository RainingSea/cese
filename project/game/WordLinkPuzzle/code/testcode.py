import unittest
import pygame
from game import Game
from grid import Grid
from score import Score
from timer import Timer
from wordlist import WordList

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.score = self.game.score
        self.timer = self.game.timer
        self.wordlist = self.game.formed_words

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        # Simulate connecting letters "C", "A", "T"
        connected_letters = ['C', 'A', 'T']
        word = ''.join(connected_letters)
        is_valid = self.game.validate_word(word)
        self.assertTrue(is_valid, "The word 'CAT' should be recognized as a valid word")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        # Simulate forming the word "DOG"
        word = "DOG"
        points = self.score.calculate_score(word)
        self.assertEqual(points, 1, "The player should receive 1 point for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        self.timer.start_timer(60)
        initial_time = self.timer.time_left
        self.timer.update_timer()
        self.assertEqual(self.timer.time_left, initial_time - 1, "Timer should count down correctly")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        self.grid.generate_grid('Hard')
        grid_size = len(self.grid.letters)
        self.assertEqual(grid_size, 8, "The grid size for 'Hard' difficulty should be 8x8")

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        self.game.save_progress()
        with open('game_state.txt', 'r') as f:
            lines = f.readlines()
        self.assertIn("Score:", lines[0], "Game state should contain score information")
        self.assertIn("Words:", lines[1], "Game state should contain words information")
        self.assertIn("Time Left:", lines[2], "Game state should contain time left information")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        self.game.save_progress()  # Ensure there is a saved state
        self.game.load_progress()
        self.assertEqual(self.score.get_score(), 0, "Score should be restored to 0")
        self.assertEqual(self.wordlist.get_words(), [], "Word list should be restored to empty")
        self.assertEqual(self.timer.time_left, 0, "Time left should be restored to 0")

if __name__ == '__main__':
    unittest.main()
