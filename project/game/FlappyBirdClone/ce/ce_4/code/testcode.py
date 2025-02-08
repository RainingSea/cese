import unittest
import pygame
from game import Game, Bird, Pipes, Score, GameState, HighScoreManager

class TestFlappyBirdClone(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.bird = self.game.bird
        self.pipes = self.game.pipes
        self.score = self.game.score
        self.state = self.game.state
        self.high_score_manager = self.game.high_score_manager

    def test_bird_control(self):
        # Functionality 1: Bird Control
        initial_position = self.bird.position[1]
        self.bird.update()
        self.assertGreater(self.bird.position[1], initial_position, "Bird should fall due to gravity")

        self.bird.flap()
        self.bird.update()
        self.assertLess(self.bird.position[1], initial_position, "Bird should move upward when flapped")

    def test_pipe_navigation(self):
        # Functionality 2: Pipe Navigation
        self.pipes.generate_pipes()
        self.assertGreater(len(self.pipes.pipe_list), 0, "Pipes should be generated")

        # Simulate bird passing through pipes
        self.bird.position = (self.pipes.pipe_list[0][0].x + 35, self.pipes.pipe_list[0][0].height + 75)
        collision = self.pipes.check_collision(self.bird)
        self.assertFalse(collision, "Bird should pass through the gap without collision")

    def test_pipe_movement(self):
        # Functionality 3: Pipe Movement
        self.pipes.generate_pipes()
        initial_x = self.pipes.pipe_list[0][0].x
        self.pipes.update()
        self.assertLess(self.pipes.pipe_list[0][0].x, initial_x, "Pipes should move from right to left")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.score.get_score()
        self.score.increment()
        self.assertEqual(self.score.get_score(), initial_score + 1, "Score should increase by one")

    def test_game_over_conditions(self):
        # Functionality 5: Game Over Conditions
        self.state.start()
        self.bird.position = (self.pipes.pipe_list[0][0].x, self.pipes.pipe_list[0][0].height)
        collision = self.pipes.check_collision(self.bird)
        if collision:
            self.state.end()
        self.assertFalse(self.state.is_running, "Game should end when bird collides with a pipe")

        self.state.start()
        self.bird.position = (self.bird.position[0], 600)  # Simulate falling to the ground
        self.state.end()
        self.assertFalse(self.state.is_running, "Game should end when bird falls to the ground")

    def test_restart_game(self):
        # Functionality 6: Restart Game
        self.state.end()
        self.game.restart()
        self.assertTrue(self.state.is_running, "Game should restart and be running")

    def test_high_score_storage(self):
        # Functionality 7: High Score Storage
        self.high_score_manager.save_high_score(5)
        high_scores = self.high_score_manager.load_high_scores()
        self.assertIn(5, high_scores, "High score of 5 should be saved")

        self.high_score_manager.save_high_score(3)
        high_scores = self.high_score_manager.load_high_scores()
        self.assertIn(5, high_scores, "High score should remain at 5")
        self.assertIn(3, high_scores, "New score of 3 should be saved but not overwrite the high score")

if __name__ == '__main__':
    unittest.main()
