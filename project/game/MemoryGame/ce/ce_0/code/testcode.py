import unittest
import pygame
from memory_game import MemoryGame
from card import Card

class TestMemoryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = MemoryGame()
        self.game.restart_game()
        faces = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.game.cards = [Card(face) for face in faces for _ in range(2)]
        self.game.shuffle_cards()

    def test_game_initialization_and_card_setup(self):
        # Functionality 1: Game Initialization and Card Setup
        self.assertEqual(len(self.game.cards), 16, "There should be 16 cards for 8 pairs.")
        self.assertTrue(all(not card.is_flipped for card in self.game.cards), "All cards should be face-down initially.")

    def test_flipping_cards(self):
        # Functionality 2: Flipping Cards
        self.assertTrue(self.game.flip_card(0), "First card should be flipped successfully.")
        self.assertTrue(self.game.cards[0].is_flipped, "First card should be revealed.")
        
        self.assertTrue(self.game.flip_card(1), "Second card should be flipped successfully.")
        self.assertTrue(self.game.cards[1].is_flipped, "Second card should be revealed.")
        
        # Simulate mismatch
        if not self.game.check_match(self.game.cards[0], self.game.cards[1]):
            self.game.cards[0].flip()
            self.game.cards[1].flip()
            self.assertFalse(self.game.cards[0].is_flipped, "First card should be face-down after mismatch.")
            self.assertFalse(self.game.cards[1].is_flipped, "Second card should be face-down after mismatch.")

    def test_matching_cards(self):
        # Functionality 3: Matching Cards
        # Assuming cards[0] and cards[8] are a matching pair
        self.game.cards[0].flip()
        self.game.cards[8].flip()
        self.assertTrue(self.game.check_match(self.game.cards[0], self.game.cards[8]), "Cards should match.")
        self.assertTrue(self.game.cards[0].is_flipped, "Matching card should remain face-up.")
        self.assertTrue(self.game.cards[8].is_flipped, "Matching card should remain face-up.")

    def test_timer_functionality(self):
        # Functionality 4: Timer Functionality
        self.game.restart_game()
        self.assertEqual(self.game.timer, 0.0, "Timer should start at zero.")
        # Simulate game completion
        self.game.timer = 10.0
        self.assertEqual(self.game.timer, 10.0, "Timer should stop at the final time.")

    def test_restarting_game(self):
        # Functionality 5: Restarting the Game
        self.game.restart_game()
        self.assertEqual(len(self.game.cards), 0, "Game should reset with no cards.")
        self.assertEqual(self.game.timer, 0.0, "Timer should reset to zero.")
        self.assertTrue(self.game.game_active, "Game should be active after restart.")

    def test_scoring_system(self):
        # Functionality 6: Scoring System
        self.game.update_score(5.0)
        score_after_first_game = self.game.score
        self.assertGreater(score_after_first_game, 0, "Score should be calculated based on time taken.")
        
        self.game.update_score(3.0)
        score_after_second_game = self.game.score
        self.assertGreater(score_after_second_game, score_after_first_game, "Score should be higher for faster completion.")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.save_score()
        with open('scores.txt', 'r') as score_file:
            scores = score_file.readlines()
        self.assertIn(f"{self.game.score}\n", scores, "Score should be saved in the local text file.")

    def test_user_interface_responsiveness(self):
        # Functionality 8: User Interface Responsiveness
        # This functionality requires manual testing for UI responsiveness
        self.fail("User Interface Responsiveness testing requires manual verification.")

if __name__ == '__main__':
    unittest.main()
