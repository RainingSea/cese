import unittest
from bird import Bird
from pipe import Pipe
from game import Game
from score_manager import ScoreManager

class TestFlappyBirdClone(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.bird = self.game.bird
        self.score_manager = self.game.score_manager

    def test_bird_control(self):
        # Functionalities 1: Test bird's initial position and flap
        initial_position = self.bird.get_position()
        self.bird.fall()
        self.assertGreater(self.bird.get_position(), initial_position, "Bird should fall due to gravity")

        self.bird.flap()
        self.assertLess(self.bird.velocity, 0, "Bird should move upward when flapped")

    def test_pipe_navigation(self):
        # Functionalities 2: Test pipe generation and navigation
        self.assertGreater(len(self.game.pipes), 0, "Pipes should be generated at the start of the game")
        # Simulate bird passing through pipes
        for pipe in self.game.pipes:
            self.bird.y_position = pipe.gap_height - 10  # Position bird to pass through the gap
            self.assertFalse(self.game.check_collision(), "Bird should pass through the gap without collision")

    def test_pipe_movement(self):
        # Functionalities 3: Test pipe movement and scoring
        initial_position = self.game.pipes[0].get_position()
        self.game.pipes[0].move()
        self.assertLess(self.game.pipes[0].get_position(), initial_position, "Pipes should move from right to left")

        # Simulate scoring
        self.game.pipes[0].x_position = -60  # Move pipe out of screen
        self.game.update()
        self.assertEqual(self.game.score, 1, "Score should increase when a pipe is passed")

    def test_scoring_system(self):
        # Functionalities 4: Test scoring system
        self.game.score = 0
        self.game.pipes[0].x_position = -60  # Move pipe out of screen
        self.game.update()
        self.assertEqual(self.game.score, 1, "Score should increase by one point for each pipe passed")

    def test_game_over_conditions(self):
        # Functionalities 5: Test game over by collision and falling
        self.bird.y_position = 600  # Simulate bird falling to the ground
        self.assertTrue(self.game.check_collision(), "Game should end when bird falls to the ground")

        self.bird.y_position = self.game.pipes[0].gap_height - 20  # Simulate collision with pipe
        self.assertTrue(self.game.check_collision(), "Game should end when bird collides with a pipe")

    def test_restart_game(self):
        # Functionalities 6: Test game restart
        self.game.restart()
        self.assertEqual(self.game.score, 0, "Game should reset score to 0 on restart")
        self.assertEqual(len(self.game.pipes), 1, "Game should reset pipes on restart")

    def test_high_score_storage(self):
        # Functionalities 7: Test high score storage
        self.score_manager.save_high_score(5)
        self.assertIn(5, self.score_manager.get_high_scores(), "High score of 5 should be saved")

        self.score_manager.save_high_score(3)
        self.assertNotIn(3, self.score_manager.get_high_scores(), "High score should not be overwritten by a lower score")

if __name__ == '__main__':
    unittest.main()
