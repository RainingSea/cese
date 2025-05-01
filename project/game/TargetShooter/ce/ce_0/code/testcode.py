import unittest
import pygame
from game import Game

class TestTargetShooterGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_player_controls_shooter(self):
        # Functionalities 1: Test aiming and shooting
        mouse_position = (400, 300)  # Simulate mouse position
        self.game.shooter.aim(mouse_position)
        self.assertEqual(self.game.shooter.position, mouse_position, "Shooter should aim at the mouse position")
        
        # Simulate shooting
        self.game.shooter.shoot()  # This will print to console, but we can check if it runs without error

    def test_moving_targets(self):
        # Functionalities 2: Start a new game and check target spawning and movement
        self.game.target_manager.spawn_target()
        self.assertGreater(len(self.game.target_manager.targets), 0, "Targets should appear after spawning")
        
        initial_positions = self.game.target_manager.targets.copy()
        self.game.target_manager.move_targets()
        self.assertNotEqual(initial_positions, self.game.target_manager.targets, "Targets should move after updating their positions")

    def test_shooting_accuracy_and_speed(self):
        # Functionalities 3: Test scoring based on hits
        self.game.score_manager.calculate_score(hit=True, time_taken=1)
        self.assertGreater(self.game.score_manager.get_score(), 0, "Score should increase when hitting a target")
        
        # Simulate multiple hits quickly
        for _ in range(5):
            self.game.score_manager.calculate_score(hit=True, time_taken=0.5)
        self.assertGreater(self.game.score_manager.get_score(), 5 * (100 - 5), "Score should reflect multiple hits")

    def test_timer_countdown(self):
        # Functionalities 4: Test timer countdown
        self.game.timer.start_timer(5)  # Start a 5 seconds timer
        self.assertEqual(self.game.timer.time_remaining, 5, "Timer should start at the specified duration")
        
        # Simulate timer updates
        for _ in range(5):
            self.game.timer.update_timer()
        self.assertEqual(self.game.timer.time_remaining, 0, "Timer should reach zero after 5 updates")

    def test_restart_game(self):
        # Functionalities 5: Test game restart
        self.game.start_game()  # Start the game
        initial_score = self.game.score_manager.get_score()
        self.game.restart_game()  # Restart the game
        self.assertEqual(self.game.score_manager.get_score(), 0, "Score should reset after restarting the game")

    def test_increasing_difficulty_levels(self):
        # Functionalities 6: Test difficulty levels (not implemented in codebase)
        self.fail("Increasing difficulty levels functionality is not implemented in the codebase")

    def test_leaderboard_tracking(self):
        # Functionalities 7: Test leaderboard tracking
        self.game.leaderboard.update_leaderboard(100)
        self.assertIn(100, self.game.leaderboard.scores, "Leaderboard should track scores")
        
        # Check if scores are sorted
        self.game.leaderboard.update_leaderboard(200)
        self.assertEqual(self.game.leaderboard.scores[0], 200, "Leaderboard should keep the highest score at the top")

    def test_competing_for_top_spot(self):
        # Functionalities 8: Test competing for top spot (not implemented in codebase)
        self.fail("Competing for top spot functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
