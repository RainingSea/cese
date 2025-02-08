import unittest
import pygame
from game import Game
from leaderboard import Leaderboard
from target import Target

class TestTargetShooterGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.start_game()

    def test_player_controls_shooter(self):
        # Functionality 1: Player Controls Shooter
        # Test moving the mouse to aim at a target
        initial_position = pygame.mouse.get_pos()
        pygame.mouse.set_pos((400, 300))
        new_position = pygame.mouse.get_pos()
        self.assertNotEqual(initial_position, new_position, "Shooter should move to align with the mouse cursor")

        # Test clicking the mouse button to shoot
        initial_score = self.game.score
        self.game.shoot_target((400, 300))
        self.assertEqual(self.game.score, initial_score, "Score should not change if no target is hit")

    def test_moving_targets(self):
        # Functionality 2: Moving Targets
        # Test targets appear at random locations
        self.game.update_targets()
        self.assertGreater(len(self.game.targets), 0, "Targets should appear on the screen")

        # Test targets move around the screen
        initial_positions = [(target.x, target.y) for target in self.game.targets]
        self.game.update_targets()
        new_positions = [(target.x, target.y) for target in self.game.targets]
        self.assertNotEqual(initial_positions, new_positions, "Targets should move around the screen")

    def test_shooting_accuracy_and_speed(self):
        # Functionality 3: Shooting Accuracy and Speed
        # Test shooting at a target and hitting it
        target = Target(400, 300, 1)
        self.game.targets.append(target)
        initial_score = self.game.score
        self.game.shoot_target((400, 300))
        self.assertGreater(self.game.score, initial_score, "Score should increase when a target is hit")

        # Test shooting at multiple targets quickly
        self.game.shoot_target((400, 300))
        self.assertGreaterEqual(self.game.score, initial_score + 10, "Score should reflect the number of hits")

    def test_timer_countdown(self):
        # Functionality 4: Timer Countdown
        # Test timer starts counting down
        self.assertEqual(self.game.time_limit, 30, "Timer should start at the set time limit")

        # Test game ends when timer reaches zero
        self.game.time_limit = 0
        self.assertFalse(self.game.run_game(), "Game should end when the timer runs out")

    def test_restart_game(self):
        # Functionality 5: Restart Game
        # Test game resets and player can start a new round
        self.game.score = 50
        self.game.restart_game()
        self.assertEqual(self.game.score, 0, "Game should reset score to zero")
        self.assertEqual(len(self.game.targets), 0, "Game should clear all targets")

    def test_increasing_difficulty_levels(self):
        # Functionality 6: Increasing Difficulty Levels
        # This functionality is not implemented in the codebase
        self.fail("Increasing difficulty levels functionality is not implemented in the codebase")

    def test_leaderboard_tracking(self):
        # Functionality 7: Leaderboard Tracking
        # Test score is saved to the local leaderboard
        leaderboard = Leaderboard()
        leaderboard.save_score("TestPlayer", 100)
        top_scores = leaderboard.get_top_scores()
        self.assertIn("TestPlayer", [entry.name for entry in top_scores], "Score should be saved to the leaderboard")

    def test_competing_for_top_spot(self):
        # Functionality 8: Competing for Top Spot
        # Test scores are updated in the leaderboard
        leaderboard = Leaderboard()
        leaderboard.save_score("TestPlayer", 200)
        top_scores = leaderboard.get_top_scores()
        self.assertEqual(top_scores[0].name, "TestPlayer", "Player's name should be at the top of the leaderboard")

if __name__ == '__main__':
    unittest.main()
