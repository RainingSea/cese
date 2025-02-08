import unittest
from game import Game, Bird, Pipe

class TestFlappyBirdClone(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.bird = self.game.bird

    def test_bird_control(self):
        # Functionalities 1: Test bird's initial position and flap
        initial_y = self.bird.y_position
        self.bird.fall()
        self.assertGreater(self.bird.y_position, initial_y, "Bird should fall due to gravity")

        self.bird.flap()
        self.assertLess(self.bird.y_position, initial_y, "Bird should move upward when flapping")

    def test_pipe_navigation(self):
        # Functionalities 2: Test pipe generation and navigation
        self.game.create_pipes()
        self.assertEqual(len(self.game.pipes), 5, "Five pipes should be generated initially")

        # Simulate bird passing through pipes
        for pipe in self.game.pipes:
            self.bird.y_position = pipe.gap_y_position
            self.assertFalse(self.game.check_collision(), "Bird should pass through the gap without collision")

    def test_pipe_movement(self):
        # Functionalities 3: Test pipe movement
        self.game.create_pipes()
        initial_x_positions = [pipe.x_position for pipe in self.game.pipes]
        self.game.update()
        for i, pipe in enumerate(self.game.pipes):
            self.assertLess(pipe.x_position, initial_x_positions[i], "Pipes should move left")

    def test_scoring_system(self):
        # Functionalities 4: Test scoring system
        self.game.create_pipes()
        initial_score = self.game.score
        self.game.update()
        self.assertGreaterEqual(self.game.score, initial_score, "Score should increase when passing through pipes")

    def test_game_over_conditions(self):
        # Functionalities 5: Test game over on collision
        self.game.is_game_over = False
        self.bird.y_position = 0  # Simulate collision
        self.game.check_collision()
        self.assertTrue(self.game.is_game_over, "Game should end when bird collides with a pipe")

        # Test game over when bird falls to the ground
        self.game.is_game_over = False
        self.bird.y_position = 800  # Simulate falling to the ground
        self.game.update()
        self.assertTrue(self.game.is_game_over, "Game should end when bird falls to the ground")

    def test_restart_game(self):
        # Functionalities 6: Test game restart
        self.game.is_game_over = True
        self.game.reset_game()
        self.assertFalse(self.game.is_game_over, "Game should reset and not be over after restart")
        self.assertEqual(self.bird.y_position, 200, "Bird should be reset to initial position")

    def test_high_score_storage(self):
        # Functionalities 7: Test high score storage
        self.game.save_high_score(5)
        high_scores = self.game.load_high_scores()
        self.assertIn(5, high_scores, "High score of 5 should be saved")

        self.game.save_high_score(3)
        high_scores = self.game.load_high_scores()
        self.assertIn(5, high_scores, "High score should remain 5 after scoring 3")
        self.assertIn(3, high_scores, "Score of 3 should be saved but not overwrite high score of 5")

if __name__ == '__main__':
    unittest.main()
