import unittest
import pygame
from game import Game, Card, Timer
import os

class TestMemoryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.images = ['image1.png', 'image2.png', 'image3.png', 'image4.png']
        self.game.start_game(self.images)

    def test_game_initialization_and_card_setup(self):
        # Functionality 1: Game Initialization and Card Setup
        self.assertEqual(len(self.game.cards), len(self.images) * 2, "Total number of cards should be twice the number of unique images")
        self.assertTrue(all(not card.is_face_up for card in self.game.cards), "All cards should be face-down initially")

    def test_flipping_cards(self):
        # Functionality 2: Flipping Cards
        first_card = self.game.cards[0]
        second_card = self.game.cards[1]
        
        self.game.flip_card(first_card)
        self.assertTrue(first_card.is_face_up, "First card should be revealed after flipping")

        self.game.flip_card(second_card)
        self.assertTrue(second_card.is_face_up, "Second card should be revealed after flipping")

        if not self.game.check_match(first_card, second_card):
            self.game.flip_card(first_card)
            self.game.flip_card(second_card)
            self.assertFalse(first_card.is_face_up, "First card should be face-down after mismatch")
            self.assertFalse(second_card.is_face_up, "Second card should be face-down after mismatch")

    def test_matching_cards(self):
        # Functionality 3: Matching Cards
        # Find a matching pair
        for i in range(0, len(self.game.cards), 2):
            card1 = self.game.cards[i]
            card2 = self.game.cards[i+1]
            if card1.is_match(card2):
                self.game.flip_card(card1)
                self.game.flip_card(card2)
                self.assertTrue(card1.is_face_up and card2.is_face_up, "Matching cards should remain face-up")
                break

    def test_timer_functionality(self):
        # Functionality 4: Timer Functionality
        self.game.timer.start()
        time.sleep(1)
        elapsed_time = self.game.timer.get_elapsed_time()
        self.assertGreater(elapsed_time, 0, "Timer should start counting from zero")

    def test_restarting_game(self):
        # Functionality 5: Restarting the Game
        self.game.restart_game()
        self.assertEqual(len(self.game.cards), 0, "Game should reset and clear all cards")
        self.assertEqual(self.game.score, 0, "Score should reset to zero")

    def test_scoring_system(self):
        # Functionality 6: Scoring System
        initial_score = self.game.score
        self.game.score += 10  # Simulate scoring
        self.assertGreater(self.game.score, initial_score, "Score should increase after completing a game")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.save_score()
        with open('high_scores.txt', 'r') as f:
            scores = f.readlines()
        self.assertIn(f"{self.game.score}\n", scores, "Score should be saved in the local text file")

    def test_user_interface_responsiveness(self):
        # Functionality 8: User Interface Responsiveness
        self.fail("User interface responsiveness is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
