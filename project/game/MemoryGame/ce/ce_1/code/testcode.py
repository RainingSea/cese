import unittest
import os
from game import Game

class TestMemoryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization_and_card_setup(self):
        # Test the total number of cards
        self.assertEqual(len(self.game.cards), 16, "Total number of cards should be 16 (8 pairs)")

    def test_flipping_cards(self):
        # Simulate flipping the first card
        self.game.flip_card(0)
        self.assertTrue(self.game.cards[0].face_up, "First card should be face up after flipping")

        # Simulate flipping the second card
        self.game.flip_card(1)
        self.assertTrue(self.game.cards[1].face_up, "Second card should be face up after flipping")

        # Simulate flipping two cards that do not match
        self.game.first_card = 0
        self.game.second_card = 1
        self.game.check_match = lambda: False  # Mocking the check_match method
        self.game.flip_card(2)  # This should trigger the flip back logic
        self.assertFalse(self.game.cards[0].face_up, "First card should be face down after mismatch")
        self.assertFalse(self.game.cards[1].face_up, "Second card should be face down after mismatch")

    def test_matching_cards(self):
        # Simulate clicking on two matching cards
        self.game.cards[0].flip()  # First card face up
        self.game.cards[1].flip()  # Second card face up
        self.game.first_card = 0
        self.game.second_card = 1
        self.game.check_match = lambda: True  # Mocking the check_match method
        self.game.flip_card(2)  # This should keep both cards face up
        self.assertTrue(self.game.cards[0].face_up, "First card should remain face up after match")
        self.assertTrue(self.game.cards[1].face_up, "Second card should remain face up after match")

    def test_restart_game(self):
        self.game.restart_game()
        self.assertEqual(self.game.score, 0, "Score should be reset to 0 after restarting")
        self.assertEqual(self.game.time, 0, "Time should be reset to 0 after restarting")
        self.assertFalse(any(card.face_up for card in self.game.cards), "All cards should be face down after restarting")

    def test_data_storage(self):
        # Complete a game and check the local text file for scores
        self.game.score = 10
        self.game.time = 30
        self.game.save_game_state()
        
        with open('gamestate.txt', 'r') as f:
            data = f.read().splitlines()
            self.assertEqual(int(data[0]), 10, "Score should be saved correctly")
            self.assertEqual(int(data[1]), 30, "Time should be saved correctly")

        # Restart the game and complete it again
        self.game.score = 20
        self.game.time = 25
        self.game.save_game_state()

        with open('gamestate.txt', 'r') as f:
            data = f.read().splitlines()
            self.assertEqual(int(data[0]), 20, "New score should overwrite the previous score")
            self.assertEqual(int(data[1]), 25, "New time should overwrite the previous time")

    def tearDown(self):
        # Clean up the gamestate file after tests
        if os.path.exists('gamestate.txt'):
            os.remove('gamestate.txt')

if __name__ == '__main__':
    unittest.main()
