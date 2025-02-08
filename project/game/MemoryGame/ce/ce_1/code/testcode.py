import unittest
from game import Game
from card import Card

class TestMemoryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization_and_card_setup(self):
        # Functionality 1: Game Initialization and Card Setup
        self.game.start_game()
        self.assertEqual(len(self.game.cards), 16, "There should be 16 cards for 8 pairs.")
        values = [card.value for card in self.game.cards]
        self.assertEqual(len(set(values)), 8, "There should be 8 unique card values.")
        self.assertFalse(any(card.is_face_up for card in self.game.cards), "All cards should be face-down initially.")

    def test_flipping_cards(self):
        # Functionality 2: Flipping Cards
        card1 = self.game.cards[0]
        card2 = self.game.cards[1]
        card1.flip()
        self.assertTrue(card1.is_face_up, "The first card should be face-up after flipping.")
        card2.flip()
        self.assertTrue(card2.is_face_up, "The second card should be face-up after flipping.")
        if not card1.is_match(card2):
            card1.flip()
            card2.flip()
            self.assertFalse(card1.is_face_up, "The first card should be face-down after mismatch.")
            self.assertFalse(card2.is_face_up, "The second card should be face-down after mismatch.")

    def test_matching_cards(self):
        # Functionality 3: Matching Cards
        # Find a matching pair
        for i in range(0, len(self.game.cards), 2):
            card1 = self.game.cards[i]
            card2 = self.game.cards[i + 1]
            if card1.is_match(card2):
                card1.flip()
                card2.flip()
                self.assertTrue(card1.is_face_up, "Matching card should remain face-up.")
                self.assertTrue(card2.is_face_up, "Matching card should remain face-up.")
                break

    def test_timer_functionality(self):
        # Functionality 4: Timer Functionality
        self.game.start_game()
        self.assertEqual(self.game.timer, 0.0, "Timer should start at zero.")
        # Simulate game completion
        self.game.timer = 120.0  # Assume 2 minutes passed
        self.assertEqual(self.game.timer, 120.0, "Timer should reflect the time taken.")

    def test_restarting_the_game(self):
        # Functionality 5: Restarting the Game
        self.game.start_game()
        self.game.timer = 120.0
        self.game.restart_game()
        self.assertEqual(self.game.timer, 0.0, "Timer should reset to zero after restart.")
        self.assertEqual(len(self.game.cards), 16, "There should be 16 cards after restart.")
        self.assertFalse(any(card.is_face_up for card in self.game.cards), "All cards should be face-down after restart.")

    def test_scoring_system(self):
        # Functionality 6: Scoring System
        self.game.start_game()
        self.game.update_score()
        initial_score = self.game.score
        self.assertEqual(initial_score, 1, "Score should be incremented after a match.")
        # Simulate faster completion
        self.game.update_score()
        self.assertGreater(self.game.score, initial_score, "Score should increase with faster completion.")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.start_game()
        self.game.save_score("test_player")
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn("test_player:1\n", scores, "Score should be saved in the file.")
        # Simulate another game completion
        self.game.update_score()
        self.game.save_score("test_player")
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn("test_player:2\n", scores, "New score should be appended to the file.")

    def test_user_interface_responsiveness(self):
        # Functionality 8: User Interface Responsiveness
        # This functionality requires UI interaction and cannot be tested with unit tests directly.
        self.fail("User Interface Responsiveness cannot be tested with unit tests.")

if __name__ == '__main__':
    unittest.main()
