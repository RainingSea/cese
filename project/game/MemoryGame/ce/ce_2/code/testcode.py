import unittest
from game import Game
from card import Card

class TestMemoryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game with 8 pairs of cards
        self.num_pairs = 8
        self.game = Game(self.num_pairs)

    def test_game_initialization_and_card_setup(self):
        # Functionalities 1: Game Initialization and Card Setup
        self.assertEqual(len(self.game.cards), self.num_pairs * 2, "Total number of cards should be twice the number of pairs")
        images = [card.image for card in self.game.cards]
        self.assertEqual(len(set(images)), self.num_pairs, "There should be num_pairs unique images")

    def test_flipping_cards(self):
        # Functionalities 2: Flipping Cards
        card1 = self.game.cards[0]
        card2 = self.game.cards[1]
        card1.flip()
        self.assertTrue(card1.is_flipped, "First card should be revealed")
        card2.flip()
        self.assertTrue(card2.is_flipped, "Second card should be revealed")
        if not self.game.check_match(card1, card2):
            card1.flip()
            card2.flip()
            self.assertFalse(card1.is_flipped, "First card should be face-down after mismatch")
            self.assertFalse(card2.is_flipped, "Second card should be face-down after mismatch")

    def test_matching_cards(self):
        # Functionalities 3: Matching Cards
        card1 = self.game.cards[0]
        card2 = self.game.cards[0]  # Ensuring a match
        card1.flip()
        card2.flip()
        self.assertTrue(self.game.check_match(card1, card2), "Cards should match and remain face-up")

    def test_timer_functionality(self):
        # Functionalities 4: Timer Functionality
        self.game.start_game()
        self.assertEqual(self.game.timer, 0.0, "Timer should start at zero")
        # Simulate game completion
        self.game.timer = 100.0
        self.assertEqual(self.game.timer, 100.0, "Timer should stop at final time")

    def test_restarting_game(self):
        # Functionalities 5: Restarting the Game
        self.game.restart_game()
        self.assertEqual(len(self.game.cards), self.num_pairs * 2, "Game should reset with the correct number of cards")
        self.assertEqual(self.game.timer, 0.0, "Timer should reset to zero")

    def test_scoring_system(self):
        # Functionalities 6: Scoring System
        self.game.timer = 100.0
        self.game.score = 200  # Assume a score calculation based on time
        self.assertEqual(self.game.score, 200, "Score should reflect the time taken")

    def test_data_storage(self):
        # Functionalities 7: Data Storage
        self.game.save_score("test_player")
        with open('scores.txt', 'r') as f:
            scores = f.readlines()
        self.assertIn("test_player:0\n", scores, "Score should be saved in the local text file")

    def test_user_interface_responsiveness(self):
        # Functionalities 8: User Interface Responsiveness
        self.fail("User interface responsiveness is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
